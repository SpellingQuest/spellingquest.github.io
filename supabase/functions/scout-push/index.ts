// Spelling Quest: Scout's reminders (web push), 29 Sep 2026.
//
// Modelled on Read Between The Lines' push.js: standard Web Push (RFC 8291
// aes128gcm payloads, RFC 8292 VAPID), no third-party service. Off until a
// grown-up turns it on, and at most one reminder a day per device.
//
// POST { action, ... } from the app:
//   key                          -> { publicKey }
//   subscribe  { sub, tz, remind_at, test_days, fam? }   (fam: the family's scrambled sync code, when there is one)
//   done       { date, fam?, endpoint? }  a sprint was finished today on some device of this family
//   update     { endpoint, tz?, remind_at?, test_days?, done?, fam? }   (done: 'YYYY-MM-DD', a sprint finished today)
//   unsubscribe { endpoint }
//   test       { endpoint }      -> sends one right now
// POST { action:'tick' } with header x-cron-key, every 15 minutes from pg_cron:
//   sends today's reminder to each device whose reminder time has come, unless a
//   sprint was already finished today, it's test day, or one was sent today.
//
// No secrets to add: the VAPID signing key is made on first use and kept in
// public.sq_push_keys (row-level security on, no policies, so only this
// function can read it). The scheduler's key lives in the same table.
import { createClient } from "npm:@supabase/supabase-js@2";

const SUBJECT = "mailto:spellingquest@gmail.com";
const ALLOWED = [/^https:\/\/spellingquest\.github\.io$/, /^http:\/\/localhost(:\d+)?$/, /^http:\/\/127\.0\.0\.1(:\d+)?$/];

const enc = new TextEncoder();
const b64u = (buf: ArrayBuffer | Uint8Array) =>
  btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = (s: string) =>
  Uint8Array.from(atob(String(s).replace(/-/g, "+").replace(/_/g, "/") + "===".slice((String(s).length + 3) % 4)), (c) => c.charCodeAt(0));
const concat = (...parts: Uint8Array[]) => {
  const out = new Uint8Array(parts.reduce((n, p) => n + p.length, 0));
  let o = 0; parts.forEach((p) => { out.set(p, o); o += p.length; }); return out;
};

async function hkdf(salt: Uint8Array, ikm: Uint8Array, info: Uint8Array, bytes: number) {
  const key = await crypto.subtle.importKey("raw", ikm, "HKDF", false, ["deriveBits"]);
  return new Uint8Array(await crypto.subtle.deriveBits({ name: "HKDF", hash: "SHA-256", salt, info }, key, bytes * 8));
}
async function encrypt(sub: any, payload: string) {
  const uaPublic = unb64u(sub.keys.p256dh), authSecret = unb64u(sub.keys.auth);
  const local = await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]);
  const asPublic = new Uint8Array(await crypto.subtle.exportKey("raw", local.publicKey));
  const uaKey = await crypto.subtle.importKey("raw", uaPublic, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const shared = new Uint8Array(await crypto.subtle.deriveBits({ name: "ECDH", public: uaKey }, local.privateKey, 256));
  const ikm = await hkdf(authSecret, shared, concat(enc.encode("WebPush: info\0"), uaPublic, asPublic), 32);
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const cek = await hkdf(salt, ikm, enc.encode("Content-Encoding: aes128gcm\0"), 16);
  const nonce = await hkdf(salt, ikm, enc.encode("Content-Encoding: nonce\0"), 12);
  const aes = await crypto.subtle.importKey("raw", cek, "AES-GCM", false, ["encrypt"]);
  const cipher = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv: nonce }, aes, concat(enc.encode(payload), new Uint8Array([2]))));
  return concat(salt, new Uint8Array([0, 0, 16, 0]), new Uint8Array([asPublic.length]), asPublic, cipher);
}

const supa = () => createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

/* the signing key: made once, then read back */
async function vapidKeys(db: any): Promise<{ jwk: any; publicKey: string }> {
  const { data } = await db.from("sq_push_keys").select("v").eq("k", "vapid").maybeSingle();
  if (data && data.v) return JSON.parse(data.v);
  const pair = await crypto.subtle.generateKey({ name: "ECDSA", namedCurve: "P-256" }, true, ["sign", "verify"]);
  const jwk = await crypto.subtle.exportKey("jwk", pair.privateKey);
  const publicKey = b64u(await crypto.subtle.exportKey("raw", pair.publicKey));
  const v = { jwk, publicKey };
  await db.from("sq_push_keys").upsert({ k: "vapid", v: JSON.stringify(v) }, { onConflict: "k", ignoreDuplicates: true });
  const again = await db.from("sq_push_keys").select("v").eq("k", "vapid").maybeSingle();   // two first-callers at once: keep one key
  return again.data ? JSON.parse(again.data.v) : v;
}
async function vapidHeader(keys: any, endpoint: string) {
  const key = await crypto.subtle.importKey("jwk", keys.jwk, { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"]);
  const head = b64u(enc.encode(JSON.stringify({ typ: "JWT", alg: "ES256" })));
  const body = b64u(enc.encode(JSON.stringify({ aud: new URL(endpoint).origin, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: SUBJECT })));
  const sig = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, key, enc.encode(head + "." + body));
  return "vapid t=" + head + "." + body + "." + b64u(sig) + ", k=" + keys.publicKey;
}
async function sendOne(keys: any, sub: any, msg: any) {
  const res = await fetch(sub.endpoint, {
    method: "POST",
    headers: { Authorization: await vapidHeader(keys, sub.endpoint), TTL: "43200", Urgency: "normal",
      "Content-Encoding": "aes128gcm", "Content-Type": "application/octet-stream" },
    body: await encrypt(sub, JSON.stringify(msg)),
  });
  return res.status;
}

/* local date, weekday and minutes-past-midnight in the family's time zone */
function localNow(tz: string) {
  const parts: any = {};
  try {
    new Intl.DateTimeFormat("en-US", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", weekday: "short", hour12: false })
      .formatToParts(new Date()).forEach((p) => parts[p.type] = p.value);
  } catch { return localNow("America/Chicago"); }
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return { date: `${parts.year}-${parts.month}-${parts.day}`, dow: days.indexOf(parts.weekday), mins: (+parts.hour % 24) * 60 + +parts.minute };
}
const LINES = [
  "Scout's ready for today's sprint! 🐝",
  "Bzzz! Time for a quick sprint with Scout.",
  "Your spelling buddy is waiting. Ready to fill the hive?",
  "Five minutes with Scout today? Let's go!",
];

const okSub = (s: any) => s && /^https:\/\//.test(String(s.endpoint || "")) && s.keys && s.keys.p256dh && s.keys.auth;
const cleanTime = (t: any) => /^([01]\d|2[0-3]):[0-5]\d$/.test(String(t)) ? String(t) : null;
const cleanDays = (d: any) => Array.isArray(d) ? [...new Set(d.map(Number).filter((n) => n >= 0 && n <= 6))] : null;
const cleanFam = (f: any) => /^[A-Za-z0-9_\-]{16,128}$/.test(String(f || "")) ? String(f) : null;
const cleanTz = (t: any) => { try { new Intl.DateTimeFormat("en-US", { timeZone: String(t) }); return String(t).slice(0, 60); } catch { return null; } };

Deno.serve(async (req) => {
  const origin = req.headers.get("origin") || "";
  const okOrigin = ALLOWED.some((r) => r.test(origin));
  const cors = { "Access-Control-Allow-Origin": okOrigin ? origin : "https://spellingquest.github.io",
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info", "Access-Control-Allow-Methods": "POST, OPTIONS", Vary: "Origin" };
  const json = (b: unknown, status = 200) => new Response(JSON.stringify(b), { status, headers: { ...cors, "Content-Type": "application/json" } });
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);

  let body: any;
  try { body = await req.json(); } catch { return json({ error: "bad json" }, 400); }
  const db = supa();
  const action = String(body.action || "");

  // ---- the scheduler ----
  if (action === "tick") {
    const { data: ck } = await db.from("sq_push_keys").select("v").eq("k", "cron").maybeSingle();
    if (!ck || req.headers.get("x-cron-key") !== ck.v) return json({ error: "no" }, 403);
    const keys = await vapidKeys(db);
    const { data: rows } = await db.from("sq_push").select("*");
    let sent = 0;
    for (const r of rows || []) {
      const now = localNow(r.tz);
      const [h, m] = String(r.remind_at).split(":").map(Number);
      const due = h * 60 + m;
      if (now.mins < due || now.mins > due + 90) continue;                       // only in the 90 minutes after their time
      if (r.last_sent === now.date || r.last_done === now.date) continue;        // one a day, and never after a finished sprint
      const days: number[] = r.test_days || [];
      if (days.includes(now.dow)) continue;                                      // test day: no nagging
      const eve = days.includes((now.dow + 1) % 7);
      const msg = { title: eve ? "Test tomorrow! 🐝" : "Spelling Quest",
        body: eve ? "One last practice with Scout tonight?" : LINES[Math.floor(Math.random() * LINES.length)],
        url: "/app/", tag: "sq-daily" };
      const code = await sendOne(keys, r.sub, msg).catch(() => 0);
      if (code === 404 || code === 410) { await db.from("sq_push").delete().eq("endpoint", r.endpoint); continue; }
      if (code >= 200 && code < 300){ sent++; await db.from("sq_push").update({ last_sent: now.date }).eq("endpoint", r.endpoint); }
    }
    return json({ ok: true, sent });
  }

  if (!okOrigin) return json({ error: "origin" }, 403);

  if (action === "key") return json({ publicKey: (await vapidKeys(db)).publicKey });

  if (action === "subscribe") {
    const s = body.sub;
    if (!okSub(s)) return json({ error: "bad subscription" }, 400);
    const row = { endpoint: String(s.endpoint).slice(0, 1000), sub: { endpoint: s.endpoint, keys: { p256dh: s.keys.p256dh, auth: s.keys.auth } },
      tz: cleanTz(body.tz) || "America/Chicago", remind_at: cleanTime(body.remind_at) || "18:30",
      test_days: cleanDays(body.test_days) || [], fam: cleanFam(body.fam), updated_at: new Date().toISOString() };
    const { error } = await db.from("sq_push").upsert(row, { onConflict: "endpoint" });
    return error ? json({ error: "store" }, 500) : json({ ok: true, on: true });
  }

  /* a sprint finished on any of the family's devices (the child's iPad, say)
     cancels today's reminder on all of them (the grown-up's phone) */
  if (action === "done") {
    const date = String(body.date || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return json({ error: "date" }, 400);
    const fam = cleanFam(body.fam), ep = /^https:\/\//.test(String(body.endpoint || "")) ? String(body.endpoint) : null;
    if (fam) await db.from("sq_push").update({ last_done: date }).eq("fam", fam);
    if (ep) await db.from("sq_push").update({ last_done: date }).eq("endpoint", ep);
    return json({ ok: true });
  }

  const endpoint = String(body.endpoint || "");
  if (!/^https:\/\//.test(endpoint)) return json({ error: "endpoint" }, 400);

  if (action === "unsubscribe") {
    await db.from("sq_push").delete().eq("endpoint", endpoint);
    return json({ ok: true, on: false });
  }
  if (action === "update") {
    const patch: any = { updated_at: new Date().toISOString() };
    if (cleanTime(body.remind_at)) patch.remind_at = cleanTime(body.remind_at);
    if (cleanTz(body.tz)) patch.tz = cleanTz(body.tz);
    if (cleanDays(body.test_days)) patch.test_days = cleanDays(body.test_days);
    if (/^\d{4}-\d{2}-\d{2}$/.test(String(body.done || ""))) patch.last_done = body.done;
    if (cleanFam(body.fam)) patch.fam = cleanFam(body.fam);
    const { data, error } = await db.from("sq_push").update(patch).eq("endpoint", endpoint).select("endpoint");
    if (error) return json({ error: "store" }, 500);
    return json({ ok: true, on: !!(data && data.length) });
  }
  if (action === "test") {
    const { data: r } = await db.from("sq_push").select("sub").eq("endpoint", endpoint).maybeSingle();
    if (!r) return json({ ok: false, on: false });
    const code = await sendOne(await vapidKeys(db), r.sub, { title: "Reminders are on ✨", body: "Scout will nudge you when it's time for today's sprint.", url: "/app/", tag: "sq-test" }).catch(() => 0);
    return json({ ok: code >= 200 && code < 300, status: code });
  }
  return json({ error: "action" }, 400);
});

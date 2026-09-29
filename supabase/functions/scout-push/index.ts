// Spelling Quest: Scout's reminders (web push), 29 Sep 2026.
//
// Modelled on Read Between The Lines' push.js: standard Web Push (RFC 8291
// aes128gcm payloads, RFC 8292 VAPID), no third-party service. Off until a
// grown-up turns it on, and at most one reminder a day per device.
//
// POST { action, ... } from the app:
//   key                          -> { publicKey }
//   subscribe  { sub, tz, remind_at, test_days, fam?, plan?, groups? }   (fam: the family's scrambled sync code, when there is one)
//   done       { date, fam?, endpoint? }  a sprint was finished today on some device of this family
//   update     { endpoint, tz?, remind_at?, test_days?, done?, fam?, plan?, groups?, seen? }
//              (done: 'YYYY-MM-DD', a sprint finished today; seen: the app was opened, so un-pause)
//   unsubscribe { endpoint }
//   test       { endpoint }      -> sends one right now
// POST { action:'tick' } with header x-cron-key, every 15 minutes from pg_cron:
//   sends each device its one message for today, in the 90 minutes after its
//   reminder time, never in quiet hours (8 pm to 7:30 am), and not at all after
//   three unopened reminders in a row, until the app is next opened.
//
// The plan (29 Sep 2026, SQ-Recommended-Notifications.pdf): the app works out
// the next nine days of possible reminders itself, since it knows each child's
// route, test day and review nights, and sends them here each time it opens.
// Each entry is { d:date, k:kind, t:title, b:body, p:priority, g:'week'|'account',
// nd:[dates], u:url }. On the day, the highest-priority entry whose group is on
// and none of whose nd dates had a finished sprint is sent. The texts never carry
// a child's name or words (the app builds them from sprint names only).
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

const KINDS = ["words", "nightly", "ppu", "eve", "test", "missed", "recap", "trial", "key"];
const isDate = (d: any) => /^\d{4}-\d{2}-\d{2}$/.test(String(d || ""));
const cleanStr = (t: any, n: number) => String(t || "").replace(/[\u0000-\u001f<>]/g, "").slice(0, n);
const cleanPlan = (pl: any) => {
  if (!Array.isArray(pl)) return null;
  return pl.slice(0, 80).filter((e: any) => e && isDate(e.d) && KINDS.includes(e.k) && e.t && e.b).map((e: any) => ({
    d: e.d, k: e.k, t: cleanStr(e.t, 80), b: cleanStr(e.b, 160),
    p: Math.max(0, Math.min(100, Number(e.p) || 0)), g: e.g === "account" ? "account" : "week",
    nd: Array.isArray(e.nd) ? e.nd.filter(isDate).slice(0, 3) : [],
    u: e.u === "/app/#open=prog" ? e.u : "/app/",
  }));
};
const cleanGroups = (g: any) => g && typeof g === "object" ? { week: g.week !== false, account: g.account !== false } : null;
const QUIET_FROM = 20 * 60;          // quiet hours 8 pm to 7:30 am
const QUIET_TO = 7 * 60 + 30;
const PAUSE_AFTER = 3;               // three ignored reminders in a row pause them until the app is opened
const daysBetween = (a: string, b: string) => Math.round((Date.parse(b) - Date.parse(a)) / 86400000);

/* today's one message for this device, or null */
function pick(r: any, now: { date: string; dow: number }) {
  const groups = r.groups || { week: true, account: true };
  const done: string[] = r.done_dates || [];
  if (Array.isArray(r.plan)) {
    const due = r.plan.filter((e: any) => e.d === now.date && groups[e.g] !== false &&
      !(e.nd || []).some((d: string) => done.includes(d)) &&
      !(e.k === "missed" && r.last_missed && daysBetween(r.last_missed, now.date) < 7));    // missed night: once a week at most
    due.sort((a: any, b: any) => b.p - a.p);
    const e = due[0];
    return e ? { title: e.t, body: e.b, url: e.u, tag: "sq-daily", kind: e.k } : null;
  }
  // no plan yet (an older copy of the app): the simple nightly nudge
  if (groups.week === false || r.last_done === now.date) return null;
  const days: number[] = r.test_days || [];
  if (days.includes(now.dow)) return null;
  const eve = days.includes((now.dow + 1) % 7);
  return { title: eve ? "Test tomorrow! 🐝" : "Spelling Quest",
    body: eve ? "One last practice with Scout tonight?" : LINES[Math.floor(Math.random() * LINES.length)],
    url: "/app/", tag: "sq-daily", kind: eve ? "eve" : "nightly" };
}

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
      if (now.mins >= QUIET_FROM || now.mins < QUIET_TO) continue;               // quiet hours
      if (r.last_sent === now.date) continue;                                    // one a day, at most
      if ((r.ignored || 0) >= PAUSE_AFTER) continue;                             // paused until the app is next opened
      const msg = pick(r, now);
      if (!msg) continue;
      const code = await sendOne(keys, r.sub, { title: msg.title, body: msg.body, url: msg.url, tag: msg.tag }).catch(() => 0);
      if (code === 404 || code === 410) { await db.from("sq_push").delete().eq("endpoint", r.endpoint); continue; }
      if (code >= 200 && code < 300){
        sent++;
        const patch: any = { last_sent: now.date, ignored: (r.ignored || 0) + 1 };
        if (msg.kind === "missed") patch.last_missed = now.date;
        await db.from("sq_push").update(patch).eq("endpoint", r.endpoint);
      }
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
      test_days: cleanDays(body.test_days) || [], fam: cleanFam(body.fam), plan: cleanPlan(body.plan),
      groups: cleanGroups(body.groups) || { week: true, account: true }, ignored: 0, updated_at: new Date().toISOString() };
    const { error } = await db.from("sq_push").upsert(row, { onConflict: "endpoint" });
    return error ? json({ error: "store" }, 500) : json({ ok: true, on: true });
  }

  /* a sprint finished on any of the family's devices (the child's iPad, say)
     cancels today's reminder on all of them (the grown-up's phone) */
  if (action === "done") {
    const date = String(body.date || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return json({ error: "date" }, 400);
    const fam = cleanFam(body.fam), ep = /^https:\/\//.test(String(body.endpoint || "")) ? String(body.endpoint) : null;
    const rows: any[] = [];
    if (fam) rows.push(...((await db.from("sq_push").select("endpoint, done_dates").eq("fam", fam)).data || []));
    if (ep && !rows.some((r) => r.endpoint === ep)) rows.push(...((await db.from("sq_push").select("endpoint, done_dates").eq("endpoint", ep)).data || []));
    for (const r of rows) {
      const dd = [...new Set([...(r.done_dates || []), date])].sort().slice(-21);   // three weeks is plenty
      // a finished sprint means the reminders are doing their job: never paused for "silence"
      await db.from("sq_push").update({ last_done: date, done_dates: dd, ignored: 0 }).eq("endpoint", r.endpoint);
    }
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
    if (cleanPlan(body.plan)) patch.plan = cleanPlan(body.plan);
    if (cleanGroups(body.groups)) patch.groups = cleanGroups(body.groups);
    if (body.seen === true) patch.ignored = 0;
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

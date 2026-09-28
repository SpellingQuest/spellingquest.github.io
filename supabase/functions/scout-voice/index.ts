// Spelling Quest: Scout the Bee's voice (28 Sep 2026).
//
// POST { text, speed: "normal" | "slow" | "sounds" | "align" }  ->  { url }
//
// "align" (29 Sep 2026): the word said slowly, plus the moment each letter is
// spoken (ElevenLabs with-timestamps). Stored as .mp3 and .json side by side.
// The app plays slices of Scout's own recording for Sound it out, which gives
// real letter sounds in her voice (the phoneme tags in "sounds" were ignored).
//
// "sounds" (29 Sep 2026): letter SOUNDS rather than letter names. The app sends
// SSML <phoneme alphabet="ipa"> and <break> tags (nothing else is allowed through)
// and they are read by eleven_flash_v2, the model that understands phoneme tags.
//
// Every phrase is recorded by ElevenLabs ONCE and stored in the public
// "scout-voice" bucket under sha256(VERSION|speed|text).mp3. The app tries that
// URL first and only calls this function when the file isn't there yet, so a
// word any family has ever heard costs nothing the second time.
//
// Secrets (Supabase dashboard -> Edge Functions -> Secrets):
//   ELEVENLABS_API_KEY  - required
//   SCOUT_VOICE_ID      - optional, overrides Scout's voice (default below, chosen by Kathryn 28 Sep 2026)
//   SCOUT_MODEL_ID      - optional, default eleven_multilingual_v2
// SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are provided automatically.
//
// VERSION must match SCOUT_VOICE_VERSION in app/index.html. Change both to
// re-record everything (for example after choosing a different voice).
import { createClient } from "npm:@supabase/supabase-js@2";

const VERSION = "v2";   // v2 (29 Sep 2026): single words recorded as "word." with sentence context, which stops the stray "ick" before clam and glad
const DEFAULT_VOICE_ID = "zz18v7gwMdL7XrVnYmMe";   // Scout's ElevenLabs voice (not a secret)
const BUCKET = "scout-voice";
const MAX_CHARS = 400;
const ALLOWED = [
  /^https:\/\/spellingquest\.github\.io$/,
  /^http:\/\/localhost(:\d+)?$/,
  /^http:\/\/127\.0\.0\.1(:\d+)?$/,
];

// Very small per-instance guard against runaway loops. The real cost cap is the
// ElevenLabs plan's character quota.
const hits = new Map<string, { n: number; t: number }>();
function tooMany(ip: string): boolean {
  const now = Date.now();
  const h = hits.get(ip);
  if (!h || now - h.t > 3600_000) { hits.set(ip, { n: 1, t: now }); return false; }
  h.n++;
  return h.n > 600;
}

async function sha256hex(s: string): Promise<string> {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin") || "";
  const okOrigin = ALLOWED.some((r) => r.test(origin));
  const cors = {
    "Access-Control-Allow-Origin": okOrigin ? origin : "https://spellingquest.github.io",
    "Access-Control-Allow-Headers": "authorization, apikey, content-type, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
  const json = (body: unknown, status = 200) =>
    new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!okOrigin) return json({ error: "origin" }, 403);

  const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "unknown";
  if (tooMany(ip)) return json({ error: "slow down" }, 429);

  let body: { text?: string; speed?: string };
  try { body = await req.json(); } catch { return json({ error: "bad json" }, 400); }
  // The app sends text already tidied the same way; tidy again so the key is stable.
  const text = String(body.text || "").replace(/\s+/g, " ").trim();
  const speed = body.speed === "slow" ? "slow" : body.speed === "sounds" ? "sounds" : body.speed === "align" ? "align" : "normal";
  if (!text || text.length > (speed === "sounds" ? 900 : MAX_CHARS)) return json({ error: "text" }, 400);
  // sounds mode: only phoneme and break tags, nothing else that looks like markup
  if (speed === "sounds") {
    const stripped = text
      .replace(/<phoneme alphabet="ipa" ph="[^"<>]{1,12}">[a-z']{1,6}<\/phoneme>/g, "")
      .replace(/<break time="\d(\.\d)?s" \/>/g, "");
    if (/[<>]/.test(stripped)) return json({ error: "text" }, 400);
  } else if (/[<>]/.test(text)) return json({ error: "text" }, 400);

  const apiKey = Deno.env.get("ELEVENLABS_API_KEY");
  const voiceId = Deno.env.get("SCOUT_VOICE_ID") || DEFAULT_VOICE_ID;
  if (!apiKey || !voiceId) return json({ error: "not configured" }, 503);
  const model = speed === "sounds" ? "eleven_flash_v2" : (Deno.env.get("SCOUT_MODEL_ID") || "eleven_multilingual_v2");
  /* ElevenLabs sometimes adds a stray sound ("ick-clam", "ig-glad") in front of a
     word said on its own. A full stop plus the sentence it lives in (not spoken)
     gives it a clean start. */
  const words = text.split(" ").length;
  if (speed === "align" && (words !== 1 || !/^[A-Za-z'-]+$/.test(text))) return json({ error: "text" }, 400);
  const say = speed !== "sounds" && words === 1 && /^[A-Za-z'-]+$/.test(text) ? text + "." : text;
  const context = speed !== "sounds" && words <= 3
    ? { previous_text: "Okay, here is our next word.", next_text: "Can you say it with me?" } : {};

  const supa = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const path = (await sha256hex(`${VERSION}|${speed}|${text}`)) + ".mp3";
  const publicUrl = supa.storage.from(BUCKET).getPublicUrl(path).data.publicUrl;

  // Already recorded? (Another device may have asked a moment ago.)
  const head = await fetch(speed === "align" ? publicUrl.replace(/\.mp3$/, ".json") : publicUrl, { method: "HEAD" });
  if (head.ok) return json({ url: publicUrl, cached: true, ...(speed === "align" ? { align: publicUrl.replace(/\.mp3$/, ".json") } : {}) });

  if (speed === "align") {
    const r = await fetch(
      `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}/with-timestamps?output_format=mp3_44100_64`,
      {
        method: "POST",
        headers: { "xi-api-key": apiKey, "Content-Type": "application/json" },
        body: JSON.stringify({
          text: say, model_id: model, ...context,
          voice_settings: { stability: 0.6, similarity_boost: 0.8, style: 0.15, use_speaker_boost: true, speed: 0.7 },
        }),
      },
    );
    if (!r.ok) { console.error("elevenlabs align", r.status, (await r.text()).slice(0, 300)); return json({ error: "tts", status: r.status }, 502); }
    const j = await r.json();
    const audio = Uint8Array.from(atob(j.audio_base64), (c) => c.charCodeAt(0));
    const al = j.alignment || j.normalized_alignment || {};
    const meta = { text: say, chars: al.characters || [], start: al.character_start_times_seconds || [], end: al.character_end_times_seconds || [] };
    const jsonPath = path.replace(/\.mp3$/, ".json");
    const up1 = await supa.storage.from(BUCKET).upload(jsonPath, new TextEncoder().encode(JSON.stringify(meta)),
      { contentType: "application/json", cacheControl: "31536000", upsert: true });
    const up2 = await supa.storage.from(BUCKET).upload(path, audio, { contentType: "audio/mpeg", cacheControl: "31536000", upsert: true });
    if (up1.error || up2.error) { console.error("upload", (up1.error || up2.error)!.message); return json({ error: "store" }, 500); }
    return json({ url: publicUrl, align: publicUrl.replace(/\.mp3$/, ".json"), cached: false });
  }

  const tts = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}?output_format=mp3_44100_64`,
    {
      method: "POST",
      headers: { "xi-api-key": apiKey, "Content-Type": "application/json", "Accept": "audio/mpeg" },
      body: JSON.stringify({
        text: say,
        model_id: model,
        ...context,
        voice_settings: {
          stability: 0.55,
          similarity_boost: 0.8,
          style: 0.25,
          use_speaker_boost: true,
          speed: speed === "slow" ? 0.75 : speed === "sounds" ? 0.9 : 1.0,
        },
      }),
    },
  );
  if (!tts.ok) {
    const detail = (await tts.text()).slice(0, 300);
    console.error("elevenlabs", tts.status, detail);
    return json({ error: "tts", status: tts.status }, 502);
  }
  const audio = new Uint8Array(await tts.arrayBuffer());
  const up = await supa.storage.from(BUCKET).upload(path, audio, {
    contentType: "audio/mpeg",
    cacheControl: "31536000",
    upsert: true,
  });
  if (up.error) {
    console.error("upload", up.error.message);
    return json({ error: "store" }, 500);
  }
  return json({ url: publicUrl, cached: false });
});

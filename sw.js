/* Spelling Quest service worker.
   Written 25 Aug 2026, following Universal Files/Service-Workers-Offline-and-Install.md.

   🔴 THE RULE: the HTML is NEVER served cache-first.

   Spelling Quest is a SINGLE hand-written index.html with no build step and no
   stamped (?v=) assets. That removes our margin for error rather than making
   this simpler: the HTML *is* the whole application. Cache it cache-first and a
   family is frozen on that build for ever, and the only way out is them
   clearing site data. There is no partial version of that failure here.

   Because nothing is stamped, there is deliberately NO cache-first branch for
   scripts. The only cache-first candidates are images and fonts — stable URLs,
   safe to reuse, cheap to re-fetch if evicted.

   Bump CACHE to throw everything away. */
const CACHE = 'spellingquest-v1';

/* Kept deliberately small. Never precache heavy media: downloading everything
   on a first visit, to a site nobody has paid for yet, is rude. */
const SHELL = ['./', './index.html', './logo.png', './manifest.webmanifest'];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c =>
    // Individually, not addAll: one 404 in addAll aborts the whole install and
    // leaves the site with no worker at all.
    Promise.all(SHELL.map(u => c.add(u).catch(() => {})))
  ));
});

self.addEventListener('activate', e => e.waitUntil((async () => {
  const names = await caches.keys();
  await Promise.all(names.map(n => n !== CACHE ? caches.delete(n) : null));
  await self.clients.claim();          // take over tabs that are already open
})()));

const isPage = req =>
  req.mode === 'navigate' ||
  (req.headers.get('accept') || '').includes('text/html');

const isCacheable = url =>
  /\.(png|jpg|jpeg|gif|webp|svg|woff2?|ttf|otf|mp3|m4a|wav)$/i.test(url.pathname);

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Never touch Supabase or anything else cross-origin. A family's progress
  // must never be answered out of a cache.
  if (url.origin !== self.location.origin) return;

  if (isPage(req)) {
    /* NETWORK FIRST. A push is picked up on the next ordinary load, exactly as
       it would be with no worker at all. The cache is only a fallback for when
       the network genuinely is not there. */
    e.respondWith((async () => {
      try {
        /* {cache:'no-store'} matters far more than it looks. A plain fetch() of a
           navigation request inside a worker can still be answered from the
           browser's OWN HTTP cache, so a new build is not picked up on an
           ordinary reload — the exact failure this whole file exists to prevent.
           Measured, not assumed: without this, test 3 failed here while the same
           page with NO worker passed. Network-first is only network-first if you
           say so explicitly. Do not remove. */
        const fresh = await fetch(req.url, { cache: 'no-store', credentials: 'same-origin' });
        if (fresh && fresh.ok) (await caches.open(CACHE)).put(req, fresh.clone());
        return fresh;
      } catch {
        return (await caches.match(req))
            || (await caches.match('./index.html'))
            || Response.error();
      }
    })());
    return;
  }

  if (isCacheable(url)) {
    /* Cache first, filled as pages are opened rather than precached. */
    e.respondWith((async () => {
      const hit = await caches.match(req);
      if (hit) return hit;
      try {
        const fresh = await fetch(req);
        if (fresh && fresh.ok) (await caches.open(CACHE)).put(req, fresh.clone());
        return fresh;
      } catch {
        return Response.error();
      }
    })());
    return;
  }

  // Anything else goes straight to the network.
});

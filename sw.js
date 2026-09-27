/* Retired root service worker — 27 Sep 2026.

   Until 27 Sep 2026 the app lived at the site root and this worker controlled
   every page. The app now lives in /app/ with its own worker (app/sw.js), and the
   root belongs to the website, which needs no worker at all.

   A browser that installed the old worker keeps checking this URL for updates.
   This version clears the old caches and unregisters itself, so the website
   pages are always served straight from the network. Leave it in place for a
   few months, then it can be deleted. */
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => e.waitUntil((async () => {
  const names = await caches.keys();
  await Promise.all(names.filter(n => n === 'spellingquest-v1').map(n => caches.delete(n)));
  await self.registration.unregister();
})()));

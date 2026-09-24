const CACHE_NAME = 'dinesh-dabeli-v7';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/bootstrap.css',
  '/static/font-awesome.min.css',
  '/static/images/favicon.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => Promise.all(
        cacheNames
          .filter(cacheName => cacheName !== CACHE_NAME)
          .map(cacheName => caches.delete(cacheName))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const isNavigation = request.mode === 'navigate' || request.destination === 'document';

  if (isNavigation) {
    // Always prefer fresh HTML so menu/catalog updates reach customers.
    event.respondWith(
      fetch(request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          return response;
        })
        .catch(() => caches.match(request).then(response => response || caches.match('/')))
    );
    return;
  }

  // Static assets are immutable enough for cache-first delivery.
  event.respondWith(
    caches.match(request).then(response => response || fetch(request))
  );
});

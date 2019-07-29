importScripts('static/cache-polyfill.js');

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open('airhorner').then(function(cache) {
      return cache.addAll([
        '/',
        './templates/layout.html',
        './templates/offline.html',
        './static/css/style.css'
      ]);
    })
  );
 });
 self.addEventListener('fetch', function(event) {
  console.log(event.request.url);
  });
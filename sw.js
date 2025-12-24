const CACHE_NAME = 'wonderland-v2.0.0';
const urlsToCache = [
  './',
  './index.html',
  './memory_game.html',
  './gallery.html',
  './favorite.html', 
  './about.html',
  './data/wonderland_data.js',
  './data/wonderland_data.json',
  './manifest.json'
];

// Instalar Service Worker
self.addEventListener('install', event => {
  console.log('SW: Instalando...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('SW: Cacheando archivos principales...');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('SW: Archivos principales cacheados');
        return self.skipWaiting(); // Forzar activación inmediata
      })
      .catch(error => {
        console.error('SW: Error en instalación:', error);
      })
  );
});

// Activar Service Worker
self.addEventListener('activate', event => {
  console.log('SW: Activando...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('SW: Borrando cache antiguo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('SW: Activado y controlando todas las páginas');
      return self.clients.claim(); // Tomar control inmediatamente
    })
  );
});

// Interceptar requests
self.addEventListener('fetch', event => {
  // Solo manejar requests HTTP/HTTPS
  if (!event.request.url.startsWith('http')) return;
  
  console.log('SW: Interceptando:', event.request.url);
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          console.log('SW: Sirviendo desde cache:', event.request.url);
          return response;
        }
        
        console.log('SW: Descargando:', event.request.url);
        return fetch(event.request)
          .then(fetchResponse => {
            // Solo cachear respuestas exitosas
            if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
              return fetchResponse;
            }
            
            // Clonar la respuesta para guardarla en cache
            const responseToCache = fetchResponse.clone();
            
            caches.open(CACHE_NAME)
              .then(cache => {
                console.log('SW: Guardando en cache:', event.request.url);
                cache.put(event.request, responseToCache);
              });
            
            return fetchResponse;
          })
          .catch(error => {
            console.log('SW: Error descargando:', event.request.url, error);
            
            // Si es una página HTML, devolver index como fallback
            if (event.request.headers.get('accept') && 
                event.request.headers.get('accept').includes('text/html')) {
              return caches.match('./index.html');
            }
            
            // Para otros archivos, devolver una respuesta vacía
            return new Response('', { 
              status: 404, 
              statusText: 'Not Found' 
            });
          });
      })
  );
});
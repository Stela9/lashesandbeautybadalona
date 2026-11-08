# Lashes & Beauty Badalona

Web del centro de estética Lashes & Beauty Badalona (Via Augusta, 5 · Badalona).
Web: https://lashesandbeautybadalona.es — sitio estático publicado con Cloudflare Pages: cada cambio en la rama `main` se publica automáticamente.

## Estructura

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Página completa (textos, estilos y estructura) |
| `assets/app.js` | Carta de servicios y precios (`SERVICES`), Black Friday, menú móvil, mapa, blog |
| `assets/bf.js` | Oculta el aviso de Black Friday cuando pasa la fecha (`data-hasta` del aviso en `index.html`) |
| `assets/img/` | Fotos de servicios e imagen para compartir (`og-image.jpg`) |
| `assets/video/` | Vídeo del centro y su imagen de portada |
| `assets/fonts/` | Tipografías (servidas desde la propia web, sin Google Fonts) |
| `_headers` | Cabeceras de seguridad y caché de Cloudflare Pages |
| `404.html`, `robots.txt`, `sitemap.xml` | Página de error, instrucciones para buscadores y mapa del sitio |
| `assets/site.css` | Estilos compartidos por todas las páginas |
| `assets/menu.js` | Menú desplegable del móvil (todas las páginas) |
| `blog/` | Índice del blog y un archivo por artículo |
| `aviso-legal.html`, `privacidad.html`, `cookies.html` | Páginas legales (LSSI y RGPD) |
| `functions/_middleware.js` | Redirige `www.` y `*.pages.dev` al dominio principal `lashesandbeautybadalona.es` |

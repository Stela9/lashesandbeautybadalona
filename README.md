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
| `tools/carta.js` | Copia la carta de servicios dentro de `index.html` y `ca/index.html` (para que funcione sin JavaScript). **Ejecutar `node tools/carta.js` cada vez que se cambien servicios o precios en `assets/app.js`** |
| `ca/` | Versión en catalán (generada: no editar a mano) |
| `assets/i18n-ca.js` | Traducción al catalán de la carta de servicios y de los botones |
| `tools/ca.py` | Genera `ca/` a partir de las páginas en castellano y añade el selector de idioma y `hreflang` a todas |

## Cómo hacer cambios

1. Edita las páginas en castellano (y `assets/app.js` para servicios y precios).
2. Si cambias un texto, cambia también su traducción en `tools/ca.py` (páginas) o en `assets/i18n-ca.js` (carta).
3. Ejecuta, en este orden:

```
python3 tools/ca.py
node tools/carta.js
```

`tools/ca.py` se detiene si no encuentra un texto en castellano que debería traducir, y `tools/carta.js` si en la carta catalana queda algo sin traducir.

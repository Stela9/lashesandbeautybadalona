// Redirige www.lashesandbeautybadalona.es y la dirección antigua *.pages.dev
// al dominio principal, conservando la ruta (301 = cambio permanente).
const PRINCIPAL = "lashesandbeautybadalona.es";
const REDIRIGIR = new Set(["www.lashesandbeautybadalona.es", "lashesandbeautybadalona.pages.dev"]);

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (REDIRIGIR.has(url.hostname)) {
    url.hostname = PRINCIPAL;
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return next();
}

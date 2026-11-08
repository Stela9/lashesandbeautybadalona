/* Oculta el aviso de Black Friday en cuanto pasa la fecha de data-hasta (se ejecuta antes de pintar el resto). */
(function () {
  var b = document.getElementById("bf-banner");
  if (b && Date.now() >= new Date(b.getAttribute("data-hasta")).getTime()) b.hidden = true;
})();

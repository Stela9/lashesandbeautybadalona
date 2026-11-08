/* Menú en móvil */
const menuBtn = document.getElementById("menu-btn"), menu = document.getElementById("menu");
menuBtn.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
  menuBtn.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
});
menu.addEventListener("click", e => { if (e.target.closest("a")) { menu.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.setAttribute("aria-label", "Abrir menú"); } });

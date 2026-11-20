/* Textos del menú según el idioma de la página */
const MENU_TXT = document.documentElement.lang === "ca" ? ["Obre el menú", "Tanca el menú"] : ["Abrir menú", "Cerrar menú"];
/* Menú en móvil */
const menuBtn = document.getElementById("menu-btn"), menu = document.getElementById("menu");
menuBtn.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
  menuBtn.setAttribute("aria-label", open ? MENU_TXT[1] : MENU_TXT[0]);
});
menu.addEventListener("click", e => { if (e.target.closest("a")) { menu.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.setAttribute("aria-label", MENU_TXT[0]); } });

/* Escape cierra el menú y devuelve el foco al botón */
document.addEventListener("keydown", e => {
  if (e.key === "Escape" && menu.classList.contains("open")) {
    menu.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.setAttribute("aria-label", MENU_TXT[0]);
    menuBtn.focus();
  }
});

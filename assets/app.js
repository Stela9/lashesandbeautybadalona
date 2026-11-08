/* ==========================================================
   CONFIGURACIÓN — edita aquí enlaces y servicios
   ========================================================== */
const BOOKING_URL = "https://widget.treatwell.es/establecimiento/lashes-beauty-badalona/";
const WHATSAPP    = "34659344275";
const WA_TEXT     = "Hola! Me gustaría pedir información sobre vuestros servicios 😊";

/* price: precio en euros.  old: precio anterior tachado (opcional).
   retoque: precio del retoque (opcional).  badge: etiqueta destacada (opcional). */
/* ===== BLACK FRIDAY =====
   Se muestra automáticamente hasta la fecha BF_HASTA y después desaparece sola. */
const BF_HASTA = document.getElementById("bf-banner").dataset.hasta;   // se edita en index.html (aviso de Black Friday)
const BLACK_FRIDAY = [
    { sub:"Promociones Black Friday", note:"Para citas hasta el 30 de noviembre.", items:[
        { name:"Microblading / micropigmentación de cejas", desc:"Cejas perfectas y naturales a un precio único. Incluye un retoque a las 4 semanas.", price:150, old:250, badge:"-40%" },
        { name:"Remodelación corporal I-MODEL · Bono 10 sesiones", desc:"Tonificación, reducción de celulitis, quema de grasa y moldeado de la figura.", price:195, old:490, badge:"-60%" },
        { name:"Dermapen con exosomas · Bono 4 sesiones", desc:"Regeneración anti-edad extrema: más firmeza y elasticidad, menos arrugas y poros.", price:195, old:316, badge:"-38%" },
        { name:"Hydraface – limpieza facial profunda", desc:"Limpieza profunda, dermoabrasión, exfoliación, extracción de impurezas e hidratación.", time:"1 h 15 min", price:59, old:99, badge:"-40%" } ]},
];
const BF_ACTIVO = Date.now() < new Date(BF_HASTA).getTime();
/* ======================== */

/* Fotos de resultados (recortadas del cartel «Realza tu mirada») */
const IMG = {
  "lifting-tinte": "assets/img/lifting-tinte.jpg",
  "laminado-cejas": "assets/img/laminado-cejas.jpg",
  "efecto-rimel": "assets/img/efecto-rimel.jpg",
  "hibridas": "assets/img/hibridas.jpg",
  "volumen-3d": "assets/img/volumen-3d.jpg",
  "volumen-glam": "assets/img/volumen-glam.jpg",
  "wispy": "assets/img/wispy.jpg",
  "efecto-mojado": "assets/img/efecto-mojado.jpg"
};

let SERVICES = {
  "Cejas": [
    { sub:"Diseño y depilación con hilo", items:[
        { name:"Depilación de cejas con hilo", desc:"Técnica natural y nada agresiva, ideal para pieles sensibles.", time:"15 min", price:11 },
        { name:"Diseño + depilación de cejas", desc:"Tomamos medidas y diseñamos la forma ideal según tus facciones.", time:"30 min", price:16 } ]},
    { sub:"Laminado y henna", items:[
        { img:"laminado-cejas", name:"Laminado de cejas", desc:"Alisado que peina y fija tus cejas, ideal si tienes remolinos.", time:"15 min", price:40 },
        { name:"Laminado + diseño de cejas + depilación", desc:"Cejas elegantes y definidas con la tecnología de la laminación.", time:"30 min", price:50 },
        { name:"Henna de cejas", desc:"Cejas más definidas y con volumen de forma natural.", time:"15 min", price:10 } ]},
  ],
  "Pestañas": [
    { sub:"Extensiones express", items:[
        { name:"Express pelo a pelo salteadas", desc:"Extensiones salteadas para una ocasión puntual. Look muy natural.", time:"1 h", price:35 },
        { name:"Express volumen 3D salteadas", desc:"Extensiones de volumen salteadas para una ocasión puntual.", time:"1 h", price:49 } ]},
    { sub:"Extensiones · puesta completa", items:[
        { img:"efecto-rimel", name:"Efecto rímel", desc:"Puesta completa con efecto natural, como si llevaras máscara. Ideal para iniciarte.", time:"1 h 30 min", price:59, retoque:39 },
        { img:"hibridas", name:"Híbridas", desc:"Puesta completa combinando pelo a pelo y volumen. Perfectas si tienes pocas pestañas.", time:"1 h 30 min", price:65, retoque:45 },
        { img:"volumen-3d", name:"Volumen ruso elegante 3D", desc:"Puesta completa que duplica y triplica tus pestañas.", time:"1 h 30 min", price:69, retoque:50 },
        { img:"volumen-glam", name:"Volumen ruso glam 5D", desc:"Puesta completa para lucir unas pestañas tupidas y con mucho impacto.", time:"1 h 30 min", price:75, retoque:55 },
        { img:"wispy", name:"Wispy", desc:"Puesta completa con pestañas más largas, tupidas y efecto puntas.", time:"1 h 30 min", price:79, retoque:59 },
        { img:"efecto-mojado", name:"Efecto mojado", desc:"Puesta completa con el look 'wet' cada vez más demandado.", time:"1 h 30 min", price:79, retoque:59 } ]},
    { sub:"Retirada y cuidado", items:[
        { name:"Retirada de extensiones del centro", desc:"Retirada segura sin dañar tus pestañas naturales.", time:"30 min", price:15 },
        { name:"Retirada de extensiones de otro centro", desc:"Retirada segura sin dañar tus pestañas naturales.", time:"30 min", price:19 },
        { name:"Mousse limpiadora", desc:"Para la higiene diaria de tus extensiones en casa.", price:17, product:true },
        { name:"Sérum de pestañas", desc:"Fortalece y cuida tus pestañas naturales.", price:45, product:true } ]},
    { sub:"Lifting y tinte", items:[
        { name:"Lifting de pestañas coreano (sin tinte)", desc:"Pestañas más largas, elevadas e hidratadas. Dura de 6 a 8 semanas.", time:"45 min", price:39 },
        { img:"lifting-tinte", name:"Lifting de pestañas coreano (con tinte)", desc:"Curvatura natural y color intenso para tus pestañas.", time:"1 h", price:45 },
        { name:"Tinte de pestañas", desc:"La intensidad del negro sin máscara de pestañas.", time:"15 min", price:10 },
        { name:"Pack laminado de pestañas y cejas", desc:"Incluye lifting de pestañas coreano + tinte y laminado de cejas.", time:"1 h", price:69 } ]},
  ],
  "Micropigmentación": [
    { sub:"Cejas · -20% dto", items:[
        { name:"Microblading (efecto pelo a pelo)", desc:"Cejas tupidas y naturales. Incluye un retoque a las 4 semanas.", time:"1 h 30 min", price:200, old:250, badge:"-20%" },
        { name:"Micropigmentación (sombreado)", desc:"Cejas perfectas durante mucho tiempo. Incluye un retoque a las 4 semanas.", time:"2 h", price:200, old:250, badge:"-20%" },
        { name:"Hybrid brows (técnica mixta)", desc:"Combinación de técnicas para un resultado muy natural. Incluye un retoque a las 4 semanas.", time:"2 h", price:224, old:280, badge:"-20%" } ]},
    { sub:"Ojos · -20% dto", items:[
        { name:"Baby eyeliner (entrepestañas)", desc:"Más densidad en la línea de pestañas sin maquillarte. Incluye un retoque a las 4 semanas.", time:"1 h", price:144, old:180, badge:"-20%" },
        { name:"Eyeliner clásico", desc:"Ahórrate el maquillaje de ojos cada mañana. Incluye un retoque a las 4 semanas.", time:"2 h", price:200, old:250, badge:"-20%" } ]},
    { sub:"Labios · -20% dto", items:[
        { name:"Perfilado de labios", desc:"Micropigmentación del contorno de labios. Incluye un retoque a las 4 semanas.", time:"1 h", price:144, old:180, badge:"-20%" },
        { name:"Labios candy acuarela", desc:"Color difuminado y natural en todo el labio. Incluye un retoque a las 4 semanas.", time:"3 h", price:200, old:250, badge:"-20%" },
        { name:"Full lips", desc:"Labios con color completo y definido. Incluye un retoque a las 4 semanas.", time:"3 h", price:224, old:280, badge:"-20%" } ]},
    { sub:"Retoques", note:"Para cejas, ojos y labios.", items:[
        { name:"Retoque hasta los 6 meses", desc:"Precio para trabajos realizados anteriormente en nuestro centro.", price:60 },
        { name:"Retoque de 6 a 11 meses", desc:"Precio para trabajos realizados anteriormente en nuestro centro.", price:90 },
        { name:"Retoque anual", desc:"Retoque de maquillaje semipermanente.", price:110 } ]},
  ],
  "Tratamientos faciales": [
    { sub:"Limpiezas y peelings", items:[
        { name:"Limpieza facial profunda", desc:"Limpieza de 6 pasos para limpiar, exfoliar, con extracción de comedones, desinfección, mascarilla nutritiva y crema hidratante finalizadora.", time:"1 h", price:59 },
        { name:"Hydraface – limpieza facial profunda", desc:"Tratamiento facial completo que combina limpieza profunda, dermoabrasión, exfoliación, extracción de impurezas e hidratación.", time:"1 h 15 min", price:79, old:99 },
        { name:"Peelings químicos", desc:"Exfolia la piel para renovar su apariencia, mejorando textura, luminosidad y reduciendo manchas o arrugas. Ideal para rejuvenecer y refrescar el rostro.", time:"1 h", price:59 } ]},
    { sub:"Dermapen", items:[
        { name:"Dermapen facial", desc:"Microagujas que estimulan el colágeno, mejorando la textura de la piel y reduciendo arrugas, cicatrices y manchas. Con ácido hialurónico, retinol, vitaminas, niacinamida y sérum efecto bótox.", time:"45 min", price:59 },
        { name:"Dermapen exosomas", desc:"Regeneración anti-edad extrema: aumenta la elasticidad y firmeza, reduce arrugas, mejora la textura, reduce los poros e iguala el tono.", time:"45 min", price:79 },
        { name:"Dermapen labios", desc:"Mejora la hidratación, suaviza las líneas de expresión y rejuvenece la piel de forma natural.", time:"15 min", price:45 } ]},
    { sub:"Bonos", items:[
        { name:"Bono 3+1 sesión gratis", desc:"Combina las sesiones que más necesites entre limpieza facial profunda, peelings y dermapen, y la cuarta te la llevas de regalo (excepto exosomas).", price:177, old:236, badge:"1 gratis" },
        { name:"Bono 4 sesiones exosomas", desc:"Te regalamos la crema facial Exoskyn de Utsukusy Cosmetics (valorada en 85 €), con exosomas de centella asiática y retinol, para complementar tu tratamiento en casa.", price:290, old:401, badge:"Regalo" } ]},
    { sub:"Depilación facial con hilo", items:[
        { name:"Labio superior con hilo", desc:"Depilación con hilo, recomendada para pieles sensibles.", price:6 },
        { name:"Mentón con hilo", desc:"Depilación con hilo, recomendada para pieles sensibles.", price:6 },
        { name:"Patillas con hilo", desc:"Depilación con hilo, recomendada para pieles sensibles.", price:11 },
        { name:"Depilación facial completa", desc:"Todo el rostro con hilo, recomendada para pieles sensibles.", price:32 } ]},
  ],
  "Tratamientos corporales": [
    { sub:"I-MODEL · remodelación corporal", items:[
        { name:"I-MODEL · 1 sesión", desc:"Remodelación corporal en sesiones de 25 minutos: tonificación, reducción de celulitis, quema de grasa y moldeado de glúteos, brazos, piernas, abdomen y espalda.", time:"25 min", price:49 },
        { name:"I-MODEL · Bono 6 sesiones", desc:"Remodelación corporal: tonifica y reduce la grasa almacenada ganando masa muscular.", price:240 },
        { name:"I-MODEL · Bono 10 sesiones", desc:"Remodelación corporal: tonifica y reduce la grasa almacenada ganando masa muscular.", price:290 } ]},
  ],
};
/* ========================================================== */

const fmt = n => n.toLocaleString("es-ES",{minimumFractionDigits:n%1?2:0,maximumFractionDigits:2}) + " €";
const waLink = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(WA_TEXT)}`;
document.querySelectorAll(".js-book").forEach(a => a.href = BOOKING_URL);
document.querySelectorAll(".js-wa").forEach(a => a.href = waLink);
document.querySelectorAll(".js-wa-gift").forEach(a => a.href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent("Hola! Me gustaría comprar una tarjeta regalo 🎁")}`);
document.getElementById("year").textContent = new Date().getFullYear();

const tabsEl = document.getElementById("tabs"), listEl = document.getElementById("services");
if (BF_ACTIVO) {
  SERVICES = { "Black Friday": BLACK_FRIDAY, ...SERVICES };
  document.getElementById("bf-banner").addEventListener("click", () => render("Black Friday"));
}
const cats = ["Todos", ...Object.keys(SERVICES)];
const card = (s, h = 4) => `
    <article class="svc${s.img ? ' has-img' : ''}">${s.img ? `<img class="svc-img" src="${IMG[s.img]}" alt="${s.name}" loading="lazy">` : ''}<div class="svc-body">
      <div class="svc-top">
        <h${h} class="svc-name">${s.name}${s.badge ? ` <span class="badge">${s.badge}</span>` : ''}</h${h}>
        <div class="price">${(s.from ? '<small>desde</small>' : '') + fmt(s.price) + (s.old ? `<s>${fmt(s.old)}</s>` : '')}</div>
      </div>
      <p>${s.desc}</p>${s.retoque ? `<p class="ret">Retoque (3ª semana): <b>${fmt(s.retoque)}</b></p>` : ''}
      <div class="meta"><span>${s.time ? '⏱ ' + s.time : ''}</span>
        ${s.product ? '<span class="instore">Producto · venta en el centro</span>' : `<a href="${BOOKING_URL}" target="_blank" rel="noopener">Reservar →</a>`}</div>
    </div></article>`;
const group = (cat, showTitle) => {
  const L = showTitle ? 4 : 3;   // con «Todos»: h3 categoría > h4 apartado > h5 servicio
  return (showTitle ? `<h3 class="cat-title">${cat}</h3>` : '') +
    SERVICES[cat].map(g => `<h${L} class="sub-title">${g.sub}${g.note ? `<span>${g.note}</span>` : ''}</h${L}>` + g.items.map(s => card(s, L + 1)).join("")).join("");
};
function render(cat){
  tabsEl.querySelectorAll(".tab").forEach(t => t.setAttribute("aria-selected", t.dataset.cat === cat));
  listEl.innerHTML = cat === "Todos" ? Object.keys(SERVICES).map(c => group(c, true)).join("") : group(cat, false);
}
tabsEl.innerHTML = cats.map(c => `<button class="tab${c === "Black Friday" ? " tab-bf" : ""}" role="tab" data-cat="${c}">${c === "Black Friday" ? "★ Black Friday" : c}</button>`).join("");
tabsEl.addEventListener("click", e => { if (e.target.dataset.cat) render(e.target.dataset.cat); });
render("Todos");

/* Reseñas: "Leer más" en móvil cuando el texto está recortado */
document.querySelectorAll(".review").forEach(r => {
  const q = r.querySelector("blockquote"), btn = document.createElement("button");
  btn.className = "rv-more"; btn.type = "button"; btn.textContent = "Leer más";
  q.after(btn);
  const check = () => btn.classList.toggle("show", r.classList.contains("open") || q.scrollHeight > q.clientHeight + 2);
  btn.addEventListener("click", () => { r.classList.toggle("open"); btn.textContent = r.classList.contains("open") ? "Leer menos" : "Leer más"; check(); });
  check(); window.addEventListener("resize", check);
});

/* Navegación del blog: muestra el artículo o la página principal según el enlace */
const home = document.getElementById("home"), baseTitle = document.title;
function route(){
  const h = decodeURIComponent(location.hash.slice(1));
  const art = h.startsWith("articulo-") ? document.getElementById(h) : null;
  document.querySelectorAll(".article-view").forEach(a => a.hidden = a !== art);
  home.hidden = !!art;
  document.title = art ? art.dataset.title : baseTitle;
  const el = !art && h && document.getElementById(h);
  const go = () => art ? window.scrollTo({ top: 0, behavior: "instant" }) : el && el.scrollIntoView({ behavior: "instant" });
  requestAnimationFrame(() => requestAnimationFrame(go)); setTimeout(go, 60);
}
window.addEventListener("hashchange", route);
route();

/* Menú en móvil */
const menuBtn = document.getElementById("menu-btn"), menu = document.getElementById("menu");
menuBtn.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
  menuBtn.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
});
menu.addEventListener("click", e => { if (e.target.closest("a")) { menu.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.setAttribute("aria-label", "Abrir menú"); } });

/* Mapa: solo se carga (y solo conecta con Google) cuando la visitante lo pide */
document.getElementById("map-load").addEventListener("click", () => {
  const box = document.getElementById("map-box");
  box.innerHTML = '<iframe title="Mapa de Lashes & Beauty Badalona" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Lashes+%26+Beauty+Badalona,+Via+Augusta+5,+08911+Badalona&output=embed"></iframe>';
});

/* Vídeo: botón de pausa y respeto a «reducir movimiento» */
const vid = document.getElementById("centro-video"), vbtn = document.getElementById("video-btn");
const setV = playing => { vbtn.textContent = playing ? "❚❚ Pausar vídeo" : "▶ Reproducir vídeo"; vbtn.setAttribute("aria-pressed", String(!playing)); };
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { vid.removeAttribute("autoplay"); vid.pause(); }
setV(!vid.paused && vid.autoplay);
vid.addEventListener("play", () => setV(true)); vid.addEventListener("pause", () => setV(false));
vbtn.addEventListener("click", () => vid.paused ? vid.play() : vid.pause());


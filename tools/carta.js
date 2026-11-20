// Copia la carta de servicios (filtros + tarjetas) dentro de index.html,
// para que esté en el HTML aunque el navegador no ejecute JavaScript.
// Los datos siguen en assets/app.js (única fuente): ejecuta esto cada vez que cambien.
//   node tools/carta.js
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const FILE = path.join(ROOT, "index.html");

// Sustituye lo que hay entre <!--NOMBRE--> y <!--/NOMBRE-->. Exige que cada marca
// aparezca exactamente una vez, para no duplicar nunca la carta.
const between = (html, name, inner) => {
  const open = `<!--${name}-->`, close = `<!--/${name}-->`;
  const count = s => html.split(s).length - 1;
  if (count(open) !== 1 || count(close) !== 1) throw new Error(`Marcas ${name} incorrectas (${count(open)} de apertura, ${count(close)} de cierre)`);
  const i = html.indexOf(open) + open.length, j = html.indexOf(close);
  return html.slice(0, i) + inner + html.slice(j);
};

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const errors = [];
  p.on("pageerror", e => errors.push(e.message));
  await p.goto("file://" + FILE);
  await p.waitForSelector("#services .svc");
  const tabs = await p.$eval("#tabs", e => e.innerHTML);
  const services = await p.$eval("#services", e => e.innerHTML);
  const n = await p.$$eval("#services .svc", s => s.length);
  await b.close();
  if (errors.length) throw new Error(errors.join("\n"));
  let html = fs.readFileSync(FILE, "utf8");
  html = between(html, "CARTA-FILTROS", tabs);
  html = between(html, "CARTA-SERVICIOS", services);
  fs.writeFileSync(FILE, html);
  const b2 = await chromium.launch(), p2 = await b2.newPage();
  await p2.goto("file://" + FILE);
  const fuera = await p2.$$eval(".svc", s => s.filter(x => !x.closest("#services")).length);
  await b2.close();
  if (fuera) throw new Error(`Hay ${fuera} tarjetas fuera de la carta: revisa index.html`);
  console.log(`Carta copiada en index.html: ${n} servicios.`);
})();

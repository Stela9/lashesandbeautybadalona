// Copia la carta de servicios (filtros + tarjetas) dentro de index.html,
// para que esté en el HTML aunque el navegador no ejecute JavaScript.
// Los datos siguen en assets/app.js (única fuente): ejecuta esto cada vez que cambien.
//   node tools/carta.js
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const FILE = path.join(ROOT, "index.html");

const between = (html, name, inner) => {
  const re = new RegExp(`<!--${name}-->[\\s\\S]*?(<!--/${name}-->|(?=</div>))`);
  if (!re.test(html)) throw new Error("No encuentro la marca " + name);
  return html.replace(re, `<!--${name}-->${inner}<!--/${name}-->`);
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
  console.log(`Carta copiada en index.html: ${n} servicios.`);
})();

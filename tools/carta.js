// Copia la carta de servicios (filtros + tarjetas) dentro de index.html y ca/index.html,
// para que esté en el HTML aunque el navegador no ejecute JavaScript.
// Los datos siguen en assets/app.js (única fuente; el catalán sale de assets/i18n-ca.js):
// ejecuta esto cada vez que cambien.
//   node tools/carta.js
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), http = require("http");
const ROOT = path.join(__dirname, "..");
const FILES = ["index.html", "ca/index.html"].filter(f => fs.existsSync(path.join(ROOT, f)));

// Sustituye lo que hay entre <!--NOMBRE--> y <!--/NOMBRE-->. Exige que cada marca
// aparezca exactamente una vez, para no duplicar nunca la carta.
const between = (html, name, inner) => {
  const open = `<!--${name}-->`, close = `<!--/${name}-->`;
  const count = s => html.split(s).length - 1;
  if (count(open) !== 1 || count(close) !== 1) throw new Error(`Marcas ${name} incorrectas (${count(open)} de apertura, ${count(close)} de cierre)`);
  const i = html.indexOf(open) + open.length, j = html.indexOf(close);
  return html.slice(0, i) + inner + html.slice(j);
};

// Servidor local mínimo: las páginas usan rutas como /assets/app.js
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".jpg": "image/jpeg", ".woff2": "font/woff2", ".mp4": "video/mp4" };
const server = http.createServer((q, r) => {
  let f = path.join(ROOT, decodeURIComponent(q.url.split("?")[0]));
  if (f.endsWith(path.sep)) f = path.join(f, "index.html");
  if (!fs.existsSync(f) || !fs.statSync(f).isFile()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
  r.end(fs.readFileSync(f));
});

(async () => {
  await new Promise(ok => server.listen(0, ok));
  const base = `http://localhost:${server.address().port}/`;
  const b = await chromium.launch();
  try {
    for (const file of FILES) {
      const url = base + file.replace(/index\.html$/, "");
      const p = await b.newPage(), errors = [];
      p.on("pageerror", e => errors.push(e.message));
      await p.goto(url);
      await p.waitForSelector("#services .svc");
      const tabs = await p.$eval("#tabs", e => e.innerHTML);
      const services = await p.$eval("#services", e => e.innerHTML);
      const n = await p.$$eval("#services .svc", s => s.length);
      await p.close();
      if (errors.length) throw new Error(file + ": " + errors.join("\n"));
      let html = fs.readFileSync(path.join(ROOT, file), "utf8");
      html = between(html, "CARTA-FILTROS", tabs);
      html = between(html, "CARTA-SERVICIOS", services);
      fs.writeFileSync(path.join(ROOT, file), html);
      // comprobación: ninguna tarjeta fuera de la carta y, en catalán, nada sin traducir
      const p2 = await b.newPage();
      await p2.goto(url);
      const fuera = await p2.$$eval(".svc", s => s.filter(x => !x.closest("#services")).length);
      const sinTraducir = file.startsWith("ca/") ? await p2.$$eval("#tabs, #services", els => {
        const txt = els.map(e => e.innerText).join("\n");
        return txt.split("\n").filter(l => /[ñ¿¡]|\b(con|para|sesiones|cejas|pestañas|tratamiento)\b/i.test(l));
      }) : [];
      await p2.close();
      if (fuera) throw new Error(`${file}: hay ${fuera} tarjetas fuera de la carta`);
      if (sinTraducir.length) throw new Error(`${file}: textos sin traducir en assets/i18n-ca.js:\n  ` + sinTraducir.join("\n  "));
      console.log(`Carta copiada en ${file}: ${n} servicios.`);
    }
  } finally { await b.close(); server.close(); }
})().catch(e => { console.error(e.message); process.exit(1); });

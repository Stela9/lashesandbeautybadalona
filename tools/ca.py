#!/usr/bin/env python3
"""Genera la versión en catalán de la web (carpeta /ca) a partir de las páginas en castellano.

Uso:   python3 tools/ca.py && node tools/carta.js

- Las páginas en castellano son la fuente: si cambias un texto en castellano, cambia aquí
  también su traducción (si no, el script se detiene y dice qué texto no encuentra).
- La carta de servicios se traduce con assets/i18n-ca.js y la escribe tools/carta.js.
- También añade a TODAS las páginas el enlace de idioma y las etiquetas hreflang.
"""
import json, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://lashesandbeautybadalona.es"
BOOK = "https://widget.treatwell.es/establecimiento/lashes-beauty-badalona/"
IG = '<li><a href="https://www.instagram.com/lashesandbeautybadalona/" target="_blank" rel="noopener">Instagram</a></li>'

enc = lambda s: urllib.parse.quote(s, safe="!'()*-._~")          # igual que encodeURIComponent
WA_ES = "https://wa.me/34659344275?text=" + enc("Hola! Me gustaría pedir información sobre vuestros servicios 😊")
WA_CA = "https://wa.me/34659344275?text=" + enc("Hola! M'agradaria demanar informació sobre els vostres serveis 😊")
GIFT_ES = "https://wa.me/34659344275?text=" + enc("Hola! Me gustaría comprar una tarjeta regalo 🎁")
GIFT_CA = "https://wa.me/34659344275?text=" + enc("Hola! M'agradaria comprar una targeta regal 🎁")

# Página en castellano -> (archivo, ruta pública castellano, archivo catalán, ruta pública catalán)
PAGES = {
    "home":        ("index.html", "/", "ca/index.html", "/ca/"),
    "blog":        ("blog/index.html", "/blog/", "ca/blog/index.html", "/ca/blog/"),
    "hilo":        ("blog/depilacion-facial-con-hilo.html", "/blog/depilacion-facial-con-hilo", "ca/blog/depilacio-facial-amb-fil.html", "/ca/blog/depilacio-facial-amb-fil"),
    "microblading":("blog/microblading-proceso-cicatrizacion.html", "/blog/microblading-proceso-cicatrizacion", "ca/blog/microblading-proces-cicatritzacio.html", "/ca/blog/microblading-proces-cicatritzacio"),
    "extensiones": ("blog/extensiones-de-pestanas-no-debilitan.html", "/blog/extensiones-de-pestanas-no-debilitan", "ca/blog/extensions-de-pestanyes-no-debiliten.html", "/ca/blog/extensions-de-pestanyes-no-debiliten"),
    "condiciones": ("condiciones.html", "/condiciones", "ca/condicions.html", "/ca/condicions"),
    "aviso":       ("aviso-legal.html", "/aviso-legal", "ca/avis-legal.html", "/ca/avis-legal"),
    "privacidad":  ("privacidad.html", "/privacidad", "ca/privacitat.html", "/ca/privacitat"),
    "cookies":     ("cookies.html", "/cookies", "ca/cookies.html", "/ca/cookies"),
}
ES2CA = {v[1]: v[3] for v in PAGES.values()}

def rd(f): return open(os.path.join(ROOT, f), encoding="utf-8").read()
def wr(f, t):
    p = os.path.join(ROOT, f); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(t)

def rep(t, a, b, n=1, where=""):
    c = t.count(a)
    if (n is None and c == 0) or (n is not None and c != n):
        sys.exit(f"[{where}] No encuentro (o no {n} veces, sino {c}) el texto:\n  {a[:160]}")
    return t.replace(a, b)

def apply(t, pairs, where):
    for p in pairs:
        a, b = p[0], p[1]; n = p[2] if len(p) > 2 else 1
        t = rep(t, a, b, n, where)
    return t

def set_attr(t, pattern, value, where):
    t2, n = re.subn(pattern, value, t, count=1)
    if n != 1: sys.exit(f"[{where}] patrón no encontrado: {pattern}")
    return t2

# ------------------------------------------------------------------ hreflang y selector
def alternates(t, es, ca):
    t = re.sub(r'\n<link rel="alternate" hreflang="[^"]+" href="[^"]*">', "", t)
    links = (f'\n<link rel="alternate" hreflang="es" href="{SITE}{es}">'
             f'\n<link rel="alternate" hreflang="ca" href="{SITE}{ca}">'
             f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{es}">')
    m = re.search(r'<link rel="canonical" href="[^"]*">', t)
    return t[:m.end()] + links + t[m.end():]

def switcher(t, href, lang, label, where):
    t = re.sub(r'\n      <li><a class="lang-switch"[^\n]*</li>', "", t)
    return rep(t, IG, IG + f'\n      <li><a class="lang-switch" href="{href}" hreflang="{lang}" lang="{lang}">{label}</a></li>', 1, where)

# ------------------------------------------------------------------ cabecera, menú y pie
def common_ca(t, where, home=False):
    p = "" if home else "/ca/"
    t = apply(t, [
        ('<html lang="es">', '<html lang="ca">'),
        ('<meta property="og:locale" content="es_ES">', '<meta property="og:locale" content="ca_ES">\n<meta property="og:locale:alternate" content="es_ES">'),
        ('>Saltar al contenido<', '>Salta al contingut<'),
        ('aria-label="Abrir menú"', 'aria-label="Obre el menú"'),
        ('href="/" class="logo"', 'href="/ca/" class="logo"'),
        ('>Servicios</a></li>', '>Serveis</a></li>'),
        ('>Reseñas</a></li>', '>Ressenyes</a></li>'),
        ('>Tarjetas regalo</a></li>', '>Targetes regal</a></li>'),
        ('>Dónde estamos</a></li>', '>On som</a></li>'),
        ('rel="noopener">Reservar</a>', 'rel="noopener">Reserva</a>'),
        ('>Reservas y cancelaciones</a>', '>Reserves i cancel·lacions</a>'),
        ('>Aviso legal</a>', '>Avís legal</a>'),
        ('>Privacidad</a>', '>Privacitat</a>'),
        ('aria-label="Contacto por WhatsApp"', 'aria-label="Contacte per WhatsApp"'),
        ('aria-label="Escríbenos por WhatsApp"', 'aria-label="Escriu-nos per WhatsApp"'),
    ], where)
    if not home:
        t = t.replace('href="/#', 'href="/ca/#').replace('<a href="/blog/">Blog</a>', '<a href="/ca/blog/">Blog</a>')
    t = t.replace(WA_ES, WA_CA)
    for es, ca in (("condiciones", "condicions"), ("aviso-legal", "avis-legal"), ("privacidad", "privacitat"), ("cookies", "cookies")):
        t = re.sub(rf'href="/?{es}"', f'href="/ca/{ca}"', t)
    return t

def head_ca(t, where, title, desc, url, keywords=None):
    t = set_attr(t, r"<title>[^<]*</title>", f"<title>{title}</title>", where)
    t = set_attr(t, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', where)
    t = set_attr(t, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', where)
    t = set_attr(t, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', where)
    t = set_attr(t, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{SITE}{url}">', where)
    t = set_attr(t, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{SITE}{url}">', where)
    if keywords: t = set_attr(t, r'<meta name="keywords" content="[^"]*">', f'<meta name="keywords" content="{keywords}">', where)
    return t

def replace_main(t, inner, where):
    i = t.index('<main id="main">') + len('<main id="main">'); j = t.index("</main>")
    return t[:i] + "\n" + inner.strip("\n") + "\n" + t[j:]

# ------------------------------------------------------------------ BLOG (contenido catalán)
ART = {
 "hilo": dict(
  title="Per què la depilació facial amb fil és la millor opció per a la teva pell",
  kicker="Depilació · 4 min de lectura",
  excerpt="Precisa, higiènica i respectuosa fins i tot amb les pells més sensibles. T'expliquem per què el fil és la nostra tècnica preferida per a celles i rostre.",
  desc="Avantatges de la depilació facial amb fil davant la cera: precisió, respecte per les pells sensibles i higiene. Preus a Lashes &amp; Beauty Badalona.",
  body='''
<p class="lead">La depilació amb fil és una tècnica mil·lenària d'origen oriental que s'ha convertit en la preferida de qui busca unes celles perfectes i un rostre sense pèl sense castigar la pell. Amb un simple fil de cotó cargolat s'atrapen els pèls un a un, o en petites files, i s'extreuen des de l'arrel.</p>

<h2>1. És la tècnica més respectuosa amb la pell</h2>
<p>La cera, sobretot la calenta, no només arrenca el pèl: també s'enganxa a la capa més superficial de la pell i l'estira. En una zona tan fina i delicada com el rostre, això pot provocar envermelliments, irritació i fins i tot petites lesions.</p>
<p>El fil, en canvi, <strong>només toca el pèl</strong>. No hi ha calor, no hi ha productes químics i no s'arrossega la pell. Per això és l'opció recomanada si:</p>
<ul>
  <li>Tens la pell sensible, reactiva o amb tendència a envermellir-se.</li>
  <li>Utilitzes cremes amb retinol, àcids exfoliants o tractaments dermatològics que aprimen la pell (en aquests casos la cera pot causar cremades o ferides).</li>
  <li>Tens acne o rosàcia a la zona.</li>
</ul>

<h2>2. Precisió mil·limètrica per a unes celles perfectes</h2>
<p>Com que treballa gairebé pèl a pèl, el fil permet un control que ni la cera ni les pinces igualen. Podem definir línies netes, respectar la forma natural de la teva cella i corregir només el necessari. Per això, en el nostre servei de <strong>disseny + depilació de celles</strong> primer prenem mides segons les teves faccions i després donem forma amb fil.</p>

<h2>3. Elimina fins i tot el pèl més fi</h2>
<p>El fil també atrapa el borrissol més curt i fi del llavi superior, el mentó o les patilles, que sovint s'escapa amb la cera. El resultat és una pell més uniforme, on a més el maquillatge llueix millor.</p>

<h2>4. Resultats duradors</h2>
<p>Com que el pèl s'extreu des de l'arrel, el resultat dura de <strong>3 a 5 setmanes</strong>, segons el teu ritme de creixement. Amb sessions regulars, moltes clientes noten que el pèl torna a créixer més fi i menys dens.</p>

<h2>5. Ràpida i higiènica</h2>
<p>Una depilació de celles amb fil dura uns 15 minuts, i el rostre complet, poca cosa més. S'utilitza <strong>un fil nou per a cada clienta</strong> i no es reutilitza cap producte, cosa que la converteix en una de les tècniques més higièniques que hi ha.</p>

<h2>Fa mal?</h2>
<p>Es nota una petita pessigada, semblant a la de les pinces però molt més ràpida. La majoria de persones la toleren molt bé i la sensació disminueix amb les sessions. Els possibles envermelliments desapareixen en pocs minuts.</p>

<h2>Consells abans i després</h2>
<ul>
  <li>Deixa créixer el pèl almenys 2 setmanes perquè el fil el pugui atrapar bé.</li>
  <li>Evita exfoliants i àcids el dia abans i el dia després.</li>
  <li>Durant les primeres hores, no et maquillis la zona ni prenguis el sol directament.</li>
</ul>

<div class="prices">
  <h3>Depilació amb fil a Lashes &amp; Beauty Badalona</h3>
  <ul>
    <li><span>Celles</span><b>11 €</b></li>
    <li><span>Disseny + depilació de celles</span><b>16 €</b></li>
    <li><span>Llavi superior</span><b>6 €</b></li>
    <li><span>Mentó</span><b>6 €</b></li>
    <li><span>Patilles</span><b>11 €</b></li>
    <li><span>Depilació facial completa</span><b>32 €</b></li>
  </ul>
</div>'''),
 "microblading": dict(
  title="Microblading: en què consisteix i com és el procés de cicatrització dia a dia",
  kicker="Celles · 6 min de lectura",
  excerpt="Què pots esperar de la sessió, com evoluciona la cella dia a dia i les cures perquè el resultat sigui perfecte i durador.",
  desc="Què és el microblading, com és la sessió, la cicatrització dia a dia, les cures i el retoc. Lashes &amp; Beauty Badalona.",
  body='''
<p class="lead">El microblading és una tècnica de micropigmentació semipermanent que dibuixa <strong>traços fins que imiten el pèl natural</strong> de la cella. És ideal si tens les celles poc poblades, amb buits o asimetries, o simplement vols llevar-te amb unes celles definides sense haver de maquillar-les.</p>

<h2>Com es fa?</h2>
<p>A diferència de la micropigmentació amb màquina, el microblading es fa amb un <strong>instrument manual</strong> amb microagulles molt fines que diposita el pigment a les capes superficials de la pell, traç a traç. Així s'aconsegueix un efecte pèl a pèl molt natural.</p>

<h2>Així és la sessió, pas a pas</h2>
<ol>
  <li><strong>Valoració i disseny.</strong> Analitzem el teu rostre, prenem mides i dibuixem la forma ideal de les teves celles. No comencem fins que el disseny t'encanta.</li>
  <li><strong>Elecció del color.</strong> Seleccionem el pigment segons el to de la teva pell, el color dels cabells i les teves celles naturals.</li>
  <li><strong>Anestèsia tòpica.</strong> Apliquem una crema anestèsica perquè la sessió sigui tan còmoda com sigui possible.</li>
  <li><strong>Traçat.</strong> Dibuixem cada pèl seguint la direcció natural de creixement.</li>
  <li><strong>Revisió final.</strong> Comprovem la simetria i t'expliquem les cures.</li>
</ol>
<p>La sessió completa dura al voltant d'<strong>1 h 30 min</strong>.</p>

<h2>El procés de cicatrització, dia a dia</h2>
<p>És molt important saber que <strong>el resultat del primer dia no és el definitiu</strong>. La cella passa per diverses fases abans de mostrar el seu color real:</p>

<div class="timeline">
  <div><b>Dies 1–3</b><p>El color es veu més fosc i intens del que serà al final, i els traços, més marcats. Hi pot haver un lleuger envermelliment o inflamació. És del tot normal.</p></div>
  <div><b>Dies 4–10</b><p>Comença la descamació: es formen petites crostes fines i pot picar. <strong>No et gratis ni arrenquis les pells</strong>: s'emportarien el pigment.</p></div>
  <div><b>Dies 10–21</b><p>Quan cauen les crostes, la cella es pot veure molt clara o pot semblar que alguns traços han desaparegut. És la fase "fantasma": el pigment continua allà, cobert per pell nova.</p></div>
  <div><b>Setmanes 3–4</b><p>La pell es regenera i el color torna a aparèixer, ja amb el to definitiu, més suau i natural.</p></div>
  <div><b>Setmanes 4–6: retoc</b><p>Revisem el resultat, omplim els traços que hagin retingut menys pigment i ajustem detalls. <strong>Els nostres preus inclouen aquest retoc a les 4 setmanes.</strong></p></div>
</div>

<h2>Cures després del microblading</h2>
<ul>
  <li>No mullis les celles durant els primers 7–10 dies; renta't la cara evitant la zona.</li>
  <li>Aplica la crema regeneradora que t'indiquem, en una capa molt fina.</li>
  <li>No et maquillis les celles fins que hagi acabat la descamació.</li>
  <li>Evita el sol directe, els raigs UVA, la sauna, la piscina, la platja i l'exercici intens amb molta suor durant 2 setmanes.</li>
  <li>No utilitzis retinol, àcids ni exfoliants a prop de les celles.</li>
  <li>No et gratis ni arrenquis les crostes.</li>
</ul>

<h2>Quant dura?</h2>
<p>El microblading dura aproximadament entre <strong>12 i 18 mesos</strong>, segons el tipus de pell (les pells greixoses el retenen menys), l'exposició al sol i la rutina de cura. Per mantenir-lo perfecte, recomanem un retoc anual.</p>

<h2>M'ho puc fer?</h2>
<p>Consulta'ns abans si estàs embarassada o en període de lactància, prens anticoagulants, tens diabetis, problemes de cicatrització (queloides) o alguna afecció activa a la pell de la zona. En la valoració prèvia resoldrem tots els teus dubtes.</p>

<div class="prices">
  <h3>Celles semipermanents a Lashes &amp; Beauty Badalona <span>-20% dte.</span></h3>
  <ul>
    <li><span>Microblading (efecte pèl a pèl)</span><b>200 € <s>250 €</s></b></li>
    <li><span>Micropigmentació (ombrejat)</span><b>200 € <s>250 €</s></b></li>
    <li><span>Hybrid brows (tècnica mixta)</span><b>224 € <s>280 €</s></b></li>
    <li><span>Retoc anual</span><b>110 €</b></li>
  </ul>
  <p class="small">Els preus inclouen un retoc a les 4 setmanes.</p>
</div>'''),
 "extensiones": dict(
  title="Les extensions de pestanyes debiliten les teves pestanyes? La veritat quan les aplica una professional",
  kicker="Pestanyes · 5 min de lectura",
  excerpt="És un dels mites més estesos. T'expliquem què danya realment les pestanyes i per què una bona aplicació les manté sanes.",
  desc="Per què unes extensions de pestanyes ben aplicades per professionals no debiliten les teves pestanyes, i com cuidar-les. Lashes &amp; Beauty Badalona.",
  body='''
<p class="lead">"M'han dit que les extensions espatllen les pestanyes." És probablement el dubte que més sentim al centre. La resposta curta: <strong>unes extensions ben aplicades per una professional no debiliten les teves pestanyes ni fan que perdis densitat</strong>. El que les danya és una mala aplicació o una mala retirada. T'expliquem per què.</p>

<h2>Primer: les pestanyes cauen soles (i és normal)</h2>
<p>Cada pestanya té el seu propi cicle de vida: creix, reposa i cau de manera natural per deixar pas a una de nova. És normal perdre <strong>entre 1 i 5 pestanyes al dia</strong>. Quan portes extensions, cada extensió està enganxada a una pestanya natural, així que cau amb ella quan li arriba el moment. Veure alguna extensió al coixí no vol dir que estiguin caient més pestanyes del compte: és el cicle natural.</p>

<h2>Què danya de debò les pestanyes</h2>
<p>Quan algú ha tingut una mala experiència, gairebé sempre es deu a algun d'aquests errors:</p>
<ul>
  <li><strong>Extensions massa pesants o llargues</strong> per a la pestanya natural. Si la pestanya no pot suportar el pes, s'afebleix i pot caure abans d'hora.</li>
  <li><strong>Pestanyes enganxades entre elles.</strong> Si una extensió uneix dues o més pestanyes naturals, quan una intenta créixer o caure, estira les altres. Això sí que provoca trencaments i pèrdua.</li>
  <li><strong>Adhesiu sobre la parpella o a l'arrel.</strong> Pot irritar el fol·licle.</li>
  <li><strong>Treure-les a casa</strong> estirant-les o amb productes inadequats, cosa que arrenca la pestanya natural.</li>
</ul>

<h2>Com treballem per protegir les teves pestanyes</h2>
<ul>
  <li><strong>Valorem les teves pestanyes naturals</strong> abans de començar: gruix, longitud i força. El disseny s'adapta al que les teves pestanyes poden suportar, i no al revés.</li>
  <li><strong>Aïllem cada pestanya</strong> i apliquem l'extensió de manera individual, sense enganxar pestanyes entre elles.</li>
  <li><strong>Triem el pes i el gruix adequats.</strong> Les tècniques de volum (3D, 5D, Wispy…) utilitzen ventalls de fibres ultrafines i lleugeres, de manera que el pes total continua sent segur.</li>
  <li><strong>Deixem una petita separació de la parpella</strong>, perquè l'adhesiu no toqui mai la pell ni el fol·licle.</li>
  <li>Utilitzem <strong>adhesius professionals</strong> específics per a pestanyes.</li>
  <li><strong>Retirada professional</strong> amb un producte que dissol l'adhesiu, sense estirades.</li>
</ul>

<h2>Les cures a casa també compten</h2>
<ul>
  <li>Les primeres 24 hores, evita mullar-les, el vapor i la sauna perquè l'adhesiu s'assequi bé.</li>
  <li>Neteja-les cada dia amb una escuma específica, com la nostra <strong>mousse netejadora</strong>, i pentina-les amb un raspallet.</li>
  <li>Evita desmaquillants i cremes amb oli a la zona dels ulls.</li>
  <li>No les freguis ni les arrenquis i, si pots, evita dormir de bocaterrosa.</li>
  <li>Fes el <strong>retoc la 3a setmana</strong>: així retirem les extensions que han crescut massa i mantenim el pes equilibrat.</li>
  <li>Si vols un extra de força, un <strong>sèrum de pestanyes</strong> ajuda a nodrir-les i enfortir-les.</li>
</ul>

<h2>I si vull descansar de les extensions?</h2>
<p>Ho pots fer quan vulguis, però no és imprescindible si estan ben aplicades i les mantens amb retocs. Si decideixes treure-te-les, vine al centre: la <strong>retirada professional</strong> és ràpida i no danya la pestanya natural. I si mentrestant prefereixes un look natural, el <strong>lifting de pestanyes coreà</strong> és una gran alternativa.</p>

<div class="prices">
  <h3>Extensions a Lashes &amp; Beauty Badalona</h3>
  <ul>
    <li><span>Efecte rímel</span><b>59 € · retoc 39 €</b></li>
    <li><span>Híbrides</span><b>65 € · retoc 45 €</b></li>
    <li><span>Volum rus elegant 3D</span><b>69 € · retoc 50 €</b></li>
    <li><span>Volum rus glam 5D</span><b>75 € · retoc 55 €</b></li>
    <li><span>Wispy / efecte mullat</span><b>79 € · retoc 59 €</b></li>
    <li><span>Retirada d'extensions del centre</span><b>15 €</b></li>
  </ul>
</div>'''),
}
ORDER = ["hilo", "microblading", "extensiones"]

def card(key, h="h3", ind="        "):
    a = ART[key]
    return (f'{ind}<a class="post-card" href="{PAGES[key][3]}">\n'
            f'{ind}  <span class="kicker">{a["kicker"]}</span>\n'
            f'{ind}  <{h}>{a["title"]}</{h}>\n'
            f'{ind}  <p>{a["excerpt"]}</p>\n'
            f'{ind}  <span class="more">Llegeix l\'article →</span>\n'
            f'{ind}</a>')

CTA = f'''    <div class="cta">
      <h2>Tens dubtes o vols reservar?</h2>
      <p>Escriu-nos i t'assessorem sense compromís, o reserva directament la teva cita en línia.</p>
      <div class="ctas">
        <a class="btn btn-gold" href="{BOOK}" target="_blank" rel="noopener">Reserva cita</a>
        <a class="btn btn-outline" href="{WA_CA}" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>'''

# ------------------------------------------------------------------ LEGAL (contenido catalán)
DATA = '''<div class="data">
      <p><strong>Titular:</strong> Estela Comella Díaz</p>
      <p><strong>NIF:</strong> 52401889T</p>
      <p><strong>Nom comercial:</strong> Lashes &amp; Beauty Badalona</p>
      <p><strong>Domicili:</strong> Via Augusta, 5 · 08911 Badalona (Barcelona)</p>{email}
      <p><strong>Telèfon / WhatsApp:</strong> <a href="tel:+34659344275">659 344 275</a></p>
    </div>'''
PREVAL = '    <p class="updated">En cas de discrepància entre la versió catalana i la castellana d\'aquest text, preval la versió en castellà. Darrera actualització: 20 de novembre de 2026.</p>'

LEGAL = {
 "condiciones": dict(eyebrow="Condicions", h1="Reserves, canvis i devolucions", noindex=False,
  desc="Com reservar cita, paga i senyal, canvis, cancel·lacions i devolucions a Lashes &amp; Beauty Badalona.",
  body=f'''
    <p>A Lashes &amp; Beauty Badalona ens comprometem a oferir-te la millor experiència i qualitat en tots els nostres serveis. Aquestes són les nostres condicions de reserva, canvis i devolucions, d'acord amb la legislació espanyola en matèria de consum.</p>

    <h2>1. Com reservar la teva cita</h2>
    <p><strong>Reserva en línia a Treatwell:</strong> pots reservar directament a la nostra <a href="{BOOK}" target="_blank" rel="noopener">agenda en línia</a>. En aquest cas s'apliquen, a més, les condicions de Treatwell.</p>
    <p><strong>Reserva per WhatsApp, telèfon o al centre:</strong> per política d'empresa i a causa de cancel·lacions no anticipades, per confirmar la teva cita has d'abonar una <strong>paga i senyal</strong>. Ho pots fer:</p>
    <ul>
      <li>Per <strong>Bizum</strong> o <strong>transferència bancària</strong>: t'enviarem les dades de pagament per WhatsApp quan reservis.</li>
      <li><strong>Al nostre saló</strong>, en efectiu o amb targeta.</li>
    </ul>
    <p>Indica el teu <strong>nom complet</strong> al concepte del pagament i envia'ns el justificant per <a href="https://wa.me/34659344275" target="_blank" rel="noopener">WhatsApp</a> al <a href="tel:+34659344275">659 344 275</a> per confirmar la teva cita. <strong>La paga i senyal es descompta del preu final</strong> del tractament.</p>

    <h2>2. Import de la paga i senyal</h2>
    <table class="deposit">
      <thead><tr><th scope="col">Tractament</th><th scope="col">Senyal</th></tr></thead>
      <tbody>
        <tr><th scope="row">Extensions pèl a pèl i híbrides</th><td>10 €</td></tr>
        <tr><th scope="row">Extensions de volum</th><td>20 €</td></tr>
        <tr><th scope="row">Lifting i laminat</th><td>10 €</td></tr>
        <tr><th scope="row">Neteja facial</th><td>10 €</td></tr>
        <tr><th scope="row">Dermapen</th><td>20 €</td></tr>
        <tr><th scope="row">Bo facial</th><td>50 €</td></tr>
        <tr><th scope="row">Microblading i micropigmentació</th><td>45 €</td></tr>
        <tr><th scope="row">Retocs de microblading i micropigmentació</th><td>20 €</td></tr>
        <tr><th scope="row">Bons I-MODEL</th><td>100 %</td></tr>
      </tbody>
    </table>

    <h2>3. Canvis i cancel·lacions de cita</h2>
    <p>Pots anul·lar o canviar la teva reserva i rebre el reemborsament de l'import, sempre que ens ho comuniquis <strong>almenys 24 hores abans</strong> de la teva cita. Per fer-ho, truca'ns o escriu-nos per <a href="https://wa.me/34659344275" target="_blank" rel="noopener">WhatsApp</a> al <a href="tel:+34659344275">659 344 275</a>.</p>
    <p>Passat aquest termini, la teva cita es donarà per feta i l'import abonat no es podrà reemborsar.</p>

    <h2>4. Serveis estètics</h2>
    <p><strong>No hi ha devolució per serveis prestats:</strong> d'acord amb la Llei general per a la defensa dels consumidors i usuaris (Reial decret legislatiu 1/2007), un cop prestat el servei (tractaments estètics, depilacions, etc.), no se'n podrà sol·licitar la devolució, excepte en els casos que estableix la llei.</p>

    <h2>5. Microblading i micropigmentació</h2>
    <p><strong>Primer retoc inclòs:</strong> tots els tractaments de microblading i micropigmentació inclouen un primer retoc gratuït dins de les 4 setmanes posteriors a la realització del tractament. Aquest retoc és indispensable per garantir els millors resultats.</p>
    <p><strong>Venciment del retoc:</strong> si no s'acudeix a la cita del retoc dins del termini de 4 setmanes, es perdrà el dret a aquest retoc gratuït. En aquest cas es podrà programar un nou retoc abonant la tarifa corresponent.</p>

    <h2>6. Bons i targetes regal</h2>
    <p><strong>Validesa:</strong> els bons són vàlids durant 1 any des de la compra, i les targetes regal, durant 3 mesos des de la data de compra.</p>
    <p><strong>No transferibilitat:</strong> els bons adquirits a Lashes &amp; Beauty Badalona són personals i intransferibles: no es poden compartir ni transferir a altres persones.</p>
    <p><strong>No reemborsament:</strong> l'import dels bons no es reemborsarà, encara que no s'utilitzin en la seva totalitat, excepte en els casos previstos per la llei. En cas de no acudir a la cita o de cancel·lar-la sense l'antelació indicada, la sessió es donarà per feta.</p>

    <h2>7. Productes estètics</h2>
    <p>Si has adquirit productes cosmètics o de cura personal a les nostres instal·lacions, la normativa espanyola estableix el següent:</p>
    <ul>
      <li><strong>Dret de desistiment:</strong> tens dret a desistir de la compra de productes dins dels 14 dies naturals següents a la recepció del producte, sense necessitat de justificació, sempre que no es tracti de productes desprecintats o usats, tal com estableix la Llei general per a la defensa dels consumidors i usuaris.</li>
      <li><strong>Excepcions:</strong> el dret de desistiment no s'aplica als productes que, per raons d'higiene o salut, no es puguin tornar si s'han desprecintat o utilitzat, ni als productes personalitzats o fabricats segons les especificacions de la clienta.</li>
    </ul>

    <h2>8. Responsabilitat del centre</h2>
    <p>El nostre centre d'estètica es compromet a prestar els serveis i lliurar els productes d'acord amb les característiques descrites i amb la màxima qualitat. No obstant això, si consideres que el servei o el producte no compleixen el que s'havia promès, tens dret a reclamar segons la normativa vigent.</p>
'''),
 "aviso": dict(eyebrow="Informació legal", h1="Avís legal", noindex=True,
  desc="Avís legal del web de Lashes &amp; Beauty Badalona.",
  body='''
    <h2>Dades identificatives</h2>
    <p>En compliment de l'article 10 de la Llei 34/2002, de serveis de la societat de la informació i de comerç electrònic (LSSI-CE), t'informem de les dades de la titular d'aquest web:</p>
    ''' + DATA.format(email="\n      <p><strong>Correu electrònic:</strong> badalona.lashesandmore [arrova] gmail.com</p>") + '''
    <p>Activitat: centre d'estètica (tractaments de pestanyes, celles, micropigmentació, facials i corporals).</p>

    <h2>Objecte i condicions d'ús</h2>
    <p>Aquest web ofereix informació sobre els serveis, preus, horaris i ubicació de Lashes &amp; Beauty Badalona. L'accés és gratuït i no requereix registre. En navegar-hi, acceptes fer un ús adequat dels seus continguts, d'acord amb la llei i amb aquest avís.</p>

    <h2>Preus i promocions</h2>
    <p>Els preus que apareixen al web inclouen l'IVA i són orientatius: el preu definitiu és el que s'indica en reservar o al centre. Les promocions són vàlides en les dates indicades en cadascuna. Podem actualitzar preus i serveis en qualsevol moment.</p>

    <h2>Reserves</h2>
    <p>Les cites es reserven a través de la plataforma Treatwell, per WhatsApp, per telèfon o al mateix centre. Les reserves en línia es regeixen, a més, per les condicions de Treatwell. Les condicions de paga i senyal, canvis, cancel·lacions i devolucions són a <a href="/ca/condicions">Reserves, canvis i devolucions</a>.</p>

    <h2>Propietat intel·lectual</h2>
    <p>Els textos, fotografies, vídeo, logotip i disseny d'aquest web pertanyen a la seva titular o s'utilitzen amb permís. No es poden copiar, reproduir ni distribuir sense autorització. Les ressenyes que es mostren són opinions publicades per clientes a Google i es reprodueixen sense modificar-ne el text.</p>

    <h2>Enllaços a altres webs</h2>
    <p>El web conté enllaços a serveis de tercers (Treatwell, WhatsApp, Instagram i Google Maps). No som responsables dels seus continguts ni de les seves polítiques, que pots consultar en cadascun d'ells.</p>

    <h2>Responsabilitat</h2>
    <p>Procurem que la informació del web sigui correcta i estigui actualitzada, però no podem garantir l'absència d'errors puntuals. Els articles del blog són informatius i no substitueixen la valoració personalitzada al centre.</p>

    <h2>Legislació aplicable</h2>
    <p>Aquest avís legal es regeix per la legislació espanyola. Per a qualsevol controvèrsia seran competents els jutjats i tribunals que corresponguin segons la normativa vigent; si ets consumidora, els del teu domicili.</p>
'''),
 "privacidad": dict(eyebrow="Informació legal", h1="Política de privacitat", noindex=True,
  desc="Política de privacitat de Lashes &amp; Beauty Badalona: quines dades tractem i quins són els teus drets.",
  body='''
    <h2>Responsable del tractament</h2>
    ''' + DATA.format(email="") + '''

    <h2>Quines dades recull aquest web?</h2>
    <p>Aquest web <strong>no té formularis, no demana registre i no instal·la cookies</strong>. Només tractem les teves dades personals si decideixes contactar amb nosaltres o reservar una cita.</p>
    <p>Per saber quantes persones visiten el web i quines pàgines els interessen, utilitzem <strong>Cloudflare Web Analytics</strong>, una eina d'estadístiques que <strong>no utilitza cookies</strong>, no desa res al teu dispositiu i no t'identifica: només obtenim dades agregades i anònimes (pàgines vistes, país, tipus de navegador o dispositiu i el web des del qual arribes). La base legal és el nostre interès legítim a millorar el web.</p>

    <h2>Dades que tractem, per a què i per què</h2>
    <ul>
      <li><strong>Si ens escrius per WhatsApp o correu electrònic, o ens truques:</strong> el teu nom, telèfon o correu electrònic i el contingut del missatge, per respondre't i, si ho demanes, gestionar la teva cita. La base legal és el teu consentiment i l'aplicació de mesures precontractuals a petició teva.</li>
      <li><strong>Si reserves a través de Treatwell:</strong> Treatwell ens comunica les dades necessàries per gestionar la teva cita (nom, contacte, servei, data i hora). La base legal és la prestació del servei que contractes. A més, Treatwell tracta les teves dades segons la seva pròpia política de privacitat.</li>
      <li><strong>Com a clienta del centre:</strong> les dades necessàries per prestar-te el servei, facturar i complir les nostres obligacions legals i fiscals.</li>
    </ul>

    <h2>Quant de temps les conservem?</h2>
    <p>Mentre sigui necessari per atendre la teva consulta o mantenir la nostra relació com a clienta i, després, durant els terminis que exigeix la llei (per exemple, la normativa fiscal).</p>

    <h2>Amb qui es comparteixen?</h2>
    <p>No venem ni cedim les teves dades a tercers, excepte per obligació legal. Utilitzem proveïdors que poden tractar dades en nom nostre o de manera independent:</p>
    <ul>
      <li><strong>Cloudflare</strong> (allotjament i estadístiques de visites del web): registra dades tècniques de la connexió, com l'adreça IP, per motius de seguretat, i genera les estadístiques anònimes de visites descrites més amunt.</li>
      <li><strong>WhatsApp (Meta)</strong>, si tries aquest canal per escriure'ns.</li>
      <li><strong>Treatwell</strong>, si reserves a través de la seva plataforma.</li>
      <li><strong>Google Maps</strong>, només si prems «Mostra el mapa» o l'enllaç «Com arribar».</li>
    </ul>
    <p>Alguns d'aquests proveïdors poden tractar dades fora de l'Espai Econòmic Europeu, amb les garanties previstes al Reglament general de protecció de dades (RGPD).</p>

    <h2>Els teus drets</h2>
    <p>Pots exercir els teus drets d'accés, rectificació, supressió, oposició, limitació del tractament i portabilitat per WhatsApp o telèfon al <a href="tel:+34659344275">659 344 275</a>, o per escrit o en persona al nostre centre (Via Augusta, 5 · 08911 Badalona). També pots retirar el teu consentiment en qualsevol moment.</p>
    <p>Si consideres que no hem tractat bé les teves dades, pots presentar una reclamació davant l'Agència Espanyola de Protecció de Dades (<a href="https://www.aepd.es" target="_blank" rel="noopener">www.aepd.es</a>).</p>
'''),
 "cookies": dict(eyebrow="Informació legal", h1="Política de cookies", noindex=True,
  desc="Política de cookies del web de Lashes &amp; Beauty Badalona.",
  body='''
    <h2>Aquest web utilitza cookies?</h2>
    <p><strong>No.</strong> Aquest web no instal·la cookies pròpies ni de tercers, ni utilitza eines de publicitat. Per això no et mostrem cap avís de cookies.</p>

    <h2>Estadístiques de visites</h2>
    <p>Utilitzem <strong>Cloudflare Web Analytics</strong> per conèixer quantes visites rep el web. Aquesta eina <strong>no utilitza cookies</strong> ni desa informació al teu dispositiu, i no permet identificar-te: només ofereix dades agregades i anònimes. Més informació a la <a href="https://www.cloudflare.com/es-es/privacypolicy/" target="_blank" rel="noopener">política de privacitat de Cloudflare</a>.</p>

    <h2>Google Maps</h2>
    <p>El mapa de la secció «On som» <strong>no es carrega fins que prems «Mostra el mapa»</strong>. En prémer-lo, Google pot instal·lar les seves pròpies cookies i rebre dades com la teva adreça IP. Pots consultar com les utilitza a la <a href="https://policies.google.com/technologies/cookies?hl=ca" target="_blank" rel="noopener">política de cookies de Google</a>. Si prefereixes no carregar el mapa, pots fer servir l'adreça: Via Augusta, 5 · 08911 Badalona.</p>

    <h2>Enllaços a altres serveis</h2>
    <p>Quan surts d'aquest web a través d'un enllaç (Treatwell, WhatsApp, Instagram o Google Maps), aquests serveis apliquen les seves pròpies polítiques de cookies.</p>

    <h2>Canvis</h2>
    <p>Si en el futur afegim cookies que requereixin el teu consentiment, actualitzarem aquesta política i te'l demanarem abans d'instal·lar-les.</p>
'''),
}

# ------------------------------------------------------------------ PORTADA: pares castellano -> catalán
HOME = [
 ('<title>Lashes & Beauty Badalona | Extensiones de pestañas, microblading y estética</title>', '<title>Lashes & Beauty Badalona | Extensions de pestanyes, microblading i estètica</title>'),
 ('content="Centro de estética en Badalona (Via Augusta 5, metro Pompeu Fabra). Extensiones y lifting de pestañas, microblading, micropigmentación, laminado de cejas, faciales e I-MODEL. 4,8★ en Treatwell. Reserva online."',
  'content="Centre d\'estètica a Badalona (Via Augusta 5, metro Pompeu Fabra). Extensions i lifting de pestanyes, microblading, micropigmentació, laminat de celles, facials i I-MODEL. 4,8★ a Treatwell. Reserva en línia."'),
 ('content="extensiones de pestañas Badalona, lifting de pestañas Badalona, microblading Badalona, micropigmentación Badalona, laminado de cejas, centro de estética Badalona, dermapen, depilación con hilo"',
  'content="extensions de pestanyes Badalona, lifting de pestanyes Badalona, microblading Badalona, micropigmentació Badalona, laminat de celles, centre d\'estètica Badalona, dermapen, depilació amb fil"'),
 ('<meta property="og:title" content="Lashes & Beauty Badalona · Centro de estética">', '<meta property="og:title" content="Lashes & Beauty Badalona · Centre d\'estètica">'),
 ('content="Extensiones y lifting de pestañas, microblading, micropigmentación y tratamientos faciales en Badalona. Reserva tu cita online."', 'content="Extensions i lifting de pestanyes, microblading, micropigmentació i tractaments facials a Badalona. Reserva la teva cita en línia."'),
 (f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/ca/">'),
 ('content="Lashes & Beauty Badalona, centro de estética en Via Augusta 5, Badalona"', 'content="Lashes & Beauty Badalona, centre d\'estètica a Via Augusta 5, Badalona"'),
 (f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/ca/">'),
 (f'"url": "{SITE}/",', f'"url": "{SITE}/ca/",'),
 ('"description": "Centro de estética especializado en extensiones y lifting de pestañas, microblading, micropigmentación, laminado de cejas, tratamientos faciales y corporales.",',
  '"description": "Centre d\'estètica especialitzat en extensions i lifting de pestanyes, microblading, micropigmentació, laminat de celles, tractaments facials i corporals.",'),
 ('"paymentAccepted": "Efectivo, tarjeta de crédito, tarjeta de débito",', '"paymentAccepted": "Efectiu, targeta de crèdit, targeta de dèbit",'),
 ('href="assets/', 'href="/assets/', None), ('src="assets/', 'src="/assets/', None), ('poster="assets/', 'poster="/assets/'),
 ('<script src="/assets/app.js"></script>', '<script src="/assets/i18n-ca.js"></script>\n<script src="/assets/app.js"></script>'),
 # Black Friday
 ('<aside aria-label="Promoción Black Friday">', '<aside aria-label="Promoció Black Friday">'),
 ('Hasta el <b>60% de descuento</b> en tratamientos seleccionados · Para citas hasta el 30 de noviembre · Reserva por WhatsApp', 'Fins al <b>60% de descompte</b> en tractaments seleccionats · Per a cites fins al 30 de novembre · Reserva per WhatsApp'),
 ('Hasta <b>-60%</b> en tratamientos seleccionados', 'Fins a <b>-60%</b> en tractaments seleccionats'),
 ('>Ver promos →<', '>Mira les promos →<'),
 # Portada
 ('<span class="eyebrow">Centro de estética · Badalona</span>', '<span class="eyebrow">Centre d\'estètica · Badalona</span>'),
 ('<h1>Realza tu mirada con <em>naturalidad</em></h1>', '<h1>Realça la teva mirada amb <em>naturalitat</em></h1>'),
 ('<p>Centro de estética en <strong>Via Augusta, 5 de Badalona</strong>, a un minuto del metro Pompeu Fabra. Especialistas en extensiones y lifting de pestañas, microblading, micropigmentación, diseño de cejas y tratamientos faciales, con resultados cuidados al detalle.</p>',
  '<p>Centre d\'estètica a <strong>Via Augusta, 5 de Badalona</strong>, a un minut del metro Pompeu Fabra. Especialistes en extensions i lifting de pestanyes, microblading, micropigmentació, disseny de celles i tractaments facials, amb resultats cuidats al detall.</p>'),
 ('>Reservar cita online</a>', '>Reserva cita en línia</a>'),
 ('Valoración en Treatwell</div>', 'Valoració a Treatwell</div>'),
 ('Opiniones de clientas</div>', 'Opinions de clientes</div>'),
 # Centro
 ('<span class="eyebrow">Nuestro centro</span>', '<span class="eyebrow">El nostre centre</span>'),
 ('<h2>Un espacio pensado para ti</h2>', '<h2>Un espai pensat per a tu</h2>'),
 ('<p>Te esperamos en un centro acogedor y tranquilo, donde cuidamos cada detalle para que disfrutes de tu momento de belleza. Ven a conocernos en Via Augusta, 5, a un minuto del metro Pompeu Fabra.</p>',
  '<p>T\'esperem en un centre acollidor i tranquil, on cuidem cada detall perquè gaudeixis del teu moment de bellesa. Vine a conèixer-nos a Via Augusta, 5, a un minut del metro Pompeu Fabra.</p>'),
 ('>Reservar cita</a>', '>Reserva cita</a>'),
 ('href="#visita">Cómo llegar</a>', 'href="#visita">Com arribar</a>'),
 ('aria-label="Vídeo del interior del centro Lashes &amp; Beauty Badalona"', 'aria-label="Vídeo de l\'interior del centre Lashes &amp; Beauty Badalona"'),
 ('aria-pressed="false">❚❚ Pausar vídeo</button>', 'aria-pressed="false">❚❚ Pausa el vídeo</button>'),
 # Tarjetas
 ('<h3>Cejas</h3><p>Diseño y depilación con hilo, laminado de cejas y henna.</p>', '<h3>Celles</h3><p>Disseny i depilació amb fil, laminat de celles i henna.</p>'),
 ('<h3>Pestañas</h3><p>Extensiones express y puesta completa, lifting coreano y tinte.</p>', '<h3>Pestanyes</h3><p>Extensions express i posada completa, lifting coreà i tint.</p>'),
 ('<h3>Micro&shy;pigmentación</h3><p>Microblading, hybrid brows, eyeliner y labios semipermanentes con -20% dto.</p>', '<h3>Micro&shy;pigmentació</h3><p>Microblading, hybrid brows, eyeliner i llavis semipermanents amb un -20% de descompte.</p>'),
 ('<h3>Tratamientos faciales</h3><p>Limpieza profunda, Hydraface, peelings, dermapen con exosomas y depilación facial con hilo.</p>', '<h3>Tractaments facials</h3><p>Neteja profunda, Hydraface, peelings, dermapen amb exosomes i depilació facial amb fil.</p>'),
 ('<h3>Tratamientos corporales</h3><p>Remodelación corporal I-MODEL: tonificación, celulitis y quema de grasa.</p>', '<h3>Tractaments corporals</h3><p>Remodelació corporal I-MODEL: tonificació, cel·lulitis i crema de greixos.</p>'),
 # Servicios
 ('<span class="eyebrow">Carta de servicios</span>', '<span class="eyebrow">Carta de serveis</span>'),
 ('<h2>Servicios y precios</h2>', '<h2>Serveis i preus</h2>'),
 ('<p>Elige tu tratamiento y reserva en un par de clics.</p>', '<p>Tria el teu tractament i reserva en un parell de clics.</p>'),
 ('aria-label="Filtrar servicios por categoría"', 'aria-label="Filtra els serveis per categoria"'),
 ('💳 Financia tus tratamientos con <strong>Alma</strong> hasta en 4 meses sin intereses y sin aportar documentación, para importes a partir de 100 €.', '💳 Finança els teus tractaments amb <strong>Alma</strong> fins a 4 mesos sense interessos i sense aportar documentació, per a imports a partir de 100 €.'),
 ('<p class="note">Precios con IVA incluido.</p>', '<p class="note">Preus amb IVA inclòs.</p>'),
 # Reseñas (el texto de las clientas se deja tal cual, en castellano)
 ('<span class="eyebrow">Reseñas de Google</span>', '<span class="eyebrow">Ressenyes de Google</span>'),
 ('<h2>Lo que dicen nuestras clientas</h2>', '<h2>El que diuen les nostres clientes</h2>'),
 ('aria-label="5 de 5 estrellas"', 'aria-label="5 de 5 estrelles"', 7),
 ('<blockquote>', '<blockquote lang="es">', 7),
 ('<small>Lifting de pestañas</small>', '<small>Lifting de pestanyes</small>'),
 ('<small>Microblading de cejas</small>', '<small>Microblading de celles</small>', 2),
 ('<small>Pestañas y cejas</small>', '<small>Pestanyes i celles</small>'),
 ('Reseñas publicadas por clientas en nuestro perfil de Google. Mostramos una selección, sin modificar su texto.', 'Ressenyes publicades per clientes al nostre perfil de Google. Mostrem una selecció, sense modificar-ne el text.'),
 ('>Ver todas las reseñas en Google →</a>', '>Mira totes les ressenyes a Google →</a>'),
 # Tarjetas regalo
 ('<span class="gc-title">Tarjeta regalo</span>', '<span class="gc-title">Targeta regal</span>'),
 ('<span class="gc-for">Para: alguien especial ♡</span>', '<span class="gc-for">Per a: algú especial ♡</span>'),
 ('<span class="eyebrow">Tarjetas regalo</span>', '<span class="eyebrow">Targetes regal</span>'),
 ('<h2>Regala belleza a tus seres queridos</h2>', '<h2>Regala bellesa a les persones que estimes</h2>'),
 ('<p>Sorprende a quien más quieres con una tarjeta regalo de Lashes &amp; Beauty Badalona. El detalle perfecto para cumpleaños, aniversarios, Navidad, el Día de la Madre… o simplemente porque sí.</p>',
  '<p>Sorprèn qui més estimes amb una targeta regal de Lashes &amp; Beauty Badalona. El detall perfecte per a aniversaris, Nadal, el Dia de la Mare… o simplement perquè sí.</p>'),
 ('<p>Escríbenos por WhatsApp o pásate por el centro y te ayudamos a prepararla. La tarjeta regalo es válida durante <strong>3 meses</strong> desde la fecha de compra.</p>',
  '<p>Escriu-nos per WhatsApp o passa pel centre i t\'ajudem a preparar-la. La targeta regal és vàlida durant <strong>3 mesos</strong> des de la data de compra.</p>'),
 (GIFT_ES, GIFT_CA),
 ('>Pedir tarjeta regalo</a>', '>Demana una targeta regal</a>'),
 ('>Ven al centro</a>', '>Vine al centre</a>'),
 # Blog
 ('<h2>Consejos de belleza</h2>', '<h2>Consells de bellesa</h2>'),
 ('<p>Resolvemos las dudas más frecuentes sobre cejas, pestañas y cuidado facial.</p>', '<p>Resolem els dubtes més freqüents sobre celles, pestanyes i cura facial.</p>'),
 ('<a href="blog/">Ver todos los artículos →</a>', '<a href="/ca/blog/">Mira tots els articles →</a>'),
 # Dónde estamos
 ('<span class="eyebrow">Visítanos</span>', '<span class="eyebrow">Visita\'ns</span>'),
 ('<h2>Dónde estamos</h2>', '<h2>On som</h2>'),
 ('<div class="label">Dirección</div>', '<div class="label">Adreça</div>'),
 ('A 1 minuto del metro Badalona Pompeu Fabra (L2)', 'A 1 minut del metro Badalona Pompeu Fabra (L2)'),
 ('<div class="label">Horario</div>', '<div class="label">Horari</div>'),
 ('<th scope="row">Lunes – Viernes</th>', '<th scope="row">Dilluns – Divendres</th>'),
 ('<th scope="row">Sábado y domingo</th><td>Cerrado</td>', '<th scope="row">Dissabte i diumenge</th><td>Tancat</td>'),
 ('<div class="label">Contacto</div>', '<div class="label">Contacte</div>'),
 ('Teléfono: <a href="tel:', 'Telèfon: <a href="tel:'),
 ('>Cómo llegar en Google Maps →</a>', '>Com arribar amb Google Maps →</a>'),
 ('id="map-load">Ver mapa</button>', 'id="map-load">Mostra el mapa</button>'),
 ('Al pulsar se carga Google Maps, que puede usar cookies propias.', 'En prémer el botó es carrega Google Maps, que pot utilitzar cookies pròpies.'),
 # Llamada final
 ('<h2>¿Lista para tu próxima cita?</h2>', '<h2>Preparada per a la teva propera cita?</h2>'),
 ('<p>Reserva online las 24 h o escríbenos por WhatsApp y te asesoramos.</p>', '<p>Reserva en línia les 24 h o escriu-nos per WhatsApp i t\'assessorem.</p>'),
 ('>Reservar ahora</a>', '>Reserva ara</a>'),
 ('>Escribir por WhatsApp</a>', '>Escriu per WhatsApp</a>'),
]

def build_home():
    es = rd("index.html")
    t = es
    # vaciar la carta (la escribe tools/carta.js ya traducida)
    for name in ("CARTA-FILTROS", "CARTA-SERVICIOS"):
        i = t.index(f"<!--{name}-->") + len(f"<!--{name}-->"); j = t.index(f"<!--/{name}-->")
        t = t[:i] + t[j:]
    t = apply(t, HOME, "portada")
    # tarjetas del blog
    i = t.index('<div class="posts">', t.index("<!-- BLOG -->")); j = t.index("</div>", i)
    t = t[:i] + '<div class="posts">\n' + "\n".join(card(k, "h3") for k in ORDER) + "\n      " + t[j:]
    t = common_ca(t, "portada", home=True)
    return t

def build_blog_index():
    t = rd("blog/index.html")
    t = head_ca(t, "blog", "Blog de bellesa | Lashes &amp; Beauty Badalona",
                "Consells de bellesa de Lashes &amp; Beauty Badalona: depilació amb fil, microblading, extensions de pestanyes i més.", "/ca/blog/")
    t = replace_main(t, f'''  <section class="post-hero">
    <div class="wrap">
      <span class="eyebrow">Blog</span>
      <h1>Consells de bellesa</h1>
      <p class="sub">Resolem els dubtes més freqüents de les nostres clientes sobre celles, pestanyes i cura facial.</p>
    </div>
  </section>
  <section class="more-posts">
    <div class="wrap">
      <div class="posts">
{chr(10).join(card(k, "h2") for k in ORDER)}
      </div>
    </div>
  </section>''', "blog")
    return common_ca(t, "blog")

def build_article(key):
    es_file, es_url, ca_file, ca_url = PAGES[key]; a = ART[key]
    t = rd(es_file)
    title = f'{a["title"]} | Lashes &amp; Beauty Badalona'
    t = head_ca(t, key, title, a["desc"], ca_url)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    ld = json.loads(m.group(1))
    ld.update(headline=a["title"], description=a["desc"].replace("&amp;", "&"), url=SITE + ca_url, mainEntityOfPage=SITE + ca_url, inLanguage="ca", dateModified="2026-11-20")
    for k in ("author", "publisher"): ld[k]["url"] = SITE + "/ca/"
    t = t[:m.start(1)] + json.dumps(ld, ensure_ascii=False) + t[m.end(1):]
    others = "".join(card(k) for k in ORDER if k != key)
    t = replace_main(t, f'''  <section class="post-hero">
    <div class="wrap narrow">
      <a class="back" href="/ca/blog/">← Torna al blog</a>
      <span class="eyebrow">{a["kicker"]}</span>
      <h1>{a["title"]}</h1>
    </div>
  </section>
  <article class="wrap narrow post">
{a["body"]}
{CTA}
  </article>
  <section class="more-posts">
    <div class="wrap">
      <h2 class="section-title">Continua llegint</h2>
      <div class="posts">
{others}
      </div>
    </div>
  </section>''', key)
    return common_ca(t, key)

def build_legal(key):
    es_file, es_url, ca_file, ca_url = PAGES[key]; L = LEGAL[key]
    t = rd(es_file)
    t = head_ca(t, key, f'{L["h1"]} | Lashes &amp; Beauty Badalona', L["desc"], ca_url)
    t = replace_main(t, f'''  <section class="post-hero">
    <div class="wrap narrow">
      <span class="eyebrow">{L["eyebrow"]}</span>
      <h1>{L["h1"]}</h1>
    </div>
  </section>
  <div class="wrap narrow doc">
{L["body"].strip(chr(10))}

{PREVAL}
  </div>''', key)
    return common_ca(t, key)

def main():
    built = {"home": build_home(), "blog": build_blog_index()}
    for k in ORDER: built[k] = build_article(k)
    for k in LEGAL: built[k] = build_legal(k)
    for key, (es_file, es_url, ca_file, ca_url) in PAGES.items():
        # página en catalán
        ca = alternates(built[key], es_url, ca_url)
        ca = switcher(ca, es_url, "es", "Castellano", ca_file)
        wr(ca_file, ca)
        # página en castellano: hreflang + enlace «Català»
        es = rd(es_file)
        es = alternates(es, es_url, ca_url)
        es = switcher(es, ca_url, "ca", "Català", es_file)
        wr(es_file, es)
    # sitemap con las dos versiones
    urls = [v[1] for v in PAGES.values() if v[1] not in ("/aviso-legal", "/privacidad", "/cookies")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for es in urls:
        ca = ES2CA[es]
        for loc in (es, ca):
            sm += ["  <url>", f"    <loc>{SITE}{loc}</loc>", "    <lastmod>2026-11-20</lastmod>",
                   f'    <xhtml:link rel="alternate" hreflang="es" href="{SITE}{es}"/>',
                   f'    <xhtml:link rel="alternate" hreflang="ca" href="{SITE}{ca}"/>', "  </url>"]
    sm.append("</urlset>")
    wr("sitemap.xml", "\n".join(sm) + "\n")
    print(f"Páginas en catalán generadas: {len(PAGES)}")

if __name__ == "__main__":
    main()

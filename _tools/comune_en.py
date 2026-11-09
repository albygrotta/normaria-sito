# -*- coding: utf-8 -*-
"""
Le parti uguali su tutte le pagine della sezione inglese /en/.

Stessa impaginazione e stesso foglio di stile del sito italiano: cambiano
solo la lingua, il menu e il piede. Chi arriva in /en/ resta in /en/.
"""

import html
from datetime import date

import comune

SITO = comune.SITO

# le voci del menu inglese, in ordine
VOCI = [
    ("method",   "The method", "/en/#method"),
    ("catalog",  "Catalog",    "/en/#catalog"),
    ("articles", "Articles",   "/en/articles.html"),
]


def menu(attiva, su=""):
    voci = []
    for chiave, testo, href in VOCI:
        classe = ' class="attiva"' if chiave == attiva else ""
        # gli indirizzi che cominciano con "/" partono dalla radice del sito:
        # non vanno preceduti dai "../" delle pagine dentro una cartella
        pre = "" if href.startswith("/") else su
        voci.append(f'          <a href="{pre}{href}"{classe}>{testo}</a>')
    # il passaggio alla sezione italiana: la radice del sito sta sopra /en/
    radice = "../" * (1 + su.count("../"))
    voci.append(f'          <a href="/" class="lingua" hreflang="it" lang="it">Italiano</a>')
    return "\n".join(voci)


def testa(attiva, su=""):
    """Intestazione + menu. `su` e' '../' per le pagine dentro una cartella."""
    radice = "../" * (1 + su.count("../"))
    return f"""  <a class="salta" href="#contenuto">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a href="/en/" class="brand">Normaria<small>Edizioni</small></a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="menu"
              aria-label="Open the menu"><span></span><span></span><span></span></button>
      <nav class="nav" id="menu">
{menu(attiva, su)}
      </nav>
    </div>
  </header>"""


def piede(su=""):
    radice = "../" * (1 + su.count("../"))
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <p class="brand-f">Normaria Edizioni</p>
          <p>Study guides built on one idea: every rule on a card of the same four blocks.</p>
        </div>
        <div>
          <h4>Browse</h4>
          <ul>
            <li><a href="/en/#method">The method</a></li>
            <li><a href="/en/#catalog">Catalog</a></li>
            <li><a href="/en/articles.html">Articles</a></li>
            <li><a href="/" hreflang="it" lang="it">Sito in italiano</a></li>
          </ul>
        </div>
        <div>
          <h4>Legal</h4>
          <ul>
            <li><a href="{radice}privacy.html">Privacy policy</a></li>
            <li><a href="{radice}cookie.html">Cookie policy</a></li>
          </ul>
        </div>
      </div>
      <div class="legal">
        Normaria Edizioni · <span class="todo">[Legal name to be added]</span> ·
        VAT <span class="todo">[to be added]</span> ·
        Registered office: <span class="todo">Grottaferrata (Rome), Italy — address to be added</span><br>
        Contact: <span class="todo">[email to be added]</span> ·
        © {date.today().year} Normaria Edizioni. All rights reserved.
      </div>
    </div>
  </footer>

  <script>
    // apre e chiude il menu sul telefono
    (function () {{
      var b = document.querySelector('.nav-toggle');
      var m = document.getElementById('menu');
      if (!b || !m) return;
      b.addEventListener('click', function () {{
        var aperto = m.classList.toggle('aperto');
        b.setAttribute('aria-expanded', aperto);
        b.setAttribute('aria-label', aperto ? 'Close the menu' : 'Open the menu');
      }});
      m.addEventListener('click', function (e) {{
        if (e.target.tagName === 'A') {{ m.classList.remove('aperto');
          b.setAttribute('aria-expanded', 'false'); }}
      }});
    }})();
  </script>"""


def pagina(titolo, descrizione, canonico, attiva, corpo, su="", extra="", tipo="website",
           alternato=""):
    """Una pagina completa della sezione inglese."""
    hreflang = ""
    if alternato:
        hreflang = (f'  <link rel="alternate" hreflang="it" href="{alternato}">\n'
                    f'  <link rel="alternate" hreflang="en" href="{canonico}">\n'
                    f'  <link rel="alternate" hreflang="x-default" href="{alternato}">\n')
    # dentro /en/ il foglio di stile sta un livello piu' su
    radice = "../" * (1 + su.count("../"))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(descrizione)}">
  <link rel="canonical" href="{canonico}">
{hreflang}
  <meta property="og:type" content="{tipo}">
  <meta property="og:title" content="{html.escape(titolo)}">
  <meta property="og:description" content="{html.escape(descrizione)}">
  <meta property="og:url" content="{canonico}">
  <meta property="og:locale" content="en_US">

  {comune.FONT}
  <link rel="stylesheet" href="{radice}style.css">
{extra}</head>
<body>

{testa(attiva, su)}

{corpo}

{piede(su)}
</body>
</html>
"""

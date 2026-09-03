#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Costruisce la sezione articoli del sito.

Da dove prende le cose:
  articoli.json            l'elenco degli articoli (titolo, data, sommario...)
  articoli/testi/<slug>.md il testo di ciascun articolo, scritto in modo semplice
  catalogo.json            i manuali, per i rimandi in fondo agli articoli

Cosa scrive:
  articoli.html            la pagina indice
  articoli/<slug>.html     una pagina per ogni articolo
  sitemap.xml              la mappa del sito per Google

Uso:  python3 _tools/genera_articoli.py
"""

import html
import json
import pathlib
import re
import sys
from datetime import date

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://normaria.net"

MESI = ("gennaio febbraio marzo aprile maggio giugno luglio "
        "agosto settembre ottobre novembre dicembre").split()

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;600;700'
        '&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600'
        '&display=swap" rel="stylesheet">')


# ---------------------------------------------------------------- utilità

def data_estesa(iso):
    a, m, g = (int(x) for x in iso.split("-"))
    return f"{g} {MESI[m - 1]} {a}"


def minuti_lettura(testo):
    return max(1, round(len(testo.split()) / 200))


def testa(titolo, descrizione, canonico, dentro_cartella, extra=""):
    """L'intestazione HTML, uguale per tutte le pagine del sito."""
    su = "../" if dentro_cartella else ""
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(descrizione)}">
  <link rel="canonical" href="{canonico}">

  <meta property="og:type" content="{'article' if dentro_cartella else 'website'}">
  <meta property="og:title" content="{html.escape(titolo)}">
  <meta property="og:description" content="{html.escape(descrizione)}">
  <meta property="og:url" content="{canonico}">
  <meta property="og:locale" content="it_IT">

  {FONT}
  <link rel="stylesheet" href="{su}style.css">
{extra}</head>
<body>

  <header class="site-header">
    <div class="wrap">
      <a href="{su}index.html" class="brand">Normaria<small>Edizioni</small></a>
      <nav class="nav">
        <a href="{su}index.html#metodo">Il metodo</a>
        <a href="{su}index.html#catalogo">Catalogo</a>
        <a href="{su}articoli.html">Articoli</a>
        <a href="{su}index.html#estratto">Estratto gratuito</a>
      </nav>
    </div>
  </header>
"""


def piede(dentro_cartella):
    su = "../" if dentro_cartella else ""
    return f"""
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <p class="brand-f">Normaria Edizioni</p>
          <p>Manuali normativi per chi prepara i concorsi pubblici. Un metodo, molte materie.</p>
        </div>
        <div>
          <h4>Naviga</h4>
          <ul>
            <li><a href="{su}index.html#metodo">Il metodo</a></li>
            <li><a href="{su}index.html#catalogo">Catalogo</a></li>
            <li><a href="{su}articoli.html">Articoli</a></li>
            <li><a href="{su}index.html#estratto">Estratto gratuito</a></li>
          </ul>
        </div>
        <div>
          <h4>Legale</h4>
          <ul>
            <li><a href="{su}privacy.html">Privacy policy</a></li>
            <li><a href="{su}cookie.html">Cookie policy</a></li>
          </ul>
        </div>
      </div>
      <div class="legal">
        Normaria Edizioni · <span class="todo">[Ragione sociale / Titolare da inserire]</span> ·
        P. IVA <span class="todo">[da inserire]</span> ·
        Sede: <span class="todo">Grottaferrata (RM) — indirizzo da inserire</span><br>
        Contatti: <span class="todo">[email da inserire]</span> ·
        © {date.today().year} Normaria Edizioni. Tutti i diritti riservati.
      </div>
    </div>
  </footer>
</body>
</html>
"""


# ------------------------------------------------- da testo semplice a HTML

def in_linea(s):
    """Grassetto, corsivo e collegamenti dentro una riga di testo."""
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
               lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def corpo(testo):
    """Converte il testo dell'articolo in HTML. Sintassi minima:
       ## titolo · ### sottotitolo · - elenco · > citazione · --- riga."""
    fuori, elenco = [], []

    def chiudi_elenco():
        if elenco:
            voci = "\n".join(f"      <li>{in_linea(v)}</li>" for v in elenco)
            fuori.append(f"    <ul>\n{voci}\n    </ul>")
            elenco.clear()

    for riga in testo.split("\n"):
        r = riga.rstrip()
        if r.startswith("- "):
            elenco.append(r[2:]); continue
        chiudi_elenco()
        if not r.strip():
            continue
        if r.startswith("### "):
            fuori.append(f"    <h3>{in_linea(r[4:])}</h3>")
        elif r.startswith("## "):
            fuori.append(f"    <h2>{in_linea(r[3:])}</h2>")
        elif r.startswith("> "):
            fuori.append(f'    <p class="nota">{in_linea(r[2:])}</p>')
        elif r.strip() == "---":
            fuori.append("    <hr>")
        else:
            fuori.append(f"    <p>{in_linea(r)}</p>")
    chiudi_elenco()
    return "\n".join(fuori)


# ------------------------------------------------------------- costruzione

def rimandi(a, per_id):
    """Il blocco finale: i manuali collegati all'articolo."""
    scelti = [per_id[i] for i in a.get("manuali", []) if i in per_id]
    if not scelti:
        return ""
    voci = "\n".join(f"""        <li>
          <a href="{html.escape(m['link'], quote=True)}" target="_blank" rel="noopener">{html.escape(m['titolo'])}</a>
          <span>{html.escape(m['descrizione'])}</span>
        </li>""" for m in scelti)
    return f"""
    <aside class="rimandi">
      <h2>Approfondire con il metodo Normaria</h2>
      <p>Ogni norma su una scheda sempre uguale: il testo, perché conta, i collegamenti, i termini chiave.</p>
      <ul>
{voci}
      </ul>
      <p class="rimandi-piu"><a href="../index.html#catalogo">Vedi tutto il catalogo</a></p>
    </aside>"""


def dati_articolo(a, descrizione):
    blocco = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["titolo"],
        "description": descrizione,
        "datePublished": a["data"],
        "dateModified": a.get("aggiornato", a["data"]),
        "inLanguage": "it",
        "author": {"@type": "Organization", "name": "Normaria Edizioni"},
        "publisher": {"@type": "Organization", "name": "Normaria Edizioni"},
        "mainEntityOfPage": f"{SITO}/articoli/{a['slug']}.html",
    }
    corpo_json = json.dumps(blocco, ensure_ascii=False, indent=2)
    return '  <script type="application/ld+json">\n' + corpo_json + "\n  </script>\n"


def pagina_articolo(a, per_id):
    testo = (RADICE / "articoli" / "testi" / f"{a['slug']}.md").read_text(encoding="utf-8")
    canonico = f"{SITO}/articoli/{a['slug']}.html"
    fonti = ""
    if a.get("fonti"):
        voci = "\n".join(
            f'        <li><a href="{html.escape(f["url"], quote=True)}" target="_blank" rel="noopener">{html.escape(f["testo"])}</a></li>'
            for f in a["fonti"])
        fonti = f"""
    <div class="fonti">
      <h2>Fonti</h2>
      <ul>
{voci}
      </ul>
    </div>"""

    return (testa(f"{a['titolo']} — Normaria Edizioni", a["sommario"], canonico,
                  True, dati_articolo(a, a["sommario"]))
            + f"""
  <main class="wrap doc articolo">
    <p class="briciole"><a href="../articoli.html">Articoli</a> · {html.escape(a['occhiello'])}</p>
    <h1>{html.escape(a['titolo'])}</h1>
    <p class="updated">{data_estesa(a['data'])} · {minuti_lettura(testo)} minuti di lettura</p>
    <p class="sommario">{html.escape(a['sommario'])}</p>

{corpo(testo)}
{fonti}
{rimandi(a, per_id)}
  </main>
""" + piede(True))


def pagina_indice(articoli):
    schede = "\n\n".join(f"""        <article class="post">
          <p class="collana">{html.escape(a['occhiello'])} · {data_estesa(a['data'])}</p>
          <h2><a href="articoli/{a['slug']}.html">{html.escape(a['titolo'])}</a></h2>
          <p>{html.escape(a['sommario'])}</p>
          <p class="post-piu"><a href="articoli/{a['slug']}.html">Leggi l'articolo</a></p>
        </article>""" for a in articoli)

    elenco = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Articoli — Normaria Edizioni",
        "url": f"{SITO}/articoli.html",
        "inLanguage": "it",
        "blogPost": [{"@type": "BlogPosting", "headline": a["titolo"],
                      "datePublished": a["data"],
                      "url": f"{SITO}/articoli/{a['slug']}.html"} for a in articoli],
    }
    extra = ('  <script type="application/ld+json">\n'
             + json.dumps(elenco, ensure_ascii=False, indent=2) + "\n  </script>\n")

    return (testa("Articoli — Normaria Edizioni",
                  "Norme spiegate una alla volta e concorsi pubblici in corso: "
                  "cosa dice la legge, perché esiste, come cade all'esame.",
                  f"{SITO}/articoli.html", False, extra)
            + f"""
  <section class="hero hero-stretto">
    <div class="wrap">
      <div>
        <p class="eyebrow">Articoli</p>
        <h1>Una norma alla volta.</h1>
        <p class="lead">Il diritto spiegato a chi non è giurista, e i concorsi in corso raccontati per quello che sono: date, requisiti, prove.</p>
      </div>
    </div>
  </section>

  <section id="elenco">
    <div class="wrap">
      <div class="posts">
{schede}
      </div>
    </div>
  </section>
""" + piede(False))


def mappa_sito(articoli):
    voci = [(f"{SITO}/", "1.0"), (f"{SITO}/articoli.html", "0.8")]
    voci += [(f"{SITO}/articoli/{a['slug']}.html", "0.7") for a in articoli]
    voci += [(f"{SITO}/privacy.html", "0.3"), (f"{SITO}/cookie.html", "0.3")]
    corpo_xml = "\n".join(
        f"  <url><loc>{u}</loc><priority>{p}</priority></url>" for u, p in voci)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + corpo_xml + "\n</urlset>\n")


def main():
    articoli = json.loads((RADICE / "articoli.json").read_text(encoding="utf-8"))["articoli"]
    articoli.sort(key=lambda a: a["data"], reverse=True)

    catalogo = json.loads((RADICE / "catalogo.json").read_text(encoding="utf-8"))
    per_id = {m["id"]: m for s in catalogo["sezioni"] for m in s["manuali"]}

    (RADICE / "articoli").mkdir(exist_ok=True)
    for a in articoli:
        sorgente = RADICE / "articoli" / "testi" / f"{a['slug']}.md"
        if not sorgente.exists():
            sys.exit(f"ERRORE: manca il testo {sorgente}")
        (RADICE / "articoli" / f"{a['slug']}.html").write_text(
            pagina_articolo(a, per_id), encoding="utf-8")

    (RADICE / "articoli.html").write_text(pagina_indice(articoli), encoding="utf-8")
    (RADICE / "sitemap.xml").write_text(mappa_sito(articoli), encoding="utf-8")
    print(f"Fatto: {len(articoli)} articoli, indice e sitemap.xml")


if __name__ == "__main__":
    main()

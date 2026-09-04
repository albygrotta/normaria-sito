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

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import comune  # noqa: E402

MESI = ("gennaio febbraio marzo aprile maggio giugno luglio "
        "agosto settembre ottobre novembre dicembre").split()


# ---------------------------------------------------------------- utilità

def data_estesa(iso):
    a, m, g = (int(x) for x in iso.split("-"))
    return f"{g} {MESI[m - 1]} {a}"


def minuti_lettura(testo):
    return max(1, round(len(testo.split()) / 200))


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
    fuori, elenco, tabella = [], [], []

    def chiudi_elenco():
        if elenco:
            voci = "\n".join(f"      <li>{in_linea(v)}</li>" for v in elenco)
            fuori.append(f"    <ul>\n{voci}\n    </ul>")
            elenco.clear()

    def chiudi_tabella():
        """Le righe che cominciano con | diventano una tabella.
           La prima riga è l'intestazione; la riga di soli trattini si salta."""
        if not tabella:
            return
        righe = [x for x in tabella if not set(x.replace("|", "").strip()) <= {"-", " ", ":"}]
        celle = [[c.strip() for c in x.strip().strip("|").split("|")] for x in righe]
        cap = "".join(f"<th>{in_linea(c)}</th>" for c in celle[0])
        corpo_t = "\n".join("      <tr>" + "".join(f"<td>{in_linea(c)}</td>" for c in r) + "</tr>"
                            for r in celle[1:])
        fuori.append('    <div class="tabella-scorre">\n    <table>\n'
                     f"      <thead><tr>{cap}</tr></thead>\n      <tbody>\n{corpo_t}\n      </tbody>\n"
                     "    </table>\n    </div>")
        tabella.clear()

    for riga in testo.split("\n"):
        r = riga.rstrip()
        if r.startswith("|"):
            chiudi_elenco(); tabella.append(r); continue
        chiudi_tabella()
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
    chiudi_elenco(); chiudi_tabella()
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


def invito():
    """L'invito a ricevere l'estratto, in fondo a ogni articolo."""
    return f"""
    <aside class="invito">
      <p class="eyebrow">Estratto gratuito</p>
      <h2>Vuoi vedere com'è fatta una scheda?</h2>
      <p>Quindici pagine dal Manuale Normativo di Diritto Amministrativo: come si legge
         una scheda, l'indice completo e le prime venti norme. Te le mandiamo per email.</p>
{comune.modulo(su="../", id_form="modulo-articolo")}
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

    corpo_pagina = f"""  <main class="wrap doc articolo" id="contenuto">
    <p class="briciole"><a href="../articoli.html">Articoli</a> · {html.escape(a['occhiello'])}</p>
    <h1>{html.escape(a['titolo'])}</h1>
    <p class="updated">{data_estesa(a['data'])} · {minuti_lettura(testo)} minuti di lettura</p>
    <p class="sommario">{html.escape(a['sommario'])}</p>

{corpo(testo)}
{fonti}
{rimandi(a, per_id)}
{invito()}
  </main>"""

    return comune.pagina(
        titolo=f"{a['titolo']} — Normaria Edizioni", descrizione=a["sommario"],
        canonico=canonico, attiva="articoli", su="../", tipo="article",
        extra=dati_articolo(a, a["sommario"]), corpo=corpo_pagina)


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

    corpo_pagina = f"""  <main id="contenuto">
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
  </main>"""

    return comune.pagina(
        titolo="Articoli — Normaria Edizioni",
        descrizione="Norme spiegate una alla volta e concorsi pubblici in corso: "
                    "cosa dice la legge, perché esiste, come cade all'esame.",
        canonico=f"{SITO}/articoli.html", attiva="articoli",
        corpo=corpo_pagina, extra=extra)


def mappa_sito(articoli):
    voci = [(f"{SITO}/", "1.0"), (f"{SITO}/metodo.html", "0.9"),
            (f"{SITO}/articoli.html", "0.8")]
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

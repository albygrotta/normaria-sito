#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Costruisce la sezione inglese del sito, sotto /en/.

Da dove prende le cose:
  en/catalogo.json              i libri in inglese
  en/articoli.json              l'elenco degli articoli in inglese
  en/articles/testi/<slug>.md   il testo di ciascun articolo

Cosa scrive:
  en/index.html                 vetrina: metodo + catalogo
  en/articles.html              la pagina indice degli articoli
  en/articles/<slug>.html       una pagina per ogni articolo

La sitemap la scrive genera_articoli.py, che legge anche questi file.

Uso:  python3 _tools/genera_en.py
"""

import html
import json
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import comune      # noqa: E402
import comune_en   # noqa: E402
import genera_articoli as ga  # noqa: E402

SITO = comune.SITO
EN = RADICE / "en"

MESI = ("January February March April May June July "
        "August September October November December").split()


def data_estesa(iso):
    a, m, g = (int(x) for x in iso.split("-"))
    return f"{MESI[m - 1]} {g}, {a}"


# ------------------------------------------------------------------ catalogo

def scheda(m):
    disponibile = m.get("stato", "disponibile") != "in-arrivo"
    titolo = html.escape(m["titolo"])
    if disponibile:
        etichetta = '<span class="tag tag-available">Available</span>'
        link = html.escape(m["link"], quote=True)
        bottone = (f'<a href="{link}" class="btn btn-ghost" '
                   f'target="_blank" rel="noopener">Buy on Amazon</a>')
        testo_misura = m.get("misura", "").strip()
    else:
        etichetta = '<span class="tag tag-soon">Coming soon</span>'
        bottone = '<a href="articles.html" class="btn btn-ghost">Read the articles</a>'
        testo_misura = "In preparation"

    misura = (f'<span class="norme mono">{html.escape(testo_misura)}</span>'
              if testo_misura else "")
    copertina = ""
    if m.get("copertina"):
        copertina = (f'            <a class="book-cover" href="{html.escape(m["link"], quote=True)}" target="_blank" rel="noopener"\n'
                     f'               aria-label="Cover of {titolo}">\n'
                     f'              <img src="{html.escape(m["copertina"], quote=True)}" alt="Cover of {titolo}" loading="lazy">\n'
                     f'            </a>\n')
    return f"""          <article class="book">
{copertina}            <div class="book-body">
              {etichetta}
              <p class="collana">{html.escape(m["materia"])}</p>
              <h3>{titolo}</h3>
              <p>{html.escape(m["descrizione"])}</p>
              <div class="book-foot">
                {misura}
                {bottone}
              </div>
            </div>
          </article>"""


def sezione(s):
    schede = "\n\n".join(scheda(m) for m in s["manuali"])
    sommario = (f'\n          <p>{html.escape(s["sommario"])}</p>'
                if s.get("sommario") else "")
    return f"""        <div class="catalog-group">
          <h3 class="group-title">{html.escape(s["nome"])}</h3>{sommario}
        </div>
        <div class="catalog">
{schede}
        </div>"""


def dati_libri(manuali):
    elementi = []
    for i, m in enumerate(manuali, start=1):
        libro = {
            "@type": "Book",
            "name": m["titolo"],
            "inLanguage": "en",
            "about": m["materia"],
            "publisher": {"@type": "Organization", "name": "Normaria Edizioni"},
            "description": m["descrizione"],
            "url": m["link"],
        }
        elementi.append({"@type": "ListItem", "position": i, "item": libro})
    blocco = {"@context": "https://schema.org", "@type": "ItemList",
              "name": "Normaria Edizioni — English catalog", "itemListElement": elementi}
    return ('  <script type="application/ld+json">\n'
            + json.dumps(blocco, ensure_ascii=False, indent=2) + "\n  </script>\n")


def scheda_esempio():
    """La scheda a quattro blocchi, in inglese, con una regola americana."""
    return """      <div class="scheda scheda-larga" aria-label="Rule card">
        <div class="scheda-head">
          <span class="art">Rule 401</span>
          <span class="title">Test for Relevant Evidence</span>
        </div>
        <div class="scheda-grid">
          <div class="scheda-block">
            <div class="b-label">Text</div>
            <div class="b-body">Evidence is relevant if: (a) it has any tendency to make a fact
              more or less probable than it would be without the evidence; and (b) the fact is of
              consequence in determining the action.</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Why it matters</div>
            <div class="b-body">The bar is low on purpose: evidence only has to move the needle a
              little. What keeps weak evidence out is Rule 403, not this one.</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Connections</div>
            <div class="b-body">Rule 402 on admissibility · Rule 403 on unfair prejudice ·
              Rule 404 on character evidence.</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Key terms</div>
            <div class="b-body">Any tendency · More or less probable · Of consequence.</div>
          </div>
        </div>
      </div>"""


def pagina_home(catalogo, articoli):
    manuali = [m for s in catalogo["sezioni"] for m in s["manuali"]]
    sezioni = "\n\n".join(sezione(s) for s in catalogo["sezioni"])
    n_libri = len(manuali)

    ultimi = ""
    if articoli:
        voci = "\n".join(f"""        <article class="post">
          <p class="collana">{html.escape(a['occhiello'])} · {data_estesa(a['data'])}</p>
          <h3><a href="articles/{a['slug']}.html">{html.escape(a['titolo'])}</a></h3>
          <p>{html.escape(a['sommario'])}</p>
        </article>""" for a in articoli[:3])
        ultimi = f"""
  <section id="articles">
    <div class="wrap">
      <h2 class="group-title">From the articles</h2>
      <div class="posts">
{voci}
      </div>
      <p class="rimandi-piu"><a href="articles.html">All articles</a></p>
    </div>
  </section>"""

    corpo = f"""  <main id="contenuto">

  <section class="hero">
    <div class="wrap">
      <div>
        <p class="eyebrow">Normaria Edizioni</p>
        <h1>Every rule on a card of four blocks.</h1>
        <p class="lead">Study guides for American exams and for the law of evidence, built on
          one idea: a rule is easier to remember when it always arrives in the same shape.</p>
        <p class="cifre mono">{n_libri} titles · English catalog</p>
        <p><a href="#catalog" class="btn">See the catalog</a></p>
      </div>
{scheda_esempio()}
    </div>
  </section>

  <section id="method">
    <div class="wrap">
      <h2 class="group-title">The method</h2>
      <p>Every rule is reduced to four fixed fields: the text, why it matters, the connections,
         the key terms. The order never changes, and neither does the number of fields.</p>
      <p>The reason is practical. After the first few cards a reader knows where on the page the
         needed fact sits, and attention moves to the content. The structure stops being an
         obstacle and becomes an index.</p>
      <ul>
        <li><strong>Text.</strong> The rule as enacted, not paraphrased. Exam questions are
          built on the drafter's words, and an elegant paraphrase drops the decisive one.</li>
        <li><strong>Why it matters.</strong> The reason behind the rule, in two lines. It makes
          the text easier to hold, and it answers questions put in an unfamiliar way.</li>
        <li><strong>Connections.</strong> The neighbouring rules. The hardest questions live on
          the border between one rule and the next.</li>
        <li><strong>Key terms.</strong> The three or four words the examiner expects to see.
          On review they pull back the rest of the card.</li>
      </ul>
      <p>Alongside it the books use the Feynman method: a concept counts as learned only when it
         can be explained in plain words to someone who does not know it. The block «Why it
         matters» is that explanation, already written.</p>
    </div>
  </section>

  <section id="catalog">
    <div class="wrap">
      <h2 class="group-title">Catalog</h2>
      <p>Prices and availability are on Amazon, where the books are sold.</p>
{sezioni}
    </div>
  </section>
{ultimi}
  </main>"""

    return comune_en.pagina(
        titolo="Normaria Edizioni — study guides built on one card",
        descrizione="English catalog of Normaria Edizioni: HESI A2, the US citizenship test and "
                    "the Federal Rules of Evidence, each rule reduced to the same four-block card.",
        canonico=f"{SITO}/en/", attiva="catalog", corpo=corpo,
        extra=dati_libri(manuali), alternato=f"{SITO}/")


# ------------------------------------------------------------------ articoli

def dati_articolo(a):
    blocco = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["titolo"],
        "description": a["sommario"],
        "datePublished": a["data"],
        "dateModified": a.get("aggiornato", a["data"]),
        "inLanguage": "en",
        "author": {"@type": "Organization", "name": "Normaria Edizioni"},
        "publisher": {"@type": "Organization", "name": "Normaria Edizioni"},
        "mainEntityOfPage": f"{SITO}/en/articles/{a['slug']}.html",
    }
    return ('  <script type="application/ld+json">\n'
            + json.dumps(blocco, ensure_ascii=False, indent=2) + "\n  </script>\n")


def rimandi(a, per_id):
    scelti = [per_id[i] for i in a.get("libri", []) if i in per_id]
    if not scelti:
        return ""
    voci = "\n".join(f"""        <li>
          <a href="{html.escape(m['link'], quote=True)}" target="_blank" rel="noopener">{html.escape(m['titolo'])}</a>
          <span>{html.escape(m['descrizione'])}</span>
        </li>""" for m in scelti)
    return f"""
    <aside class="rimandi">
      <h2>Going further</h2>
      <p>Every rule on the same card: the text, why it matters, the connections, the key terms.</p>
      <ul>
{voci}
      </ul>
      <p class="rimandi-piu"><a href="/en/#catalog">See the whole catalog</a></p>
    </aside>"""


def pagina_articolo(a, per_id):
    testo = (EN / "articles" / "testi" / f"{a['slug']}.md").read_text(encoding="utf-8")
    fonti = ""
    if a.get("fonti"):
        voci = "\n".join(
            f'        <li><a href="{html.escape(f["url"], quote=True)}" target="_blank" rel="noopener">{html.escape(f["testo"])}</a></li>'
            for f in a["fonti"])
        fonti = f"""
    <div class="fonti">
      <h2>Sources</h2>
      <ul>
{voci}
      </ul>
    </div>"""

    corpo = f"""  <main class="wrap doc articolo" id="contenuto">
    <p class="briciole"><a href="../articles.html">Articles</a> · {html.escape(a['occhiello'])}</p>
    <h1>{html.escape(a['titolo'])}</h1>
    <p class="updated">{data_estesa(a['data'])} · {ga.minuti_lettura(testo)} min read</p>
    <p class="sommario">{html.escape(a['sommario'])}</p>

{ga.corpo(testo)}
{fonti}
{rimandi(a, per_id)}
  </main>"""

    return comune_en.pagina(
        titolo=f"{a['titolo']} — Normaria Edizioni", descrizione=a["sommario"],
        canonico=f"{SITO}/en/articles/{a['slug']}.html", attiva="articles",
        su="../", tipo="article", extra=dati_articolo(a), corpo=corpo)


def pagina_indice(articoli):
    if articoli:
        schede = "\n\n".join(f"""        <article class="post">
          <p class="collana">{html.escape(a['occhiello'])} · {data_estesa(a['data'])}</p>
          <h2><a href="articles/{a['slug']}.html">{html.escape(a['titolo'])}</a></h2>
          <p>{html.escape(a['sommario'])}</p>
          <p class="post-piu"><a href="articles/{a['slug']}.html">Read the article</a></p>
        </article>""" for a in articoli)
    else:
        schede = '        <article class="post"><p>The first articles are on their way.</p></article>'

    corpo = f"""  <main id="contenuto">
  <section class="hero hero-stretto">
    <div class="wrap">
      <div>
        <p class="eyebrow">Articles</p>
        <h1>One rule at a time.</h1>
        <p class="lead">What a rule says, why it exists, and how it turns into an exam question.
          Written for readers who are not lawyers.</p>
      </div>
    </div>
  </section>

  <section id="list">
    <div class="wrap">
      <div class="posts">
{schede}
      </div>
    </div>
  </section>
  </main>"""

    return comune_en.pagina(
        titolo="Articles — Normaria Edizioni",
        descrizione="Rules explained one at a time, and the American exams that test them: "
                    "what the rule says, why it exists, how it is asked.",
        canonico=f"{SITO}/en/articles.html", attiva="articles", corpo=corpo)


def main():
    catalogo = json.loads((EN / "catalogo.json").read_text(encoding="utf-8"))
    per_id = {m["id"]: m for s in catalogo["sezioni"] for m in s["manuali"]}

    elenco = EN / "articoli.json"
    articoli = []
    if elenco.exists():
        articoli = json.loads(elenco.read_text(encoding="utf-8"))["articoli"]
        articoli.sort(key=lambda a: a["data"], reverse=True)

    (EN / "articles").mkdir(parents=True, exist_ok=True)
    for a in articoli:
        sorgente = EN / "articles" / "testi" / f"{a['slug']}.md"
        if not sorgente.exists():
            sys.exit(f"ERRORE: manca il testo {sorgente}")
        (EN / "articles" / f"{a['slug']}.html").write_text(
            pagina_articolo(a, per_id), encoding="utf-8")

    (EN / "index.html").write_text(pagina_home(catalogo, articoli), encoding="utf-8")
    (EN / "articles.html").write_text(pagina_indice(articoli), encoding="utf-8")
    print(f"Fatto: sezione inglese, {len(per_id)} libri e {len(articoli)} articoli")


if __name__ == "__main__":
    main()

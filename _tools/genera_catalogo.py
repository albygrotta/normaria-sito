#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera le schede del catalogo dentro index.html a partire da catalogo.json.

Perché esiste: aggiungere un manuale al sito deve costare una riga di testo in
catalogo.json, non un blocco di HTML. Questo script riscrive da solo la parte
di pagina compresa fra i segnalibri CATALOGO:INIZIO / CATALOGO:FINE e il
blocco di dati per Google fra SCHEMA:INIZIO / SCHEMA:FINE.

Uso:  python3 _tools/genera_catalogo.py
"""

import html
import json
import pathlib
import re
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
DATI = RADICE / "catalogo.json"
PAGINA = RADICE / "index.html"
SITO = "https://normaria.net"


def scheda(m):
    """Costruisce l'HTML di una singola scheda-libro."""
    disponibile = m.get("stato", "disponibile") != "in-arrivo"
    titolo = html.escape(m["titolo"])
    materia = html.escape(m["materia"])
    descrizione = html.escape(m["descrizione"])

    if disponibile:
        etichetta = '<span class="tag tag-available">Disponibile</span>'
        link = html.escape(m["link"], quote=True)
        bottone = (f'<a href="{link}" class="btn btn-ghost" '
                   f'target="_blank" rel="noopener">Acquista su Amazon</a>')
        testo_misura = m.get("misura", "").strip()
    else:
        etichetta = '<span class="tag tag-soon">In arrivo</span>'
        bottone = '<a href="#estratto" class="btn btn-ghost">Avvisami all\'uscita</a>'
        testo_misura = "In lavorazione"

    misura = (f'<span class="norme mono">{html.escape(testo_misura)}</span>'
              if testo_misura else "")

    return f"""          <article class="book">
            {etichetta}
            <p class="collana">{materia}</p>
            <h3>{titolo}</h3>
            <p>{descrizione}</p>
            <div class="book-foot">
              {misura}
              {bottone}
            </div>
          </article>"""


def sezione(s):
    """Titolo di sezione + griglia delle sue schede."""
    schede = "\n\n".join(scheda(m) for m in s["manuali"])
    sommario = (f'\n          <p>{html.escape(s["sommario"])}</p>'
                if s.get("sommario") else "")
    return f"""        <div class="catalog-group">
          <h3 class="group-title">{html.escape(s["nome"])}</h3>{sommario}
        </div>
        <div class="catalog">
{schede}
        </div>"""


def tutti(sezioni):
    """Tutti i manuali di tutte le sezioni, in ordine di pagina."""
    return [m for s in sezioni for m in s["manuali"]]


def dati_per_google(manuali):
    """Blocco JSON-LD schema.org: dice a Google che questi sono libri."""
    elementi = []
    for i, m in enumerate(manuali, start=1):
        libro = {
            "@type": "Book",
            "name": m["titolo"],
            "bookFormat": "https://schema.org/Paperback",
            "inLanguage": "it",
            "about": m["materia"],
            "genre": "Preparazione ai concorsi pubblici",
            "publisher": {"@type": "Organization", "name": "Normaria Edizioni"},
            "description": m["descrizione"],
        }
        if m.get("stato", "disponibile") != "in-arrivo":
            libro["url"] = m["link"]
        elementi.append({"@type": "ListItem", "position": i, "item": libro})

    blocco = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Catalogo Normaria Edizioni",
        "url": SITO + "/#catalogo",
        "itemListElement": elementi,
    }
    corpo = json.dumps(blocco, ensure_ascii=False, indent=2)
    return '  <script type="application/ld+json">\n' + corpo + "\n  </script>"


def sostituisci(testo, nome, contenuto):
    inizio, fine = f"<!-- {nome}:INIZIO -->", f"<!-- {nome}:FINE -->"
    schema = re.compile(re.escape(inizio) + r".*?" + re.escape(fine), re.S)
    if not schema.search(testo):
        sys.exit(f"ERRORE: segnalibri {nome} non trovati in index.html")
    return schema.sub(f"{inizio}\n{contenuto}\n{fine}", testo, count=1)


def main():
    sezioni = json.loads(DATI.read_text(encoding="utf-8"))["sezioni"]
    pagina = PAGINA.read_text(encoding="utf-8")
    pagina = sostituisci(pagina, "CATALOGO",
                         "\n\n".join(sezione(s) for s in sezioni))
    pagina = sostituisci(pagina, "SCHEMA", dati_per_google(tutti(sezioni)))
    PAGINA.write_text(pagina, encoding="utf-8")
    print(f"Fatto: {len(tutti(sezioni))} manuali in {len(sezioni)} sezioni")


if __name__ == "__main__":
    main()

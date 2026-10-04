#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Costruisce la pagina del metodo e rimette intestazione e piede uguali
in tutte le pagine fisse del sito.

Uso:  python3 _tools/genera_pagine.py
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import comune  # noqa: E402

RADICE = pathlib.Path(__file__).resolve().parent.parent

# quale voce del menu va evidenziata su ciascuna pagina fissa
PAGINE = {
    "index.html": "",
    "privacy.html": "",
    "cookie.html": "",
}


def scheda(art, titolo, testo, perche, collegamenti, termini):
    return f"""      <div class="scheda scheda-larga" aria-label="Scheda normativa">
        <div class="scheda-head">
          <span class="art">{art}</span>
          <span class="title">{titolo}</span>
        </div>
        <div class="scheda-grid">
          <div class="scheda-block">
            <div class="b-label">Testo</div>
            <div class="b-body">{testo}</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Perché conta</div>
            <div class="b-body">{perche}</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Collegamenti</div>
            <div class="b-body">{collegamenti}</div>
          </div>
          <div class="scheda-block">
            <div class="b-label">Termini chiave</div>
            <div class="b-body">{termini}</div>
          </div>
        </div>
      </div>"""


CORPO_METODO = """  <main id="contenuto">

  <section class="hero hero-stretto hero-doc">
    <div class="wrap">
      <div>
        <p class="eyebrow">Il metodo</p>
        <h1>Ogni norma in una scheda di quattro blocchi.</h1>
        <p class="lead">Il metodo Normaria dà a ogni articolo la stessa forma. Il metodo Feynman serve a controllare di averlo capito davvero.</p>
      </div>
    </div>
  </section>

  <section class="doc-wide">
    <div class="wrap">

      <h2>Perché un manuale discorsivo non prepara a un quiz</h2>
      <p>Un manuale per concorsi supera spesso le mille pagine, e il tempo per studiarlo sono tre mesi. Chi lo legge arriva in fondo con i titoli dei capitoli in testa. Poi apre una banca dati di quesiti e trova domande di tutt'altro tipo: che cosa dispone l'art. 2094 c.c., e in che cosa si distingue dall'art. 2222 c.c.</p>
      <p>Il problema sta nella forma del materiale, non nella memoria di chi studia. Un testo discorsivo è costruito per una lettura continua. Una prova a risposta multipla premia invece chi conserva molte informazioni brevi e precise, e le ritrova in pochi secondi. Il manuale tradizionale allena la prima abilità e lascia scoperta la seconda.</p>

      <h2>La scheda a quattro blocchi</h2>
      <p>La scheda normativa è la riduzione di un articolo a quattro campi fissi: il testo, perché conta, i collegamenti, i termini chiave. L'ordine non cambia mai, e nemmeno il numero dei campi.</p>

__SCHEDA__

      <p>La forma fissa ha una ragione pratica. Dopo le prime schede si sa già in quale punto della pagina sta il dato che serve, e l'attenzione si sposta sul contenuto. La struttura, cioè, smette di essere un ostacolo e diventa un indice.</p>

      <h3>I quattro blocchi</h3>
      <ul>
        <li><strong>Testo.</strong> L'articolo nella formulazione vigente, non parafrasato. I quesiti sono costruiti sulle parole del legislatore, e una parafrasi elegante perde proprio la parola decisiva.</li>
        <li><strong>Perché conta.</strong> La ragione della norma in due righe. Rende il testo più facile da ricordare e permette di rispondere anche a domande formulate in modo nuovo.</li>
        <li><strong>Collegamenti.</strong> I rimandi agli articoli vicini e alle altre leggi. Le domande più insidiose nascono sul confine fra una norma e l'altra.</li>
        <li><strong>Termini chiave.</strong> Le tre o quattro parole che la commissione si aspetta di trovare. Al ripasso richiamano il resto della scheda.</li>
      </ul>

      <h2>Il metodo Feynman</h2>
      <p>Il metodo Feynman è una tecnica di verifica: un concetto si considera appreso solo quando si riesce a spiegarlo con parole proprie a chi non lo conosce. Prende il nome dal fisico Richard Feynman, premio Nobel nel 1965, noto per la chiarezza delle sue lezioni.</p>
      <p>Si applica in quattro passaggi:</p>
      <ol>
        <li><strong>Si sceglie un concetto e si scrive in cima a un foglio.</strong> Uno solo: la subordinazione, per esempio.</li>
        <li><strong>Si spiega per iscritto in lingua comune</strong>, senza gergo e senza formule imparate a memoria.</li>
        <li><strong>Si segna il punto in cui la spiegazione si ferma.</strong> Chi si accorge di ricopiare le parole del manuale ha trovato il punto che non ha capito.</li>
        <li><strong>Si torna alla fonte, si chiarisce quel punto e si riscrive</strong>, finché la spiegazione regge dall'inizio alla fine.</li>
      </ol>
      <p>La rilettura dà un'impressione di padronanza che dipende solo dalla familiarità con il testo. La spiegazione a voce o per iscritto, invece, o riesce o non riesce: per questo è una verifica attendibile.</p>

      <h3>Il blocco «Perché conta»</h3>
      <p>Il blocco «Perché conta» applica il metodo Feynman all'articolo riportato sopra. L'art. 2094 c.c. definisce prestatore di lavoro subordinato chi collabora nell'impresa «alle dipendenze e sotto la direzione» dell'imprenditore. Tradotto in lingua comune:</p>
      <p class="nota">Se le modalità del lavoro — come, quando e dove — le decide un altro, il rapporto è subordinato. Se le decide chi lavora, e quello che consegna è il risultato, il rapporto è autonomo. Ferie, licenziamento, contributi e tutele dipendono da questa distinzione.</p>
      <p>Formulata così, la definizione diventa una domanda che si può porre davanti a un caso concreto: un rider, un consulente, un collaboratore. È quello che chiede il quesito d'esame, che raramente domanda di ripetere la definizione.</p>

      <h2>I due metodi insieme</h2>
      <p>La scheda dà l'ordine. Un manuale di trecento o quattrocento schede si ripassa per intero, perché ogni pagina è costruita allo stesso modo. L'ordine, da solo, produce però un archivio ordinato e nulla di più.</p>
      <p>Il metodo Feynman dà la comprensione, ma costa tempo. Applicarlo da zero a quattrocento norme in tre mesi non è praticabile.</p>
      <p>Nei manuali i due si incastrano. La scheda fornisce la struttura ripetibile; il blocco «Perché conta» contiene la spiegazione già costruita, che chi studia verifica invece di doverla ricavare da sé. Al ripasso bastano i termini chiave per richiamare l'intera scheda.</p>

      <h2>Che cosa il metodo non fa</h2>
      <ul>
        <li><strong>Non riassume.</strong> Il testo dell'articolo resta integrale; si aggiunge intorno il contesto che serve a fissarlo.</li>
        <li><strong>Non sostituisce le esercitazioni.</strong> I quesiti verificano, non insegnano: chi parte dai quiz impara le risposte di quei quiz.</li>
        <li><strong>Non sostituisce il codice.</strong> Il codice resta la fonte; la scheda è il modo per percorrerlo senza perdersi.</li>
      </ul>

      <div class="rimandi">
        <h2>Vedere il metodo all'opera</h2>
        <p>Ogni manuale del catalogo è costruito su questa struttura, materia per materia e concorso per concorso.</p>
        <p class="rimandi-piu"><a href="index.html#catalogo">Vai al catalogo</a></p>
      </div>

    </div>
  </section>

  </main>"""


def main():
    corpo = CORPO_METODO.replace("__SCHEDA__", scheda(
        "Art. 2094 c.c.",
        "Prestatore di lavoro subordinato",
        "È prestatore di lavoro subordinato chi si obbliga mediante retribuzione a "
        "collaborare nell'impresa, prestando il proprio lavoro intellettuale o manuale "
        "alle dipendenze e sotto la direzione dell'imprenditore.",
        "È la linea che separa il lavoro dipendente da quello autonomo: da questa "
        "distinzione discendono tutele, licenziamento, ferie e contributi.",
        "Art. 2222 c.c. sul contratto d'opera · art. 2103 c.c. sulle mansioni · "
        "art. 2 del d.lgs. 81/2015 sulle collaborazioni etero-organizzate.",
        "Dipendenze · Direzione · Collaborazione · Retribuzione."))

    (RADICE / "metodo.html").write_text(comune.pagina(
        titolo="Il metodo Normaria e il metodo Feynman — Normaria Edizioni",
        descrizione="La scheda a quattro blocchi dei manuali Normaria e il metodo "
                    "Feynman, spiegati con un esempio svolto sull'art. 2094 c.c.: "
                    "che cosa contiene ogni scheda e a che cosa serve ciascun blocco.",
        canonico=f"{comune.SITO}/metodo.html",
        attiva="metodo", corpo=corpo, tipo="article"), encoding="utf-8")

    for nome, attiva in PAGINE.items():
        f = RADICE / nome
        t = f.read_text(encoding="utf-8")
        t = comune.sostituisci(t, "HEADER", comune.testa(attiva))
        t = comune.sostituisci(t, "FOOTER", comune.piede())
        if "<!-- MODULO:INIZIO -->" in t:
            t = comune.sostituisci(t, "MODULO", comune.modulo())
        f.write_text(t, encoding="utf-8")

    print(f"Fatto: metodo.html + intestazione e piede in {len(PAGINE)} pagine")


if __name__ == "__main__":
    main()

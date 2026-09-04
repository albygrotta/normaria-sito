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
        <h1>Una scheda sempre uguale batte mille pagine.</h1>
        <p class="lead">Due idee semplici tenute insieme: ridurre ogni norma alla stessa forma, e non passare oltre finché non sai spiegarla con parole tue.</p>
      </div>
    </div>
  </section>

  <section class="doc-wide">
    <div class="wrap">

      <h2>Il problema, detto senza giri di parole</h2>
      <p>Chi prepara un concorso pubblico si trova davanti un manuale da mille o millecinquecento pagine e tre mesi di tempo. Lo legge. Alla fine ricorda i titoli dei capitoli e la sensazione di aver studiato. Poi apre una banca dati di quesiti e scopre che le domande non chiedono i capitoli: chiedono <em>cosa dice l'articolo 2094</em>, e chiedono di distinguerlo dall'articolo 2222.</p>
      <p>Il difetto non è la memoria di chi studia. È la forma del materiale. Un testo discorsivo è fatto per essere letto una volta; una prova a quiz è fatta per essere superata da chi ha immagazzinato molte informazioni piccole e precise, e sa recuperarle in trenta secondi. Sono due mestieri diversi, e il manuale tradizionale ne insegna solo uno.</p>

      <h2>La prima idea: ridurre ogni norma alla stessa scheda</h2>
      <p>Nei manuali Normaria ogni articolo è ridotto a una scheda con <strong>quattro blocchi, sempre gli stessi, sempre nello stesso ordine</strong>. Non tre, non cinque, non «dipende dalla norma». Quattro.</p>

__SCHEDA__

      <p>La ripetizione non è pigrizia editoriale: è il punto. Quando la forma è sempre identica, dopo venti schede il cervello smette di chiedersi <em>dove sarà scritta questa cosa</em> e comincia a cercarla direttamente nel posto giusto. Lo sforzo si sposta dalla navigazione alla sostanza. È lo stesso motivo per cui in cucina i coltelli stanno sempre nello stesso cassetto.</p>

      <h3>Perché proprio questi quattro</h3>
      <ul>
        <li><strong>Testo.</strong> La norma nella formulazione vigente, non parafrasata. In sede d'esame la domanda è costruita sulle parole esatte del legislatore: una parafrasi elegante ti fa perdere proprio la parola su cui si gioca il quesito.</li>
        <li><strong>Perché conta.</strong> La ragione della norma in due righe. Serve a due cose: rende il testo memorabile, e permette di rispondere anche quando la domanda è formulata in modo che non hai mai visto.</li>
        <li><strong>Collegamenti.</strong> I rimandi ad altri articoli e ad altre leggi. Le norme non vivono da sole e i quesiti più insidiosi nascono proprio sui confini fra una norma e l'altra.</li>
        <li><strong>Termini chiave.</strong> Le tre o quattro parole che la commissione si aspetta di sentire. Sono anche le parole che riattivano tutto il resto della scheda quando le rileggi al ripasso.</li>
      </ul>

      <h2>La seconda idea: il metodo Feynman</h2>
      <p>Richard Feynman era un fisico, premio Nobel, ed era famoso soprattutto per una cosa: sapeva spiegare argomenti difficilissimi a chi non ne sapeva nulla. Il metodo che porta il suo nome nasce da un'osservazione tanto banale quanto scomoda — <strong>puoi credere di aver capito una cosa fino al momento esatto in cui provi a spiegarla a qualcun altro.</strong> Lì scopri la verità.</p>
      <p>Si applica in quattro passaggi:</p>
      <ol>
        <li><strong>Scegli un concetto e scrivilo in cima a un foglio.</strong> Uno solo. «Subordinazione», per esempio.</li>
        <li><strong>Spiegalo per iscritto come lo spiegheresti a tuo cugino che fa il liceo.</strong> Niente gergo, niente formule imparate a memoria, niente «in quanto tale».</li>
        <li><strong>Segna il punto in cui ti blocchi.</strong> Se ti accorgi di star ricopiando le parole del manuale invece di usare le tue, quello è il punto in cui non hai capito. Non è un fallimento: è l'informazione che stavi cercando.</li>
        <li><strong>Torna alla fonte, chiarisci quel punto e riscrivi.</strong> Poi ripeti finché la spiegazione fila senza inciampi.</li>
      </ol>
      <p>Il metodo è potente perché è impietoso. Rileggere dà l'impressione di sapere, perché il testo ti risulta familiare. Spiegare non lascia scampo: o la frase esce, o non esce.</p>

      <h3>Come si vede dentro un manuale Normaria</h3>
      <p>Il blocco <strong>«Perché conta»</strong> è il metodo Feynman fatto per te, in due righe. Non è un riassunto del testo: è la risposta alla domanda «e allora?». Prendiamo l'articolo di prima. Il testo dice che è lavoratore subordinato chi collabora nell'impresa «alle dipendenze e sotto la direzione» dell'imprenditore. Detto così è una definizione. Detto alla Feynman diventa:</p>
      <p class="nota">Se qualcun altro decide <em>come</em>, <em>quando</em> e <em>dove</em> fai il lavoro, sei un dipendente. Se lo decidi tu e consegni solo il risultato, sei un autonomo. Tutto il resto del diritto del lavoro — ferie, licenziamento, contributi, tutele — si appoggia su questa singola distinzione.</p>
      <p>Nove parole di norma diventano una domanda che puoi porti davanti a qualsiasi caso concreto. Ed è esattamente quello che ti chiederà il quesito: non di ripetere la definizione, ma di applicarla a un rider, a un consulente, a un collaboratore.</p>

      <h2>Perché i due metodi si tengono insieme</h2>
      <p>Da soli sono zoppi. La scheda a quattro blocchi dà l'<strong>ordine</strong>: sai sempre dove guardare, e puoi ripassare quattrocento norme in una settimana perché sono tutte fatte allo stesso modo. Ma l'ordine da solo produce schedari, non comprensione.</p>
      <p>Il metodo Feynman dà la <strong>comprensione</strong>: ti costringe a possedere il concetto invece di riconoscerlo. Ma da solo non scala: non puoi rifare l'esercizio su quattrocento norme in tre mesi partendo da zero ogni volta.</p>
      <p>Messi insieme, uno risolve il limite dell'altro. La scheda ti dà la struttura ripetibile; il blocco «perché conta» ci mette dentro il lavoro di comprensione già fatto, così tu puoi verificarlo invece di doverlo costruire. E quando arrivi al ripasso, i termini chiave ti riaccendono l'intera scheda in pochi secondi.</p>

      <h2>Cosa il metodo non è</h2>
      <ul>
        <li><strong>Non è un riassunto.</strong> Un riassunto toglie parole al testo. Qui il testo resta intero: si aggiunge il contesto che serve a fissarlo.</li>
        <li><strong>Non è un eserciziario.</strong> I quesiti servono a verificare, non a imparare. Chi comincia dai quiz impara le risposte, non le norme — e all'esame le domande sono altre.</li>
        <li><strong>Non sostituisce il codice.</strong> Lo rende utilizzabile. Il codice resta la fonte; la scheda è il modo per attraversarlo senza perdersi.</li>
      </ul>

      <div class="rimandi">
        <h2>Vedere il metodo all'opera</h2>
        <p>Ogni manuale del catalogo applica esattamente questa struttura, materia per materia e concorso per concorso.</p>
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
        descrizione="La scheda a quattro blocchi e il metodo Feynman spiegati con un "
                    "esempio svolto: perché una forma sempre uguale e una spiegazione "
                    "con parole tue battono mille pagine di manuale.",
        canonico=f"{comune.SITO}/metodo.html",
        attiva="metodo", corpo=corpo, tipo="article"), encoding="utf-8")

    for nome, attiva in PAGINE.items():
        f = RADICE / nome
        t = f.read_text(encoding="utf-8")
        t = comune.sostituisci(t, "HEADER", comune.testa(attiva))
        t = comune.sostituisci(t, "FOOTER", comune.piede())
        f.write_text(t, encoding="utf-8")

    print(f"Fatto: metodo.html + intestazione e piede in {len(PAGINE)} pagine")


if __name__ == "__main__":
    main()

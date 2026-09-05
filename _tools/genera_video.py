#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Costruisce la sezione video del sito, a partire da video.json.

Come funziona il riquadro di un video, e perché è fatto così:
  sul sito non compare nessun pezzo di YouTube finché il visitatore non
  clicca. Prima del clic c'è solo una scheda disegnata da noi, con i nostri
  colori; al clic quella scheda viene sostituita dal riproduttore. Così la
  pagina resta leggera, si apre in fretta anche da cellulare, e nessun dato
  del visitatore parte verso terzi senza che lui l'abbia scelto.

Cosa scrive:
  video.html                 la pagina con tutti i video
  la striscia in home page   fra i segnalibri VIDEO:INIZIO / VIDEO:FINE

Uso:  python3 _tools/genera_video.py
"""

import html
import json
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import comune  # noqa: E402


def scheda(v, su=""):
    """Una scheda video: prima del clic è solo grafica nostra."""
    etichetta = html.escape(f"Riproduci il video: {v['titolo']}")
    return f"""        <article class="video" data-video="{html.escape(v['id'], quote=True)}">
          <button type="button" class="video-avvia" aria-label="{etichetta}">
            <span class="video-alto">
              <span class="video-occhiello">{html.escape(v['occhiello'])}</span>
              <span class="video-titolo">{html.escape(v['titolo'])}</span>
            </span>
            <span class="video-play" aria-hidden="true">
              <svg viewBox="0 0 64 64" width="54" height="54" focusable="false">
                <circle cx="32" cy="32" r="30" fill="none" stroke="currentColor" stroke-width="1.5"/>
                <path d="M26 20 L46 32 L26 44 Z" fill="currentColor"/>
              </svg>
            </span>
            <span class="video-basso">{html.escape(v['sommario'])}</span>
          </button>
        </article>"""


def griglia(video, su="", classe="video-griglia"):
    return f'      <div class="{classe}">\n' + "\n".join(scheda(v, su) for v in video) + "\n      </div>"


# Lo script che sostituisce la scheda col riproduttore, solo al clic.
SCRIPT = """
  <script>
    // Finché nessuno clicca, di YouTube sul sito non c'è nulla.
    document.querySelectorAll('.video').forEach(function (riquadro) {
      var bottone = riquadro.querySelector('.video-avvia');
      if (!bottone) return;
      bottone.addEventListener('click', function () {
        var id = riquadro.getAttribute('data-video');
        var telaio = document.createElement('iframe');
        telaio.src = 'https://www.youtube-nocookie.com/embed/' + id +
                     '?autoplay=1&rel=0&modestbranding=1';
        telaio.title = bottone.getAttribute('aria-label') || 'video';
        telaio.loading = 'lazy';
        telaio.allow = 'accelerometer; autoplay; encrypted-media; picture-in-picture';
        telaio.setAttribute('allowfullscreen', '');
        telaio.className = 'video-telaio';
        riquadro.replaceChildren(telaio);
      });
    });
  </script>"""


def striscia_home(video, canale):
    """La striscia di tre video in home page."""
    return f"""  <section id="video" class="sezione-video">
    <div class="wrap">
      <div class="video-intro">
        <div>
          <p class="eyebrow">Il metodo in venti secondi</p>
          <h2>Una norma alla volta, spiegata a voce.</h2>
          <p class="lead-piccolo">Gli stessi quattro blocchi dei manuali, in formato breve:
             il testo, perché conta, dove si incastra. Il video parte solo se lo avvii tu.</p>
        </div>
        <p class="video-tutti"><a href="video.html">Vedi tutti i video</a></p>
      </div>
{griglia(video)}
    </div>
  </section>"""


def pagina_video(video, canale):
    corpo = f"""  <main id="contenuto">
  <section class="hero hero-stretto">
    <div class="wrap">
      <div>
        <p class="eyebrow">Video</p>
        <h1>Il metodo, in venti secondi.</h1>
        <p class="lead">Ogni video prende una singola norma o una singola regola di concorso
           e la porta a casa: cosa dice, perché esiste, dove ti aspetta all'esame.
           Sono gli stessi quattro blocchi delle schede dei manuali, detti a voce.</p>
      </div>
    </div>
  </section>

  <section class="sezione-video sezione-video-piena">
    <div class="wrap">
{griglia(video)}
      <p class="video-canale">Tutti i video escono prima sul canale
         <a href="{html.escape(canale, quote=True)}" target="_blank" rel="noopener">YouTube di Normaria Edizioni</a>.</p>
    </div>
  </section>
  </main>"""

    return comune.pagina(
        titolo="Video — Normaria Edizioni",
        descrizione="Norme e regole di concorso spiegate in venti secondi, con i quattro "
                    "blocchi del metodo Normaria: il testo, perché conta, i collegamenti, "
                    "i termini chiave.",
        canonico=f"{comune.SITO}/video.html",
        attiva="video", corpo=corpo)


def main():
    dati = json.loads((RADICE / "video.json").read_text(encoding="utf-8"))
    video, canale = dati["video"], dati["canale"]

    (RADICE / "video.html").write_text(pagina_video(video, canale), encoding="utf-8")

    home = RADICE / "index.html"
    t = home.read_text(encoding="utf-8")
    t = comune.sostituisci(t, "VIDEO",
                           striscia_home([v for v in video if v.get("inHome")], canale))
    home.write_text(t, encoding="utf-8")

    print(f"Fatto: video.html con {len(video)} video, striscia in home con "
          f"{sum(1 for v in video if v.get('inHome'))}")


if __name__ == "__main__":
    main()

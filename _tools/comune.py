# -*- coding: utf-8 -*-
"""
Le parti uguali su tutte le pagine del sito: intestazione, menu e piede.

Stanno qui una volta sola, così un cambiamento al menu si riflette
ovunque senza doverlo riscrivere pagina per pagina.
"""

import html
from datetime import date

SITO = "https://normaria.net"

# le voci del menu, in ordine. La chiave serve a evidenziare la pagina attiva.
VOCI = [
    ("metodo",   "Il metodo",         "metodo.html"),
    ("catalogo", "Catalogo",          "index.html#catalogo"),
    ("articoli", "Articoli",          "articoli.html"),
    ("estratto", "Estratto gratuito", "index.html#estratto"),
]

FONT = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;600;700'
    '&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600'
    '&display=swap" rel="stylesheet">'
)


def menu(attiva, su=""):
    voci = []
    for chiave, testo, href in VOCI:
        classe = ' class="attiva"' if chiave == attiva else ""
        voci.append(f'          <a href="{su}{href}"{classe}>{testo}</a>')
    return "\n".join(voci)


# indirizzo del modulo Brevo (lista "Estratto gratuito")
MODULO = ("https://7afa150f.sibforms.com/serve/MUIFAHGS7Q22mxHcMhBnefBc_lxVtG-KWymnZ3qHRgGF"
          "Sqrb_IDItqDXUhF3xop4CYa9eYUxTJO0u9YIu_xRLFPcaR2IDti2WsVdOMSOlKAlT50J0PnkDCa3I6eEmhJ"
          "fBuyVt1vUTr_Mc-qdHqGu-cgLGZsaVdPWHoujCMlyOINI-LgEJcu0CdoF5Vr4_cUEdpmVC323v6HRfTfTdw")


def modulo(su="", id_form="modulo-estratto"):
    """Il modulo di iscrizione.

    L'invio va a Brevo dentro un riquadro nascosto (l'iframe qui sotto), così
    il visitatore resta sul sito: è il modo che Brevo accetta davvero.
    """
    return f"""      <form class="signup" id="{id_form}" method="POST" action="{MODULO}"
            target="brevo-{id_form}" accept-charset="utf-8">
        <div class="signup-riga">
          <input type="email" name="EMAIL" required autocomplete="email"
                 placeholder="La tua email" aria-label="Il tuo indirizzo email">
          <button type="submit" class="btn btn-light">Ricevi l'estratto</button>
        </div>
        <!-- campo trappola per i robot: resta vuoto -->
        <input type="text" name="email_address_check" value="" tabindex="-1"
               autocomplete="off" aria-hidden="true" class="trappola">
        <input type="hidden" name="locale" value="it">
        <input type="hidden" name="html_type" value="simple">
        <label class="consenso">
          <input type="checkbox" required name="consenso">
          <span>Acconsento a ricevere l'estratto e a essere informato sui nuovi manuali.
          Ho letto l'<a href="{su}privacy.html">informativa sulla privacy</a> e so che
          posso disiscrivermi in qualsiasi momento.</span>
        </label>
        <p class="esito" role="status" hidden></p>
      </form>
      <iframe name="brevo-{id_form}" class="trappola" title="invio del modulo" aria-hidden="true"></iframe>"""


SCRIPT_MODULO = """
  <script>
    // l'invio finisce nel riquadro nascosto: mostriamo qui il messaggio
    document.querySelectorAll('form.signup').forEach(function (f) {
      var inviato = false;
      var telaio = document.getElementsByName(f.target)[0];
      f.addEventListener('submit', function () {
        inviato = true;
        f.querySelector('button[type=submit]').disabled = true;
      });
      if (telaio) {
        telaio.addEventListener('load', function () {
          if (!inviato) return;
          var esito = f.querySelector('.esito');
          f.querySelector('.signup-riga').hidden = true;
          f.querySelector('.consenso').hidden = true;
          esito.className = 'esito riuscito';
          esito.textContent = 'Fatto. Ti abbiamo mandato una email con il link per scaricare l\u2019estratto: controlla la posta, e anche la cartella spam se non la vedi.';
          esito.hidden = false;
        });
      }
    });
  </script>"""


def testa(attiva, su=""):
    """Intestazione + menu. `su` è '../' per le pagine dentro una cartella."""
    return f"""  <a class="salta" href="#contenuto">Vai al contenuto</a>
  <header class="site-header">
    <div class="wrap">
      <a href="{su}index.html" class="brand">Normaria<small>Edizioni</small></a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="menu"
              aria-label="Apri il menu"><span></span><span></span><span></span></button>
      <nav class="nav" id="menu">
{menu(attiva, su)}
      </nav>
    </div>
  </header>"""


def piede(su=""):
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <p class="brand-f">Normaria Edizioni</p>
          <p>Manuali normativi per chi prepara i concorsi pubblici. Un metodo, molte materie.</p>
        </div>
        <div>
          <h4>Naviga</h4>
          <ul>
            <li><a href="{su}metodo.html">Il metodo</a></li>
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

  <script>
    // apre e chiude il menu sul telefono
    (function () {{
      var b = document.querySelector('.nav-toggle');
      var m = document.getElementById('menu');
      if (!b || !m) return;
      b.addEventListener('click', function () {{
        var aperto = m.classList.toggle('aperto');
        b.setAttribute('aria-expanded', aperto);
        b.setAttribute('aria-label', aperto ? 'Chiudi il menu' : 'Apri il menu');
      }});
      m.addEventListener('click', function (e) {{
        if (e.target.tagName === 'A') {{ m.classList.remove('aperto');
          b.setAttribute('aria-expanded', 'false'); }}
      }});
    }})();
  </script>""" + SCRIPT_MODULO


def pagina(titolo, descrizione, canonico, attiva, corpo, su="", extra="", tipo="website"):
    """Una pagina completa del sito."""
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(descrizione)}">
  <link rel="canonical" href="{canonico}">

  <meta property="og:type" content="{tipo}">
  <meta property="og:title" content="{html.escape(titolo)}">
  <meta property="og:description" content="{html.escape(descrizione)}">
  <meta property="og:url" content="{canonico}">
  <meta property="og:locale" content="it_IT">

  {FONT}
  <link rel="stylesheet" href="{su}style.css">
{extra}</head>
<body>

{testa(attiva, su)}

{corpo}

{piede(su)}
</body>
</html>
"""


def sostituisci(testo, nome, contenuto):
    """Riscrive la parte fra i segnalibri <!-- NOME:INIZIO --> e <!-- NOME:FINE -->."""
    import re
    import sys
    inizio, fine = f"<!-- {nome}:INIZIO -->", f"<!-- {nome}:FINE -->"
    schema = re.compile(re.escape(inizio) + r".*?" + re.escape(fine), re.S)
    if not schema.search(testo):
        sys.exit(f"ERRORE: segnalibri {nome} non trovati")
    return schema.sub(f"{inizio}\n{contenuto}\n{fine}", testo, count=1)

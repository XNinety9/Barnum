"""Mise en forme : texte pour le terminal, dictionnaire pour JSON."""
import datetime as dt
import textwrap

from .lecture import MOIS, Horoscope
from .zodiaque import ASTRES, SIGNES

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
LARGEUR, MARGE = 72, 10
RETRO = "℞"
NBSP = "\u00a0"  # empêche textwrap de couper une position en deux


def date_fr(d: dt.date) -> str:
    return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]} {d.year}"


def bloc(titre: str, texte: str, entete: str = "") -> list:
    corps = textwrap.wrap(texte, LARGEUR - MARGE)
    return [f"{titre:<{MARGE}}{entete}".rstrip()] + [" " * MARGE + l for l in corps]


def etoiles(note: int) -> str:
    return "★" * note + "☆" * (5 - note)


def ciel_texte(ciel: dict) -> str:
    return f"{NBSP}· ".join(
        f"{ASTRES[a].symbole}{NBSP}{SIGNES[p.signe].nom}{NBSP}{int(p.degre)}°"
        + (f"{NBSP}{RETRO}" if p.retrograde else "")
        for a, p in ciel.items())


def texte(h: Horoscope, avec_ciel: bool = False) -> str:
    lune = SIGNES[h.ciel["Lune"].signe].nom
    out = [f"{h.signe.symbole}  {h.signe.nom.upper()} · {date_fr(h.date)}",
           f"{h.phase.emoji}  {h.phase.nom.capitalize()} en {lune}", ""]
    if avec_ciel:
        out += bloc("Ciel", ciel_texte(h.ciel))
    out += bloc("Climat", h.climat)
    for d in h.domaines:
        out += bloc(d.libelle, d.texte, etoiles(d.note))
    out += bloc("Conseil", h.conseil)
    out += ["", f"Couleur : {h.couleur} · Chiffre : {h.chiffre} · Humeur : {h.humeur}"]
    return "\n".join(out)


def dictionnaire(h: Horoscope) -> dict:
    return {
        "signe": h.signe.nom,
        "date": h.date.isoformat(),
        "lune": {"phase": h.phase.nom, "signe": SIGNES[h.ciel["Lune"].signe].nom},
        "ciel": [{"astre": a, "signe": SIGNES[p.signe].nom,
                  "degre": round(p.degre, 2), "retrograde": p.retrograde}
                 for a, p in h.ciel.items()],
        "transit": h.transit and {"astre": h.transit.astre, "aspect": h.transit.aspect},
        "climat": h.climat,
        "domaines": [{"cle": d.cle, "note": d.note, "texte": d.texte,
                      "influence": d.influence} for d in h.domaines],
        "conseil": h.conseil,
        "couleur": h.couleur,
        "chiffre": h.chiffre,
        "humeur": h.humeur,
    }

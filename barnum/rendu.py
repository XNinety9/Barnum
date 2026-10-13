"""Mise en forme : texte pour le terminal, dictionnaire pour JSON."""
import textwrap

from .redaction import Horoscope
from .zodiaque import ASTRES

LARGEUR, MARGE = 72, 10
RETRO = "℞"
NBSP = " "  # empêche textwrap de couper une position en deux


def bloc(titre: str, texte: str, entete: str = "") -> list:
    corps = textwrap.wrap(texte, LARGEUR - MARGE)
    return [f"{titre:<{MARGE}}{entete}".rstrip()] + [" " * MARGE + l for l in corps]


def etoiles(note: int) -> str:
    return "★" * note + "☆" * (5 - note)


def ciel_texte(h: Horoscope) -> str:
    return f"{NBSP}· ".join(
        f"{ASTRES[a].symbole}{NBSP}{h.langue.signes[p.signe]}{NBSP}{int(p.degre)}°"
        + (f"{NBSP}{RETRO}" if p.retrograde else "")
        for a, p in h.ciel.items())


def texte(h: Horoscope, avec_ciel: bool = False) -> str:
    lg, et = h.langue, h.langue.etiquettes
    lune = lg.signes[h.ciel["Lune"].signe]
    phase = lg.phases[h.phase.nom][0]
    out = [f"{h.signe.symbole}  {lg.signes[h.signe.index].upper()} · {lg.date_longue(h.date)}",
           f"{h.phase.emoji}  {phase.capitalize()}{lg.dans(lune)}", ""]
    if avec_ciel:
        out += bloc(et["ciel"], ciel_texte(h))
    out += bloc(et["climat"], h.climat)
    for d in h.domaines:
        out += bloc(d.libelle, d.texte, etoiles(d.note))
    out += bloc(et["conseil"], h.conseil)
    out += ["", et["pied"].format(couleur=h.couleur, chiffre=h.chiffre, humeur=h.humeur)]
    return "\n".join(out)


def dictionnaire(h: Horoscope) -> dict:
    """Clés stables (françaises) ; valeurs dans la langue de l'horoscope,
    sauf les identifiants (signe_id, astre_id) qui ne changent jamais."""
    lg = h.langue
    nom_astre = lambda a: a and lg.astres[a][0]  # noqa: E731
    return {
        "langue": lg.code,
        "signe": lg.signes[h.signe.index],
        "signe_id": h.signe.index,
        "date": h.date.isoformat(),
        "lune": {"phase": lg.phases[h.phase.nom][0],
                 "signe": lg.signes[h.ciel["Lune"].signe]},
        "ciel": [{"astre": nom_astre(a), "astre_id": a, "signe": lg.signes[p.signe],
                  "degre": round(p.degre, 2), "retrograde": p.retrograde}
                 for a, p in h.ciel.items()],
        "transit": h.transit and {"astre": nom_astre(h.transit.astre),
                                  "aspect": h.transit.aspect},
        "climat": h.climat,
        "domaines": [{"cle": d.cle, "libelle": d.libelle, "note": d.note, "texte": d.texte,
                      "influence": nom_astre(d.influence)} for d in h.domaines],
        "conseil": h.conseil,
        "couleur": h.couleur,
        "chiffre": h.chiffre,
        "humeur": h.humeur,
    }

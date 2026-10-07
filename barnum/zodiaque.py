"""Vocabulaire du zodiaque : signes, astres, phases de lune."""
import datetime as dt
import unicodedata
from typing import NamedTuple


class Signe(NamedTuple):
    index: int  # 0 = Bélier, ordre zodiacal
    nom: str
    symbole: str
    element: str
    maitre: str  # clé de ASTRES
    debut: tuple  # (mois, jour) d'entrée du Soleil, dates usuelles


SIGNES = [Signe(i, *s) for i, s in enumerate([
    ("Bélier", "♈", "feu", "Mars", (3, 21)),
    ("Taureau", "♉", "terre", "Vénus", (4, 20)),
    ("Gémeaux", "♊", "air", "Mercure", (5, 21)),
    ("Cancer", "♋", "eau", "Lune", (6, 21)),
    ("Lion", "♌", "feu", "Soleil", (7, 23)),
    ("Vierge", "♍", "terre", "Mercure", (8, 23)),
    ("Balance", "♎", "air", "Vénus", (9, 23)),
    ("Scorpion", "♏", "eau", "Pluton", (10, 23)),
    ("Sagittaire", "♐", "feu", "Jupiter", (11, 22)),
    ("Capricorne", "♑", "terre", "Saturne", (12, 22)),
    ("Verseau", "♒", "air", "Uranus", (1, 20)),
    ("Poissons", "♓", "eau", "Neptune", (2, 19)),
])]


class Astre(NamedTuple):
    nom: str
    symbole: str
    sujet: str  # forme avec article, sujet d'une phrase
    nature: float  # > 0 bénéfique, < 0 maléfique (astrologie traditionnelle)


ASTRES = {a.nom: a for a in [
    Astre("Soleil", "☉", "le Soleil", 0.5),
    Astre("Lune", "☽", "la Lune", 0.5),
    Astre("Mercure", "☿", "Mercure", 0.5),
    Astre("Vénus", "♀", "Vénus", 1.0),
    Astre("Mars", "♂", "Mars", -0.5),
    Astre("Jupiter", "♃", "Jupiter", 1.0),
    Astre("Saturne", "♄", "Saturne", -1.0),
    Astre("Uranus", "♅", "Uranus", -0.5),
    Astre("Neptune", "♆", "Neptune", 0.0),
    Astre("Pluton", "♇", "Pluton", -0.5),
]}


class Phase(NamedTuple):
    nom: str
    sujet: str
    groupe: str  # clé des effets de phase
    emoji: str
    debut: float  # élongation Lune - Soleil (degrés) à partir de laquelle elle commence


# Les phases principales ne durent qu'une journée de part et d'autre de l'instant exact.
PHASES = [
    Phase("nouvelle lune", "la nouvelle lune", "nouvelle", "🌑", -12),
    Phase("premier croissant", "le premier croissant de lune", "croissante", "🌒", 12),
    Phase("premier quartier", "le premier quartier de lune", "croissante", "🌓", 78),
    Phase("lune gibbeuse croissante", "la lune gibbeuse croissante", "croissante", "🌔", 102),
    Phase("pleine lune", "la pleine lune", "pleine", "🌕", 168),
    Phase("lune gibbeuse décroissante", "la lune gibbeuse décroissante", "decroissante", "🌖", 192),
    Phase("dernier quartier", "le dernier quartier de lune", "decroissante", "🌗", 258),
    Phase("dernier croissant", "le dernier croissant de lune", "decroissante", "🌘", 282),
]


def phase_de(elongation: float) -> Phase:
    e = elongation % 360
    if e >= 348:
        e -= 360
    return [p for p in PHASES if p.debut <= e][-1]


def signe_de_naissance(d: dt.date) -> Signe:
    md = (d.month, d.day)
    passes = [s for s in SIGNES if s.debut <= md]
    return max(passes, key=lambda s: s.debut) if passes else SIGNES[9]  # Capricorne


def normaliser(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", txt.strip().lower())
                   if unicodedata.category(c) != "Mn")


def trouver_signe(nom: str) -> Signe:
    for s in SIGNES:
        if normaliser(s.nom) == normaliser(nom):
            return s
    noms = ", ".join(s.nom for s in SIGNES)
    raise ValueError(f"signe inconnu : {nom!r} (attendu : {noms})")

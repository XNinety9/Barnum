"""Le zodiaque, indépendamment de la langue : signes, astres, phases de lune.

Les noms français servent d'identifiants internes ; les libellés affichés
viennent de barnum.langues."""
import datetime as dt
import unicodedata
from typing import NamedTuple

from .langues import LANGUES


class Signe(NamedTuple):
    index: int  # 0 = Bélier, ordre zodiacal
    nom: str  # identifiant (français)
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
    nature: float  # > 0 bénéfique, < 0 maléfique (astrologie traditionnelle)


ASTRES = {a.nom: a for a in [
    Astre("Soleil", "☉", 0.5),
    Astre("Lune", "☽", 0.5),
    Astre("Mercure", "☿", 0.5),
    Astre("Vénus", "♀", 1.0),
    Astre("Mars", "♂", -0.5),
    Astre("Jupiter", "♃", 1.0),
    Astre("Saturne", "♄", -1.0),
    Astre("Uranus", "♅", -0.5),
    Astre("Neptune", "♆", 0.0),
    Astre("Pluton", "♇", -0.5),
]}


class Phase(NamedTuple):
    nom: str  # identifiant (français)
    groupe: str  # clé des effets de phase
    emoji: str
    debut: float  # élongation Lune - Soleil (degrés) à partir de laquelle elle commence


# Les phases principales ne durent qu'une journée de part et d'autre de l'instant exact.
PHASES = [
    Phase("nouvelle lune", "nouvelle", "🌑", -12),
    Phase("premier croissant", "croissante", "🌒", 12),
    Phase("premier quartier", "croissante", "🌓", 78),
    Phase("lune gibbeuse croissante", "croissante", "🌔", 102),
    Phase("pleine lune", "pleine", "🌕", 168),
    Phase("lune gibbeuse décroissante", "decroissante", "🌖", 192),
    Phase("dernier quartier", "decroissante", "🌗", 258),
    Phase("dernier croissant", "decroissante", "🌘", 282),
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
    """Accepte le nom du signe dans n'importe quelle langue disponible."""
    for lg in LANGUES.values():
        for i, libelle in enumerate(lg.signes):
            if normaliser(libelle) == normaliser(nom):
                return SIGNES[i]
    noms = ", ".join(s.nom for s in SIGNES)
    raise ValueError(f"signe inconnu : {nom!r} (attendu : {noms})")

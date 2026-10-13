"""Interprétation : du ciel réel du jour à la lecture d'un signe.

Méthode des horoscopes de presse (« signes solaires ») : chaque astre forme un
aspect avec le signe selon le nombre de signes qui les séparent. Ces aspects,
pondérés par les astres qui gouvernent chaque domaine, donnent les notes.

La lecture ne contient aucun texte : elle est identique quelle que soit la
langue de rédaction (voir redaction.py). Son seul aléa (choix du transit mis en
avant, léger bruit sur les notes, chiffre, couleur, humeur) vient d'une graine
déterministe.
"""
import datetime as dt
import hashlib
import random
from dataclasses import dataclass

from . import astro
from .langues import N_COULEURS, N_HUMEURS
from .zodiaque import ASTRES, SIGNES, Phase, Signe, phase_de

# Aspect par nombre de signes d'écart (aspects « par signe entier »)
ASPECTS = {0: "conjonction", 2: "sextile", 10: "sextile", 3: "carré", 9: "carré",
           4: "trigone", 8: "trigone", 6: "opposition"}
VALENCES = {"sextile": 0.5, "trigone": 1.0, "carré": -1.0, "opposition": -0.75}

# Astres gouvernant chaque domaine, avec leur poids
DOMAINES = {
    "amour": {"Vénus": 1.0, "Lune": 0.6, "Mars": 0.4, "Neptune": 0.2},
    "travail": {"Mercure": 0.6, "Mars": 0.6, "Saturne": 0.5, "Soleil": 0.5, "Jupiter": 0.3},
    "argent": {"Jupiter": 0.8, "Vénus": 0.6, "Saturne": 0.4, "Mercure": 0.3},
    "forme": {"Soleil": 0.6, "Mars": 0.6, "Lune": 0.6, "Saturne": 0.3, "Neptune": 0.2},
}
PENALITE_RETRO = 0.4
BRUIT = 0.75  # amplitude du hasard ajouté aux notes
SEUIL_INFLUENCE = 0.5

# Probabilité relative qu'un astre soit retenu comme transit du jour :
# les astres rapides changent souvent, ce sont eux qui font « l'actualité ».
SAILLANCE = {"Lune": 1.0, "Mercure": 0.9, "Vénus": 0.9, "Soleil": 0.8, "Mars": 0.8,
             "Jupiter": 0.6, "Saturne": 0.6, "Uranus": 0.4, "Neptune": 0.4, "Pluton": 0.4}
BONUS_MAITRE = 0.6
RETRO_SIGNALES = ("Mercure", "Vénus", "Mars")


@dataclass(frozen=True)
class Transit:
    astre: str
    position: astro.Position
    aspect: str | None
    valence: float  # > 0 harmonieux, < 0 tendu


@dataclass(frozen=True)
class Note:
    cle: str
    note: int  # 1 à 5
    influence: str | None  # astre déterminant, nommé seulement s'il va dans le sens de la note


@dataclass(frozen=True)
class Lecture:
    signe: Signe
    date: dt.date
    ciel: dict
    phase: Phase
    transit: Transit | None
    retro: str | None  # planète personnelle rétrograde à signaler
    fin_retro: dt.date | None
    n_element: int  # astres situés dans l'élément du signe
    notes: list
    chiffre: int
    couleur: int  # index dans Langue.couleurs
    humeur: int  # index dans Langue.humeurs


def graine(signe: Signe, date: dt.date, sel: str, flux: str) -> random.Random:
    h = hashlib.sha256(f"{date.isoformat()}|{signe.nom}|{sel}|{flux}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def transits(ciel: dict, signe: Signe) -> list:
    out = []
    for nom, pos in ciel.items():
        aspect = ASPECTS.get((pos.signe - signe.index) % 12)
        if aspect == "conjonction":
            valence = ASTRES[nom].nature
        else:
            valence = VALENCES.get(aspect, 0.0)
        out.append(Transit(nom, pos, aspect, valence))
    return out


def contributions(trs: list, poids: dict) -> dict:
    out = {}
    for t in trs:
        if t.astre in poids:
            c = poids[t.astre] * t.valence
            if t.position.retrograde:
                c -= PENALITE_RETRO * poids[t.astre]
            out[t.astre] = c
    return out


def _note(rng: random.Random, trs: list, cle: str, poids: dict) -> Note:
    contrib = contributions(trs, poids)
    note = max(1, min(5, round(3 + sum(contrib.values()) + rng.uniform(-BRUIT, BRUIT))))
    meneur = max(contrib, key=lambda a: abs(contrib[a]), default=None)
    influence = None
    if (meneur and abs(contrib[meneur]) >= SEUIL_INFLUENCE
            and (contrib[meneur] > 0) == (note >= 3)):
        influence = meneur
    return Note(cle, note, influence)


def lire(signe: Signe, date: dt.date, sel: str = "") -> Lecture:
    rng = graine(signe, date, sel, "lecture")
    ciel = astro.ciel(date)
    trs = transits(ciel, signe)

    candidats = [t for t in trs if t.aspect]
    transit = None
    if candidats:
        poids = [SAILLANCE[t.astre] + (BONUS_MAITRE if t.astre == signe.maitre else 0)
                 for t in candidats]
        transit = rng.choices(candidats, weights=poids)[0]

    retro = next((a for a in RETRO_SIGNALES if ciel[a].retrograde), None)
    return Lecture(
        signe=signe, date=date, ciel=ciel,
        phase=phase_de(astro.elongation(date)),
        transit=transit,
        retro=retro,
        fin_retro=astro.fin_retrograde(retro, date) if retro else None,
        n_element=sum(1 for p in ciel.values() if SIGNES[p.signe].element == signe.element),
        notes=[_note(rng, trs, cle, poids) for cle, poids in DOMAINES.items()],
        chiffre=rng.randint(1, 49),
        couleur=rng.randrange(N_COULEURS),
        humeur=rng.randrange(N_HUMEURS),
    )

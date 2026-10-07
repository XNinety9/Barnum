"""Interprétation : du ciel réel du jour à l'horoscope d'un signe.

Méthode des horoscopes de presse (« signes solaires ») : chaque astre forme un
aspect avec le signe selon le nombre de signes qui les séparent. Ces aspects,
pondérés par les astres qui gouvernent chaque domaine, donnent les notes ; le
texte est ensuite choisi pour être cohérent avec les notes et le transit
principal. Seul le choix des formules (et un léger bruit sur les notes) est
aléatoire, avec une graine déterministe.
"""
import datetime as dt
import hashlib
import random
from dataclasses import dataclass

from . import astro
from .grammaire import Grammaire
from .textes import BASE, CONSEILS_RETRO, EFFETS, ELEMENTS, NOMBRES, PHASE_EFFETS
from .zodiaque import ASTRES, SIGNES, Phase, Signe, phase_de

# Aspect par nombre de signes d'écart (aspects « par signe entier »)
ASPECTS = {0: "conjonction", 2: "sextile", 10: "sextile", 3: "carré", 9: "carré",
           4: "trigone", 8: "trigone", 6: "opposition"}
VALENCES = {"sextile": 0.5, "trigone": 1.0, "carré": -1.0, "opposition": -0.75}

# Astres gouvernant chaque domaine, avec leur poids
DOMAINES = [  # clé, libellé, gabarit (%s = haut/bas), poids
    ("amour", "Amour", "En couple, {couple_%s} Célibataire, {celib_%s}",
     {"Vénus": 1.0, "Lune": 0.6, "Mars": 0.4, "Neptune": 0.2}),
    ("travail", "Travail", "{travail_%s} {travail_conseil}",
     {"Mercure": 0.6, "Mars": 0.6, "Saturne": 0.5, "Soleil": 0.5, "Jupiter": 0.3}),
    ("argent", "Argent", "{argent_%s}",
     {"Jupiter": 0.8, "Vénus": 0.6, "Saturne": 0.4, "Mercure": 0.3}),
    ("forme", "Forme", "{forme_%s}",
     {"Soleil": 0.6, "Mars": 0.6, "Lune": 0.6, "Saturne": 0.3, "Neptune": 0.2}),
]
PENALITE_RETRO = 0.4
BRUIT = 0.75  # amplitude du hasard ajouté aux notes
SEUIL_INFLUENCE = 0.5

# Probabilité relative qu'un astre soit retenu comme transit du jour :
# les astres rapides changent souvent, ce sont eux qui font « l'actualité ».
SAILLANCE = {"Lune": 1.0, "Mercure": 0.9, "Vénus": 0.9, "Soleil": 0.8, "Mars": 0.8,
             "Jupiter": 0.6, "Saturne": 0.6, "Uranus": 0.4, "Neptune": 0.4, "Pluton": 0.4}
BONUS_MAITRE = 0.6
RETRO_SIGNALES = ("Mercure", "Vénus", "Mars")

ARTICLES = {"Gémeaux": "les ", "Poissons": "les ", "Vierge": "la ", "Balance": "la "}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]

# Symboles fournis à la volée par ce module (en plus de textes.BASE)
DYNAMIQUES = {"trait", "element_de", "phase", "phase_effet", "lune_ou", "n_element",
              "t_astre", "t_signe", "t_ou", "t_aspect", "t_effet",
              "r_astre", "r_fin", "r_conseil", "infl"}


@dataclass(frozen=True)
class Transit:
    astre: str
    position: astro.Position
    aspect: str | None
    valence: float  # > 0 harmonieux, < 0 tendu


@dataclass(frozen=True)
class Domaine:
    cle: str
    libelle: str
    note: int  # 1 à 5
    texte: str
    influence: str | None  # astre le plus déterminant, s'il pèse assez


@dataclass(frozen=True)
class Horoscope:
    signe: Signe
    date: dt.date
    ciel: dict
    phase: Phase
    transit: Transit | None
    climat: str
    domaines: list
    conseil: str
    couleur: str
    chiffre: int
    humeur: str


def avec_article(signe: str) -> str:
    return ARTICLES.get(signe, "le ") + signe


def date_courte(d: dt.date) -> str:
    return f"{'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]}"


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


def graine(signe: Signe, date: dt.date, sel: str) -> random.Random:
    h = hashlib.sha256(f"{date.isoformat()}|{signe.nom}|{sel}".encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def regles(signe: Signe, phase: Phase) -> dict:
    return {**BASE, **ELEMENTS[signe.element],
            "phase": [phase.sujet], "phase_effet": PHASE_EFFETS[phase.groupe]}


def _climat(g: Grammaire, rng: random.Random, trs: list, signe: Signe,
            ciel: dict, date: dt.date) -> tuple:
    phrases = []
    candidats = [t for t in trs if t.aspect]
    transit = None
    if candidats:
        poids = [SAILLANCE[t.astre] + (BONUS_MAITRE if t.astre == signe.maitre else 0)
                 for t in candidats]
        transit = rng.choices(candidats, weights=poids)[0]
        nom_signe = SIGNES[transit.position.signe].nom
        harmonieux, tendu = EFFETS[transit.astre]
        g.regles.update(t_astre=[ASTRES[transit.astre].sujet], t_signe=[nom_signe],
                        t_ou=[avec_article(nom_signe)], t_aspect=[transit.aspect],
                        t_effet=harmonieux if transit.valence >= 0 else tendu)
        sym = "transit_conj" if transit.aspect == "conjonction" else "transit_aspect"
        phrases.append(g.developper("{%s}" % sym))
    else:
        phrases.append(g.developper("{transit_calme}"))

    retro = next((a for a in RETRO_SIGNALES if ciel[a].retrograde), None)
    if retro:
        fin = astro.fin_retrograde(retro, date)
        g.regles.update(r_astre=[ASTRES[retro].sujet], r_conseil=CONSEILS_RETRO[retro],
                        r_fin=[f" jusqu'au {date_courte(fin)}" if fin else ""])
        phrases.append(g.developper("{retro_phrase}"))

    lune_signe = SIGNES[ciel["Lune"].signe].nom
    deja_cite = transit is not None and transit.astre == "Lune"
    g.regles["lune_ou"] = ["" if deja_cite else f" en {lune_signe}"]
    phrases.append(g.developper("{lune_phrase}"))

    if not retro:
        n = sum(1 for p in ciel.values() if SIGNES[p.signe].element == signe.element)
        if n >= 3:
            g.regles["n_element"] = [NOMBRES[n]]
            phrases.append(g.developper("{element_honneur}"))
        else:
            phrases.append(g.developper("{element_phrase}"))
    return " ".join(phrases), transit


def _domaine(g: Grammaire, rng: random.Random, trs: list, cle, libelle, gabarit,
             poids) -> Domaine:
    contrib = contributions(trs, poids)
    brut = sum(contrib.values()) + rng.uniform(-BRUIT, BRUIT)
    note = max(1, min(5, round(3 + brut)))
    haut = note >= 3
    texte = g.developper(gabarit.replace("%s", "haut" if haut else "bas"))

    # On nomme l'astre le plus influent seulement s'il va dans le sens de la note.
    meneur = max(contrib, key=lambda a: abs(contrib[a]), default=None)
    influence = None
    if meneur and abs(contrib[meneur]) >= SEUIL_INFLUENCE and (contrib[meneur] > 0) == haut:
        influence = meneur
        g.regles["infl"] = [ASTRES[meneur].sujet]
        texte = g.developper("{influence_%s} " % ("pos" if haut else "neg")) + texte
    return Domaine(cle, libelle, note, texte, influence)


def horoscope(signe: Signe, date: dt.date, sel: str = "") -> Horoscope:
    rng = graine(signe, date, sel)
    ciel = astro.ciel(date)
    phase = phase_de(astro.elongation(date))
    trs = transits(ciel, signe)
    g = Grammaire(regles(signe, phase), rng)

    climat, transit = _climat(g, rng, trs, signe, ciel, date)
    domaines = [_domaine(g, rng, trs, *d) for d in DOMAINES]
    return Horoscope(
        signe=signe, date=date, ciel=ciel, phase=phase, transit=transit,
        climat=climat, domaines=domaines, conseil=g.developper("{conseil}"),
        couleur=g.developper("{couleur}"), chiffre=rng.randint(1, 49),
        humeur=g.developper("{humeur}"),
    )

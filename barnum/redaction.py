"""Rédaction : d'une lecture du ciel à un horoscope dans une langue donnée.

Seul le choix des formules dépend de la langue ; les notes, le transit mis en
avant, le chiffre, la couleur et l'humeur viennent de la lecture et sont donc
les mêmes dans toutes les langues.
"""
import datetime as dt
from dataclasses import dataclass

from .grammaire import Grammaire
from .langues import PAR_DEFAUT, Langue, langue as trouver_langue
from .lecture import Lecture, graine, lire
from .zodiaque import SIGNES, Signe

# Symboles fournis à la volée par ce module (en plus de Langue.base)
DYNAMIQUES = {"trait", "element_de", "phase", "phase_effet", "lune_ou", "n_element",
              "t_astre", "t_signe", "t_ou", "t_aspect", "t_effet",
              "r_astre", "r_fin", "r_conseil", "infl"}


@dataclass(frozen=True)
class Domaine:
    cle: str
    libelle: str
    note: int
    texte: str
    influence: str | None


@dataclass(frozen=True)
class Horoscope:
    lecture: Lecture
    langue: Langue
    climat: str
    domaines: list
    conseil: str

    signe = property(lambda self: self.lecture.signe)
    date = property(lambda self: self.lecture.date)
    ciel = property(lambda self: self.lecture.ciel)
    phase = property(lambda self: self.lecture.phase)
    transit = property(lambda self: self.lecture.transit)
    chiffre = property(lambda self: self.lecture.chiffre)

    @property
    def couleur(self) -> str:
        return self.langue.couleurs[self.lecture.couleur]

    @property
    def humeur(self) -> str:
        return self.langue.humeurs[self.lecture.humeur]


def nom_signe(index: int, lg: Langue) -> str:
    return lg.signes[index]


def _climat(g: Grammaire, lu: Lecture, lg: Langue) -> str:
    phrases = []
    t = lu.transit
    if t:
        ou = nom_signe(t.position.signe, lg)
        harmonieux, tendus = lg.effets[t.astre]
        g.regles.update(t_astre=[lg.astres[t.astre][1]], t_signe=[ou],
                        t_ou=[lg.depuis(ou)], t_aspect=[lg.aspects.get(t.aspect, "")],
                        t_effet=harmonieux if t.valence >= 0 else tendus)
        sym = "transit_conj" if t.aspect == "conjonction" else "transit_aspect"
        phrases.append(g.developper("{%s}" % sym))
    else:
        phrases.append(g.developper("{transit_calme}"))

    if lu.retro:
        g.regles.update(r_astre=[lg.astres[lu.retro][1]],
                        r_conseil=lg.conseils_retro[lu.retro],
                        r_fin=[lg.jusqua(lu.fin_retro) if lu.fin_retro else ""])
        phrases.append(g.developper("{retro_phrase}"))

    lune_deja_citee = t is not None and t.astre == "Lune"
    lune = nom_signe(lu.ciel["Lune"].signe, lg)
    g.regles["lune_ou"] = ["" if lune_deja_citee else lg.dans(lune)]
    phrases.append(g.developper("{lune_phrase}"))

    if not lu.retro:
        if lu.n_element >= 3:
            g.regles["n_element"] = [lg.nombres[lu.n_element]]
            phrases.append(g.developper("{element_honneur}"))
        else:
            phrases.append(g.developper("{element_phrase}"))
    return " ".join(phrases)


def rediger(lu: Lecture, lg: Langue, sel: str = "") -> Horoscope:
    rng = graine(lu.signe, lu.date, sel, "texte")
    g = Grammaire({**lg.base, **lg.elements[lu.signe.element],
                   "phase": [lg.phases[lu.phase.nom][1]],
                   "phase_effet": lg.phase_effets[lu.phase.groupe]}, rng)
    climat = _climat(g, lu, lg)

    domaines = []
    for n in lu.notes:
        libelle, gabarit = lg.domaines[n.cle]
        haut = n.note >= 3
        texte = g.developper(gabarit.replace("%s", "haut" if haut else "bas"))
        if n.influence:
            g.regles["infl"] = [lg.astres[n.influence][1]]
            texte = g.developper("{influence_%s} " % ("pos" if haut else "neg")) + texte
        domaines.append(Domaine(n.cle, libelle, n.note, texte, n.influence))

    return Horoscope(lu, lg, climat, domaines, g.developper("{conseil}"))


def horoscope(signe: Signe, date: dt.date, sel: str = "",
              langue: str | Langue = PAR_DEFAUT) -> Horoscope:
    lg = trouver_langue(langue) if isinstance(langue, str) else langue
    return rediger(lire(signe, date, sel), lg, sel)

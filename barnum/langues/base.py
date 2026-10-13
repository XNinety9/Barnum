"""Ce qu'une langue doit fournir pour rédiger un horoscope."""
import datetime as dt
from dataclasses import dataclass
from typing import Callable

# Couleur et humeur sont tirées par index, indépendamment de la langue :
# toutes les langues doivent donc proposer des listes parallèles de même taille.
N_COULEURS, N_HUMEURS = 10, 8


@dataclass(frozen=True)
class Langue:
    code: str
    signes: tuple  # 12 noms, ordre zodiacal
    astres: dict  # clé de zodiaque.ASTRES -> (nom, sujet de phrase)
    phases: dict  # Phase.nom -> (nom, sujet de phrase)
    aspects: dict  # aspect -> forme attendue par les gabarits de transit
    domaines: dict  # clé de domaine -> (libellé, gabarit ; %s = haut/bas)
    etiquettes: dict  # ciel, climat, conseil, pied
    base: dict  # corpus de la grammaire
    elements: dict
    phase_effets: dict
    effets: dict  # astre -> (harmonieux, tendus)
    conseils_retro: dict
    nombres: dict
    couleurs: tuple
    humeurs: tuple
    depuis: Callable[[str], str]  # nom de signe -> complément de provenance
    dans: Callable[[str], str]  # nom de signe -> « en Vierge », « in Virgo »
    jusqua: Callable[[dt.date], str]  # fin de rétrogradation
    date_longue: Callable[[dt.date], str]

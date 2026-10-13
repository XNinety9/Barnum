"""Langues disponibles. Pour en ajouter une : copier en.py, traduire, l'enregistrer ici."""
from . import en, fr
from .base import N_COULEURS, N_HUMEURS, Langue

LANGUES = {l.code: l for l in (fr.LANGUE, en.LANGUE)}
PAR_DEFAUT = "fr"


def langue(code: str) -> Langue:
    try:
        return LANGUES[code.lower()]
    except KeyError:
        raise ValueError(f"langue inconnue : {code!r} (disponibles : {', '.join(LANGUES)})")


__all__ = ["LANGUES", "PAR_DEFAUT", "Langue", "langue", "N_COULEURS", "N_HUMEURS"]

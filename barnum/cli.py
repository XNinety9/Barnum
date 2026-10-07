"""Ligne de commande.

    barnum                          # les 12 signes, aujourd'hui
    barnum lion                     # un signe (casse/accents ignorés)
    barnum --naissance 1990-08-02   # signe déduit de la date de naissance
    barnum scorpion --date 2026-12-25 --ciel
    barnum --json
"""
import argparse
import datetime as dt
import json
import sys

from . import rendu
from .lecture import horoscope
from .zodiaque import SIGNES, signe_de_naissance, trouver_signe


def _date(txt: str) -> dt.date:
    try:
        return dt.date.fromisoformat(txt)
    except ValueError:
        raise argparse.ArgumentTypeError(f"date invalide : {txt!r} (format AAAA-MM-JJ)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="barnum",
                                description="Horoscopes offline et déterministes, "
                                            "calculés sur le ciel réel.")
    qui = p.add_mutually_exclusive_group()
    qui.add_argument("signe", nargs="?", help="nom du signe (tous si omis)")
    qui.add_argument("--naissance", type=_date, metavar="AAAA-MM-JJ",
                     help="déduit le signe de la date de naissance")
    p.add_argument("--date", type=_date, default=None, metavar="AAAA-MM-JJ",
                   help="jour de l'horoscope (aujourd'hui par défaut)")
    p.add_argument("--sel", default="", help="change la série de formules générées")
    p.add_argument("--ciel", action="store_true", help="affiche la position des astres")
    p.add_argument("--json", action="store_true", help="sortie JSON")
    a = p.parse_args(argv)

    if a.naissance:
        cibles = [signe_de_naissance(a.naissance)]
    elif a.signe:
        try:
            cibles = [trouver_signe(a.signe)]
        except ValueError as e:
            p.error(str(e))
    else:
        cibles = SIGNES
    date = a.date or dt.date.today()
    if not 1800 <= date.year <= 2050:
        print("attention : éphémérides peu fiables hors de 1800-2050", file=sys.stderr)
    hs = [horoscope(s, date, a.sel) for s in cibles]

    if a.json:
        data = [rendu.dictionnaire(h) for h in hs]
        print(json.dumps(data if len(data) > 1 else data[0], ensure_ascii=False, indent=2))
    else:
        sep = "\n\n" + "·" * rendu.LARGEUR + "\n\n"
        print(sep.join(rendu.texte(h, a.ciel) for h in hs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

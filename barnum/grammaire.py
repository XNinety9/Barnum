"""Moteur de grammaire générative (style Tracery)."""
import random
import re

TOKEN = re.compile(r"\{(\w+)(?:\.(\w+))?\}")
PROFONDEUR_MAX = 32


class Grammaire:
    """Expansion récursive de {symbole} ou {symbole.cap}.

    Évite de réutiliser une même option tant que les autres n'ont pas servi.
    """

    def __init__(self, regles: dict, rng: random.Random):
        self.regles, self.rng, self.utilises = regles, rng, {}

    def choisir(self, sym: str) -> str:
        options = self.regles[sym]
        deja = self.utilises.setdefault(sym, set())
        libres = [i for i in range(len(options)) if i not in deja]
        if not libres:
            deja.clear()
            libres = list(range(len(options)))
        i = self.rng.choice(libres)
        deja.add(i)
        return options[i]

    def developper(self, texte: str, profondeur: int = 0) -> str:
        if profondeur > PROFONDEUR_MAX:
            raise RecursionError("grammaire trop profonde (cycle ?)")

        def sub(m):
            out = self.developper(self.choisir(m[1]), profondeur + 1)
            return out[:1].upper() + out[1:] if m[2] == "cap" else out

        return TOKEN.sub(sub, texte)


def symboles(texte: str) -> list:
    return [(m[1], m[2]) for m in TOKEN.finditer(texte)]


def a_un_cycle(regles: dict) -> bool:
    etat = {}

    def dfs(sym):
        if etat.get(sym) == 1:
            return True
        if etat.get(sym) == 2 or sym not in regles:
            return False
        etat[sym] = 1
        cyc = any(dfs(s) for t in regles[sym] for s, _ in symboles(t))
        etat[sym] = 2
        return cyc

    return any(dfs(k) for k in regles)

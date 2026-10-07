import datetime as dt
import json
import unittest
from collections import Counter

from barnum import rendu
from barnum.grammaire import a_un_cycle, symboles
from barnum.lecture import DOMAINES, DYNAMIQUES, horoscope
from barnum.textes import BASE, ELEMENTS, PHASE_EFFETS
from barnum.zodiaque import SIGNES


class Grammaire(unittest.TestCase):
    def test_symboles_definis_et_sans_cycle(self):
        connus = set(BASE) | DYNAMIQUES
        for sym in ELEMENTS["feu"]:
            self.assertIn(sym, DYNAMIQUES)
        textes = [t for opts in BASE.values() for t in opts]
        textes += [g.replace("%s", n) for _, _, g, _ in DOMAINES for n in ("haut", "bas")]
        textes += ["{influence_pos}", "{influence_neg}"]
        for t in textes:
            for sym, mod in symboles(t):
                self.assertIn(sym, connus, t)
                self.assertIn(mod, (None, "cap"), t)
        self.assertFalse(a_un_cycle({**BASE, **ELEMENTS["eau"],
                                     "phase_effet": PHASE_EFFETS["pleine"]}))


class Balayage(unittest.TestCase):
    """Une année complète pour les 12 signes."""

    @classmethod
    def setUpClass(cls):
        debut = dt.date(2026, 1, 1)
        cls.hs = [horoscope(s, debut + dt.timedelta(days=i))
                  for i in range(365) for s in SIGNES]

    def test_deterministe(self):
        for h in self.hs[::97]:
            self.assertEqual(rendu.texte(h), rendu.texte(horoscope(h.signe, h.date)))

    def test_texte_propre(self):
        for h in self.hs:
            txt = rendu.texte(h, avec_ciel=True)
            for motif in ("{", "}", "  .", "..", " ,", "de le ", "à le "):
                self.assertNotIn(motif, txt, f"{h.signe.nom} {h.date}")

    def test_notes_variees(self):
        notes = Counter(d.note for h in self.hs for d in h.domaines)
        self.assertEqual(set(notes), {1, 2, 3, 4, 5})
        self.assertGreater(notes[3], notes[1])  # courbe en cloche, pas uniforme

    def test_diversite(self):
        corps = {h.climat + "".join(d.texte for d in h.domaines) for h in self.hs}
        self.assertGreater(len(corps) / len(self.hs), 0.99)

    def test_influence_coherente_avec_la_note(self):
        pos = {t.replace("{infl.cap}", "").strip() for t in BASE["influence_pos"]}
        for h in self.hs:
            for d in h.domaines:
                if d.influence and d.note < 3:
                    self.assertFalse(any(p in d.texte for p in pos), d.texte)


class Divers(unittest.TestCase):
    def test_le_sel_change_le_texte(self):
        d = dt.date(2026, 1, 1)
        self.assertNotEqual(horoscope(SIGNES[0], d, "a").climat,
                            horoscope(SIGNES[0], d, "b").climat)

    def test_le_sel_ne_change_pas_le_ciel(self):
        d = dt.date(2026, 1, 1)
        a, b = horoscope(SIGNES[0], d, "a"), horoscope(SIGNES[0], d, "b")
        self.assertEqual(a.ciel, b.ciel)
        self.assertEqual(a.phase, b.phase)

    def test_json(self):
        h = horoscope(SIGNES[4], dt.date(2026, 10, 7))
        data = json.loads(json.dumps(rendu.dictionnaire(h), ensure_ascii=False))
        self.assertEqual(data["signe"], "Lion")
        self.assertEqual(len(data["ciel"]), 10)
        self.assertTrue(all(1 <= d["note"] <= 5 for d in data["domaines"]))


if __name__ == "__main__":
    unittest.main()

import datetime as dt
import json
import unittest
from collections import Counter

from barnum import rendu
from barnum.grammaire import a_un_cycle, symboles
from barnum.langues import LANGUES, N_COULEURS, N_HUMEURS
from barnum.lecture import DOMAINES, lire
from barnum.redaction import DYNAMIQUES, horoscope
from barnum.zodiaque import ASTRES, PHASES, SIGNES

# Tournures fautives, par langue
SUSPECTS = {"fr": ("de le ", "à le ", " ,"), "en": ("the the ", " a a", " ,", " :")}


class Langues(unittest.TestCase):
    def test_completude(self):
        fr = LANGUES["fr"]
        for code, lg in LANGUES.items():
            with self.subTest(langue=code):
                self.assertEqual(set(lg.base), set(fr.base))
                self.assertEqual(len(lg.signes), 12)
                self.assertEqual(set(lg.astres), set(ASTRES))
                self.assertEqual(set(lg.effets), set(ASTRES))
                self.assertEqual(set(lg.phases), {p.nom for p in PHASES})
                self.assertEqual(set(lg.phase_effets), {p.groupe for p in PHASES})
                self.assertEqual(set(lg.domaines), set(DOMAINES))
                self.assertEqual(set(lg.elements), {s.element for s in SIGNES})
                self.assertLessEqual({"sextile", "trigone", "carré", "opposition"},
                                     set(lg.aspects))
                self.assertEqual(set(lg.nombres), set(range(3, 9)))
                self.assertEqual((len(lg.couleurs), len(lg.humeurs)), (N_COULEURS, N_HUMEURS))

    def test_grammaire(self):
        for code, lg in LANGUES.items():
            connus = set(lg.base) | DYNAMIQUES
            textes = [t for opts in lg.base.values() for t in opts]
            textes += [g.replace("%s", n) for _, g in lg.domaines.values() for n in ("haut", "bas")]
            for t in textes:
                for sym, mod in symboles(t):
                    self.assertIn(sym, connus, f"{code}: {t}")
                    self.assertIn(mod, (None, "cap"), f"{code}: {t}")
            for sym in lg.elements["feu"]:
                self.assertIn(sym, DYNAMIQUES)
            self.assertFalse(a_un_cycle({**lg.base, **lg.elements["eau"],
                                         "phase_effet": lg.phase_effets["pleine"]}))


class Balayage(unittest.TestCase):
    """Une année complète pour les 12 signes, dans chaque langue."""

    @classmethod
    def setUpClass(cls):
        debut = dt.date(2026, 1, 1)
        jours = [debut + dt.timedelta(days=i) for i in range(365)]
        cls.hs = {code: [horoscope(s, d, langue=code) for d in jours for s in SIGNES]
                  for code in LANGUES}

    def test_deterministe(self):
        for code, hs in self.hs.items():
            for h in hs[::97]:
                self.assertEqual(rendu.texte(h), rendu.texte(horoscope(h.signe, h.date,
                                                                       langue=code)))

    def test_texte_propre(self):
        for code, hs in self.hs.items():
            for h in hs:
                rendu_complet = rendu.texte(h, avec_ciel=True)
                self.assertNotIn("{", rendu_complet)
                self.assertNotIn("}", rendu_complet)
                genere = " ".join([h.climat, h.conseil] + [d.texte for d in h.domaines])
                for motif in ("  ", " .", "..") + SUSPECTS[code]:
                    self.assertNotIn(motif, genere, f"{code} {h.signe.nom} {h.date}")

    def test_langues_paralleles(self):
        """Mêmes notes, transit, chiffre, couleur et humeur dans toutes les langues."""
        fr, en = self.hs["fr"], self.hs["en"]
        for a, b in zip(fr, en):
            self.assertIs(a.lecture.signe, b.lecture.signe)
            self.assertEqual([d.note for d in a.domaines], [d.note for d in b.domaines])
            self.assertEqual(a.transit, b.transit)
            self.assertEqual((a.chiffre, a.lecture.couleur, a.lecture.humeur),
                             (b.chiffre, b.lecture.couleur, b.lecture.humeur))

    def test_notes_variees(self):
        notes = Counter(d.note for h in self.hs["fr"] for d in h.domaines)
        self.assertEqual(set(notes), {1, 2, 3, 4, 5})
        self.assertGreater(notes[3], notes[1])  # courbe en cloche, pas uniforme

    def test_diversite(self):
        for code, hs in self.hs.items():
            corps = {h.climat + "".join(d.texte for d in h.domaines) for h in hs}
            self.assertGreater(len(corps) / len(hs), 0.99, code)

    def test_influence_coherente_avec_la_note(self):
        for code, lg in LANGUES.items():
            pos = {t.replace("{infl.cap}", "").strip() for t in lg.base["influence_pos"]}
            for h in self.hs[code]:
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
        a, b = lire(SIGNES[0], d, "a"), lire(SIGNES[0], d, "b")
        self.assertEqual((a.ciel, a.phase), (b.ciel, b.phase))

    def test_langue_inconnue(self):
        with self.assertRaises(ValueError):
            horoscope(SIGNES[0], dt.date(2026, 1, 1), langue="xx")

    def test_json(self):
        for code in LANGUES:
            h = horoscope(SIGNES[4], dt.date(2026, 10, 7), langue=code)
            data = json.loads(json.dumps(rendu.dictionnaire(h), ensure_ascii=False))
            self.assertEqual(data["langue"], code)
            self.assertEqual(data["signe"], LANGUES[code].signes[4])
            self.assertEqual(data["signe_id"], 4)
            self.assertEqual(len(data["ciel"]), 10)
            self.assertTrue(all(1 <= d["note"] <= 5 for d in data["domaines"]))


if __name__ == "__main__":
    unittest.main()

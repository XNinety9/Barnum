"""Éphémérides comparées à des événements astronomiques connus."""
import datetime as dt
import unittest

from barnum import astro
from barnum.zodiaque import SIGNES, phase_de

UTC = dt.timezone.utc


def t(*a):
    return dt.datetime(*a, tzinfo=UTC)


class Longitudes(unittest.TestCase):
    def proche(self, obtenu, attendu, tol):
        self.assertLess(abs(astro.ecart(attendu, obtenu)), tol, f"{obtenu} vs {attendu}")

    def test_soleil_equinoxes_et_solstices(self):
        self.proche(astro.longitude("Soleil", t(2024, 3, 20, 3, 6)), 0, 0.05)
        self.proche(astro.longitude("Soleil", t(2024, 6, 20, 20, 51)), 90, 0.05)
        self.proche(astro.longitude("Soleil", t(2024, 12, 21, 9, 20)), 270, 0.05)

    def test_grande_conjonction_2020(self):
        jupiter = astro.longitude("Jupiter", t(2020, 12, 21, 18))
        saturne = astro.longitude("Saturne", t(2020, 12, 21, 18))
        self.proche(jupiter, 300.5, 0.3)
        self.proche(saturne, 300.5, 0.3)

    def test_eclipse_totale_2024(self):
        moment = t(2024, 4, 8, 18, 21)
        self.proche(astro.longitude("Soleil", moment), 19.4, 0.1)
        self.proche(astro.longitude("Lune", moment), 19.4, 0.5)

    def test_stations_de_mercure_2024(self):
        self.proche(astro.longitude("Mercure", t(2024, 4, 1, 22, 14)), 27.22, 0.1)
        self.proche(astro.longitude("Mercure", t(2024, 4, 25, 12, 54)), 15.97, 0.1)


class Signes(unittest.TestCase):
    def test_lents_dans_le_bon_signe(self):
        cas = [("Jupiter", dt.date(2024, 8, 1), "Gémeaux"),
               ("Jupiter", dt.date(2025, 8, 1), "Cancer"),
               ("Saturne", dt.date(2024, 8, 1), "Poissons"),
               ("Saturne", dt.date(2026, 6, 1), "Bélier"),
               ("Uranus", dt.date(2024, 6, 1), "Taureau"),
               ("Neptune", dt.date(2026, 6, 1), "Bélier"),
               ("Pluton", dt.date(2025, 6, 1), "Verseau")]
        for astre, d, attendu in cas:
            with self.subTest(astre=astre, date=d):
                self.assertEqual(SIGNES[astro.ciel(d)[astre].signe].nom, attendu)


class Retrogradations(unittest.TestCase):
    def test_periodes_connues(self):
        cas = [("Mercure", dt.date(2024, 3, 20), False),
               ("Mercure", dt.date(2024, 4, 10), True),
               ("Mercure", dt.date(2024, 5, 10), False),
               ("Mercure", dt.date(2024, 8, 15), True),
               ("Mercure", dt.date(2024, 12, 5), True),
               ("Vénus", dt.date(2025, 3, 20), True),
               ("Vénus", dt.date(2025, 5, 1), False),
               ("Mars", dt.date(2025, 1, 15), True),
               ("Soleil", dt.date(2025, 1, 15), False)]
        for astre, d, attendu in cas:
            with self.subTest(astre=astre, date=d):
                self.assertEqual(astro.ciel(d)[astre].retrograde, attendu)

    def test_fin_retrograde(self):
        # Mercure redevient direct le 25 avril 2024 à 12 h 54 UTC
        self.assertEqual(astro.fin_retrograde("Mercure", dt.date(2024, 4, 10)),
                         dt.date(2024, 4, 26))


class Phases(unittest.TestCase):
    def test_dates_connues(self):
        cas = [(dt.date(2024, 4, 8), "nouvelle lune"),
               (dt.date(2024, 4, 15), "premier quartier"),
               (dt.date(2024, 4, 23), "pleine lune"),
               (dt.date(2025, 9, 7), "pleine lune"),
               (dt.date(2026, 1, 18), "nouvelle lune"),
               (dt.date(2024, 4, 11), "premier croissant")]
        for d, attendu in cas:
            with self.subTest(date=d):
                self.assertEqual(phase_de(astro.elongation(d)).nom, attendu)

    def test_bornes(self):
        self.assertEqual(phase_de(-5).nom, "nouvelle lune")
        self.assertEqual(phase_de(355).nom, "nouvelle lune")
        self.assertEqual(phase_de(347.9).nom, "dernier croissant")
        self.assertEqual(phase_de(180).nom, "pleine lune")


if __name__ == "__main__":
    unittest.main()

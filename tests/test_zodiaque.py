import datetime as dt
import unittest

from barnum.zodiaque import signe_de_naissance, trouver_signe


class Naissance(unittest.TestCase):
    def test_bornes(self):
        cas = [((3, 21), "Bélier"), ((3, 20), "Poissons"), ((1, 1), "Capricorne"),
               ((12, 22), "Capricorne"), ((12, 21), "Sagittaire"), ((1, 20), "Verseau"),
               ((7, 23), "Lion"), ((2, 29), "Poissons"), ((12, 31), "Capricorne")]
        for (m, j), attendu in cas:
            with self.subTest(jour=j, mois=m):
                self.assertEqual(signe_de_naissance(dt.date(2024, m, j)).nom, attendu)


class Recherche(unittest.TestCase):
    def test_casse_et_accents(self):
        self.assertEqual(trouver_signe("belier").nom, "Bélier")
        self.assertEqual(trouver_signe(" GÉMEAUX ").nom, "Gémeaux")

    def test_noms_anglais(self):
        self.assertEqual(trouver_signe("Scorpio").nom, "Scorpion")
        self.assertEqual(trouver_signe("capricorn").nom, "Capricorne")

    def test_inconnu(self):
        with self.assertRaises(ValueError):
            trouver_signe("ophiuchus")


if __name__ == "__main__":
    unittest.main()

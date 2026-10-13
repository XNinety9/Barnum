# Barnum

Générateur d'horoscopes en français et en anglais : offline, déterministe, sans dépendance.

Le texte relève de l'[effet Barnum](https://fr.wikipedia.org/wiki/Effet_Barnum),
mais le ciel, lui, est vrai. Les positions des planètes viennent des éléments
képlériens du JPL, la Lune d'une théorie lunaire simplifiée. On en tire les
signes, les rétrogradations, la phase et les aspects avec chaque signe. Les
notes et le texte découlent de ces aspects.

## Usage

    python3 main.py                        # les 12 signes, aujourd'hui
    python3 main.py lion --ciel            # un signe, avec la position des astres
    python3 main.py --naissance 1990-08-02
    python3 main.py scorpion --date 2026-12-25
    python3 main.py --json                 # pour une intégration
    python3 main.py leo --lang en          # en anglais

Ou, après `pip install -e .`, la commande `barnum`.

Même date + même signe + même `--sel` = même horoscope, sur toute machine
(le ciel est calculé à midi UTC).

Les langues sont parallèles : pour un même jour et un même signe, l'horoscope
anglais a les mêmes notes, le même transit, le même chiffre et la même couleur
que le français. Seule la formulation change.

## Organisation

| Module          | Rôle                                                       |
|-----------------|------------------------------------------------------------|
| `astro.py`      | éphémérides : longitudes, rétrogradations, élongation      |
| `zodiaque.py`   | signes, astres, phases de lune                             |
| `lecture.py`    | interprétation, sans texte : aspects → notes, transit      |
| `redaction.py`  | rédaction d'une lecture dans une langue                    |
| `langues/`      | corpus et libellés : `fr.py`, `en.py`                      |
| `grammaire.py`  | moteur d'expansion (style Tracery)                         |
| `rendu.py`      | sortie terminal et JSON                                    |

## Ajouter une langue

Copier `langues/en.py`, traduire en gardant les mêmes symboles `{…}` et des
listes de couleurs et d'humeurs parallèles, puis l'enregistrer dans
`langues/__init__.py`. Le test `test_completude` signale tout oubli.

## Tests

    python3 -m unittest

Les éphémérides sont vérifiées contre des événements connus : équinoxes,
grande conjonction de 2020, éclipse du 8 avril 2024, stations de Mercure.
Validité des éléments JPL : 1800–2050.

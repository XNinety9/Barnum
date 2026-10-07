"""Éphémérides simplifiées, sans dépendance externe.

Planètes : éléments képlériens approchés publiés par le JPL (E. M. Standish,
« Keplerian Elements for Approximate Positions of the Major Planets »), valides
de 1800 à 2050. Précision : la minute d'arc pour les planètes proches, quelques
minutes au-delà. C'est largement assez pour savoir dans quel signe se trouve un
astre et s'il est rétrograde.

Lune : termes principaux de la théorie lunaire (précision d'environ 0,3°).

Toutes les longitudes sont géocentriques, écliptiques, rapportées à l'équinoxe
de la date : c'est le zodiaque tropical utilisé en astrologie occidentale.
"""
import datetime as dt
import math
from functools import lru_cache
from typing import NamedTuple

UTC = dt.timezone.utc
J2000 = dt.datetime(2000, 1, 1, 12, tzinfo=UTC)
PRECESSION = 1.396971  # degrés par siècle julien (J2000 -> équinoxe de la date)

# a (UA), e, I, L, ϖ, Ω (degrés), puis leurs dérivées par siècle julien
ELEMENTS = {
    "Mercure": ((0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
                (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081)),
    "Vénus": ((0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
              (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418)),
    "Terre": ((1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
              (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0)),
    "Mars": ((1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
             (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343)),
    "Jupiter": ((5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
                (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106)),
    "Saturne": ((9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
                (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794)),
    "Uranus": ((19.18916464, 0.04725744, 0.77263783, 313.23810451, 170.95427630, 74.01692503),
               (-0.00196176, -0.00004397, -0.00242939, 428.48202785, 0.40805281, 0.04240589)),
    "Neptune": ((30.06992276, 0.00859048, 1.77004347, -55.12002969, 44.96476227, 131.78422574),
                (0.00026291, 0.00005105, 0.00035372, 218.45945325, -0.32241464, -0.00508664)),
    "Pluton": ((39.48211675, 0.24882730, 17.14001206, 238.92903833, 224.06891629, 110.30393684),
               (-0.00031596, 0.00005170, 0.00004818, 145.20780515, -0.04062942, -0.01183482)),
}

ASTRES = ("Soleil", "Lune", "Mercure", "Vénus", "Mars", "Jupiter", "Saturne",
          "Uranus", "Neptune", "Pluton")


class Position(NamedTuple):
    astre: str
    longitude: float  # degrés, 0 = point vernal
    retrograde: bool

    @property
    def signe(self) -> int:
        """Index du signe (0 = Bélier)."""
        return int(self.longitude // 30)

    @property
    def degre(self) -> float:
        return self.longitude % 30


def moment(d: dt.date) -> dt.datetime:
    """Instant de référence d'une journée : midi UTC, identique sur toute machine."""
    return dt.datetime(d.year, d.month, d.day, 12, tzinfo=UTC)


def _jours(t: dt.datetime) -> float:
    return (t - J2000).total_seconds() / 86400


def _heliocentrique(nom: str, T: float) -> tuple:
    el, var = ELEMENTS[nom]
    a, e, i, L, w, o = (x + dx * T for x, dx in zip(el, var))
    M = math.radians((L - w + 180) % 360 - 180)
    E = M + e * math.sin(M)
    for _ in range(10):  # Newton sur l'équation de Kepler
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    xp, yp = a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E)
    i, w, o = math.radians(i), math.radians(w - o), math.radians(o)
    x = ((math.cos(w) * math.cos(o) - math.sin(w) * math.sin(o) * math.cos(i)) * xp
         + (-math.sin(w) * math.cos(o) - math.cos(w) * math.sin(o) * math.cos(i)) * yp)
    y = ((math.cos(w) * math.sin(o) + math.sin(w) * math.cos(o) * math.cos(i)) * xp
         + (-math.sin(w) * math.sin(o) + math.cos(w) * math.cos(o) * math.cos(i)) * yp)
    return x, y


def _lune(j: float) -> float:
    s = lambda deg: math.sin(math.radians(deg))  # noqa: E731
    L = 218.316 + 13.176396 * j   # longitude moyenne
    Ml = 134.963 + 13.064993 * j  # anomalie moyenne de la Lune
    F = 93.272 + 13.229350 * j    # argument de latitude
    D = 297.850 + 12.190749 * j   # élongation moyenne
    Ms = 357.529 + 0.98560028 * j  # anomalie moyenne du Soleil
    return (L + 6.289 * s(Ml) + 1.274 * s(2 * D - Ml) + 0.658 * s(2 * D)
            + 0.214 * s(2 * Ml) - 0.186 * s(Ms) - 0.114 * s(2 * F)) % 360


def longitude(astre: str, t: dt.datetime) -> float:
    j = _jours(t)
    if astre == "Lune":
        return _lune(j)
    T = j / 36525
    tx, ty = _heliocentrique("Terre", T)
    if astre == "Soleil":
        x, y = -tx, -ty
    else:
        px, py = _heliocentrique(astre, T)
        x, y = px - tx, py - ty
    return (math.degrees(math.atan2(y, x)) + PRECESSION * T) % 360


def ecart(a: float, b: float) -> float:
    """b - a ramené dans ]-180, 180]."""
    return (b - a + 180) % 360 - 180


def est_retrograde(astre: str, t: dt.datetime) -> bool:
    if astre in ("Soleil", "Lune"):
        return False
    h = dt.timedelta(hours=12)
    return ecart(longitude(astre, t - h), longitude(astre, t + h)) < 0


@lru_cache(maxsize=4096)
def ciel(d: dt.date) -> dict:
    """Positions de tous les astres pour la journée d (à midi UTC)."""
    t = moment(d)
    return {a: Position(a, longitude(a, t), est_retrograde(a, t)) for a in ASTRES}


def elongation(d: dt.date) -> float:
    """Écart Lune - Soleil en degrés (0 = nouvelle lune, 180 = pleine lune)."""
    c = ciel(d)
    return (c["Lune"].longitude - c["Soleil"].longitude) % 360


@lru_cache(maxsize=1024)
def fin_retrograde(astre: str, d: dt.date, horizon: int = 120):
    """Premier jour où l'astre redevient direct, ou None au-delà de l'horizon."""
    for k in range(1, horizon + 1):
        jour = d + dt.timedelta(days=k)
        if not est_retrograde(astre, moment(jour)):
            return jour
    return None

"""English. Same structure and symbols as fr.py; lists of colours and moods are
parallel to the French ones (same index = same meaning)."""
import datetime as dt

from .base import Langue

BASE = {
    "transit_conj": ["{t_astre.cap} is passing through your sign and {t_effet}."],
    "transit_aspect": [
        "{t_astre.cap} in {t_signe} {t_aspect} your sign and {t_effet}.",
        "From {t_ou}, {t_astre} {t_aspect} your sign and {t_effet}.",
    ],
    "transit_calme": [
        "No planet is calling on you directly: the sky leaves you a free hand.",
        "The sky stays quiet for you, so the day is yours to write.",
    ],
    "lune_phrase": ["{phase.cap}{lune_ou} {phase_effet}."],
    "retro_phrase": ["{r_astre.cap} is retrograde{r_fin}: {r_conseil}."],
    "element_phrase": [
        "{trait.cap} will be your best asset.",
        "Beware of {trait}, though.",
        "Count on {trait} to make the difference.",
    ],
    "element_honneur": [
        "{element_de.cap} signs are in the spotlight, hosting {n_element} celestial bodies.",
    ],
    "influence_pos": [
        "{infl.cap} is smiling on you.", "{infl.cap} is working in your favor.",
        "{infl.cap} gives you a boost.",
    ],
    "influence_neg": [
        "{infl.cap} holds you back.", "{infl.cap} stirs up a little chaos.",
        "{infl.cap} makes things harder.",
    ],
    "couple_haut": [
        "a surprise rekindles your closeness.", "your partner appreciates your attentiveness.",
        "plans for two are taking shape.", "an evening for two is in order.",
        "tenderness is in the air.",
    ],
    "couple_bas": [
        "a misunderstanding could settle in, so talk it through soon.",
        "steer clear of touchy subjects tonight.",
        "a little space will do you both good.",
        "routine is weighing on you, so shake it up.",
        "your touchiness could play tricks on you.",
    ],
    "celib_haut": [
        "an unexpected encounter could upend your plans.",
        "your charm is working, so make the most of it.",
        "people notice you more than you think.",
        "an old acquaintance resurfaces, for the better.",
        "an invitation deserves a yes.",
    ],
    "celib_bas": [
        "don't force fate today.",
        "take time to figure out what you really want.",
        "beware of promises that sound too good to be true.",
        "an ex resurfaces, so tread carefully.",
        "solitude has its virtues too.",
    ],
    "travail_haut": [
        "A stalled project finally moves forward.", "Your rigor gets noticed.",
        "An opportunity comes up: seize it.",
        "You get through a huge amount of work.", "Your ideas land well in meetings.",
    ],
    "travail_bas": [
        "Tasks pile up faster than expected.",
        "A colleague throws a wrench in the works.",
        "A meeting drags on with nothing to show for it.",
        "Motivation is missing in action.", "Something unexpected upsets your schedule.",
    ],
    "travail_conseil": [
        "Stay diplomatic.", "Don't sign anything without rereading it.",
        "Delegate what you can.", "Bet on {trait}.", "Dare to put your ideas forward.",
        "Keep your cards close a little longer.", "Make a list and stick to it.",
    ],
    "argent_haut": [
        "Some unexpected money could come your way.",
        "A good day to go over your accounts.",
        "A negotiation turns in your favor.",
        "Your efforts to save are paying off.",
        "Sound advice saves you both time and money.",
    ],
    "argent_bas": [
        "Keep an eye out for an unexpected expense.", "Avoid impulse purchases.",
        "Today is not the day to lend money.",
        "Check your bills: there may be a mistake hiding in them.",
        "Put off big purchases for now.",
    ],
    "forme_haut": [
        "Your energy is set fair.", "You are brimming with vitality.",
        "A workout will do you a world of good.", "Your spirits are sky-high.",
        "You bounce back quickly, so make the most of it.",
    ],
    "forme_bas": [
        "Expect a dip in energy late in the day, so go easy on yourself.",
        "Remember to drink more water.", "Sleep will be your best ally.",
        "Go easy at the dinner table.",
        "A walk in the fresh air will ease the tension.",
    ],
    "conseil": [
        "Sow patience and you will reap serenity.",
        "The right moment is often the one you choose.",
        "A step sideways is sometimes worth more than a step forward.",
        "Listen more than you speak.", "Simplicity is a strength.",
        "What goes unsaid cannot be heard.",
        "Don't put off until tomorrow what sets you free today.",
    ],
}

COULEURS = ("midnight blue", "ochre", "sage green", "burgundy", "turquoise",
            "mustard yellow", "pearl gray", "coral", "purple", "ivory")
HUMEURS = ("conquering", "dreamy", "serene", "playful", "nostalgic",
           "electric", "contemplative", "daring")

ELEMENTS = {
    "feu": {"trait": ["your drive", "your enthusiasm", "your natural impatience",
                      "your boldness"], "element_de": ["fire"]},
    "terre": {"trait": ["your practical sense", "your patience", "your tenacity",
                        "your need for security"], "element_de": ["earth"]},
    "air": {"trait": ["your curiosity", "your quick wit", "your love of conversation",
                      "your lightness of touch"], "element_de": ["air"]},
    "eau": {"trait": ["your intuition", "your sensitivity", "your imagination",
                      "your empathy"], "element_de": ["water"]},
}

PHASE_EFFETS = {
    "nouvelle": ["marks a fresh start", "is ideal for setting intentions",
                 "invites rest and reflection"],
    "croissante": ["favors new projects", "gives momentum to your intentions",
                   "feeds your ambition"],
    "pleine": ["amplifies your emotions", "brings hidden things to light",
               "makes for restless nights"],
    "decroissante": ["invites you to let go", "is good for taking stock",
                     "pushes you to sort out what really matters"],
}

EFFETS = {
    "Soleil": (["brings a spark to your initiatives", "boosts your confidence",
                "puts you in the spotlight"],
               ["puts your ego to the test", "pushes you to force your way through",
                "stirs up rivalries"]),
    "Lune": (["softens your mood", "favors time with family",
              "sharpens your intuition"],
             ["makes your mood changeable", "reopens old sore spots",
              "sets your nerves on edge"]),
    "Mercure": (["makes conversations flow", "favors paperwork",
                 "makes your ideas crystal clear"],
                ["scrambles communication", "breeds misunderstandings",
                 "complicates travel"]),
    "Vénus": (["smooths relationships", "favors simple pleasures",
               "brightens your daily life"],
              ["makes hearts demanding", "tempts you into needless spending",
               "sparks a little jealousy"]),
    "Mars": (["multiplies your energy", "lends courage to your plans",
              "makes you want to act"],
             ["fuels impatience", "makes clashes more likely",
              "pushes you to rush things"]),
    "Jupiter": (["opens doors", "brings a wave of optimism",
                 "broadens your horizons"],
                ["pushes you to excess", "inflates expectations",
                 "makes you promise more than you can deliver"]),
    "Saturne": (["rewards your efforts", "strengthens what you are building",
                 "clarifies your priorities"],
                ["slows your plans down", "reminds you of your obligations",
                 "weighs on your spirits"]),
    "Uranus": (["brings a pleasant surprise", "unleashes your appetite for change",
                "stimulates your creativity"],
               ["upsets your plans", "triggers the unexpected",
                "makes the air crackle"]),
    "Neptune": (["fires your imagination", "refines your intuition",
                 "invites daydreaming"],
                ["keeps things hazy", "blurs your bearings",
                 "makes you easy to sway"]),
    "Pluton": (["helps you turn the page", "reveals your inner strength",
                "supports a deep transformation"],
               ["brings buried tensions to the surface", "tests your limits",
                "intensifies power struggles"]),
}

CONSEILS_RETRO = {
    "Mercure": ["double-check everything", "confirm your appointments",
                "don't rush into signing anything"],
    "Vénus": ["old stories resurface", "avoid buying on a whim",
              "take time to reassess your attachments"],
    "Mars": ["channel your energy instead of forcing things",
             "this is no time to declare war",
             "finish what you started before taking on anything new"],
}

NOMBRES = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}

JOURS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MOIS = ["January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December"]


def date_longue(d: dt.date) -> str:
    return f"{JOURS[d.weekday()]}, {MOIS[d.month - 1]} {d.day}, {d.year}"


def jusqua(d: dt.date) -> str:
    return f" until {MOIS[d.month - 1]} {d.day}"


LANGUE = Langue(
    code="en",
    signes=("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
            "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"),
    astres={"Soleil": ("Sun", "the Sun"), "Lune": ("Moon", "the Moon"),
            "Mercure": ("Mercury", "Mercury"), "Vénus": ("Venus", "Venus"),
            "Mars": ("Mars", "Mars"), "Jupiter": ("Jupiter", "Jupiter"),
            "Saturne": ("Saturn", "Saturn"), "Uranus": ("Uranus", "Uranus"),
            "Neptune": ("Neptune", "Neptune"), "Pluton": ("Pluto", "Pluto")},
    phases={
        "nouvelle lune": ("new moon", "the new moon"),
        "premier croissant": ("waxing crescent", "the waxing crescent moon"),
        "premier quartier": ("first quarter", "the first quarter moon"),
        "lune gibbeuse croissante": ("waxing gibbous", "the waxing gibbous moon"),
        "pleine lune": ("full moon", "the full moon"),
        "lune gibbeuse décroissante": ("waning gibbous", "the waning gibbous moon"),
        "dernier quartier": ("last quarter", "the last quarter moon"),
        "dernier croissant": ("waning crescent", "the waning crescent moon"),
    },
    aspects={"sextile": "forms a sextile with", "trigone": "forms a trine with",
             "carré": "squares", "opposition": "opposes"},
    domaines={
        "amour": ("Love", "In a relationship, {couple_%s} Single, {celib_%s}"),
        "travail": ("Work", "{travail_%s} {travail_conseil}"),
        "argent": ("Money", "{argent_%s}"),
        "forme": ("Health", "{forme_%s}"),
    },
    etiquettes={"ciel": "Sky", "climat": "Overview", "conseil": "Advice",
                "pied": "Color: {couleur} · Number: {chiffre} · Mood: {humeur}"},
    base=BASE, elements=ELEMENTS, phase_effets=PHASE_EFFETS, effets=EFFETS,
    conseils_retro=CONSEILS_RETRO, nombres=NOMBRES, couleurs=COULEURS, humeurs=HUMEURS,
    depuis=lambda signe: signe,
    dans=lambda signe: f" in {signe}",
    jusqua=jusqua,
    date_longue=date_longue,
)

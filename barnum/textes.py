"""Corpus de la grammaire. Les symboles dynamiques (transit du jour, astre
influent…) sont injectés par lecture.py ; voir lecture.DYNAMIQUES."""

BASE = {
    "transit_conj": ["{t_astre.cap} traverse votre signe et {t_effet}."],
    "transit_aspect": [
        "{t_astre.cap} en {t_signe}, en {t_aspect} avec votre signe, {t_effet}.",
        "En {t_aspect} avec votre signe depuis {t_ou}, {t_astre} {t_effet}.",
    ],
    "transit_calme": [
        "Aucun astre ne vous interpelle franchement : le ciel vous laisse les mains libres.",
        "Le ciel reste discret pour vous, à vous d'écrire la journée.",
    ],
    "lune_phrase": ["{phase.cap}{lune_ou} {phase_effet}."],
    "retro_phrase": ["{r_astre.cap} est rétrograde{r_fin} : {r_conseil}."],
    "element_phrase": [
        "{trait.cap} sera votre meilleur atout.",
        "Méfiez-vous toutefois de {trait}.",
        "Comptez sur {trait} pour faire la différence.",
    ],
    "element_honneur": [
        "Les signes {element_de} sont à l'honneur : {n_element} astres y séjournent.",
    ],
    "influence_pos": [
        "{infl.cap} vous sourit.", "{infl.cap} joue en votre faveur.",
        "{infl.cap} vous donne un coup de pouce.",
    ],
    "influence_neg": [
        "{infl.cap} freine vos élans.", "{infl.cap} sème un peu de désordre.",
        "{infl.cap} vous complique la tâche.",
    ],
    "couple_haut": [
        "une surprise ravive la complicité.", "votre partenaire apprécie vos attentions.",
        "les projets à deux prennent forme.", "une soirée en tête-à-tête s'impose.",
        "la tendresse est au rendez-vous.",
    ],
    "couple_bas": [
        "un malentendu risque de s'installer, parlez-en vite.",
        "évitez les sujets qui fâchent ce soir.",
        "un peu de distance vous fera du bien à tous les deux.",
        "la routine pèse, cassez-la.", "votre susceptibilité pourrait jouer des tours.",
    ],
    "celib_haut": [
        "une rencontre inattendue pourrait bousculer vos plans.",
        "votre charme opère, profitez-en.", "on vous remarque plus que vous ne le croyez.",
        "un ancien contact refait surface pour le meilleur.",
        "une invitation mérite d'être acceptée.",
    ],
    "celib_bas": [
        "ne forcez pas le destin aujourd'hui.",
        "prenez le temps de savoir ce que vous voulez vraiment.",
        "méfiez-vous des promesses trop belles.", "un ex refait surface, prudence.",
        "la solitude a aussi ses vertus.",
    ],
    "travail_haut": [
        "Un projet en attente se débloque enfin.", "Votre rigueur est remarquée.",
        "Une opportunité se présente, saisissez-la.",
        "Vous abattez un travail considérable.", "Vos idées font mouche en réunion.",
    ],
    "travail_bas": [
        "Les tâches s'accumulent plus vite que prévu.",
        "Un collègue vous met des bâtons dans les roues.",
        "Une réunion s'éternise sans résultat.",
        "La motivation n'est pas au rendez-vous.", "Un imprévu bouscule votre planning.",
    ],
    "travail_conseil": [
        "Restez diplomate.", "Ne signez rien sans relire.", "Déléguez ce qui peut l'être.",
        "Misez sur {trait}.", "Osez proposer vos idées.",
        "Gardez vos cartes en main encore un peu.", "Faites une liste et tenez-vous-y.",
    ],
    "argent_haut": [
        "Une rentrée d'argent pourrait vous surprendre.",
        "Bonne journée pour faire vos comptes.",
        "Une négociation tourne à votre avantage.",
        "Vos efforts d'économie portent leurs fruits.",
        "Un conseil avisé vous fait gagner du temps et de l'argent.",
    ],
    "argent_bas": [
        "Une dépense imprévue est à surveiller.", "Évitez les achats impulsifs.",
        "Ce n'est pas le jour pour prêter de l'argent.",
        "Relisez vos factures, une erreur s'y cache peut-être.",
        "Remettez à plus tard les gros achats.",
    ],
    "forme_haut": [
        "Votre énergie est au beau fixe.", "Vous débordez de vitalité.",
        "Une séance de sport vous fera un bien fou.", "Votre moral est au zénith.",
        "Vous récupérez vite, profitez-en.",
    ],
    "forme_bas": [
        "Un coup de fatigue en fin de journée, ménagez-vous.",
        "Pensez à vous hydrater davantage.", "Le sommeil sera votre meilleur allié.",
        "Attention aux excès de table.",
        "Une marche au grand air chassera les tensions.",
    ],
    "conseil": [
        "Qui sème la patience récolte la sérénité.",
        "Le bon moment est souvent celui qu'on choisit.",
        "Un pas de côté vaut parfois mieux qu'un pas en avant.",
        "Écoutez plus que vous ne parlez.", "La simplicité est une force.",
        "Ce qui n'est pas dit ne peut pas être entendu.",
        "Ne remettez pas à demain ce qui vous libère aujourd'hui.",
    ],
    "couleur": ["bleu nuit", "ocre", "vert sauge", "bordeaux", "turquoise",
                "jaune moutarde", "gris perle", "corail", "violet", "ivoire"],
    "humeur": ["conquérante", "rêveuse", "sereine", "joueuse", "nostalgique",
               "électrique", "contemplative", "audacieuse"],
}

ELEMENTS = {
    "feu": {"trait": ["votre fougue", "votre enthousiasme", "votre impatience naturelle",
                      "votre audace"], "element_de": ["de feu"]},
    "terre": {"trait": ["votre sens pratique", "votre patience", "votre ténacité",
                        "votre besoin de sécurité"], "element_de": ["de terre"]},
    "air": {"trait": ["votre curiosité", "votre esprit vif", "votre goût de l'échange",
                      "votre légèreté"], "element_de": ["d'air"]},
    "eau": {"trait": ["votre intuition", "votre sensibilité", "votre imagination",
                      "votre empathie"], "element_de": ["d'eau"]},
}

PHASE_EFFETS = {
    "nouvelle": ["marque un nouveau départ", "est idéale pour poser vos intentions",
                 "invite au repos et à l'introspection"],
    "croissante": ["favorise les nouveaux projets", "donne de l'élan à vos intentions",
                   "nourrit votre ambition"],
    "pleine": ["amplifie vos émotions", "met en lumière ce qui était caché",
               "rend les nuits agitées"],
    "decroissante": ["invite au lâcher-prise", "est propice aux bilans",
                     "vous pousse à trier l'essentiel"],
}

# Effet d'un astre sur le signe : (harmonieux, tendu)
EFFETS = {
    "Soleil": (["donne de l'éclat à vos initiatives", "renforce votre confiance",
                "vous place sous les projecteurs"],
               ["met votre ego à l'épreuve", "vous pousse à forcer le passage",
                "attise les rivalités"]),
    "Lune": (["adoucit votre humeur", "favorise les moments en famille",
              "aiguise votre intuition"],
             ["rend votre humeur changeante", "réveille de vieilles susceptibilités",
              "met vos nerfs à fleur de peau"]),
    "Mercure": (["facilite les échanges", "favorise les démarches administratives",
                 "rend vos idées limpides"],
                ["brouille la communication", "multiplie les malentendus",
                 "complique les déplacements"]),
    "Vénus": (["adoucit les relations", "favorise les plaisirs simples",
               "embellit votre quotidien"],
              ["rend les cœurs exigeants", "pousse aux dépenses superflues",
               "fait naître quelques jalousies"]),
    "Mars": (["décuple votre énergie", "donne du courage à vos projets",
              "vous donne l'envie d'agir"],
             ["attise l'impatience", "rend les accrochages plus probables",
              "vous pousse à brûler les étapes"]),
    "Jupiter": (["ouvre des portes", "souffle un vent d'optimisme",
                 "élargit vos horizons"],
                ["pousse à l'excès", "gonfle les attentes",
                 "vous fait promettre plus que vous ne pourrez tenir"]),
    "Saturne": (["récompense vos efforts", "consolide ce que vous bâtissez",
                 "clarifie vos priorités"],
                ["ralentit vos projets", "vous rappelle à vos obligations",
                 "pèse sur votre moral"]),
    "Uranus": (["apporte une bonne surprise", "libère vos envies de changement",
                "stimule votre créativité"],
               ["bouscule vos plans", "provoque des imprévus",
                "rend l'atmosphère électrique"]),
    "Neptune": (["stimule votre imagination", "affine votre intuition",
                 "invite à la rêverie"],
                ["entretient le flou", "brouille vos repères",
                 "vous rend influençable"]),
    "Pluton": (["vous aide à tourner une page", "révèle votre force intérieure",
                "favorise une transformation profonde"],
               ["fait remonter des tensions enfouies", "met vos limites à l'épreuve",
                "intensifie les rapports de force"]),
}

CONSEILS_RETRO = {
    "Mercure": ["relisez tout deux fois", "vérifiez vos rendez-vous",
                "évitez de signer dans la précipitation"],
    "Vénus": ["les histoires passées refont surface", "évitez les achats coup de cœur",
              "prenez le temps de réévaluer vos attachements"],
    "Mars": ["canalisez votre énergie plutôt que de forcer",
             "ce n'est pas le moment de déclarer les hostilités",
             "finissez ce qui est commencé avant d'attaquer autre chose"],
}

NOMBRES = {3: "trois", 4: "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit"}

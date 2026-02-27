import random


AI_NAMES = [
    "LightningLeo",
    "SpeedySam",
    "TurboTom",
    "RapidRalf",
    "BlazeBen",
    "NitroNick",
    "ShadowSchumi"
]


def generate_ai_drivers(existing_players, min_ai=2, max_ai=11):
    ai_players = {}

    amount = random.randint(min_ai, max_ai)

    available_names = [
        name for name in AI_NAMES
        if name.lower() not in existing_players
    ]

    random.shuffle(available_names)

    for name in available_names[:amount]:
        key = name.lower()
        ai_players[key] = {
            "display": name,
            "pos": 0,
            "lap": 0,
            "is_ai": True,
            "speed": random.randint(1, 3)
        }

    return ai_players

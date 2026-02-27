import asyncio
import random

race_active = False
race_join_open = False
race_players = {}

TRACK_LENGTH = 30
AUTO_RACE_INTERVAL = 1380  # 23 Minuten


# =============================
# JOIN RACE (!g)
# =============================
async def join_race(user, send_chat):
    global race_active

    if not race_active:
        asyncio.create_task(start_race(send_chat))

    await asyncio.sleep(0.1)

    if not race_join_open:
        return

    key = user.lower()
    if key in race_players:
        return

    race_players[key] = {
        "display": user,
        "position": 0,
        "is_ai": False
    }

    await send_chat(f"✅ {user} ist dem Rennen beigetreten!")


# =============================
# START RACE
# =============================
async def start_race(send_chat):
    global race_active, race_join_open, race_players

    race_active = True
    race_join_open = True
    race_players = {}

    await send_chat("🏁 Autorennen startet! Tippe !g zum Mitfahren!")

    await asyncio.sleep(10)  # Join-Zeit

    race_join_open = False

    # IMMER KI hinzufügen
    add_ai_players()

    await send_chat("🚦 START!")

    winner = await run_race(send_chat)

    await send_chat(f"🏆 Gewinner: {race_players[winner]['display']}!")

    race_active = False


# =============================
# RENN-LOGIK
# =============================
async def run_race(send_chat):
    winner = None

    while not winner:
        await asyncio.sleep(1)

        status_line = ""

        for player in race_players:

            # KI etwas schneller machen
            if race_players[player]["is_ai"]:
                race_players[player]["position"] += random.randint(2, 4)
            else:
                race_players[player]["position"] += random.randint(1, 3)

            pos = race_players[player]["position"]
            status_line += f"{race_players[player]['display']}:{pos} "

            if pos >= TRACK_LENGTH:
                winner = player

        await send_chat(status_line.strip())

    return winner


# =============================
# KI SPIELER
# =============================
def add_ai_players():
    ai_names_pool = [
        "TurboTom",
        "BlitzBen",
        "SpeedySam",
        "NitroNina",
        "DriftDieter",
        "LightningLeo",
        "PhantomPaul",
        "RocketRalf"
    ]

    random.shuffle(ai_names_pool)

    ai_count = random.randint(2, 4)

    for i in range(ai_count):
        name = ai_names_pool[i]

        race_players[name.lower()] = {
            "display": name,
            "position": 0,
            "is_ai": True
        }


# =============================
# AUTO RENNEN (alle 23 Min)
# =============================
async def auto_race_loop(send_chat):
    while True:
        await asyncio.sleep(AUTO_RACE_INTERVAL)

        if not race_active:
            await start_race(send_chat)

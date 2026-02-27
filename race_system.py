import asyncio
import random

from .ai_system import generate_ai_drivers
from .commentator import (
    announce_start,
    announce_lap,
    announce_overtake,
    announce_winner,
)

race_active = False
race_join_open = False
race_players = {}

TRACK_LENGTH = 20
TOTAL_LAPS = 3
AUTO_RACE_INTERVAL = 180  # 3 Minuten


# =================================
# JOIN
# =================================
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
        "pos": 0,
        "lap": 0,
        "is_ai": False,
        "speed": random.randint(1, 3),
    }

    await send_chat(f"🏎 {user} ist dem Rennen beigetreten!")


# =================================
# START RACE
# =================================
async def start_race(send_chat):
    global race_active, race_join_open, race_players

    if race_active:
        return

    race_active = True
    race_join_open = True
    race_players = {}

    await send_chat("🏁 Autorennen startet! Tippe !g zum Mitfahren!")
    await asyncio.sleep(4)

    race_join_open = False

    # 🤖 KI generieren
    ai_players = generate_ai_drivers(race_players)
    race_players.update(ai_players)

    if ai_players:
        names = ", ".join([p["display"] for p in ai_players.values()])
        await send_chat(f"🤖 KI treten an: {names}")

    await send_chat("🚦 Die Ampeln gehen aus...")
    announce_start()

    await asyncio.sleep(2)

    await run_race(send_chat)


# =================================
# RACE LOOP (MIT RUNDENANZEIGE)
# =================================
async def run_race(send_chat):
    global race_active

    finished = False

    while not finished:
        await asyncio.sleep(2)

        for player in race_players.values():
            player["pos"] += player["speed"]

            # 🔄 Neue Runde erreicht
            if player["pos"] >= TRACK_LENGTH:
                player["lap"] += 1
                player["pos"] = 0

                # 🎙 Audio-Kommentar
                announce_lap(player["display"], player["lap"], TOTAL_LAPS)

                # 💬 Chat-Ausgabe
                await send_chat(
                    f"🏎 {player['display']} startet Runde {player['lap']} von {TOTAL_LAPS}!"
                )

                # 🔥 Dramatische letzte Runde
                if player["lap"] == TOTAL_LAPS:
                    await send_chat(
                        f"🔥 LETZTE RUNDE für {player['display']}!"
                    )

                # 🏆 Gewinner prüfen
                if player["lap"] >= TOTAL_LAPS:
                    finished = True
                    winner = player
                    break

    await send_chat(f"🏆 Gewinner: {winner['display']}")
    announce_winner(winner["display"])

    race_active = False


# =================================
# AUTO LOOP
# =================================
async def auto_race_loop(send_chat):
    while True:
        await asyncio.sleep(AUTO_RACE_INTERVAL)
        if not race_active:
            await start_race(send_chat)

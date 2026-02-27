import pyttsx3
import threading
import random

engine = pyttsx3.init()

# 🎙 F1 Kommentator Einstellungen
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
for voice in voices:
    if "german" in voice.id.lower() or "de" in voice.id.lower():
        engine.setProperty("voice", voice.id)
        break


def speak(text):
    def run():
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass

    threading.Thread(target=run, daemon=True).start()


# 🏁 F1 Events

def announce_start():
    lines = [
        "Und damit gehen die Lichter aus!",
        "Das Rennen ist freigegeben!",
        "Und das Feld setzt sich in Bewegung!"
    ]
    speak(random.choice(lines))


def announce_lap(player, lap, total_laps):
    if lap == total_laps:
        speak(f"Letzte Runde für {player}! Jetzt zählt jede Sekunde!")
    else:
        speak(f"{player} geht in Runde {lap}!")


def announce_overtake(player):
    lines = [
        f"{player} setzt zum Überholmanöver an!",
        f"Was für ein Move von {player}!",
        f"{player} kämpft sich nach vorne!"
    ]
    speak(random.choice(lines))


def announce_winner(player):
    speak(f"Und das ist der Sieg für {player}! Was für ein Rennen!")

import json
import os
from logger import log_info

STATS_FILE = "stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        log_info("Keine stats.json gefunden – neue wird erstellt.")
        return {}

    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

import json
from pathlib import Path

DATA_FILE = Path("data/store.json")

def load_store():
    with open(DATA_FILE) as f:
        return json.load(f)
    return {"decks": []}

def save_store(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
import json
from pathlib import Path
import uuid
from datetime import date

DATA_FILE = Path("data/store.json")

def load_store():
    if not DATA_FILE.exists():
        return {"decks": []}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_store(data):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    
def generate_id():
    return str(uuid.uuid4())
# decks
def add_deck(title):
    store = load_store()
    deck = {
        "id": generate_id(),
        "title":title,
        "cards":[]

    }
    store["decks"].append(deck)
    save_store(store)
    return deck

def get_decks():
    store = load_store()
    return store["decks"]

def delete_deck(deck_id):
    store = load_store()
    store["decks"] = [d for d in store["decks"] if d["id"] != deck_id]
    save_store(store)

def get_deck_by_id(deck_id):
    store = load_store()
    for deck in store["decks"]:
        if deck["id"] == deck_id:
            return deck
    return None

# cards

def add_card(deck_id, front, back):
    store = load_store()
    for deck in store["decks"]:
        if deck["id"] == deck_id:
            card = {
                "id": generate_id(),
                "front": front,
                "back": back,
                "tags": [],
                "difficulty": "medium",
                "date_created": str(date.today()),
                "srs": {
                    "interval": 1,
                    "ease_factor": 2.5,
                    "repetitions": 0,
                    "next_review": None,
                    "last_result": None
                }
            }
            deck["cards"].append(card)
            save_store(store)
            return card

def get_cards(deck_id):
    deck = get_deck_by_id(deck_id)
    if deck is None:
        return []
    return deck["cards"]

def delete_card(deck_id, card_id):
    store = load_store()
    for deck in store["decks"]:
        if deck["id"] == deck_id:
            deck["cards"] = [c for c in deck["cards"] if c["id"] != card_id]
            save_store(store)
            return
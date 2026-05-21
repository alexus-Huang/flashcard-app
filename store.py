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

def get_due_cards(deck_id):
    """
    return only the cards that are due for review today
    card is due if next_review date is today or ealier - compare date.today() against next_review field
    """
    store = load_store()
    deck_of_cards = get_deck_by_id(deck_id)
    if deck_of_cards is None:
        return []
    due_cards = []
    for each_card in deck_of_cards["cards"]:
        if each_card["srs"]["next_review"] is None:
            continue
        review_date = date.fromisoformat(each_card["srs"]["next_review"])
        if review_date <= date.today():
            due_cards.append(each_card)
    
    return due_cards
def show_card(card):
    """
    display the front of a card and wait for the user to press their enter that shows the back
    """
    print(card["front"])
    input("Press enter to see the answer...")
    print(card["back"])

def get_user_result():
    """
    after showing the answer, ask the user if they got it right or not
    returns true or false based on input - press 1 for correct and 2 for incorrect
    """
    while True:
        answer = input("Did you get it right?\n(1) Yes\n(2) No")
        if answer == "1":
            return True
        elif answer == "2":
            return False
        else:
            print("Please enter a valid choice")

def run_study_session(deck_id):
    # get due cards for the deck
    # if no cards are due then tell the user and exit
    # loop thorugh each card, show it, get the result,
    # at the end print a summary "3/5 correct"
    due_cards = get_due_cards(deck_id)
    total_cards = len(due_cards)
    correct_cards = 0
    if len(due_cards) == 0:
        print("No cards are due")
        return 
    for each_card in due_cards:
        show_card(each_card)
        user_result = get_user_result()
        if user_result:
            correct_cards +=1
    print(f"{correct_cards}/{total_cards} correct")   
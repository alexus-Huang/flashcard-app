from store import load_store, save_store, add_deck, get_decks, add_card, get_cards, delete_card, delete_deck


# add deck
deck = add_deck("Terms")
print("Created:", deck["title"])

# cards
add_card(deck["id"], "Hello", "A way of greeting someone")
add_card(deck["id"], "Bye", "Something to say when leaving")

# print cards
cards = get_cards(deck["id"])
print("Cards:", len(cards))
for card in cards:
    print(" -", card["front"], "->", card["back"])


from store import load_store, save_store

store = load_store()
print("Loaded:", store)

# test deck

# confirm test deck is in store.json
store = load_store()
print("Reloaded:", store["decks"][0]["title"])
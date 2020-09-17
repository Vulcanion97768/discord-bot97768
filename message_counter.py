class MessageCounter:
    def __init__(self):
        self.message_count = 0
        self.inventory_count = 0
        self.pokemon_available = True

    def add_to_count(self):
        self.message_count += 1
        self.inventory_count += 1

    def reset_count(self):
        self.message_count = 0

    def reset_inventory_count(self):
        self.inventory_count = 0

    



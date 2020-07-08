class MessageCounter:
    def __init__(self):
        self.message_count = 0

    def add_to_count(self):
        self.message_count += 1

    def reset_count(self):
        self.message_count = 0


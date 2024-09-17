class Memory:
    def __init__(self):
        self.history = ""

    def add_message(self, update: str):
        if not isinstance(update, str):
            raise ValueError("Message must be a string")
        self.history += update

    def get_history(self):
        return self.history

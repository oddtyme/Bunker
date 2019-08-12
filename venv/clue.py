
class Clue:

    # permanent constructor
    def __init__(self, clue, value, category, correct):
        self.clue = clue
        self.value = value
        self.category = category
        self.correct_response = correct

    def print(self):
        print(self.category)
        print(self.value)
        print(self.clue)
        print(self.correct_response)
        print("\n")

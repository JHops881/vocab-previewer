class Deck:

    class Card:

        def __init__(self, word: str) -> None:
            self.word: str                 = word
            self.word_pinyin: str          = ""
            self.word_translation: str     = ""
            self.sentence: str             = ""
            self.sentence_pinyin: str      = ""
            self.sentence_translation: str = ""

        def print(self) -> None:
            """Debug"""
            print(self.word)
            print(self.word_pinyin)
            print(self.word_translation)
            print(self.sentence)
            print(self.sentence_pinyin)
            print(self.sentence_translation)

    def __init__(self) -> None:
        self.cards: list[self.Card] = []

    def add_new_card(self, word: str) -> None:
        self.cards.append(self.Card(word))

    def print(self) -> None:
        for card in self.cards:
            print("\n")
            card.print()

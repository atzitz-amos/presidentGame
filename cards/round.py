class Round:

    def __init__(self):
        self.cards = []
        self.players = []

        self.folded = []

        self.first = None

    def add(self, cards, player):
        if not cards:
            self.folded.append(player)
            return
        if len([1 for card in cards if card == cards[0]]) != 1:
            raise ValueError("Duplicated card")
        if not all([card.value == cards[0].value for card in cards]):
            raise ValueError("All cards must have the same value")
        if not self.first:
            self.first = cards
        else:
            self.validate(cards)
        self.cards.append(cards)
        self.players.append((player, cards))

    def validate(self, cards):
        if len(cards) != len(self.first):
            raise ValueError("Invalid number of cards, expected %d, got %d" % (len(self.first), len(cards)))
        if self.cards[-1][0] > cards[0]:
            raise ValueError(f"Invalid cards, should be better or equal than `{self.cards[-1][0]}`")

    @property
    def winner(self):
        return self.players[-1][0]

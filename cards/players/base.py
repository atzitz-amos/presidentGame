import enum


class PlayerType(enum.Enum):
    BOT = "Bot"
    HUMAN = "Human"


class BasePlayer:
    """ Base interface for players """

    def __init__(self, name, ptype):
        self.name = name
        self.ptype = ptype

        self.hand = []
        self.position = None

    def deal_cards(self, cards):
        self.hand = cards

    def ask_cards(self, rd):
        return NotImplemented

    def notifyError(self, exc):
        raise NotImplementedError("Unhandled exception") from exc

    def assign(self, role):
        self.position = role

    @property
    def won(self):
        return not self.hand

    def __str__(self):
        return f"{self.name} ({self.ptype.value}){' [' + str(self.position) + ']' if self.position else ''}"

    __repr__ = __str__

    def best_cards(self, num):
        hand = list(sorted(self.hand, reverse=True))
        return hand[:num]

    def choose_exchange(self, num):
        raise NotImplementedError("Method `choose_exchange` was not implemented")

    def exchange(self, a, b):
        assert len(a) == len(b)
        for i in range(len(a)):
            self.hand.remove(a[i])
            self.hand.append(b[i])

    def notifyCard(self, player, cards):
        pass

    def notifyPlayer(self, player):
        pass

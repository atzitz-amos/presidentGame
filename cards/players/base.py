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
        self.hand.extend(cards)

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
        return f"{self.name} ({self.ptype.value})"

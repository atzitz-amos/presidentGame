import enum


class CardType(enum.Enum):
    HEARTS = 0
    DIAMONDS = 1
    SPADES = 2
    CLUBS = 3


class CardValue(enum.IntEnum):
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    AS = 1


class Card:
    __all = []

    def __new__(cls, ctype, value):
        for (t, v, i) in cls.__all:
            if t == ctype and v == value:
                return i
        inst = super().__new__(cls)
        cls.__all.append((ctype, value, inst))
        return inst

    def __init__(self, ctype, value):
        self.value = value
        self.ctype = ctype

    def __str__(self):
        return f"{self.value.name.title()} of {self.ctype.name}"

    __repr__ = __str__

    @staticmethod
    def deck():
        return list(Cards.all())

    def __eq__(self, other):
        return other.value == self.value and self.ctype == other.ctype

    def __or__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        """ C_7 > C_6 -> True"""
        return other.value > self.value

    def __lt__(self, other):
        return other.value < self.value

    def __ge__(self, other):
        return other.value >= self.value

    def __le__(self, other):
        return other.value <= self.value

    def __hash__(self):
        return hash(self.value)


class Cards:
    """ Holder for static instances of Card objects """
    SIX_OF_HEARTS = Card(CardType.HEARTS, CardValue.SIX)
    SEVEN_OF_HEARTS = Card(CardType.HEARTS, CardValue.SEVEN)
    EIGHT_OF_HEARTS = Card(CardType.HEARTS, CardValue.EIGHT)
    NINE_OF_HEARTS = Card(CardType.HEARTS, CardValue.NINE)
    TEN_OF_HEARTS = Card(CardType.HEARTS, CardValue.TEN)
    JACK_OF_HEARTS = Card(CardType.HEARTS, CardValue.JACK)
    QUEEN_OF_HEARTS = Card(CardType.HEARTS, CardValue.QUEEN)
    KING_OF_HEARTS = Card(CardType.HEARTS, CardValue.KING)
    AS_OF_HEARTS = Card(CardType.HEARTS, CardValue.AS)
    SIX_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.SIX)
    SEVEN_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.SEVEN)
    EIGHT_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.EIGHT)
    NINE_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.NINE)
    TEN_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.TEN)
    JACK_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.JACK)
    QUEEN_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.QUEEN)
    KING_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.KING)
    AS_OF_DIAMONDS = Card(CardType.DIAMONDS, CardValue.AS)
    SIX_OF_SPADES = Card(CardType.SPADES, CardValue.SIX)
    SEVEN_OF_SPADES = Card(CardType.SPADES, CardValue.SEVEN)
    EIGHT_OF_SPADES = Card(CardType.SPADES, CardValue.EIGHT)
    NINE_OF_SPADES = Card(CardType.SPADES, CardValue.NINE)
    TEN_OF_SPADES = Card(CardType.SPADES, CardValue.TEN)
    JACK_OF_SPADES = Card(CardType.SPADES, CardValue.JACK)
    QUEEN_OF_SPADES = Card(CardType.SPADES, CardValue.QUEEN)
    KING_OF_SPADES = Card(CardType.SPADES, CardValue.KING)
    AS_OF_SPADES = Card(CardType.SPADES, CardValue.AS)
    SIX_OF_CLUBS = Card(CardType.CLUBS, CardValue.SIX)
    SEVEN_OF_CLUBS = Card(CardType.CLUBS, CardValue.SEVEN)
    EIGHT_OF_CLUBS = Card(CardType.CLUBS, CardValue.EIGHT)
    NINE_OF_CLUBS = Card(CardType.CLUBS, CardValue.NINE)
    TEN_OF_CLUBS = Card(CardType.CLUBS, CardValue.TEN)
    JACK_OF_CLUBS = Card(CardType.CLUBS, CardValue.JACK)
    QUEEN_OF_CLUBS = Card(CardType.CLUBS, CardValue.QUEEN)
    KING_OF_CLUBS = Card(CardType.CLUBS, CardValue.KING)
    AS_OF_CLUBS = Card(CardType.CLUBS, CardValue.AS)

    @staticmethod
    def all():
        return [v for k, v in Cards.__dict__.items() if not k.startswith('__') and k != "all"]

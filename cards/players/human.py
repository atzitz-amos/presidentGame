from cards.card import CardType, CardValue, Card
from cards.players.base import BasePlayer, PlayerType
from cards.round import Round


class CMDHumanPlayer(BasePlayer):
    def choose_exchange(self, num):
        print("Your hand is:", self.hand)
        cards = []
        while len(cards) != num:
            cards = input(f"[Player {self}] Choose {num} cards to exchange: ").split()
        return list(map(self.get_card, cards))

    def __init__(self, name):
        BasePlayer.__init__(self, name, PlayerType.HUMAN)

    def remove_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def get_card(self, s):
        """EXPRESSED IN FORMAT <number><type>, ex. 2S(pade) T(en)Heart J(ack)D(iamond) A(s)C(lub)"""
        num, color = s
        num, color = num.upper(), color.upper()
        value = None
        ctype = None
        match num:
            case "T":
                value = 10
            case "J":
                value = 11
            case "Q":
                value = 12
            case "K":
                value = 13
            case "A":
                value = 1
            case _:
                value = int(num)
        match color:
            case "S":
                ctype = CardType.SPADES
            case "D":
                ctype = CardType.DIAMONDS
            case "H":
                ctype = CardType.HEARTS
            case "C":
                ctype = CardType.CLUBS
            case _:
                raise ValueError("Bad card color")
        value = [x for x in CardValue if x.value == value][0]
        return Card(ctype, value)

    def notifyError(self, exc):
        print("Error: ", exc.args[0])

    def ask_cards(self, rd):
        print("Your hand is", list(sorted(self.hand)))
        print("Last played:", self.format_last(rd))
        cards = list(map(self.get_card, input("Enter cards separated by spaces: ").split()))
        return cards

    def format_last(self, rd: Round):
        return ", ".join([str(x) for x in (rd.cards[-1] if rd.cards else [])])

    def assign(self, role):
        super(CMDHumanPlayer, self).assign(role)
        print(f"Assigned role {role} to player {self}")

    def exchange(self, a, b):
        super(CMDHumanPlayer, self).exchange(a, b)
        print(f"[{self}] Exchanged cards `{a}` and `{b}`")

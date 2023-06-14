from math import factorial

from cards.card import Cards, CardValue
from cards.players.base import BasePlayer, PlayerType


def C(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


class BotPlayer(BasePlayer):
    def choose_exchange(self, num):
        pass

    def __init__(self, name):
        BasePlayer.__init__(self, name, PlayerType.BOT)

        self.cards = []
        self.cards_players = {}

    def remove_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def notifyError(self, exc):
        print("Error: ", exc.args[0])

    def ask_cards(self, rd):
        pass

    def notifyCard(self, player, cards):
        self.cards.extend(cards)
        if player.name not in self.cards_players:
            self.cards_players[player.name] = []
        self.cards_players[player.name].append(cards)

    def assign(self, role):
        super(BotPlayer, self).assign(role)
        print(f"Assigned role {role} to bot {self}")

    def exchange(self, a, b):
        super(BotPlayer, self).exchange(a, b)
        print(f"[{self}] Exchanged cards `{a}` and `{b}`")

    def probability(self, card, amount, cards, split=3):
        if len(cards) < amount:
            return 0
        if amount > split:
            return 0
        return C(cards.count(card), amount) * C(len(cards) - cards.count(card), split - amount) / C(len(cards), split)

    def beatable_probability(self, card, amount, cards, split=3):
        card_values = [cv for cv in CardValue if cv < card]
        probability = 0
        if amount < 3:
            probability = self.probability(card, amount, cards, split)
        for value in card_values:
            probability += self.probability(value, amount, cards, split)
        return probability if probability < 1 else 1


if __name__ == '__main__':
    player = BotPlayer("B1")
    cs = Cards.all()
    # print(player.beatable_probability(CardValue.KING, 1, cs, split=9))
    print(player.beatable_probability(CardValue.JACK, 4, [v.value for v in cs], split=4))

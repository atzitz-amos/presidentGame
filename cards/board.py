import random

from cards.card import Card, Cards
from cards.players.human import HumanPlayer
from cards.roles import RolesHolder
from cards.round import Round


class NextRound(StopIteration):
    pass


class Board:

    def __init__(self, players):
        self.players = players
        self.current_turn = 0
        self.leading_player = None

        self.playing = False

        self.roles = RolesHolder(len(self.players))

        self.deck = Card.deck()

    def start(self):
        self.playing = True
        self.deal()
        while len([1 for p in self.players if not p.won]) > 1:
            self.play_turn()

    def deal(self):
        random.shuffle(self.deck)
        amount = len(self.deck) // len(self.players)
        for i, player in enumerate(self.players):
            player.deal_cards(self.deck[i * amount: (i + 1) * amount])
            print(f"dealt to player {player} cards {self.deck[i * amount: (i + 1) * amount]}")

    def play_turn(self):
        if not self.leading_player:
            if self.roles.LABOURER:
                self.leading_player = self.roles.LABOURER
            else:
                self.leading_player = [player for player in self.players if Cards.TEN_OF_HEARTS in player.hand][0]

        rd = Round()

        index = self.players.index(self.leading_player)
        while len(rd.folded) < len([p for p in self.players if not p.won]) - 1:
            player = self.players[index]
            if player.won or player in rd.folded:
                index += 1
                if index >= len(self.players):
                    index = 0
                continue

            print(f"Turn of player {player}")

            try:
                cards = player.ask_cards(rd)
                if not cards and not rd.cards:
                    raise ValueError("Leading player cannot fold")
                if not all([card in player.hand for card in cards]):
                    raise ValueError("Invalid cards, you do not have all of them")
                rd.add(cards, player)
            except ValueError as e:
                player.notifyError(e)
                continue

            player.remove_cards(cards)
            self.remove_cards(cards)

            if player.won:
                role = self.roles.queue(player)
                player.assign(role)
                print(f"Assigned role {role} to player {player}")

            if not cards:
                print(f"{player} folded, {len(rd.folded)} players are now folded")
            index += 1
            if index >= len(self.players):
                index = 0
            print("--------------------------------------------------------")

        self.leading_player = rd.winner
        print(f"Round finished, {self.leading_player} takes the round")
        i = self.players.index(self.leading_player)
        while self.leading_player.won:
            self.leading_player = self.players[i + 1]
            if i == len(self.players):
                i = 0

    def remove_cards(self, cards):
        for card in cards:
            self.deck.remove(card)


if __name__ == '__main__':
    board = Board([HumanPlayer("1"), HumanPlayer("2"), HumanPlayer("3"), HumanPlayer("4")])
    board.start()

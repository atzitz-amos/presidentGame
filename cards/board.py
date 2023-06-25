import random

from cards.card import Card, Cards
from cards.players.bot import BotPlayer
from cards.players.human import CMDHumanPlayer
from cards.roles import RolesHolder
from cards.round import Round


class NextRound(StopIteration):
    pass


class Board:

    def __init__(self, players, dummies=None):
        if dummies is None:
            dummies = []
        self.players = players
        self.current_turn = 0
        self.leading_player = None

        self.playing = False

        self.roles = RolesHolder(len(self.players))

        self.deck = Card.deck()

        self.dummies = []

    def play(self, last_roles=None):
        self.playing = True
        try:
            while True:
                self.play_turn(leading_player=last_roles.LABOURER if last_roles else None)
        except NextRound:
            return self.roles

    def deal(self):
        random.shuffle(self.deck)
        amount = len(self.deck) // len(self.players)
        for i, player in enumerate(self.players):
            player.deal_cards(self.deck[i * amount: (i + 1) * amount])
            print(f"dealt to player {player} cards {self.deck[i * amount: (i + 1) * amount]}")

    def play_turn(self, leading_player=None):
        if not self.leading_player:
            if leading_player:
                self.leading_player = leading_player
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

            print(f"<GeneralInfo>: Turn of player {player}")
            self.notify_dummies("turnOf", player=player)
            for pl in self.players:
                pl.notifyTurn(player)

            try:
                cards = player.ask_cards(rd)
                if not cards and not rd.cards:
                    raise ValueError("Leading player cannot fold")
                if not all([card in player.hand for card in cards]):
                    raise ValueError("Invalid cards, you do not have all of them")
                rd.add(cards, player)
                self.notify_dummies("playerPlayed", player=player, cards=cards)
                for pl in self.players:
                    pl.notifyCard(player, cards)
            except ValueError as e:
                player.notifyError(e)
                continue

            player.remove_cards(cards)
            self.remove_cards(cards)

            if player.won:
                role = self.roles.queue(player)
                player.assign(role)
                self.notify_dummies("playerWon", player=player)

            if not cards:
                print(f"{player} folded, {len(rd.folded)} players are now folded")
            index += 1
            if index >= len(self.players):
                index = 0
            print("--------------------------------------------------------")

        self.leading_player = rd.winner
        print(f"Round finished, {self.leading_player} takes the round")
        self.notify_dummies("roundFinished", winner=self.leading_player)
        i = self.players.index(self.leading_player)

        not_won = [p for p in self.players if not p.won]
        if len(not_won) == 1:
            not_won[0].assign(self.roles.queue(not_won[0]))
            self.notify_dummies("playerWon", player=not_won[0])
            print("Game finished")
            self.notify_dummies("gameFinished")
            print("President:", self.roles.PRESIDENT)
            if self.roles.VICE_PRESIDENT: print("Vice President:", self.roles.VICE_PRESIDENT)
            if self.roles.SERVITOR: print("Servitor:", self.roles.SERVITOR)
            print("Labourer:", self.roles.LABOURER)
            raise NextRound

        while self.leading_player.won:
            try:
                self.leading_player = self.players[i + 1]
            except IndexError:
                print(self.players, i)
                i = -1
                continue
            if i == len(self.players) - 1:
                i = -1

    def remove_cards(self, cards):
        for card in cards:
            self.deck.remove(card)

    def notify_dummies(self, event, **kwargs):
        for dummy in self.dummies:
            if callable(getattr(dummy, "event", None)):
                dummy.event(event, **kwargs)
            if callable(getattr(dummy, "on" + event.title(), None)):
                getattr(dummy, "on" + event.title())(**kwargs)


if __name__ == '__main__':
    board = Board([BotPlayer("Player 1"), CMDHumanPlayer("Player 2"), CMDHumanPlayer("Player 3"),
                   CMDHumanPlayer("Player 4")])
    board.deal()

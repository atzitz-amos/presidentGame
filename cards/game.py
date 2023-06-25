from cards.board import Board
from cards.players.bot import BotPlayer


class Game:

    def __init__(self, players, rounds=4):
        self.rounds_count = rounds

        self.players = players

        for player1 in players:
            for player2 in players:
                if player1 != player2:
                    player1.notifyPlayer(player2)

        self.rounds = []

        self.dummies = []

    def start(self):
        for round_num in range(self.rounds_count):
            self.play_round(Board(self.players, dummies=self.dummies), round_num=round_num)

    def play_round(self, board, round_num=0):
        board.deal()

        if len(self.rounds):
            president = self.rounds[-1].roles.PRESIDENT
            labourer = self.rounds[-1].roles.LABOURER

            while True:
                try:
                    best, worst = labourer.best_cards(2), president.choose_exchange(2)
                    president.exchange(worst, best)
                    labourer.exchange(best, worst)
                    break
                except Exception as e:
                    president.notifyError(e)

            if self.rounds[-1].roles.VICE_PRESIDENT:
                vice_president = self.rounds[-1].roles.VICE_PRESIDENT
                servitor = self.rounds[-1].roles.SERVITOR
                while True:
                    try:
                        best, worst = servitor.best_cards(1), vice_president.choose_exchange(1)
                        vice_president.exchange(worst, best)
                        servitor.exchange(best, worst)
                        break
                    except Exception as e:
                        vice_president.notifyError(e)

        board.play(last_roles=self.rounds[-1].roles if len(self.rounds) else None)
        self.rounds.append(board)

    def register_dummy(self, dummy):
        self.dummies.append(dummy)


if __name__ == '__main__':
    Game([BotPlayer("Player 1"), BotPlayer("Player 2"), BotPlayer("Player 3"),
          BotPlayer("Player 4")], rounds=2).start()

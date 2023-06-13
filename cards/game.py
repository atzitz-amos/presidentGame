from cards.board import Board
from cards.players.human import CMDHumanPlayer


class Score:

    def __init__(self, players):
        self.scores = {p.name: 0 for p in players}
        self.players = {p.name: p for p in players}

    def update(self, roles):
        if roles.PRESIDENT:
            self.scores[roles.PRESIDENT.name] += 2
        if roles.VICE_PRESIDENT:
            self.scores[roles.VICE_PRESIDENT.name] += 1
        if roles.MERCHANT:
            self.scores[roles.MERCHANT.name] += 0
        if roles.SERVITOR:
            self.scores[roles.SERVITOR.name] -= 1
        if roles.LABOURER:
            self.scores[roles.LABOURER.name] -= 2

    @property
    def winners(self):
        mv = max(self.scores.values())
        return [self.players[k] for k, v in self.scores.items() if v == mv]


class Game:

    def __init__(self, players, rounds=4):
        self.score = Score(players)
        self.rounds_count = rounds

        self.players = players

        self.rounds = []

    def start(self):
        for round_num in range(self.rounds_count):
            self.play_round(Board(self.players), round_num=round_num)

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

        self.score.update(board.play())
        self.rounds.append(board)


if __name__ == '__main__':
    Game([CMDHumanPlayer("Player 1"), CMDHumanPlayer("Player 2"), CMDHumanPlayer("Player 3"),
          CMDHumanPlayer("Player 4")], rounds=2).start()

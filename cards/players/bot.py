from math import factorial

from cards.card import Cards, CardValue
from cards.players.base import BasePlayer, PlayerType


def C(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


class BotPlayer(BasePlayer):
    def deal_cards(self, cards):
        super(BotPlayer, self).deal_cards(cards)

        self.cards = list(Cards.all())
        for card in cards:
            self.cards.remove(card)

    def choose_exchange(self, num):
        return list(sorted(self.hand))[:num]

    def __init__(self, name):
        BasePlayer.__init__(self, name, PlayerType.BOT)

        self.players = []

        self.cards_players = {}

    def remove_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def notifyError(self, exc):
        print("Error: ", exc.args[0])

    def ask_cards(self, rd):
        if not rd:
            return self.ask_cards_first()
        answers = self.possible_answers(rd[-1])
        if not answers:
            return []
        total_score = self.score_hand(self.hand)
        score_list = {total_score: []}
        print(f"[{self}] Hand: {list(sorted(self.hand))}")
        print("Score:", total_score)
        print("Answers:", answers)
        for answer in answers:
            c = self.hand.copy()
            [c.remove(a) for a in answer]
            score = self.score_hand(c)
            score_list[score] = answer
        print("Playing:", score_list[min(score_list)])
        return score_list[min(score_list)]

    def notifyPlayer(self, player):
        self.players.append(player)

    def notifyCard(self, player, cards):
        if player == self:
            return
        [self.cards.remove(card) for card in cards]
        if player.name not in self.cards_players:
            self.cards_players[player.name] = []
        self.cards_players[player.name].append(cards)

    def assign(self, role):
        super(BotPlayer, self).assign(role)
        print(f"Assigned role {role} to bot {self}")

    def possible_answers(self, last):
        c = last[0]
        amount = len(last)
        res = []
        already = []
        for card in self.hand:
            if card >= c and self.hand.count(card) >= amount and card.value not in already:
                res.append([ca for ca in self.hand if ca == card][:amount])
                already.append(card.value)
        return res

    def exchange(self, a, b):
        super(BotPlayer, self).exchange(a, b)
        print(f"[{self}] Exchanged cards `{a}` and `{b}`")

        for i in range(len(a)):
            self.cards.append(a[i])
            self.cards.remove(b[i])

    def probability(self, card, amount, cards, split=3):
        if cards.count(card) < amount or card not in cards:
            return 0
        if amount > split:
            return 0
        if len(cards) <= split:
            return 1
        return C(cards.count(card), amount) * C(len(cards) - cards.count(card), split - amount) / C(len(cards), split)

    def beatable_probability(self, card, amount, cards, split=3):
        card_values = [cv for cv in CardValue if cv < card]
        probability = 0
        if amount < 3:
            probability = self.probability(card, amount, cards, split)
        for value in card_values:
            probability += self.probability(value, amount, cards, split)
        return probability

    def score(self, card, amount):
        score = {}
        last_scores = {}
        for player in self.players:
            if len(player.hand) in last_scores:
                probability = last_scores[len(player.hand)]
            else:
                try:
                    probability = self.beatable_probability(card, amount, [c.value for c in self.cards],
                                                            split=len(player.hand))
                except Exception:
                    print(card, amount, [c.value for c in self.cards], len(player.hand))
                    raise
            last_scores[len(player.hand)] = probability
            score[player] = probability
        return score

    def score_hand(self, hand):
        final_score = 0
        data = {}
        hand = [c.value for c in hand]
        for card in set(hand):
            scores = self.score(card, hand.count(card))
            player_score = 0
            for player, score in scores.items():
                if player not in data:
                    data[player] = {}
                if score not in data[player]:
                    data[player][score] = []
                data[player][score].append((card, hand.count(card)))
                player_score += score
            final_score += player_score / len(scores)
        res = {}
        for player, scores in data.items():
            res[player] = [(scores[k], k) for k in sorted(scores)]

        return final_score

    def ask_cards_first(self):
        hand = sorted(self.hand)
        print("calculating first move with", hand)
        hand_amounts = []
        for card in hand:
            try:
                if card.value == hand_amounts[-1][0]:
                    hand_amounts[-1][1] += 1
                    continue
            except IndexError:
                pass
            hand_amounts.append([card.value, 1])
        best_openings = [
            [CardValue.KING, 4],
            [CardValue.QUEEN, 4],
            [CardValue.JACK, 4],
            [CardValue.TEN, 4],
            [CardValue.NINE, 4],
            [CardValue.EIGHT, 4],
            [CardValue.SEVEN, 4],
            [CardValue.KING, 3],
            [CardValue.KING, 2],
            [CardValue.QUEEN, 3],
            [CardValue.JACK, 3],
            [CardValue.KING, 1],
            [CardValue.QUEEN, 2],
            [CardValue.JACK, 2],
            [CardValue.QUEEN, 1],
            [CardValue.JACK, 1],
        ]

        for combination in best_openings:
            if combination in hand_amounts:
                print(hand_amounts)
                answer = [x for x in hand if x.value == combination[0]]
                break
        else:
            answer = [x for x in hand if x.value == hand[0].value]
        print("Playing:", answer)
        return answer

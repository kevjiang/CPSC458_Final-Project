import cards
import hands
import logging
import random
import preflop_sim

class GameState:
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

class Game(object):
    def __init__(self, playerbank, herobank):
        self.theDeck = cards.Deck()
        self.theDeck.shuffle()
        self.hero = cards.Hand()
        self.player = cards.Hand()
        self.table = cards.Hand()
        self.player_bankroll = playerbank
        self.hero_bankroll = herobank
        self.pot = 0
        self.player_is_big_blind = (random.random() > .5)
        self.small_blind = 1
        self.big_blind = 2
        self.state = GameState.PREFLOP

    def preflop(self):
        self.hero.add_card(self.theDeck.deal_card())
        self.hero.add_card(self.theDeck.deal_card())
        self.player.add_card(self.theDeck.deal_card())
        self.player.add_card(self.theDeck.deal_card())
        # sb first

    def flop(self):
        self.state = FLOP
        for i in range(3):
            self.table.add_card(self.theDeck.deal_card())
        # bb first

    def turn(self):
        self.state = TURN
        self.table.add_card(self.theDeck.deal_card())
        # bb first

    def river(self):
        self.state = RIVER
        self.table.add_card(self.theDeck.deal_card())
        # bb first

    def eval(self):
        return hands.compare_hands(self.player, self.hero, self.table)

    def end_game(self):
        res = hands.compare_hands(self.player, self.hero, self.table)
        if res == 'left':
            self.player += self.pot
            return 'You won with a ' + res[1]
        elif res == 'right':
            self.hero += self.pot
            return 'Hero won with a ' + res[1]
        else:
            self.player += self.pot/2
            self.hero += self.pot/2
            return 'The game was a tie.'
        return res

    def bankrolls(self):
        return (self.player_bankroll, self.hero_bankroll)

    def get_bets(self):
        pass

def basic_game():
    theDeck = cards.Deck()
    theDeck.shuffle()
    player = cards.Hand()
    big = cards.Hand()
    table = cards.Hand()

# Preflop
    big.add_card(theDeck.deal_card())
    big.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())

# Flop
    for i in range(3):
        table.add_card(theDeck.deal_card())
    logging.info(str(['flop', small.list_rep(), big.list_rep(), table.list_rep()]))

# Turn
    table.add_card(theDeck.deal_card())
    logging.info(str(['turn', small.list_rep(), big.list_rep(), table.list_rep()]))

# River
    table.add_card(theDeck.deal_card())
    logging.info(str(['table', small.list_rep(), big.list_rep(), table.list_rep()]))
    return hands.compare_hands(small, big, table)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    print basic_game()

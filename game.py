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

class Choice:
    CHECK_CALL = 0
    FOLD = 1
    RAISE 2

class Player(object):
    def __init__(self, hand, stack=100):
        self.hand = hand
        self.stack = stack
    # def


class Game(object):
    def __init__(self, playerbank, herobank):
        self.theDeck = cards.Deck()
        self.theDeck.shuffle()
        self.hero = cards.Hand()
        self.player = cards.Hand()
        self.table = cards.Hand()
        self.required = 0
        self.pot = 0
        self.player_is_big_blind = (random.random() > .5)
        self.small_blind = 1
        self.big_blind = 2
        self.state = GameState.PREFLOP

    def big_blind():
        if self.player_is_big_blind:
            return self.player
        else:
            return self.hero

    def littler_blind():
        if self.player_is_big_blind:
            return self.hero
        else:
            return self.player

    def parse_input(var):
        v = var.strip().split()
        if len(v) == 1:
            if v[0] == 'check':
                return game.Choice.CHECK_CALL
            elif v[0] == 'fold':
                return game.Choice.FOLD
        elif len(v) == 2:
            if v[0] == 'bet':
                n = int(v[1])
                if n > 0 and n < min(self.hero.stack, self.player.stack):
                    return (game.Choice.BET, n)
        raise ValueError('The input is invalid.')

    def player_decide():
        sys.stdout.write('\ncheck/fold/bet > ')
        val = parse_input(sys.stdin.readline())
        return val

    def hero_decide():
        val = preflop_player.play_preflop(self.hero, self.pot, self.required, self.hero.stack, not self.player_is_big_blind, False)
        return self.interpret(val)

    def preflop(self):
        self.hero.add_card(self.theDeck.deal_card())
        self.hero.add_card(self.theDeck.deal_card())
        self.player.add_card(self.theDeck.deal_card())
        self.player.add_card(self.theDeck.deal_card())

        self.pot = self.pot + self.big_blind + self.small_blind
        if self.player_is_big_blind:
            self.player.stack -= self.big_blind
            self.hero.stack -= self.small_blind
            self.required = self.big_blind - self.small_blind
            res = hero_decide()
            self.play()
        else:
            self.hero.stack -= self.big_blind
            self.player.stack -= self.small_blind
            self.required = self.big_blind - self.small_blind
            res = player_decide()
            self.play()


        self.required = val

        if self.interpret(val) == Choice.FOLD:
# end game
            return -1
        player_input()

        #while (val != ):
        #    preflop_player.play_preflop()

'''
    preflop alg:
        start with big blind: bb

        if bb call:
            done.
        if bb raise:
            if sb raise:
                if bb raise:
                    ...
            else if sb call
                done
            else
                fold
        else



        on : bb

        resp = X.resp
        while response is raise
            resp = X.resp
            X = other one
        if resp is call:
            if resp is check:
                while response is raise
                    resp = X.resp
                    X = other one
                ...
            ...
        if resp is fold:
            ...


pot
required
stacks
bet

'''

    def play(self, player, hero):
        first_player = ''
        response = get_response('first_player')
        while len(response) > 0: # raise
            self.pot += self.required
            self.required = 0
            bet_amt = response[1]
            self.required += bet_amt
            first_player.stack
`

        # sb first
    def interpret(self, val):
        if val < self.required:
            print "Hero has folded."
            return Choice.FOLD
        if val == self.required:
            print "Hero has checked"
            return Choice.CHECK_CALL
        else:
            print "Hero has raised by " + str(val - self.required)
            return (Choice.RAISE, (val - self.required))

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

    def stacks(self):
        return (self.player.stack, self.hero.stack)

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

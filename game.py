import cards
import hands
import logging
import random
import preflop_sim
import preflop_player
import sys

class Round:
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3

class State(object):
    def __init__(self, hero, human):
        self.deck = cards.Deck()
        self.deck.shuffle()
        self.table = cards.Hand()
        self.pot = 0
        self.big_blind, self.small_blind = random.sample((hero, human), 2)
        self.small_blind_val = 1
        self.big_blind_val = 2
        self.round = Round.PREFLOP

    def __str__(self):
        return str((self.required(), self.pot, self.big_blind.stack, self.big_blind.escrow, self.small_blind.stack, self.small_blind.escrow))

    def clear_ecrows(self):
        esc = min(self.big_blind.escrow, self.small_blind.escrow)
        self.big_blind.escrow -= esc
        self.small_blind.escrow -= esc
        self.pot += 2 * esc

    def required(self):
        return abs(self.big_blind.escrow - self.small_blind.escrow)

class Player(object):
    def __init__(self, hand, stack=100):
        self.hand = hand
        self.stack = stack
        self.escrow = 0

    def push(self, state, amt):
        self.stack -= amt
        self.escrow += amt

class Human(Player):
    def __init__(self, hand, stack=100):
        Player.__init__(self, hand, stack)
        self.name = 'Human'

    def parse_input(self, var):
        v = var.strip().split()
        if len(v) != 1:
            return None
        return int(v[0])
    def get_next(self, state, hero, min_bet, max_bet):
        # print the table state
        '''
            Finds a move that isnt malformed
        '''
        out = None
        while out == None:
            sys.stdout.write('\nPlayer descision {-1, [' + str(min_bet) +', ' + str(max_bet) + ']} > ')
            out = self.parse_input(sys.stdin.readline())
            if out == None:
                print 'Malformed descision'
        return out

class Hero(Player):
    def __init__(self, hand, stack=100):
        Player.__init__(self, hand, stack)
        self.name = 'Hero'
    def get_next(self, state, human, min_bet, max_bet):
        val = preflop_player.play_preflop(
                self.hand, state.pot / 2 + self.escrow, state.required(),
                state.big_blind_val, self.stack,
                self == state.big_blind, self == state.small_blind)
        logging.info((
                val,
                self.hand, state.pot / 2 + self.escrow, state.required(),
                state.big_blind_val, self.stack,
                self == state.big_blind, self == state.small_blind                ))
        return val


class Game(object):
    def __init__(self, human_stack, hero_stack):
        self.hero = Hero(cards.Hand(), hero_stack)
        self.human = Human(cards.Hand(), human_stack)
        self.state = State(self.hero, self.human)

    def play_game(self):
        r = self.preflop()
        if r != -1:
            self.end_game()
        return self.stacks()

    def other_player(self, player):
        if player == self.hero:
            return self.human
        elif player == self.human:
            return self.hero
        else:
            return None

    def get_move(self, player):
        max_bet = min(self.hero.stack, self.human.stack)
        min_bet = self.state.required()
        bet_valid = False
        bet = 0
        while not bet_valid:
            bet = player.get_next(self.state, self.other_player(player), min_bet, max_bet)
            if bet < min_bet:
                self.fold(player)
                return (bet, min_bet)
                # print 'Bet of ' + str(bet) + ' too low. The minimum is', min_bet
            elif bet > max_bet:
                print 'Bet of ' + str(bet) + ' too high. The maximum is', max_bet
            else:
                bet_valid = True

        player.push(self.state, bet)

        if bet == 0:
            print player.name + ' has checked'
        elif bet == min_bet:
            print player.name + ' has called'
        else:
            print player.name + ' raised to ' + str(bet)
        return (bet, min_bet)

    def preflop(self):
        self.hero.hand.add_card(self.state.deck.deal_card())
        self.hero.hand.add_card(self.state.deck.deal_card())
        self.human.hand.add_card(self.state.deck.deal_card())
        self.human.hand.add_card(self.state.deck.deal_card())

        if self.human == self.state.small_blind:
            print 'You are small blind.'
        else:
            print 'You are big blind.'

        print 'Your hand is', self.human.hand

        # coordinate blinds
        self.state.small_blind.push(self.state, self.state.small_blind_val)
        logging.info(self.state)
        self.state.big_blind.push(self.state, self.state.big_blind_val)
        logging.info(self.state)

        # get small blind move first
        person = self.state.small_blind
        move, min_bet = self.get_move(person)
        logging.info(move)
        raised = False
        while move > min_bet:
            person = self.other_player(person)
            move, min_bet = self.get_move(person)
        if move < min_bet:
            return -1

        logging.info(self.state)
        self.state.clear_ecrows()
        logging.info(('hi', str(self.state), self.human.stack, self.hero.stack))



    def fold(self, loser):
        print loser.name + ' has folded.'
        winner = self.other_player(loser)
        winner.stack += loser.escrow
        winner.stack += winner.escrow
        winner.stack += self.state.pot
        logging.info(('hi', str(self.state)))

    def end_game(self):
        while len(self.state.table.cards) < 5:
            self.state.table.add_card(self.state.deck.deal_card())

        res, reason = hands.compare_hands(self.human.hand, self.hero.hand, self.state.table)
        winner = None
        if res == 'left':
            winner = self.human
        elif res == 'right':
            winner = self.hero
        else:
            self.human += self.state.pot / 2.0
            self.hero += self.state.pot / 2.0
            print 'The game was a tie.'
            print 'Hero had', self.hero.hand
            return

        loser = self.other_player(winner)
        print winner.name + ' has won the round with a ' + reason
        print 'Hero had', self.hero.hand
        winner.stack += loser.escrow
        winner.stack += winner.escrow
        winner.stack += self.state.pot
        logging.info(('hi', str(self.state)))

    def stacks(self):
        return (self.human.stack, self.hero.stack)


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
#
#     def flop(self):
#         self.state = FLOP
#         for i in range(3):
#             self.table.add_card(self.theDeck.deal_card())
#         # bb first
#
#     def turn(self):
#         self.state = TURN
#         self.table.add_card(self.theDeck.deal_card())
#         # bb first
#
#     def river(self):
#         self.state = RIVER
#         self.table.add_card(self.theDeck.deal_card())
#         # bb first
#
#     def eval(self):
#         return hands.compare_hands(self.player, self.hero, self.table)
#
#     def end_game(self):
#         res = hands.compare_hands(self.player, self.hero, self.table)
#         if res == 'left':
#             self.player += self.pot
#             return 'You won with a ' + res[1]
#         elif res == 'right':
#             self.hero += self.pot
#             return 'Hero won with a ' + res[1]
#         else:
#             self.player += self.pot/2
#             self.hero += self.pot/2
#             return 'The game was a tie.'
#         return res



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

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
    def __init__(self, hero, human, blinds, rounds):
        self.deck = cards.Deck()
        self.deck.shuffle()
        self.table = cards.Hand()
        self.pot = 0
        if rounds % 2:
            self.big_blind, self.small_blind = (hero, human)
        else:
            self.big_blind, self.small_blind = (human, hero)
        self.small_blind_val = blinds[0]
        self.big_blind_val = blinds[1]
        self.round = Round.PREFLOP
        self.first_bet = None

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
            sys.stdout.write('\nHuman decision {-1, [' + str(min_bet) +', ' + str(max_bet) + ']} -> ')
            out = self.parse_input(sys.stdin.readline())
            print ''
            if out == None:
                print 'Malformed decision'
        return out

class Hero(Player):
    def __init__(self, hand, stack=100):
        Player.__init__(self, hand, stack)
        self.name = 'Hero'
    def get_next(self, state, human, min_bet, max_bet):
        val = None
        money_in = self.escrow + state.pot/2
        money_required = max(self.escrow, human.escrow) + state.pot/2
        logging.info(('first bet', state.first_bet))
        if state.round == Round.PREFLOP:
            val = preflop_player.play_preflop(
                    self.hand,
                    money_in,
                    money_required,
                    state.big_blind_val,
                    max_bet,
                    self == state.big_blind,
                    state.first_bet)
        elif state.round == Round.FLOP:
            val = preflop_player.play_afterflop(
                    self.hand,
                    state.table,
                    money_in,
                    money_required,
                    state.big_blind_val,
                    max_bet,
                    self == state.big_blind, # no
                    state.first_bet)# no
        elif state.round == Round.TURN:
            val = preflop_player.play_turn(
                    self.hand,
                    state.table,
                    money_in,
                    money_required,
                    state.big_blind_val,
                    max_bet,
                    self == state.big_blind, # no
                    state.first_bet) # no
        elif state.round == Round.RIVER:
            val = preflop_player.play_river(
                    self.hand,
                    state.table,
                    money_in,
                    money_required,
                    state.big_blind_val,
                    max_bet,
                    self == state.big_blind, # no
                    state.first_bet) # no
        return val


class Game(object):
    def __init__(self, human_stack, hero_stack, blinds, rounds):
        self.hero = Hero(cards.Hand(), hero_stack)
        self.human = Human(cards.Hand(), human_stack)
        self.state = State(self.hero, self.human, blinds, rounds)

    def play_game(self):
        r = self.preflop()
        if r != -1:
            r = self.deal_and_play(3)
        if r != -1:
            r = self.deal_and_play(1)
        if r != -1:
            r = self.deal_and_play(1)
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
        other = self.other_player(player)
        max_bet = min(player.stack, other.stack + other.escrow - player.escrow)
        min_bet = min(self.state.required(), max_bet)
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
        self.state.first_bet = True
        move, min_bet = self.get_move(person)
        self.state.first_bet = False
        logging.info(move)
        bb_gone = False
        if move < min_bet:
            return -1
        while (not bb_gone) or move > min_bet:
            person = self.other_player(person)
            move, min_bet = self.get_move(person)
            bb_gone = True
        if move < min_bet:
            return -1

        logging.info(self.state)
        self.state.clear_ecrows()
        logging.info(('hi', str(self.state), self.human.stack, self.hero.stack))
        self.state.round += 1

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

    def deal_and_play(self, n=1):
        for i in xrange(n):
            self.state.table.add_card(self.state.deck.deal_card())

        print 'The cards', self.state.table, 'are now on the table.'

        # big blind move first
        person = self.state.big_blind
        self.state.first_bet = True
        move, min_bet = self.get_move(person)
        logging.info(move)
        sb_gone = False
        self.state.first_bet = False
        if move < min_bet:
            return -1
        while (not sb_gone) or move > min_bet:
            person = self.other_player(person)
            move, min_bet = self.get_move(person)
            sb_gone = True
        if move < min_bet:
            return -1

        logging.info(self.state)
        self.state.clear_ecrows()
        logging.info(('hi', str(self.state), self.human.stack, self.hero.stack))
        self.state.round += 1

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    print basic_game()

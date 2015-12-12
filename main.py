import cards
import hands
import logging
import sys
import time
import game

def parse_input(var):
    v = var.strip().split()
    if len(v) == 1:
        if v[0] == 'check':
            return 'check'
        elif v[0] == 'fold':
            return 'fold'
    elif len(v) == 2:
        if v[0] == 'bet':
            n = int(v[1])
            if n > 0 and n < 100:
                return ('bet', n)
    return 'invalid'

if __name__ == '__main__':
    k = 0
    try:
        print '''
            This is the heads up poker player!

            You are playing against a single opponent.
            Each of you have $100.

            The blinds are 1, 2.

            You are the small blind.

            These are your options:
                check
                fold
                bet number

        '''
        # start_game
        gm = game.Game()
        gm.preflop()
        print 'Your ' + str(gm.small)
        sys.stdout.write('> ')
# preflop
        val = parse_input(sys.stdin.readline())
        sys.stdout.write('> ')
# flop
        val = parse_input(sys.stdin.readline())
        sys.stdout.write('> ')
# turn
        val = parse_input(sys.stdin.readline())
        sys.stdout.write('> ')
# river
        val = parse_input(sys.stdin.readline())
    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

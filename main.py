import cards
import hands
import logging
import sys
import time
import game
import preflop_sim

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
    raise ValueError('The input is invalid.')

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
        print 'Your ', gm.small
        print 'Your preflop strngth is ', preflop_sim.getPreflopStrength(gm.small)

        sys.stdout.write('\nPreflop choice > ')
        val = parse_input(sys.stdin.readline())


        gm.flop()
        print gm.table

        sys.stdout.write('\nFlop choice    > ')
        val = parse_input(sys.stdin.readline())

        gm.turn()
        print gm.table

        sys.stdout.write('\nTurn choice    > ')
        val = parse_input(sys.stdin.readline())

        gm.river()
        print gm.table

        sys.stdout.write('\nRiver choice   > ')
        val = parse_input(sys.stdin.readline())
    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

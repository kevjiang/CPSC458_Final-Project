import cards
import hands
import logging
import sys
import time
import game

def parse_input(var):
    return 'sdf'

if __name__ == '__main__':
    k = 0
    try:
        print '''
            Here's some instructions...
            Lolcats

        '''
        # start_game
        gm = game.Game()
        gm.preflop()
        print 'Your ' + str(gm.small)
        sys.stdout.write('> ')
        preflop = sys.stdin.readline()
        sys.stdout.write('> ')
        flop = sys.stdin.readline()
        sys.stdout.write('> ')
        turn = sys.stdin.readline()
        sys.stdout.write('> ')
        river = sys.stdin.readline()
    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

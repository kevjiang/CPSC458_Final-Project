import cards
import hands
import logging
import sys
import time
import game
import preflop_sim
import random

def parse_input(var):
    v = var.strip().split()
    if len(v) == 1:
        if v[0] == 'check':
            return game.Choice.CHECK
        elif v[0] == 'fold':
            return game.Choice.FOLD
    elif len(v) == 2:
        if v[0] == 'bet':
            n = int(v[1])
            if n > 0 and n < min(hero_bankroll, player_bankroll):
                return (game.Choice.BET, n)
    raise ValueError('The input is invalid.')

if __name__ == '__main__':
    rounds = 0
    player_bankroll = 100
    hero_bankroll = 100
    try:
        print '''
            This is the heads up poker player!

            You are playing against a single opponent.
            Each of you have $100.

            The blinds are 1, 2.

            You are the small blind.

            To play, use the following format:
            These are your options:
                check           -- this calls or checks
                fold            -- this folds your hand
                bet number      -- this bets (number) dollars
        '''

        print ' You have ' + player_bankroll +  ' dollars and hero has ' +  hero_bankroll + ' dollars.'

        # start_game
        gm = game.Game(player_bankroll, hero_bankroll)
        gm.preflop()
        # fold, endgame.

        sys.stdout.write('\ncheck/fold/bet > ')
        val = parse_input(sys.stdin.readline())

        gm.flop()
        print 'The table contains: ', gm.table

        sys.stdout.write('\nFlop choice    > ')
        val = parse_input(sys.stdin.readline())

        gm.turn()
        print 'The table contains: ', gm.table

        sys.stdout.write('\nTurn choice    > ')
        val = parse_input(sys.stdin.readline())

        gm.river()
        print 'The table contains: ', gm.table

        sys.stdout.write('\nRiver choice   > ')
        val = parse_input(sys.stdin.readline())

        print gm.end_game()

        player_bankroll, hero_bankroll = gm.bankrolls()


    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

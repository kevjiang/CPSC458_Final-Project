import cards
import hands
import logging
import sys
import time
import game
import preflop_sim
import random


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')
    rounds = 1
    try:
        print '''
           __  ___________    ____  _____    __  ______  __
  __/|_   / / / / ____/   |  / __ \/ ___/   / / / / __ \/ /  __/|_
 |    /  / /_/ / __/ / /| | / / / /\__ \   / / / / /_/ / /  |    /
/_ __|  / __  / /___/ ___ |/ /_/ /___/ /  / /_/ / ____/_/  /_ __|
 |/    /_/ /_/_____/_/  |_/_____//____/   \____/_/   (_)    |/


            You are playing against a single opponent named Hero.
            Each of you have $100.

            The blinds are $1 and $2.

            To play, use the following format:
            These are your options:

                anything < min_bet        --    fold
                0                         --    check
                [min_bet ... max_bet]     --    raise or call
        '''

        human_stack = 100
        hero_stack = 100
        while hero_stack > 0 and human_stack > 0:
            print '================================================================================ '
            print '             Round ' + str(rounds)

            print ' You have ' + str(human_stack) +  \
                    ' dollars and hero has ' +  str(hero_stack) + ' dollars.'

            # start_game
            gm = game.Game(human_stack, hero_stack)
            gm.play_game()
            human_stack, hero_stack = gm.stacks()

        print 'game over'



    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

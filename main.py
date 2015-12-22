import cards
import hands
import logging
import sys
import time
import game
import preflop_sim
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(message)s')
    rounds = 1
    try:
        print bcolors.OKBLUE + '''
           __  ___________    ____  _____    __  ______  __
  __/|_   / / / / ____/   |  / __ \/ ___/   / / / / __ \/ /  __/|_
 |    /  / /_/ / __/ / /| | / / / /\__ \   / / / / /_/ / /  |    /
/_ __|  / __  / /___/ ___ |/ /_/ /___/ /  / /_/ / ____/_/  /_ __|
 |/    /_/ /_/_____/_/  |_/_____//____/   \____/_/   (_)    |/

        ''' + bcolors.ENDC

        print '''
            Let's play some no limit texas hold'em!

            You are playing against a single opponent named Hero.

            To play, use the following format:
            These are your options:

                anything < min_bet        --    fold
                0                         --    check
                [min_bet ... max_bet]     --    raise or call
        '''

        human_stack = 300
        hero_stack = 300
        blinds = (5, 10)

        print 'The big blind is', blinds[1], 'and the little blind is', blinds[0]
        while hero_stack > 0 and human_stack > 0:
            print '================================================================================ '
            print '             Round ' + str(rounds)

            print 'You have ' + str(human_stack) +  \
                    ' dollars and hero has ' +  str(hero_stack) + ' dollars.'

            # start_game
            gm = game.Game(human_stack, hero_stack, blinds, rounds)
            gm.play_game()
            human_stack, hero_stack = gm.stacks()
            rounds += 1

        print 'game over'



    except KeyboardInterrupt:
       sys.stdout.flush()
       pass

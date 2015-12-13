import cards
import hands
import preflop_sim

# returns bet size of small blind, with -1 being fold
# small_blind is true if small blind, false if big blind or reraise
# position is False if small blind player, True if big blind player
# stack size is smallest stack on the table
# money in is money already on the table (small blind)
# money required is how much to call
def play_preflop(hand, money_in, money_required, stack_size, position = False, small_blind = True):
  return money_required - money_in # this just calls
    

#def play_preflop(hand, small_blind, big_blind, stack_size, position = False, which_blind = True):
#  kPositionAdvantage = .025
#  kPositionDisadvantage = .026
#  hand_strength = getPreflopStrength(hand)
#  win_ratio = hand_strength[0] / hand_strength[2]
#  if small_blind:
    

import cards
import hands
import preflop_sim

import random

# returns bet size of small blind, with -1 being fold
# small_blind is true if small blind, false if big blind or reraise
# position is False if small blind player, True if big blind player
# stack size is smallest stack on the table
# money in is money already on the table (small blind)
# money required is how much to call
#def play_preflop(hand, money_in, money_required, stack_size, position = False, small_blind = True):
#  return money_required - money_in # this just calls
    

# write this later to include a random factor
def randomPermute(value, random_factor):
  factor = 1
  if random.random() < .5:
    factor = -1

  return (random.random() * random_factor * factor + 1) * value

def play_preflop(hand, money_in, money_required, big_blind, stack_size, position = False, small_blind = True):
  kPositionAdvantage = .025
  kPositionDisadvantage = .025
  kRandomFactor = .1 # max value of random factor
  kUndercut = .33 # chance that hero bets small with a really good hand
  kLimp = .2 # chance that hero limps in with a poor hand
  kGoodHand = .075 # really good hand differential
  kConstantBetFactor = .75
  kBetFactor = 9 
  kCallPercent = .3 # percent of big blind that the raise is for us just to call
  kLowHandFactor = .1
  kLowHandConstant = .035 # makes it more likely to play jacks and 10s
  kReallyGoodRatio = .55
  final_bet = 0

  hand_strength = preflop_sim.getPreflopStrength(hand)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  cost_benefit_ratio = (money_required - money_in) / float(money_required)
  if position:
    win_ratio = win_ratio * (1 + kPositionAdvantage)
  else:
    win_ratio = win_ratio * (1 - kPositionDisadvantage)

  if small_blind:
    if win_ratio > cost_benefit_ratio:
      # bluff by calling with a really good hand
      if win_ratio - cost_benefit_ratio > kGoodHand:
        if random.random() < kUndercut:
          final_bet = money_required - money_in

      bet = (win_ratio - cost_benefit_ratio) * kBetFactor * big_blind + big_blind * kConstantBetFactor + money_required - money_in
      bet = randomPermute(bet, kRandomFactor)
      if bet - money_required < kCallPercent * big_blind:
        final_bet = money_required - money_in
      else:
        final_bet = int(bet) - money_in
    else:
      win_ratio = randomPermute(win_ratio, kLowHandFactor)
      if win_ratio + kLowHandConstant > cost_benefit_ratio or random.random() < kLimp:
        final_bet = money_required - money_in
      else:
        final_bet = -1
  else:
    if win_ratio > kReallyGoodRatio:
      final_bet = stack_size - money_in
      # do stuff here like bet a lot

    # recalculate win ratio - be a little generous
    if cost_benefit_ratio < win_ratio:
      final_bet = money_required - money_in
      # basically stretch this shit out - low hands only bet when cost_benefit_ratio is really low and high hands can be adjusted higher
      #adjust it on a scale of like .3 to .7
      # check if they're betting a lot - scary

    else:
      final_bet = -1

    #if win_ratio > cost_benefit_ratio:
    # risk that his cards are better than mine -> possible fold


  # this is just to make sure we're not overambitious with betting
  if final_bet > (stack_size - money_in):
    return stack_size - money_in
  else:
    return final_bet

# note: money_in == money_required when first_bet == True
def play_afterflop(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  # find flags here - like multiple suited and straight draws
  # find straight and flush outs
  # find what i have w/ win percentages
  cost_benefit_ratio = (money_required - money_in) / float(money_required)
  return money_required - money_in

def play_turn(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  return money_required - money_in

def play_river(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  return money_required - money_in

theDeck = cards.Deck()
theDeck.shuffle()
hand = cards.Hand()
hand.add_card(theDeck.deal_card())
hand.add_card(theDeck.deal_card())
print hand
print play_preflop(hand, 5, 10, 10, 300, False, True)

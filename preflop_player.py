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

def play_preflop(hand, money_in, money_required, stack_size, position = False, small_blind = True):
  kPositionAdvantage = .025
  kPositionDisadvantage = .025
  kRandomFactor = .1 # max value of random factor
  kUndercut = .33 # chance that hero bets small with a really good hand
  kLimp = .2 # chance that hero limps in with a poor hand
  kGoodHand = .075 # really good hand differential
  kBigBlind = 10
  kConstantBetFactor = .75
  kBetFactor = 9 
  kCallPercent = .3 # percent of big blind that the raise is for us just to call
  kLowHandFactor = .1
  kLowHandConstant = .035 # makes it more likely to play jacks and 10s

  hand_strength = preflop_sim.getPreflopStrength(hand)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  cost_benefit_ratio = (money_required - money_in) / float(money_required)
  if small_blind:
    if position:
      win_ratio = win_ratio * (1 + kPositionAdvantage)
    else:
      win_ratio = win_ratio * (1 - kPositionDisadvantage)

    if win_ratio > cost_benefit_ratio:
      # bluff by calling with a really good hand
      if win_ratio - cost_benefit_ratio > kGoodHand:
        if random.random() < kUndercut:
          return money_required - money_in

      bet = (win_ratio - cost_benefit_ratio) * kBetFactor * kBigBlind + kBigBlind * kConstantBetFactor + money_required - money_in
      bet = randomPermute(bet, kRandomFactor)
      if bet - money_required < kCallPercent * kBigBlind:
        return money_required - money_in
      return int(bet) - money_in
    else:
      win_ratio = randomPermute(win_ratio, kLowHandFactor)
      if win_ratio + kLowHandConstant > cost_benefit_ratio or random.random() < kLimp:
        return money_required - money_in
      else:
        return -1
  else:
    return money_required - money_in

theDeck = cards.Deck()
theDeck.shuffle()
hand = cards.Hand()
hand.add_card(theDeck.deal_card())
hand.add_card(theDeck.deal_card())
print hand
print play_preflop(hand, 5, 10, 300, False, True)

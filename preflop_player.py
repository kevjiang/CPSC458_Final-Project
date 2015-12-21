import cards
import hands
import preflop_sim
import afterflop_sim
import afterturn_sim
import afterriver_sim

import random

kPositionAdvantage = .025
kPositionDisadvantage = .025
kRandomFactor = .1 # max value of random factor


# returns bet size of small blind, with -1 being fold
# small_blind is true if small blind, false if big blind or reraise
# position is False if small blind player, True if big blind player
# stack size is smallest stack on the table
# money in is money already on the table (small blind)
# money required is how much to call
# write this later to include a random factor
def randomPermute(value, random_factor):
  factor = 1
  if random.random() < .5:
    factor = -1

  return (random.random() * random_factor * factor + 1) * value

def play_preflop(hand, money_in, money_required, big_blind, stack_size, position = False, small_blind = True):
  kUndercut = .33 # chance that hero bets small with a really good hand
  kLimp = .2 # chance that hero limps in with a poor hand
  kGoodHand = .1 # really good hand differential
  kBetFactor = 4
  kConstantBetFactor = .75
  kCallPercent = .3 # percent of big blind that the raise is for us just to call
  kLowHandConstant = .08 # makes it more likely to play beter hands
  kStretchFactor = 1.2
  kGoodRatio = .60
  kReallyGoodRatio = .66
  final_bet = 0

  hand_strength = preflop_sim.getPreflopStrength(hand)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  cost_benefit_ratio = (money_required - money_in) / float(money_required)

  # correcting for advantageous position
  if position:
    win_ratio = win_ratio * (1 + kPositionAdvantage)
  else:
    win_ratio = win_ratio * (1 - kPositionDisadvantage)

  if small_blind:
    if win_ratio > cost_benefit_ratio:
      # 'bluff' by calling with a really good hand
      if random.random() < kUndercut:
        final_bet = money_required - money_in

      else:
        bet = (win_ratio + kConstantBetFactor) * big_blind + money_required - money_in
        bet = randomPermute(bet, kRandomFactor)
        if bet - money_required < kCallPercent * big_blind:
          final_bet = money_required - money_in
        else:
          final_bet = int(bet) - money_in
    else:
      win_ratio = randomPermute(win_ratio, kRandomFactor)
      if win_ratio + kLowHandConstant > cost_benefit_ratio or random.random() < kLimp:
        final_bet = money_required - money_in
      else:
        final_bet = -1
  else:
    # use random_permute to sometimes play slightly worse hands as good hands
    if randomPermute(win_ratio, kRandomFactor) > kGoodRatio:
      if random.random() < kUndercut:
        final_bet = money_required - money_in
      else:
        tentative_bet = (win_ratio + kConstantBetFactor) * big_blind + win_ratio * (money_required - money_in) * kBetFactor
        if tentative_bet < money_required - money_in:
          if win_ratio > kReallyGoodRatio:
            final_bet = int(randomPermute((money_required - money_in) * 2, kRandomFactor))
          else:
            final_bet = money_required - money_in
        else:
          final_bet = int(tentative_bet)
    else:
      # kStretchFactor to err on the side of calling a bit
      if cost_benefit_ratio < randomPermute(win_ratio, kRandomFactor) * kStretchFactor:
        final_bet = money_required - money_in
      else:
        final_bet = -1

  # this is just to make sure we're not overambitious with betting
  if final_bet > (stack_size - money_in):
    return stack_size - money_in
  else:
    return final_bet

# note: money_in == money_required when first_bet == True
def play_afterflop(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  kUndercut = .4 # chance that hero bets small with a really good hand
  kReallyGoodRatio = .7
  kBetRatio = .6 # win percentage that needs to be exceeded to bet first
  kGoodRatio = .5
  kBetFactor = 2
  kConstantBetFactor = .75
  kRandomFactor = .1 # max value of random factor
  kReallyRandomFactor = 20
  kSmallBetFactor = .5
  kStretchFactor = 1.2
  kLimp = .2 # chance that hero limps in with a poor hand
  final_bet = 0

  hand_strength = afterflop_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  cost_benefit_ratio = (money_required - money_in) / float(money_required)

  # correcting for advantageous position
  if position:
    win_ratio = win_ratio * (1 + kPositionAdvantage)
  else:
    win_ratio = win_ratio * (1 - kPositionDisadvantage)

  if first_bet:
    if win_ratio > kBetRatio:
      if random.random() < kUndercut:
        if random.random() < kUndercut:
          final_bet = 0
        else:
          final_bet = int(randomPermute(money_in * kSmallBetFactor, kRandomFactor * kReallyRandomFactor))
      else:
        final_bet = int(win_ratio * kBetFactor * money_in)
    else:
      win_ratio = randomPermute(win_ratio, kRandomFactor)
      if randomPermute(win_ratio, kRandomFactor) > kGoodRatio or random.random() < kLimp:
        if random.random() < kLimp:
          final_bet = int(randomPermute(money_in * kSmallBetFactor, kRandomFactor * kReallyRandomFactor)) # weird bluff bet
        else:
          if money_in > big_blind * 2:
            final_bet = int(randomPermute(big_blind, kRandomFactor))
          else:
            final_bet = int(randomPermute(money_in * kSmallBetFactor, kRandomFactor))
      else:
        final_bet = 0
    if final_bet < 0:
      final_bet = 0
  else:
    if win_ratio > kBetRatio:
      if random.random() < kUndercut:
        final_bet = money_required - money_in
      else:
        if randomPermute(win_ratio, kRandomFactor * 2) < cost_benefit_ratio:
          if win_ratio > kReallyGoodRatio:
            final_bet = randomPermute((money_required - money_in) * 2, kRandomFactor)
          else:
            final_bet = -1
        else:
          tentative_bet = (win_ratio + kConstantBetFactor) * big_blind + win_ratio * (money_required - money_in) * kBetFactor
          if tentative_bet < money_required - money_in:
            if win_ratio > kReallyGoodRatio:
              final_bet = (money_required - money_in) * 2
            else:
              final_bet = money_required - money_in
          else:
            final_bet = int(tentative_bet)
    else:
      # kStretchFactor to err on the side of calling a bit
      if cost_benefit_ratio < randomPermute(win_ratio, kRandomFactor) * kStretchFactor:
        final_bet = money_required - money_in
      else:
        final_bet = -1

  if final_bet > (stack_size - money_in):
    return stack_size - money_in
  else:
    return final_bet

def play_turn(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  hand_strength = afterturn_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  print win_ratio

  return money_required - money_in

def play_river(hand, table, money_in, money_required, big_blind, stack_size, position = False, first_bet = True):
  hand_strength = afterriver_sim.getStrength(hand, table)
  win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])
  print win_ratio

  return money_required - money_in

if __name__ == '__main__':
    #central tenant #1 - aggressive AI is better than passive AI
    #central tenant #2 - AI is good because of randomness
    #central tenant #3 - AI is good because of monte carlo

    theDeck = cards.Deck()
    theDeck.shuffle()
    hand = cards.Hand()
    table = cards.Hand()
    hand.add_card(theDeck.deal_card())
    hand.add_card(theDeck.deal_card())

    for j in range(3):
      table.add_card(theDeck.deal_card())

    print hand, table
    print play_afterflop(hand, table, 10, 20, 10, 300, True, False)

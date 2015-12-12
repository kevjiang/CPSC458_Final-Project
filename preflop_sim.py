import cards
import hands
import pickle

from random import *

# gets indices from hand of size 2
def getIndicesFromHand(hand):
  first = hand.cards[0]
  second = hand.cards[1]

  suited = False
  if first.suit == second.suit:
    suited = True

  firstval = first.get_value()
  secondval = second.get_value()

  if (firstval > secondval and suited) or (firstval < secondval and not suited):
    return [firstval - 1, secondval - 1]
  else:
    return [secondval - 1, firstval - 1]

# creates monte carlo simulation, lower left triangular piece of matrix is unsigned, upper right is signed
def simulate(filename = "preflop_values", trials = 0):
  # holds card combos and results in a vector of [#wins, #ties, #losses]
  #mat = []
  #for i in range(13):
  #  tmat = []
  #  for j in range(13):
  #    tmat.append([0,0,0])
  #  mat.append(tmat)

  mat = pickle.load(open(filename, "rb"))

  for i in range(trials):
    theDeck = cards.Deck()
    theDeck.shuffle()
    herohand = cards.Hand()
    adversaryhand = cards.Hand()

    for j in range(2):
      herohand.add_card(theDeck.deal_card())
      adversaryhand.add_card(theDeck.deal_card())

    indices = getIndicesFromHand(herohand)
  
    table = cards.Hand()
    # 5 cards on table
    for j in range(5):
      table.add_card(theDeck.deal_card())

    result = hands.compare_hands(herohand, adversaryhand, table)

    if result[0] == 'left':
      mat[indices[0]][indices[1]][0] += 1
    elif result[0] == 'none':
      mat[indices[0]][indices[1]][1] += 1
    elif result[0] == 'right':
      mat[indices[0]][indices[1]][2] += 1
      
  pickle.dump(mat, open(filename, "wb"))

def printMatrix(filename = "preflop_values")
  mat = pickle.load(open(filename, "rb"))
  print mat

def preflopStrength(hand, filename = "preflop_values", trials = 10000):
  mat = pickle.load(open(filename, "rb"))
  indices = getIndicesFromHand(hand)
  return mat[indices[0]][indices[1]]

simulate("preflop_values", 9900)
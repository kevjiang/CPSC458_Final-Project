import cards
import hands
import preflop_sim
import afterflop_sim
import pickle

def simulate(filename = "postturn_values", trials = 0):
  #mat = []
  #for j in range(19):
  #  mat.append([0,0,0])

  mat = pickle.load(open(filename, "rb"))

  for i in range(trials):
    theDeck = cards.Deck()
    theDeck.shuffle()
    herohand = cards.Hand()
    adversaryhand = cards.Hand()
    table = cards.Hand()

    for j in range(2):
      herohand.add_card(theDeck.deal_card())
      adversaryhand.add_card(theDeck.deal_card())

    for j in range(4):
      table.add_card(theDeck.deal_card())

    handscore = afterflop_sim.getHandCode(herohand, table)

    # evaluating results of hand
    table.add_card(theDeck.deal_card())

    result = hands.compare_hands(herohand, adversaryhand, table)

    if result == 'left':
      mat[handscore][0] += 1
    elif result == 'none':
      mat[handscore][1] += 1
    elif result == 'right':
      mat[handscore][2] += 1

  print mat
  pickle.dump(mat, open(filename, "wb"))

def getStrength(hand, table, filename = "postturn_values"):
  mat = pickle.load(open(filename, "rb"))
  code = afterflop_sim.getHandCode(hand, table)
  chances = mat[code]
  s = chances[0] + chances[1] + chances[2]
  return [chances[0] / float(s), chances[1] / float(s), chances[2] / float(s)]


#simulate("postturn_values", 900000)

def printMatrix(filename = "postturn_values"):
  mat = pickle.load(open(filename, "rb"))
  print mat

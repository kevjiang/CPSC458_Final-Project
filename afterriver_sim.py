import cards
import hands
import preflop_sim
import afterflop_sim
import pickle

# add more features if we have time

features = { 'high-pair':0, 'middle-pair':1, 'low-pair':2, '2-pair-good':3, '3-kind':4, 'straight':5, 'flush':6, 'full-house':7, '4-kind':8, 'straight-flush':9, 'really-good-high':10, 'good-high':11, 'middle-high':12, 'bad-high':13, 'really-bad-high':14, '2-pair-bad':15 }

def simulate(filename = "postriver_values", trials = 0):
  #mat = []
  #for j in range(16):
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

    for j in range(5):
      table.add_card(theDeck.deal_card())

    handscore = 0
    herohandplus = herohand.list_rep() + table.list_rep()
    evaluated = hands.evaluate_hand(herohandplus)

    if evaluated[2] > 3:
      handscore = evaluated[2]
    elif evaluated[2] == 3:
      high_pair = evaluated[1][0]
      highest_card = True
      for e in evaluated[1]:
        if high_pair < e:
          highest_card = False
      if highest_card:
        handscore = afterflop_sim.features['2-pair-good']
      else:
        handscore = afterflop_sim.features['2-pair-bad']
    elif evaluated[2] == 2:
      high_pair = evaluated[1][0]
      num_card_greater = 0
      for e in evaluated[1]:
        if high_pair < e:
          num_card_greater += 1
      
      if num_card_greater == 0:
        handscore = afterflop_sim.features['high-pair']
      elif num_card_greater == 1:
        handscore = afterflop_sim.features['middle-pair']
      else:
        handscore = afterflop_sim.features['low-pair']
    elif evaluated[2] == 1:
      hand_strength = preflop_sim.getPreflopStrength(herohand)
      win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])

      if win_ratio > afterflop_sim.REALLYGOODHAND:
        handscore = features['really-good-high']
      elif win_ratio > afterflop_sim.GOODHAND:
        handscore = features['good-high']
      elif win_ratio > afterflop_sim.MIDDLEHAND:
        handscore = features['middle-high']
      elif win_ratio > afterflop_sim.BADHAND:
        handscore = features['bad-high']
      else: 
        handscore = features['really-bad-high']

    result = hands.compare_hands(herohand, adversaryhand, table)

    if result == 'left':
      mat[handscore][0] += 1
    elif result == 'none':
      mat[handscore][1] += 1
    elif result == 'right':
      mat[handscore][2] += 1

  print mat
  pickle.dump(mat, open(filename, "wb"))

simulate("postriver_values", 900000)

def printMatrix(filename = "postriver_values"):
  mat = pickle.load(open(filename, "rb"))
  print mat

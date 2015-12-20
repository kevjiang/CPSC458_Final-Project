import cards
import hands
import preflop_sim
import pickle

# add more features if we have time

REALLYGOODHAND = .62
GOODHAND = .53
MIDDLEHAND = .47
BADHAND = .38

features = { 'high-pair':0, 'middle-pair':1, 'low-pair':2, '2-pair-good':3, '3-kind':4, 'straight':5, 'flush':6, 'full-house':7, '4-kind':8, 'straight-flush':9, 'really-good-high':10, 'good-high':11, 'middle-high':12, 'bad-high':13, 'really-bad-high':14, '2-pair-bad':15, 'flush-draw-4':16, 'straight-draw-good':17, 'straight-draw-bad':18}

def checkflush4(h):
  suits = [x[-1] for x in h]
  i = hands.Most_Common(suits)
  # one suit appears 5 or more times
  if i[1] >= 4:
    return True
  else:
    return False

def checkstraight(h):
  r = cards.RANKS
  straightchance = 0
  for rank in r:
    card = cards.Card('C', rank) # suit doesn't matter
    newhand = cards.Hand()
    newhand.add_card(card)
    if hands.contains_seq(h + newhand.list_rep()):
      straightchance += 1
  return straightchance

def simulate(filename = "postflop_values", trials = 0):
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

    for j in range(3):
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
        handscore = features['2-pair-good']
      else:
        handscore = features['2-pair-bad']
    elif evaluated[2] == 2:
      high_pair = evaluated[1][0]
      num_card_greater = 0
      for e in evaluated[1]:
        if high_pair < e:
          num_card_greater += 1
      
      if num_card_greater == 0:
        handscore = features['high-pair']
      elif num_card_greater == 1:
        handscore = features['middle-pair']
      else:
        handscore = features['low-pair']
    elif evaluated[2] == 1:
      straightchance = checkstraight(herohandplus)
      # evaluating for flush draw
      if checkflush4(herohandplus):
        handscore = features['flush-draw-4']
      # evaluating for straight draw
      elif straightchance >= 2:
        handscore = features['straight-draw-good']
      elif straightchance == 1:
        handscore = features['straight-draw-bad']
      else:
        hand_strength = preflop_sim.getPreflopStrength(herohand)
        win_ratio = hand_strength[0] / (hand_strength[0] + hand_strength[2])

        if win_ratio > REALLYGOODHAND:
          handscore = features['really-good-high']
        elif win_ratio > GOODHAND:
          handscore = features['good-high']
        elif win_ratio > MIDDLEHAND:
          handscore = features['middle-high']
        elif win_ratio > BADHAND:
          handscore = features['bad-high']
        else: 
          handscore = features['really-bad-high']

    # evaluating results of hand
    for j in range(2):
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

def printMatrix(filename = "postflop_values"):
  mat = pickle.load(open(filename, "rb"))
  print mat

# simulate("postflop_values", 800000)

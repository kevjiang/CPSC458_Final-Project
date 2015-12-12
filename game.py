import cards
import hands
import logging

class Game(object):
    def __init__(self):
        self.theDeck = cards.Deck()
        self.theDeck.shuffle()
        self.small = cards.Hand()
        self.big = cards.Hand()
        self.table = cards.Hand()

    def preflop(self):
        self.big.add_card(self.theDeck.deal_card())
        self.big.add_card(self.theDeck.deal_card())
        self.small.add_card(self.theDeck.deal_card())
        self.small.add_card(self.theDeck.deal_card())

def basic_game():
    theDeck = cards.Deck()
    theDeck.shuffle()
    small = cards.Hand()
    big = cards.Hand()
    table = cards.Hand()

# Preflop
    big.add_card(theDeck.deal_card())
    big.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())

# Flop
    for i in range(3):
        table.add_card(theDeck.deal_card())
    logging.info(str(['flop', small.list_rep(), big.list_rep(), table.list_rep()]))

# Turn
    table.add_card(theDeck.deal_card())
    logging.info(str(['turn', small.list_rep(), big.list_rep(), table.list_rep()]))

# River
    table.add_card(theDeck.deal_card())
    logging.info(str(['table', small.list_rep(), big.list_rep(), table.list_rep()]))
    return hands.compare_hands(small, big, table)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    print basic_game()

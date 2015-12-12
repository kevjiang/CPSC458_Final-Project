import cards
import hands
import logging

def basic_game():
    theDeck = cards.Deck()
    theDeck.shuffle()
    small = cards.Hand()
    big = cards.Hand()
    river = cards.Hand()

# Preflop
    big.add_card(theDeck.deal_card())
    big.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())
    small.add_card(theDeck.deal_card())

# River
    for i in range(5):
        river.add_card(theDeck.deal_card())
        logging.info(str([small.list_rep(), big.list_rep(), river.list_rep()]))
        logging.info(str(hands.compare_hands(small, big, river)))
    return hands.compare_hands(small, big, river)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    print basic_game()

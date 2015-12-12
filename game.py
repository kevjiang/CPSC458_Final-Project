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

# Flop
    for i in range(3):
        river.add_card(theDeck.deal_card())
    logging.info(str(['flop', small.list_rep(), big.list_rep(), river.list_rep()]))

# Turn
    river.add_card(theDeck.deal_card())
    logging.info(str(['turn', small.list_rep(), big.list_rep(), river.list_rep()]))

# River
    river.add_card(theDeck.deal_card())
    logging.info(str(['river', small.list_rep(), big.list_rep(), river.list_rep()]))
    return hands.compare_hands(small, big, river)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    print basic_game()

import cards
import hands
import logging

if __name__ == '__main__':
    theDeck = cards.Deck()
    theDeck.shuffle()
    playerhand = cards.Hand()
    househand = cards.Hand()
    for i in range(5):
        playerhand.add_card(theDeck.deal_card())
        househand.add_card(theDeck.deal_card())
    # playerscore = playerhand.get_value()
    # house_val = househand.get_value()
    print playerhand.list_rep()
    print househand.list_rep()
    print hands.compare_hands(playerhand, househand)

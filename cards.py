import random
import logging

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)

# initialize some useful global variables
global in_play
in_play = False
global outcome
outcome = " start game"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13}


# define card class
class Card:

    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def rank_suit(self):
        return self.rank + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_value(self):
        return VALUES[self.rank]

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(
            card_images, card_loc, CARD_SIZE, [
                pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class


class Hand:

    def __init__(self, stack=100):
        self.cards = []
        self.stack = stack

    def __str__(self):
        ans = ""
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def list_rep(self):
        rep = []
        for i in range(len(self.cards)):
            rep.append(self.cards[i].rank_suit())
        return rep

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand

# define deck class


class Deck:

    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck

    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck

    def remove_specific_card(self, suit, rank):
        for d in self.deck:
            if d.suit == suit and d.rank == rank:
                self.deck.remove(d)


if __name__ == '__main__':
    # deal()
    theDeck = Deck()
    theDeck.shuffle()
    playerhand = Hand()
    househand = Hand()
    playerhand.add_card(theDeck.deal_card())
    playerhand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())
    playerscore = playerhand.get_value()
    house_val = househand.get_value()
    print playerhand
    print househand

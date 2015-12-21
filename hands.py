import logging
import itertools
from collections import Counter

# gets card value from  a hand. converts A to 14,  is_seq function will
# convert the 14 to a 1 when necessary to evaluate A 2 3 4 5 straights
def convert_tonums(h, nums={'T': 10, 'J': 11, 'Q': 12, 'K': 13, "A": 14}):
    for x in xrange(len(h)):
        if (h[x][0]) in nums.keys():
            h[x] = str(nums[h[x][0]]) + h[x][1]
    return h

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0]

def get_high(h):
    return list(sorted([int(x[:-1])
                        for x in convert_tonums(h)], reverse=True))[:5]
# converts hand to number values and then evaluates if they are sequential
# AKA a straight, returns True with the value of the highest card in the straight
def contains_seq(h):
    ace = False
    # h is now a list of the numbers only
    h = [x[:-1] for x in convert_tonums(h)]
    h = [int(x) for x in h]
    h = list(set(h)) # remove duplicate numbers
    if len(h) < 5:
        return False

    h = list(sorted(h))[::-1] # sort high to low
    ref = True
    for i in range(0, len(h)-4):
        ref = True
        for x in range(0+i, 4+i):
            if not h[x] - 1 == h[x + 1]:
                ref = False
                break
        # if the hand is a straight then it's the highest, set r equal to it and stop looking
        if ref:
            return True, h[i:i+5]

    aces = [i for i in h if str(i) == "14"]
    if len(aces) == 1:
        for x in range(len(h)):
            if str(h[x]) == "14":
                h[x] = 1

    h = list(sorted(h))[::-1]
    for i in range(0, len(h)-4):
        ref = True
        for x in range(0+i, 4+i):
            if not h[x] - 1 == h[x + 1]:
                ref = False
                break
        if ref:
            high = h[i]
            return True, h[i:i+5]

    return False

# assumes the hand you get is 7 card and already sorted from high to low
def contains_flush(h):
    # suit is the last number in each element of the list
    suits = [x[-1] for x in h]
    nh = []
    i = Most_Common(suits)
    # one suit appears 5 or more times
    if i[1] >= 5:
        # make a list of all the cards with that suit in it
        for x in range(0,len(suits)):
            if suits[x] == i[0]:
                nh.append(h[x])
        # return all cards with that suit
        return True, nh
    else:
        return False

# is straight flush
# if a hand is a straight and a flush return True and the highest card value
def contains_straightflush(h):
    nh = []
    if contains_flush(h):
        nh = contains_flush(h)[1]
        if contains_seq(nh):
            return True, contains_seq(nh)[1]
    return False

# if the most common element occurs 4 times then it is a four of a kind
# returns True and the value of the four of a
def contains_fourofakind(h):
    h = [a[:-1] for a in convert_tonums(h)]
    h = [int(a) for a in h]
    data = Counter(h)
    a = data.most_common(1)[0]
    if a[1] == 4:
        h = list(set(h))
        h.remove(a[0])
        hand = [a[0]] * 4
        hand.append(max(h))
        return True, hand
    else:
        return False

# if the most common element occurs 3 times then it is a three of a kind
# returns true and the value of the highest 3 of a kind
def contains_threeofakind(h):
    h = [a[:-1] for a in convert_tonums(h)] # all the numbers
    h = [int(a) for a in h]
    data = Counter(h)
    a = data.most_common(1)[0]
    if a[1] == 3:
        h = list(set(h))
        h.remove(a[0])
        second = max(h)
        h.remove(second)
        third = max(h)
        return True, [a[0],a[0],a[0],second,third]

    return False

# run after 4 of a kind so there can't be 4 of the same card -- therefore must be at least 3 distinct numbers
# take first 3 common elements and if first is 3 and second or third is 2 then full house
# returns True and the values of the full house
def contains_fullhouse(h):
    h = [a[:-1] for a in convert_tonums(h)]
    h = [int(a) for a in h]
    data = Counter(h)
    a, b, c = data.most_common(1)[0], data.most_common(2)[-1], data.most_common(3)[-1]
    if a[1] == 3 and b[1] >=2:
        if c[1] == 2: # then b[1] must equal 2
            if b[0] > c[0]:
                return True, [a[0], a[0], a[0], b[0], b[0]]
            else:
                return True, [a[0], a[0], a[0], c[0], c[0]]
        if b[1] == 3:
            if b[0] > a[0]:
                return True, [b[0], b[0], b[0], a[0], a[0]]
        return True, [a[0], a[0], a[0], b[0], b[0]]
    return False

# if the first 2 most common elements have counts of 2 and 2 then it is a
# two pair
def contains_twopair(h):
    h = [a[:-1] for a in convert_tonums(h)]
    h = [int(a) for a in h]
    data = Counter(h)
    a, b, c = data.most_common(1)[0], data.most_common(2)[-1], data.most_common(3)[-1]
    if a[1] == 2 and b[1] == 2:
        if c[1] == 2:
            lst = [a[0],b[0],c[0]]
            high = max(lst)
            lst.remove(high)
            high2 = max(lst)
            h = list(set(h))
            h.remove(high)
            h.remove(high2)
            return True, [high, high, high2, high2, max(h)]
        if b[0] > a[0]:
            h = list(set(h))
            h.remove(a[0])
            h.remove(b[0])
            return True, [b[0], b[0], a[0], a[0], max(h)]
        h = list(set(h))
        h.remove(a[0])
        h.remove(b[0])
        return True, [a[0], a[0], b[0], b[0], max(h)]
    return False

# if the first most common element is 2 then it is a pair
# DISCLAIMER: this will return true if the hand is a two pair, but this
# should not be a conflict because is_twopair is always evaluated and
# returned first
def contains_pair(h):
    h = [a[:-1] for a in convert_tonums(h)]
    h = [int(a) for a in h]
    data = Counter(h)
    a = data.most_common(1)[0]

    if str(a[1]) == '2':
        h = list(set(h))
        h.remove(a[0])
        h = list(sorted(h, reverse = True))
        return True, [a[0], a[0], h[0], h[1], h[2]]
    else:
        return False

# get the high card

# FOR HIGH CARD or ties, this function compares two hands by ordering the
# hands from highest to lowest and comparing each card and returning when
# one is higher then the other
def compare(xs, ys):
    xs, ys = list(sorted(xs, reverse=True)), list(sorted(ys, reverse=True))

    for i, c in enumerate(xs):
        if ys[i] > c:
            return 'RIGHT'
        elif ys[i] < c:
            return 'LEFT'

    return "TIE"


# categorized a hand based on previous functions
# returns the entire hand
def evaluate_hand(h):

    if contains_straightflush(h):
        return "STRAIGHT FLUSH", contains_straightflush(h)[1], 9 # returns the cards
    elif contains_fourofakind(h):
        return "FOUR OF A KIND", contains_fourofakind(h)[1], 8
    elif contains_fullhouse(h):
        return "FULL HOUSE", contains_fullhouse(h)[1], 7
    elif contains_flush(h):
        cards = contains_flush(h)[1]
        cards = [a[:-1] for a in convert_tonums(cards)]
        cards = [int(a) for a in cards]
        cards = list(sorted(cards))[::-1][:5]
        return "FLUSH", cards, 6
    elif contains_seq(h):
        return "STRAIGHT", contains_seq(h)[1], 5
    elif contains_threeofakind(h):
        return "THREE OF A KIND", contains_threeofakind(h)[1], 4
    elif contains_twopair(h):
        return "TWO PAIR", contains_twopair(h)[1], 3
    elif contains_pair(h):
        return "PAIR", contains_pair(h)[1], 2
    else:
        return "HIGH CARD", get_high(h), 1

# takes two lists and finds the one with the larger value
# returns "left" if lst1 is bigger, "right" if lst2 is bigger, "none" otherwise
def find_bigger_list(lst1, lst2):
    for i in range(0, len(lst1)):
        if lst1[i] == lst2[i]:
            continue
        elif lst1[i] > lst2[i]:
            return "left"
        else:
            return "right"
    return "none"

# function that compares two hands
def compare_hands_helper(h1, h2):
    one, two = evaluate_hand(h1), evaluate_hand(h2)
    out =  None
    if one[0] == two[0]:
        out = find_bigger_list(one[1], two[1])
    elif one[2] > two[2]:
        out = "left"
    else:
        out = "right"
    if out == 'left':
        return ('left',  one[0])
    elif out == 'right':
        return ('right', two[0])
    else:
        return ('none', one[0])



def compare_hands(h1, h2, table=None):
    if table:
        return compare_hands_helper(
            h1.list_rep() + table.list_rep(),
            h2.list_rep() + table.list_rep())
    else:
        return compare_hands_helper(h1.list_rep(), h2.list_rep())

if __name__ == '__main__':
    a = ['QD', 'KD', '9D', 'JD', 'TD']
    b = ['JS', '8S', 'KS', 'AS', 'QS']
    print compare_hands_helper(a,b)

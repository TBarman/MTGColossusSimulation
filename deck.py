import random
from card import Card, cardTypes
from collections import deque

class Deck:
    def __init__(self, cheap_reanimation, expensive_reanimation, neutral=3, colossus=1):
        lands = 99 - colossus - cheap_reanimation - neutral - expensive_reanimation
        forest = lands // 2
        swamp = lands - forest
        cardTypeCounts = [cheap_reanimation, expensive_reanimation,
                          neutral, colossus, forest, swamp]
        self.deck = deque() # Top of the deck is the end
        for i in range(len(cardTypes)):
            self.deck.extend([cardTypes[i]] * cardTypeCounts[i])
        self.shuffle()

    def shuffle(self):
        lst = list(self.deck)
        random.shuffle(lst)
        self.deck = deque(lst)

    def draw(self):
        return self.deck.pop()  # draw from top -- O(1)

    def bottom(self, card):
        self.deck.appendleft(card)  # add to bottom -- O(1)

    def drawHand(self):

        # makes sure deck is shuffled before new hands are drawn
        self.shuffle()

        hand = [] # will be list of card objects
        for i in range(7):
            hand.append(self.draw())

        return hand

    def bottomCards(self, cards):
        for card in cards:
            self.bottom(card)




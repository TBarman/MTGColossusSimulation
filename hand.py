from deck import Deck
from card import Card, cardTypes

def acceptable(hand, toBottom):
    '''
    Checks if the hand is acceptable.
    Acceptable if...
    - Hand has at least one reanimation
    - Hand has at least one forest
    - Hand has at least one swamp
    - Hand has no colossus or can bottom the colossus
    '''
    hasReanimation = Card.CHEAP_REANIMATION in hand or Card.EXPENSIVE_REANIMATION in hand
    hasForest = Card.FOREST in hand
    hasSwamp = Card.SWAMP in hand
    meetsRequirements = hasReanimation and hasForest and hasSwamp

    canHandleColossus = (Card.COLOSSUS not in hand or toBottom >= 1)
    return meetsRequirements and canHandleColossus

def finishMulligan(deck, hand, toBottom):
    '''
    This function handles the logic behind which cards to put on the bottom of the deck.
    Assumes toBottom is less than 7.

     Rules for getting rid of cards (priority):
    - If colossus, bottom it
    - If more than one reanimation, keep bottoming expensive, then cheap reanimation until one left
    - If neutral cards, bottom it
    - Bottom forest until one left
    - Bottom swamp until one left
    '''
    bottom = []
    if (toBottom == 0):
        return hand
    else:
        while toBottom > 0:
            reanimationCount = hand.count(Card.CHEAP_REANIMATION) + hand.count(Card.EXPENSIVE_REANIMATION)
            forestCount = hand.count(Card.FOREST)
            swampCount = hand.count(Card.SWAMP)
            if Card.COLOSSUS in hand:
                hand.remove(Card.COLOSSUS)
                bottom.append(Card.COLOSSUS)
            elif reanimationCount > 1:
                if Card.EXPENSIVE_REANIMATION in hand:
                    hand.remove(Card.EXPENSIVE_REANIMATION)
                    bottom.append(Card.EXPENSIVE_REANIMATION)
                else:
                    hand.remove(Card.CHEAP_REANIMATION)
                    bottom.append(Card.CHEAP_REANIMATION)
            elif Card.NEUTRAL in hand:
                hand.remove(Card.NEUTRAL)
                bottom.append(Card.NEUTRAL)
            elif forestCount > 1:
                hand.remove(Card.FOREST)
                bottom.append(Card.FOREST)
            elif swampCount > 1:
                hand.remove(Card.SWAMP)
                bottom.append(Card.SWAMP)

            # If we got here, this means we have only one reanimation, one forest,
            # and one swamp, and still need to mulligan
            else: # Worst case we only keep one reanimation
                if forestCount > 0:
                    hand.remove(Card.FOREST)
                    bottom.append(Card.FOREST)
                else:
                    hand.remove(Card.SWAMP)
                    bottom.append(Card.SWAMP)
            toBottom -= 1

    # put the bottomed cards back in the deck
    deck.bottomCards(bottom)

    return hand


def drawProperHand(deck):
    '''
    :param deck: [reanimation, neutral, colossus, forest, swamp]
    :return: hand that follows the specifications.
    Specifications (Final hand):
    - Hand must have at least one reanimation
    - Hand must have at least one forest and one swamp
    - Hand must NOT have colossus

    Rules for repeated drawing:
    - First redraw of hand still has 7 cards
    - Next redraws will still draw 7, but must get rid of one card for each extra redraw (besides first)
    '''

    toBottom = 0 # Number of cards we must bottom at the end
    isAcceptable = False
    freeMull = True
    # keep drawing until you get an acceptable hand
    while not isAcceptable and toBottom < 6: # toBottom < 6 since no point in toBottom = 7, might as well hold last card
        hand = deck.drawHand()
        isAcceptable = acceptable(hand, toBottom)
        if not isAcceptable:
            if freeMull:
                freeMull = False
            else:
                toBottom += 1
            deck.bottomCards(hand)

    # handle mulligan logic
    finalHand = finishMulligan(deck, hand, toBottom)

    return finalHand

def simulateDrawProperHand(iterations=10000):
    distribution = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, iterations + 1):
        if (i % (iterations/10) == 0):
            print(f"{i/iterations*100}% Completed")

        deck = Deck(8, 2)
        finalHand = drawProperHand(deck)
        cards = len(finalHand)
        distribution[cards] += 1

    print(distribution)

#simulateDrawProperHand()



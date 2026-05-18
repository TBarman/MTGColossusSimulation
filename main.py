from hand import drawProperHand
from deck import Deck
from card import Card
import random
import csv

def searchColossus(deck):
    '''
    Removes the colossus from the deck
    '''
    toBottom = []
    draw = deck.draw()
    while draw != Card.COLOSSUS:
        toBottom.append(draw)
        draw = deck.draw()
    random.shuffle(toBottom)
    deck.bottomCards(toBottom)

def cultivator(hand, deck, landsInPlay):
    while (Card.FOREST in hand or Card.SWAMP in hand) and len(deck.deck) > 0:
        if Card.SWAMP in hand:
            hand.remove(Card.SWAMP)
            landsInPlay.append(Card.SWAMP)
        elif Card.FOREST in hand:
            hand.remove(Card.FOREST)
            landsInPlay.append(Card.FOREST)

        hand.append(deck.draw())

def game(deck):
    hand = drawProperHand(deck)
    landsInPlay = []
    '''FIRST THREE TURNS'''
    for i in range(3):
        hand.append(deck.draw())
        # Land drop logic (Makes sure we have at least one of each type in play first)
        if Card.SWAMP not in landsInPlay:
            if Card.SWAMP in hand:
                hand.remove(Card.SWAMP)
                landsInPlay.append(Card.SWAMP)
        elif Card.FOREST not in landsInPlay:
            if Card.FOREST in hand:
                hand.remove(Card.FOREST)
                landsInPlay.append(Card.FOREST)
        else:
            if Card.SWAMP in hand:
                hand.remove(Card.SWAMP)
                landsInPlay.append(Card.SWAMP)
            elif Card.FOREST in hand:
                hand.remove(Card.FOREST)
                landsInPlay.append(Card.FOREST)

    # Put colossus in graveyard
    if Card.COLOSSUS not in hand:
        searchColossus(deck)
    else:
        return len(landsInPlay)

    '''TURN FOUR'''
    hand.append(deck.draw())
    if Card.CHEAP_REANIMATION in hand:
        if len(landsInPlay) >= 3:
            hand.remove(Card.CHEAP_REANIMATION)
            cultivator(hand, deck, landsInPlay)
        else:
            # Not enough lands so make land drop
            if Card.SWAMP in hand:
                hand.remove(Card.SWAMP)
                landsInPlay.append(Card.SWAMP)
            elif Card.FOREST in hand:
                hand.remove(Card.FOREST)
                landsInPlay.append(Card.FOREST)

            # Check again
            if len(landsInPlay) >= 3:
                hand.remove(Card.CHEAP_REANIMATION)
                cultivator(hand, deck, landsInPlay)

    elif Card.EXPENSIVE_REANIMATION in hand:
        # Not enough lands so make land drop
        if Card.SWAMP in hand:
            hand.remove(Card.SWAMP)
            landsInPlay.append(Card.SWAMP)
        elif Card.FOREST in hand:
            hand.remove(Card.FOREST)
            landsInPlay.append(Card.FOREST)

        if len(landsInPlay) >= 4:
            hand.remove(Card.EXPENSIVE_REANIMATION)
            cultivator(hand, deck, landsInPlay)

    else:
        # Just make land drop
        if Card.SWAMP in hand:
            hand.remove(Card.SWAMP)
            landsInPlay.append(Card.SWAMP)
        elif Card.FOREST in hand:
            hand.remove(Card.FOREST)
            landsInPlay.append(Card.FOREST)


    return len(landsInPlay)


def experiment(deckConfig, iterations=1000000):
    gameResults = []
    for i in range(iterations):
        deck = Deck(*deckConfig)
        gameResults.append(game(deck))

    return gameResults

def saveResults(data, filename='results.csv'):
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        # header row
        # writer.writerow(['cheap_reanimation', 'expensive_reanimation', 'lands_in_play'])
        # data rows
        for (cheap, expensive), results in data.items():
            for result in results:
                writer.writerow([cheap, expensive, result])

def dataProduction():
    # Want at least 1 reanimation spell, have that one be cheap which is why (1, 10) and (0, 10)
    deckConfigs = [(i, j) for i in range(0, 10) for j in range(0, 10) if ((i + j) > 0 and (i == 0 or j == 0))]
    data = {}
    for deckConfig in deckConfigs:
        print(f"Computing config {deckConfig}...")
        data[deckConfig] = experiment(deckConfig)

    saveResults(data)
#
# dataProduction()
# print("Done")
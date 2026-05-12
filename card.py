from enum import Enum

class Card(Enum):
    CHEAP_REANIMATION = 0
    EXPENSIVE_REANIMATION = 1
    NEUTRAL = 2
    COLOSSUS = 3
    FOREST = 4
    SWAMP = 5

cardTypes = [Card.CHEAP_REANIMATION, Card.EXPENSIVE_REANIMATION, Card.NEUTRAL,
                     Card.COLOSSUS, Card.FOREST, Card.SWAMP]
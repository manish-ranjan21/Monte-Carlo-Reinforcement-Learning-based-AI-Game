import random


class InitHand:
    def __init__(self):
        self.draw = []
        
    def draw(self,deck):
        draw = []
        #re-shuffling each time to ensure randomness in draw
        random.shuffle(deck)
        #Using pop to remove the last value in the deck to ensure that it cannot be selected again
        draw.append(deck.pop(random.randrange(0,len(deck))))
        random.shuffle(deck)
        draw.append(deck.pop(random.randrange(0,len(deck))))
        return draw
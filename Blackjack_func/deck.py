

class Deck:
    def __init__(self, total_decks = 3):
        self.cards = 4 * ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.card_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
        self.total_decks = total_decks
        
    def deck(self):
        deck = []
         
        # Create the base deck
        for x in range(0,self.total_decks):
            for card in self.cards:
                deck.append(self.card_values[card])
        return deck
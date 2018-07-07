from card import Card

# required for card class:
import datetime
import math

class Deck:
    def __init__(self,cards=[]):
        '''Initialise deck with a list of cards (empty list created if none passed).'''
        self.cards = cards

    def _find_card(self,card_id):
        '''Retrieve card with the given id.'''
        for card in self.cards:
            if card.id == card_id:
                return card
        return None
    
    def add_card(self,word,meaning,pronunciation,example):
        '''Create a new card and add it to the deck.'''
        self.cards.append(Card(word,meaning,pronunciation,example))
    
    def edit_card(self,card_id,field,value):
        '''Edit a field of an IDed card.'''
        setattr(self._find_card(card_id), str(field), value)
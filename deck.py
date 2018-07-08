from card import Card
from datetime import datetime, timedelta
fd.orom operator import itemgetter

class Deck:
    def __init__(self,cards=None):
        '''Initialise deck with a list of cards 
        (empty list created if none passed).'''
        if not cards:
            self.cards = []
        else:
            self.cards = cards
            self.build_overdue_stack()
        self.overdue = []

    def build_overdue_stack(self):
        '''Creates a stack of overdue cards.'''
        self.overdue = []
        for card in self.cards:
            if card.next_review < (datetime.now() + timedelta(days=1)):
                self.overdue.append(card)
        # self.sort_overdue()
    
    def sort_overdue(self):
        '''Sorts overdue cards from most to least overdue,
        removing any cards that are not overdue.'''
    #     for card in self.overdue:
    #         if card.next_review > datetime.now():
    #             self.overdue.remove(card)
    #     self.overdue = sorted(self.overdue, key=itemgetter('next_review')) 
        pass

    def find_card(self,card_id):
        '''Retrieve card with the given id.'''
        for card in self.cards:
            if card.id == card_id:
                return card
        return None
    
    def add_card(self,content,data=None):
        '''Create a new card and add it to the deck.'''
        self.cards.append(Card(content,data))
        self.build_overdue_stack()
    
    def edit_card(self,card_id,field,value):
        '''Set value of field of card of given id.'''
        setattr(self.find_card(card_id), str(field), value)
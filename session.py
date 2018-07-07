from card import Card
from deck import Deck
import datetime
import math

class Session:
    def __init__(self,deck):
        '''Create a deck session and schedule cards for study'''
        self.deck = deck
        self._schedule()

    def _schedule(self):
        '''populates study list with all cards in deck that require reviewing'''
        self.study_list = []
        for card in self.deck.cards:
            if card.next_review < datetime.datetime.now():
                self.study_list.append(card)

    def review_card(self):
        ''''''
        # This will be the only necessary method for the session class
        # Menu and other class methods can handle what a session actually looks like

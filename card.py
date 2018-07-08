from datetime import datetime, timedelta
import math
import re

class Card:
    def __init__(self,content,data=None):
        '''Initialise the card by setting its content
        and data values.'''
        # content
        # [key,pronunciation,meaning,example]
        self.key = content[0]
        self.pronunciation = content[1]
        self.meaning = content[2]
        self.example = re.sub(r'([^\{]*)(?=\})','',content[3])
        self.cloze = re.search(r'([^\{]*)(?=\})',content[3]).group()
        # data
        # [id,date_added,stability,next_review]
        if not data:
            self.id = 0
            self.date_created = datetime.now()
            self.stability = 0
            self.next_review = datetime.now()
        else:
            self._set_data(data)

    def schedule(self,retrievablity_threshold=0.5):
        '''Takes retrievablity threshold and stability of a card and uses
        forgetting curve to calculate and return next review time'''
        t = math.log(retrievablity_threshold)*-self.stability
        self.next_review = datetime.now() + timedelta(days=t)

    def _set_data(self,data):
        '''sets card data from list of values provided'''
        self.id = data[0]
        self.date_created = data[1]
        self.stability = data[2]
        self.next_review = data[3]

    def match(self,filter):
        '''Determine if this card matches the filter
        text. Return True if it matches, False otherwise.

        Search is case sensitive and matches key.'''
        return filter in self.key

    def test(self,answer):
        '''return pass or fail mark for answer of card's question.'''
        if answer:
            self.sttability += 1
        else:
            self.stability = 0
        self.schedule()
import datetime
import math

# temporary method for generating unique id for each card object
id = 1

class Card:
    def __init__(self,word,meaning,pronunciation,example):
        '''Initialise the card by setting front, back
        and other automatically-generated properties.'''
        # Semantic Content
        self.word = word
        self.meaning = meaning
        self.pronunciation = pronunciation
        self.example = example
        # Study properties
        self.r = 0.5    #retrievable
        self.s = 0      #stability
        self.t = math.log(self.r)*-self.s
        self.reschedule() # sets self.next_review
        # Properties
        self.created_at = datetime.datetime.now()
        # temporary approach for unique id generation
        # to be replaced with database class method
        global id
        self.id = id
        id += 1

    def match(self,filter):
        '''Determine if this card matches the filter
        text. Return True if it matches, False otherwise.

        Search is case sensitive and matches both word, meaning and pronunciation.'''
        return filter in self.word or filter in self.meaning or filter in self.pronunciation
    
    def evaluate_answer(self,answer):
        '''return pass or fail mark for answer of card's question.'''
        if answer:
            self.s += 1
        else:
            self.s = 0
        self.reschedule()
    
    def reschedule(self):
        '''schedule next review based on retrievability decay threshold and stability
        using Ebbinghaus's forgetting curve.'''
        self.t = math.log(self.r)*-self.s
        self.next_review = datetime.datetime.now() + datetime.timedelta(days=self.t)

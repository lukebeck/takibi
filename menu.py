from card import Card
from deck import Deck
from session import Session
import datetime
import math
import subprocess as sp
import sys

class Menu:
    def __init__(self,session):
        '''Initialises the application session.'''
        self.session = session

    def clear_screen(self):
        '''Clears the terminal screen.'''
        tmp = sp.call('clear',shell=True)

    def run(self):
        '''Runs the application.'''
        action = self._main_menu()
        self.clear_screen()
        if action == '1':
            self.study()
        if action == '2':
            pass # to be implemented at a later date
        if action == '3':
            pass # to be implemented at a later date
        if action == '4':
            self.quit()
        else:
            print('Sorry, that is not a valid input.\nPlease enter again.')
            self.run()
    
    def _main_menu(self):
        '''Displays the main menu screen of the application and returns the users input.'''
        print('''💧 Mizutama 💧
{} cards to review

1. Study
2. Add Note
3. Edit Note
4. Quit
'''.format(len(self.session.study_list))
        )
        return self.quit_check(input('>>> '))

    def study(self):
        self.clear_screen()
        while len(self.session.study_list) > 0:
            self.review_card()
            self.clear_screen()
            self.session._schedule() # this is a computationally intense way of doing this
            # a better option would be to just *_reshuffle()* the study_list through a new session method
    
    def review_card(self):
        card = self.session.study_list[0]
        self._question(card)
        self.clear_screen()
        self._flip_card(card)
        self._answer(card,self.quit_check(input('Fail (1) or pass (2)?\n>>> ')))

    def _question(self,card):
        print('{}\n\n\n\n\n\n\n'.format(card.word))
        self.quit_check(input('Flip card: enter '))
        self.clear_screen()

    def _answer(self,card,ans):
        if ans == '1':
            card.evaluate_answer(False)
            print('fail')
        elif ans == '2':
            card.evaluate_answer(True)
            print('pass')
        else:
            
            self._answer(card,self.quit_check(input('Invalid input. Try again.\n>>> ')))

    def _flip_card(self,card):
        print('''
{}
{}
{}

example:
    {}\n'''.format(card.word,card.pronunciation,card.meaning,card.example))

    def quit(self):
        self.clear_screen()
        '''Exits the application.'''
        # print('Saving...')
        # This needs to include a save to database feature when database is implemented that would go here
        print('Exiting Mizutama...')
        sys.exit(0)

    def quit_check(self,input_string):
        '''Checks input to see if user wants to quit application.'''
        if input_string == 'xx':
            self.quit()
        else:
            return input_string

if __name__ == '__main__':
    # for easy testing purposes
    card = Card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d = Deck()
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')
    d.add_card('漢字','kanji','かんじ','漢字は2000以上ある！')

    s = Session(d)
    m = Menu(s)

    m.run()

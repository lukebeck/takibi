from card import Card
from deck import Deck
import subprocess as sp
import sys

class Menu:
    def __init__(self,deck):
        '''Initialises the application session.'''
        self.deck = deck
        self.input_error_message = \
            'Invalid input. Please reinput.'
        self.overdue_message = \
            '{} cards to review'.format(len(self.deck.overdue))
        self.main_menu_message = \
            '💧 Mizutama 💧\n' + \
            '{}\n\n' + \
            '1. Study\n' + \
            '2. Add Note (to be implemented)\n' + \
            '3. Edit Note (to be implemented)\n' + \
            '4. Quit\n'
        self.main_menu(self.overdue_message)

    def main_menu(self,message=None):
        '''Displays the main menu.'''
        self.clear_screen()
        print(self.main_menu_message.format(message))
        action = self._quit_check(input('>>> '))
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
            self.main_menu(self.input_error_message)

    def clear_screen(self):
        '''Clears the terminal screen.'''
        tmp = sp.call('clear',shell=True)

    def quit(self):
        self.clear_screen()
        '''Exits the application.'''
        # print('Saving...')
        # This needs to include a save to database feature 
        # when database is implemented that would go here
        print('Exiting Mizutama...')
        sys.exit(0)

    def _quit_check(self,input_string):
        '''Checks input to see if user wants to quit application.'''
        if input_string == 'xx':
            self.quit()
        else:
            return input_string

    def study(self):
        '''Starts a study session.'''
        while len(self.deck.overdue) > 0:
            self.review_card()
            self.clear_screen()
            self.deck.build_overdue_stack()

    def review_card(self):
        '''Presents a card for the user to review.'''
        card = self.deck.overdue[0]
        self.question(card)
        self.clear_screen()
        self.flip_card(card)
        self.answer(card,self._quit_check(input('Fail (1) or pass (2)?\n>>> ')))

    def question(self,card):
        '''Presents the question side of the card.'''
        print(card.example.format('_'*len(card.cloze)))
        self._quit_check(input('\n\n\n\n\n\n>>> '))


    def flip_card(self,card):
        '''Flips a card to show its answer side.'''
        print('{}\n\n{}\n{}\n\n{}'.format(
            card.example.format(card.cloze),
            card.key,
            card.pronunciation,
            card.meaning))

    def answer(self,card,answer):
        '''Evaluates users answer to a card.'''
        if answer == '1':
            card.test(False)
        elif answer == '2':
            card.test(True)
        else:
            self.answer(card,self._quit_check(input('Invalid input. Try again.\n>>> ')))

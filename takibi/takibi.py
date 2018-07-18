from collections import OrderedDict
import csv
from datetime import datetime,timedelta
import math
import os
import re
import subprocess
import sys

file_path = os.path.dirname(os.path.realpath(__file__))

db_file = file_path + '/db/db.csv'
import_db_file = file_path + '/db/import.csv'


class Database:
    def __init__(self,file):
        '''Initialises database by importing from file.'''
        self.file = file
        self.entries,self.fieldnames = self.read(self.file)
    
    def read(self,file):
        '''Reads a file and returns list of its entries.'''
        entries = []
        fieldnames = []
        with open(file) as open_file:
            reader = csv.DictReader(open_file)
            fieldnames = reader.fieldnames
            for row in reader:
                entries.append(row)
        return [entries,fieldnames]

    def write(self):
        '''Writes entries to database file'''
        self.backup(self.file)
        fieldnames = self.fieldnames
        with open(self.file, 'w') as open_file:
            writer = csv.DictWriter(open_file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry)

    def import_cards(self,file):
        '''Import new cards from database file.'''
        entries,fieldnames = self.read(file)
        with open(file, 'w') as open_file:
            writer = csv.DictWriter(open_file, fieldnames=fieldnames)
            writer.writeheader()        
        return entries

    def backup(self,file):
        '''Creates a backup of a file.'''
        # This needs to be improved to allow n amount of backups
        with open(file,'r') as original,open('{}.bak'.format(file),'w') as backup:
            content = original.read()
            backup.write(content) 

class Card:
    def __init__(self,entry):
        '''Initialises a card from a database entry'''
        self.key = entry['key']
        self.pronunciation = entry['pronunciation']
        self.meaning = entry['meaning']
        self.example = entry['example']
        self.clozedexample = re.sub(r'([^\{]*)(?=\})','',self.example)
        self.cloze = re.search(r'([^\{]*)(?=\})',self.example).group()
        self.definition = entry['definition']
        self.stability = int(entry['stability'])
        self.date_created = datetime.strptime(entry['date_created'],'%Y-%m-%d %H:%M:%S')
        self.next_review = datetime.strptime(entry['next_review'],'%Y-%m-%d %H:%M:%S')

    def schedule_review(self):
        '''Schedules next review'''
        # r: retrievability threshold
        # t: time before cards retrievability falls below threshold
        r = 0.55 
        t = math.log(r) * -self.stability 
        self.next_review = datetime.now() + timedelta(days=t)

    def test(self,answer):
        '''Evaluates answer and schedules next review accordingly.'''
        if answer:
            self.stability += 1
        else:
            self.stability = 0
        self.schedule_review()
    
    def export(self):
        '''Exports card information.'''
        export = OrderedDict([
            ('key',self.key),
            ('pronunciation',self.pronunciation),
            ('meaning',self.meaning),
            ('example',self.example),
            ('definition',self.definition),
            ('stability',self.stability),
            ('date_created',self.date_created.strftime('%Y-%m-%d %H:%M:%S')),
            ('next_review',self.next_review.strftime('%Y-%m-%d %H:%M:%S'))
        ])
        return export

class Deck:
    def __init__(self,database):
        '''Initialises card deck'''
        self.database = database
        self.cards = [self.create_card(entry) for entry in database.entries]
        self.stage()

    def create_card(self,dictionary):
        '''Creates a card from a dictionary setting default values if needed.'''
        dictionary.setdefault('stability',0)
        dictionary.setdefault('date_created','1970-01-01 00:00:00')
        dictionary.setdefault('next_review','1970-01-01 00:00:00')
        return Card(dictionary)

    def overdue(self):
        '''Returns a list of cards with overdue review dates.'''
        overdue = []
        for card in self.cards:
            cond1 = card.next_review < (datetime.now() + timedelta(days=0.5))
            cond2 = int(card.stability) < 31
            cond3 = card.date_created != datetime(1970,1,1)
            if cond1 and cond2 and cond3:
                overdue.append(card)
        return sorted(overdue, key=lambda card:card.next_review)

    def import_cards(self,file):
        '''Imports new cards from database file.'''
        entries = self.database.import_cards(file)
        for entry in entries:
            self.cards.append(self.create_card(entry))
        self.stage()
        
    def export(self):
        '''Exports the deck to database file.'''
        self.database.entries = []
        for card in self.cards:
            self.database.entries.append(card.export())
        self.database.write()

    def created_today(self):
        '''Returns number of cards in deck created today.'''
        created = 0
        for card in self.cards:
            if datetime.now() - card.date_created < timedelta(hours=18):
                created +=1
        return created     

    def stage(self):
        '''Stages daily amount of unstaged cards'''
        unstaged_date = datetime(1970,1,1)
        unstaged = [card for card in self.cards if card.date_created == unstaged_date]
        to_stage = 7 - self.created_today()
        for card in unstaged[:to_stage]:
            card.date_created = datetime.now()
            card.next_review = datetime.now()

class Menu:
    def __init__(self,deck):
        '''Initialises the application menu.'''
        self.deck = deck
        self.options = {
            'xx': self.exit,
        }
        self.input = Input(self.options)
        self.main()

    def message(self):
        '''Creates welcome message.'''
        length = len(self.deck.overdue())
        message = '{} cards to review'.format(length)
        if length == 0:
            message = 'Finished!'
        return message

    def main(self,message=None):
        '''Displays the main menu.'''
        if not message:
            message = self.message()
        self.clear()
        main_menu = [
            '🔥 Takibi 🔥',
            '{}\n\n'.format(message),
            '1. Study',
            '2. Save',
            '3. Import',
            '4. Quit']
        main_options ={
            '1': self.study,
            '2': self.save,
            '3': self.import_cards,
            '4': self.exit,
        }
        Input.lprint(main_menu)
        action = self.input.eval()
        self.clear()
        if action in main_options:
            main_options[action]()
        else:
            self.main()

    def clear(self):
        '''Clears the terminal screen.'''
        tmp = subprocess.call('clear',shell=True)

    def study(self):
        '''Start a session.'''
        while len(self.deck.overdue()) > 0:
            self.review_card()
            self.clear()
            self.deck.overdue()
        self.main('Finished!')

    def review_card(self):
        '''Displays card for review.'''
        card = self.deck.overdue()[0]
        self.display_question(card)
        flip = self.input.eval('Hit enter to flip card >>> ')
        self.clear()
        self.display_answer(card)
        answer = self.input.eval('Fail:1 or pass:2 >>> ')
        self.answer(card,answer)

    def display_question(self,card):
        '''Presents the question side of the card.'''
        front = [
            '「{}」'.format(card.clozedexample).format('_' * len(card.cloze)),
            ' ',
            ' ',
            ' ',
            ' ',
            card.definition,
            card.meaning,
            ' ',
        ]
        Input.lprint(front)

    def display_answer(self,card):
        '''Presents the answer side of the card.'''
        back = [
            card.clozedexample.format(card.cloze),
            ' ',
            card.key,
            card.pronunciation,
            ' ',
            card.definition,
            card.meaning,
            ' '
        ]
        Input.lprint(back)

    def answer(self,card,answer):
        '''Evaluates user answer to a card.'''
        if answer == '1':
            card.test(False)
        elif answer == '2':
            card.test(True)
        else:
            answer = self.input.eval('Invalid input. Try again.\n>>> ')
            self.answer(card,answer)

    def save(self):
        self.deck.export()
        self.main('Deck saved')

    def import_cards(self):
        # file = self.input.eval('input file name\n>>> ')
        # file name currently hard coded
        # add input option only actually useful
        self.deck.import_cards(import_db_file)
        self.deck.overdue()
        self.main('Import successful\n{}'.format(self.message()))
    
    def exit(self):
        self.clear()
        '''Exits the application.'''
        print('Saving...')
        self.deck.export()
        print('Exiting Takibi...')
        sys.exit(0)

class Input:
    def __init__(self,options):
        '''Initialises the input with an options object'''
        self.options = options

    def eval(self,prompt='>>> '):
        '''evalutates a string to see if it contains an option
        and returns either that option or the string'''
        output = input(prompt)
        if output in self.options:
            output = self.options[output]()
        return output

    @staticmethod
    def lprint(list):
        '''Prints each item of a list to a new line.'''
        for item in list:
            print(item)

def run():
    db = Database(db_file)
    d = Deck(db)
    m = Menu(d)
from deck import Deck
from card import Card
from menu import Menu

if __name__ == '__main__':
    # for easy testing purposes
    s = '漢字,かんじ,kanij,日本語は{漢字}で書く'
    s_list = s.split(',')

    d = Deck()

    d.add_card(s_list)
    d.add_card(s_list)
    d.add_card(s_list)
    d.add_card(s_list)

    m = Menu(d)


import os
import time
import random
from os import system, name
import sys


class Deck:
    def __init__(self):
        self.cards = []
        self.new_deck()

    def new_deck(self):
        self.cards.clear()
        values = [11, 10, 10, 10, 10, 9, 8, 7 ,6, 5, 4, 3, 2]
        names = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        suits = ['♣', '♠', '♦', '♥']

        for i in range(len(values)):
            for suit in suits:
                self.cards.append(Card(names[i], suit, values[i]))
 
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.cards)

    def print_deck(self):
        for card in self.cards:
            card.print_card()

    def draw_card(self):
        card = self.cards.pop()
        return card


class Card:
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value


    def print_card(self):
        print(f'+----+')
        print(f'|{self.suit}   |')
        print(f'| {self.name:2} |')
        print(f'|   {self.suit}|')
        print(f'+----+')


class Player:
    def __init__(self):
        self.hand = []
        self.chips = 100
        self.choice = ''

    def print_hand(self):
        number_of_cards = len(self.hand)
 
        for i in range(number_of_cards):
            print(f'+----+ ' , end='')
 
        print()
        for i in range(number_of_cards):
            card = self.hand[i]
            print(f'|{card.suit}   | ' , end='')
 
        print()
        for i in range(number_of_cards):
            card = self.hand[i]
            print(f'| {card.name:2} | ', end='')
 
        print()
        for i in range(number_of_cards):
            card = self.hand[i]
            print(f'|   {card.suit}| ' , end='')
 
        print()    
        for i in range(number_of_cards):
            print(f'+----+ ', end='')       


    def calc_hand(self):
        value = 0
        for card in self.hand:
            value += card.value

        if value > 21:
            for card in self.hand:
                if card == 11:
                    value -= 10
                if value <= 21:
                    break

        return value


def print_logo():
    print(r'''
                                        WELCOME TO:
        ===================================================================================                                
           __       ___                    __                             __      __     
          /\ \     /\_ \                  /\ \        __                 /\ \    /\ \    
          \ \ \____\//\ \      __      ___\ \ \/'\   /\_\     __      ___\ \ \/'\\ \ \   
           \ \ '__`\ \ \ \   /'__`\   /'___\ \ , <   \/\ \  /'__`\   /'___\ \ , < \ \ \  
            \ \ \L\ \ \_\ \_/\ \L\.\_/\ \__/\ \ \\`\  \ \ \/\ \L\.\_/\ \__/\ \ \\`\\ \_\ 
             \ \_,__/ /\____\ \__/.\_\ \____\\ \_\ \_\_\ \ \ \__/.\_\ \____\\ \_\ \_\/\_\
              \/___/  \/____/\/__/\/_/\/____/ \/_/\/_/\ \_\ \/__/\/_/\/____/ \/_/\/_/\/_/
                                                     \ \____/                            
                                                      \/___/                             
        ====================================================================================
          ''')

#Create the game components
player = Player()
dealer = Player()
deck = Deck()


def print_game():
    time.sleep(1)
    clear_screen()
    print_logo()

    print('\n~~~DEALER~~~')
    dealer.print_hand()
    print()
    if dealer.choice == 'H' or dealer.choice == 'S':
        print(f'Hand value: {dealer.calc_hand()}')
    else:
        print()

    print('\n~~~PLAYER~~~')
    player.print_hand()
    print(f'\nChips: {player.chips}')
    print(f'Hand value: {player.calc_hand()}')


def clear_screen():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux 
    else: 
        _ = system('clear') 


def new_game():
    # Reset all parameters
    deck.new_deck()

    player.hand.clear()
    player.choice = ''

    dealer.hand.clear()
    dealer.choice = ''

    print_game()

    # Deal new cards
    # Two to player and one to dealer

    player.hand.append(deck.draw_card())
    print_game()
    dealer.hand.append(deck.draw_card())
    print_game()
    player.hand.append(deck.draw_card())
    print_game()

# Start new game
new_game()

while True:
    # Player turn

    while player.choice != 'S':
        print_game()
        player.choice = input('Do you want to (h)it or (s)tand? ').upper()

        if player.choice == 'H':
            player.hand.append(deck.draw_card())

        print_game()

        # Check to see if player goes over 21
        if player.calc_hand() > 21:
            dealer.choice = 'S'
            dealer.hand.append(deck.draw_card())
            player.chips -= 5
            print_game()
            print('\nPlayer Bust. Lose 5 chips')

            play_again = input('Do you want to keep playing? (Y)es or (N)o? ').upper()
            new_game()
         
            # while True:
            #     play_again = input('Do you want to keep playing? (Y)es or (N)o? ').upper()
            #     if play_again == 'Y':
            #         new_game()
            #         continue
            #     elif play_again == 'N':
            #         print('Thanks for playing blackjack. Please come again')
            #         time.sleep(3)
            #         sys.exit()

    # Dealer turn
    while dealer.choice != 'S':
        print_game()

        if dealer.calc_hand() < player.calc_hand() or dealer.calc_hand() < 17:
            dealer.hand.append(deck.draw_card())
            dealer.choice = 'H'

        else:
            dealer.choice = 'S'

        print_game()

        if dealer.calc_hand() > 21:
            player.chips += 5
            print_game()
            print('\nDealer busts. Player gains 5 chips')
            play_again = input('Do you want to keep playing? (Y)es or (N)o? ').upper()
            new_game()



    # Who wins is closest to 21
    if player.calc_hand() > dealer.calc_hand():
        player.chips += 5
        print_game()
        print(f'\nPlayer wins with score {player.calc_hand()} vs dealer score {dealer.calc_hand()}')
        print('\nGain 5 chips')
        new_game()
    else:
        player.chips -= 5
        print_game()
        print(f'\nDealer wins with score {dealer.calc_hand()} vs player score {player.calc_hand()}')
        print('\nLose five chips')
        play_again = input('Do you want to keep playing? (Y)es or (N)o? ').upper()
        new_game()


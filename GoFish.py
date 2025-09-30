#!/usr/bin/env python3
'''
Date: March 23, 2017
Author: Wren Kohler
'''
#Go Fish game
import random

def to_card_string(card):
    '''
    returns cards in string notation
    '''
    ranks = ["Ace","2","3","4","5","6","7",
                   "8","9","10","Jack","Queen","King"]
    suits = ["Hearts", "Diamonds", "Spades","Clubs"]
    return ranks[card[0]] + " of " + suits[card[1]]

def get_rank_counts(hand):
    '''
    returns list of how often each rank 0-12 occurs in a hand
    e.g., list[2] = # of 3s, list[10] = # of jacks
    '''
    counts = [0]*13
    for card in hand:
        rank = card[0]
        counts[rank] += 1
    return counts


def get_deck():
    '''
    create and return an unshuffled deck of cards
    '''
    deck = []
    for rank in range(0,13):
        for suit in range(0,4):
            deck.append([rank,suit])
    return deck

def update_deck(deck, hand):
    '''
    updates deck by removing the cards already in hand
    '''
    for card in hand:
        deck.remove(card)
    return deck


def get_hand(deck, n):
    '''
    shuffles deck and takes a random slice of length n
    '''
    random.shuffle(deck)
    return deck[0:n]

def print_hand(hand):
    '''
    prints hand passed to it
    '''
    print('[', end  = ' ')
    for i in range(0,len(hand)-1):
        print(to_card_string(hand[i]) + ' ][ ', end = ' ')
    print(to_card_string(hand[-1]), end = ' ')
    print(']')


def print_format(books, token):
    '''
    prints format for each round
    '''
    if token == 0:
        print('*'.center(30, '*'))
        print('SCORE: Player: ' + str(books['player']) + ' | Opponent: '
          + str(books['opponent']))
        print('>Your turn')
    else:
        print('>>Opponent turn')

def guess(hand):
    '''
    takes a guess from the player
    '''
    guess = input('Enter guess (or enter R to see guessing rules): ')
    while True:
        while (guess.lower() != 'r' and guess != '+'
               and guess not in '1 2 3 4 5 6 7 8 9 10 11 12 13'):
            guess = input('Enter guess (or enter R to see rules): ')
        if guess.lower() == 'r':
            print_guessing_rules()
            guess = input('Enter guess (or enter R to see rules): ')
        elif guess == '+':
            print_hand(hand)
            guess = input('Enter guess (or enter R to see rules): ')
        elif guess == '':
            guess = input('Enter guess (or enter R to see rules): ')
        else:
            break
    return guess


def check_books(hand, books, token):
    '''
    checks for books and updates dictionary and each hand
    '''
    ranks = get_rank_counts(hand)
    hand_changed = hand[:]
    for i in range(0,13):
        if ranks[i] == 4:
            for card in hand:
                if card[0] == i:
                    hand_changed.remove(card)
            if token == 0:
                books['player'] += 1
            else:
                books['opponent'] += 1
    return (hand_changed, books)

def check_guess(guess, deck, player_hand, opp_hand, token):
    '''
    checks guess for each player, if found takes cards and moves them
    if not found, draws from deck
    '''
    return_list = []
    key = 0
    if token == 0:
        print('      Do I have any %ss?' % guess)
        for card in opp_hand:
            if card[0] == int(guess)-1:
                return_list.append(card)
        if len(return_list) == 0:
            print('      Nope, go fish!')
            draw_card = get_hand(deck, 1)
            if len(draw_card) != 0:
                deck = update_deck(deck, draw_card)
                print('Card drawn: ', end = ' ')
                print_hand(draw_card)
                player_hand += draw_card
            else:
                print('Deck is empty!')
        else:
            print('      Yes, I have %d %s(s)' % (len(return_list), guess))
            for card in return_list:
                opp_hand.remove(card)
                card = [card]
                player_hand += card
                key = 1
    else:
        print('      Do you have any %ss?' % guess)
        for card in player_hand:
            if card[0] == int(guess)-1:
                return_list.append(card)
        if len(return_list) == 0:
            print("      No? I'll go fish!")
            opp_draw_card = get_hand(deck, 1)
            if len(opp_draw_card) != 0:
                deck = update_deck(deck, opp_draw_card)
                opp_hand += opp_draw_card
            else:
                print('Deck is empty!')
        else:
            print('      Yes! You had %d %s(s)' % (len(return_list), guess))
            for card in return_list:
                player_hand.remove(card)
                card = [card]
                opp_hand += card
                key = 1
    return (deck, player_hand, opp_hand, key)


def take_turn(deck, player_hand, opp_hand, books):
    '''
    plays one full turn (one player turn and one opponent turn)
    '''
    print_format(books, 0)
    key = 1
    while key == 1:
        if books['player'] + books['opponent'] == 13:
            return (deck, player_hand, opp_hand, books)
        if len(player_hand) != 0:
            print('Your hand: ', end = ' ')
            print_hand(player_hand)
        if len(player_hand) == 0 and len(deck) != 0:
            player_hand = get_hand(deck, 5)
        (player_hand, books) = check_books(player_hand, books, 0)
        your_guess = guess(player_hand)
        (deck, player_hand, opp_hand, key) = check_guess(
            your_guess, deck, player_hand, opp_hand, 0)
        (player_hand, books) = check_books(player_hand, books, 0)
    if books['player'] + books['opponent'] == 13:
        return (deck, player_hand, opp_hand, books)
    print_format(books, 1)
    key = 1
    while key == 1:
        if books['player'] + books['opponent'] == 13:
            return (deck, player_hand, opp_hand, books)
        if len(opp_hand) == 0 and len(deck) != 0:
            opp_hand = get_hand(deck, 5)
            print('got sum')
        opp_guess = random.randint(1,13)
        (deck, player_hand, opp_hand, key) = check_guess(
            opp_guess, deck, player_hand, opp_hand, 1)
        (opp_hand, books) = check_books(opp_hand, books, 1)
    return (deck, player_hand, opp_hand, books)


def initialize():
    '''
    creates deck, hand for player, hand for opponent
    '''
    deck = get_deck()
    books = {'player' : 0, 'opponent' : 0}
    hand_a = get_hand(deck, 5)
    deck = update_deck(deck, hand_a)
    hand_b = get_hand(deck, 5)
    deck = update_deck(deck, hand_b)
    return (deck, hand_a, hand_b, books)

def start_game():
    '''
    starts and plays game
    '''
    print('Welcome to Go Fish!')
    (ocean, player_hand, opp_hand, books) = initialize()
    while True:
        (ocean, player_hand, opp_hand, books) = take_turn(
            ocean, player_hand, opp_hand, books)
        if books['player'] + books['opponent'] == 13:
            break
    end_game(books)

def end_game(score):
    if score['player'] > score['opponent']:
        print('Congratulations, YOU WIN!')
        print('Final score was: Player: ' + str(score['player'])
              + ' | Opponent: ' + str(score['opponent']))
    elif score['opponent'] > score ['player']:
        print('YOU LOSE'.center(30,'*'))
        print('Final score was: Player: ' + str(score['player'])
              + ' | Opponent: ' + str(score['opponent']))
    play_again = input('Play again? (y/n): ')
    while play_again.lower() != 'y' and play_again.lower() != 'n':
        play_again = input('Please enter y or n ')
    if play_again.lower() == 'y':
        start_game()
    else:
        print('Thank you for playing!')
        print()
        exit()


def print_game_rules():
    '''
    prints out rules to the game
    '''
    print('*'.center(50,'*'))
    print('RULES TO GO FISH (credit to Hoyle Gaming)')
    print('Each player gets five cards. If you are dealt a four of a \
kind, or get four of a kind during game play, those cards are \
removed from your hand, and you get a point.')
    print('Moving clockwise, players take turns asking a specific player \
for a given rank of card. If someone asks you for a rank that you have, \
the cards are taken from your hand. if you do not have any cards of \
that rank, your opponent must go fish, taking one new card from the pile \
of cards.')
    print('When it\'s your turn, select a player you think might have a \
needed card. Pick a desired rank of card. If the \
player has the desired card, he or she must pass it over. If not, you \
must go fish. If you get the card you asked for, you get to go again.')
    print('If you run out of cards and there are still cards left, you get \
five free cards. Play continues until all hands are empty and there are \
no more cards to draw from. The winner is the player with the most \
points at the end of the game.')
    print()

def print_guessing_rules():
    '''
    prints out the rules for guessing
    '''
    print('When asked for guess, enter number 1 to 13 for card rank')
    print('ex: 1 ace, 2 two ... 11 jack, 12 queen, 13 king')
    print('You can also enter + to see your hand')


if __name__ == "__main__":
    print_game_rules()
    print_guessing_rules()
    start_game()

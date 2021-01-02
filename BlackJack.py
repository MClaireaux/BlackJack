# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:36:54 2020

@author: marion
"""
# ** Import libraries **

import random
import Blackjack_ASCII
import os
from time import sleep

# ** Import logo **
# Turn = player turn: If there are several players, there are several turns in one round
# Round = A round is over after the dealer played. There are several rounds in one game


def blackjack():    
# *** Starting the program
    print(Blackjack_ASCII.logo)
    play_game = input("Would you like to play BlackJack? y or n: ")
    
    if play_game == "y": # Game has started

# *** Preparation of the game book, with initial settings
#Get the list of players
        name_list=input("Enter player names separated by a space: ").split(" ") 
        if '' in name_list:   #Remove any accidental space                                                  
            name_list.remove('')     
  
#Create a dictionary entry for the dealer      
        game_book = {
            'dealer': {
                "hand": [], #Stores the ASCII art for the hand
                'card_nb': [], #Stores the value of the cards in the hand
                'score': 0, # Stores the score of the player
                }
            }                                                         
                                                                              
 #Create a dictionary entry for every player       
        for people in name_list: 
            game_book[people] = {}                                       
            game_book[people]["chips"] =  50   #Chips number    
                  
#Cards and score are defined at the start of player turn as they need to be reset at the start of each round
#Starting chips are defined now as their will be updated each round

        game_is_on = True #Starting the game                                     
        
        print("\nEach player got 50 chips")
        sleep(2)
        clear()
        # *** Starting the game      
        while game_is_on:  #                                                     
            
            card_deck = Blackjack_ASCII.cards #Load ASCII art card game
            
            # *** Starting the round
            for people in game_book:
                
                #Finish the initial entry for each player in the dictionary
                game_book[people]["hand"] = [] #Initial hand
                game_book[people]["card_nb"] = [] #value of the cards in the hand
                game_book[people]["score"] = 0 #Initial score
                
                #Deal the starting hand and update the player entry accordingly
                for _ in range(2):
                    new_score(game_book[people], card_deck) 
                
                #Deal cards to the dealer and make him play. His results are not shown until the end of the round
                if people == "dealer": #                                         
                    card_up = game_book[people]['hand'][0] #Save the ASCII art of the first card to show it to player later
                    
                    #The dealer plays until he has a score smaller than 17
                    while game_book[people]['score'] < 17:                      
                        new_score(game_book[people], card_deck)                     
                 
                # *** Starting the turn
                else:
                    player_turn = True                                         
                    print(f"♣️ ♦️ It is {people}'s turn ❤️ ♠️")
                    print(f"\nYou have {game_book[people]['chips']} chips. ")
                    sleep(1)
                    #Player places a bet before his hand and dealer's hand is revealed
                        #The function creates an entry in player dictionnary to save the bet
                        #If the bet is higher than the number of chips or is not a number, it returns an error and asks for another entry
                    bet_input(game_book[people])                
                
                    # If a player gets 21 from the start, he gets a BlackJack and his turn is over
                    if game_book[people]['score'] == 21:  
                        print("♠️ ❤️ ♣️ ♦️  You have got a BlackJack! Your turn is over ♣️ ♦️ ❤️ ♠️")
                        print_card(game_book[people]['hand']) #Shows player hand in ASCII art
                        #Store the result for the summary at the end of the game
                        game_book[people]['result'] = "♠️ ❤️ ♣️ ♦️ You got a blackjack. You win double your bet! ♣️ ♦️ ❤️ ♠️"  
                        #Update the amount of chips
                        game_book[people]['chips'] += game_book[people]['bet']*2
                        #Player turn is over
                        player_turn = False
                        sleep(1)
                    
                    #If no BlackJack
                    while player_turn == True: 
                        clear()
                        #Show player hand in ASCII art and player score
                        print(f"♣️ ♦️ It is {people}'s turn ❤️ ♠️")
                        print(" ")
                        print(f"Your score is: {game_book[people]['score']}")
                        print_card(game_book[people]['hand'])
                        #Show dealer card
                        print(f"\nThe dealer has:\n{card_up}")
                        sleep(1)
                        
                        #The player can choose to hit or stand
                        #If the player stands
                        if input("Press any key to draw another card, N to pass: ") == "N": 
                                #Compare the player hand to dealer hand
                                #Update the player chips number and save the result in the dictionary
                                compare_cards(game_book['dealer']['score'],game_book[people])   
                                #End player turn
                                player_turn = False
                                clear()

                        #If the player hits        
                        else:
                            #Give a new card and update the hand and score of player accordingly
                            new_score(game_book[people], card_deck)   
                            clear()
                            
                            #If the player goes over 21 after picking a card
                            if game_book[people]['score'] > 21:
                                #Print score and hand
                                print(f"♣️ ♦️ It is {people}'s turn ❤️ ♠️")
                                print(" ")
                                print("You went over 21! Your turn is over")
                                print_card(game_book[people]['hand'])
                                #Save result and update chips
                                game_book[people]['result'] = "You went over 21. You lose your bet."
                                game_book[people]['chips'] -= int(game_book[people]['bet'])
                                #End player turn
                                player_turn = False
                                sleep(2)
                                clear()
                                
                            #If the player's score is under 21, we go back at the start of while player_turn 
                            #and the player is offered to hit or stand again
                                
                            
            # *** Ending the round
            #Show dealer's hand and score  
            clear()             
            print("♠️ ❤️ ♣️ ♦️ ♠️ ❤️ ♣️ ♦️ End of game: ♠️ ❤️ ♣️ ♦️ ♠️ ❤️ ♣️ ♦️")
            print(f"The dealer score is {game_book['dealer']['score']}")
            print_card(game_book['dealer']['hand'])
            sleep(2)
            
            # Summary of the round
            for people in game_book:
                
                if people != "dealer":
                    #If people went under 0, chips number is set to 0
                    if game_book[people]['chips'] < 0:
                        game_book[people]['chips'] = 0
                    #Summary each player's turn, showing result and updated amount of chips
                    print(" ")
                    print(f"{people}, {game_book[people]['result']} You have {game_book[people]['chips']} chips left.")
                    #If a player does not havve chips, it is kicked out of the game
                    if game_book[people]['chips'] == 0:
                        print(f"{people} lost all his/her chips! {people} is out of the game.")
                        del game_book[people]
                        
            #Player can choose for another round, another gane or to exit the program
            choose_again = True
            
            while choose_again == True:
                user_choice = input("Would you like to play again? Type Y for a new round, N for a new game or E to exit the program:")

                if user_choice == "Y":
                    game_is_on = True
                    choose_again = False
                    #One more round
                    clear()
                elif user_choice == "N":
                    print("♣️ ♦️ Let's start over! ❤️ ♠️")
                    print(" ")
                    choose_again = False
                    clear()
                    blackjack()
                    #Starts a new game
                    
                elif user_choice == "E":
                    print("♣️ ♦️ It was fun playing with you. Good-bye! ❤️ ♠️") 
                    game_is_on = False
                    #Exit the program
                else:
                    print("This is an invalid answer.")
                    choose_again = True
                    #Back at the start of the while loop

    # *** Ending the turn            
    elif play_game == 'n':
        game_is_on = False
        print("♣️ ♦️ It was fun playing with you. Good-bye! ❤️ ♠️")
        #Exit program
    else:
        print('This key is not recognised')
        blackjack()
        #Starts again if play_game input is not 'n' or 'y'
        

      
    
def compare_cards(dealer_score, game_book):
    ''' Compares player and dealer score. Updates player result and chips '''    
    if dealer_score > 21:
        game_book['result'] = "The dealer went over 21, you won your bet."
        game_book['chips'] += int(game_book['bet'])
        
    elif dealer_score > game_book['score']:
        game_book['result'] = f"Your score is {game_book['score']}. The dealer has a higher score, you lose your bet."
        game_book['chips'] -= int(game_book['bet'])

    elif dealer_score < game_book['score']:
        game_book['result'] = f"Your score is {game_book['score']}. ♣️ ♦️ You have a higher score, you won what you bet! ❤️ ♠️"
        game_book['chips'] += int(game_book['bet'])
                                
    else:
        game_book['result'] = f"Your score is {game_book['score']}. It is a draw, you do not gain or lose anything!"

    
def new_score(game_book, deck):
    ''' give a new card to the player, update player hand and score'''
    delt_card = deal(deck)
    game_book['hand'] += [delt_card[0]]
    game_book['card_nb'] +=  [delt_card[1]]          
    game_book['score'] += delt_card[1]
                    
    if game_book['score'] > 21 and 11 in game_book['card_nb']:    
        game_book['card_nb'] = [1 if x==11 else x for x in game_book['card_nb']]
    
    game_book['score'] = sum(game_book['card_nb'])
    


def deal(deck):
    ''' Pick a random card from the deck. The card is then removed, so it cannot be picked again'''
    
    card_picture =False
    while card_picture == False:
        #Pick a random suit
        card_suit= random.choice(range(1,5))
        #Pick a random card
        card_value= random.choice(range(1,15))
        
        #Store the card corresponding to the random pick. Delete the card from the deck dictionary.
        #I the card was previously picked, the loop starts again to pick a new card
        card_picture = deck[card_suit].pop(card_value, False)
        
        #Jacks, Queens and Kings have an initial value of 12, 13 and 14 in the deck
        #We need to set their value at 10 for the sake of the game
        if card_value > 11:
            card_value = 10
        
    return [card_picture,  card_value]


def bet_input(game_book):
    '''Function to ensure the bet entered does not go over the nb of chips'''
    try:
        game_book['bet'] = int(input('How much would you like to bet? '))
        while game_book['bet'] > game_book['chips']:
            game_book['bet'] = int(input("You do not have enough chips. Pick another bet: "))
    except ValueError:
        print("This is not a number.")
        bet_input(game_book)                


def print_card(hand):
    '''Function to print the hand in ASCII art, with the cards side by side '''
    #We need one entry per card
    hand_size = [] 
    for i in range(len(hand)):
        hand_size += [i]  
    #We split the art for each card in lines    
    lines = [hand[i].splitlines() for i in hand_size]
    for l in zip(*lines):
        #Print the first lines of each cards 
        #Then the second
        #etc....
        print(*l, sep='')
    
def clear(): 
    '''Clear the console'''
    print('\033[H\033[J', end='')

# now call function we defined above
    
blackjack()
       
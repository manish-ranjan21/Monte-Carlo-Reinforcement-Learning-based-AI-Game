# import numpy
# import matplotlib
import pandas as pd
import gym
from gym import spaces
import os
import Blackjack_func
import random
from datetime import datetime
import threading
import sys


#create a counter to keep track of how many games were played
gameCounter = 0
blackjackcounter = 0

#From proposal, we decided that the user would start out with $100 in the bank
bank = 100.00
max_bank = bank

#if no value is supplied, 2 is the default bet value (not applicable in case of AI playing)
default_bet_value = 2.00

## Number of wins and losses
wins = 0
losses = 0
ties = 0

win_df = pd.DataFrame({"win":[]})

##Agent Reward tracker
RoundRewards = []

#Initiatlizing agent continue playing
AgentContinue = 'Y'


file = 'InteractiveLogs/'+str(os.path.basename(__file__)).replace('.py','')+datetime.now().strftime("%Y%m%d_%H%M%S")+'.log'

o = open(file,'w')
def print_both(*args):
    toprint = ' '.join([str(arg) for arg in args])
    print(toprint)
    o.write("\n"+toprint)


#currently utilizing a while loop for testing. If Bank goes below 1.00 or deck goes below a summed value of 60, stop
#When the deck class is created, we can create a nested while loop
#The outer loop will check for bank value, the inner loop will check for deck size and re-shuffle when deck goes below a summed value of 60
while bank >= 1.00 and str.upper(AgentContinue) in ('Y','YES'):
    if gameCounter == 0:
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)
    
    #Agent choice each new turn, currently set to default value for testing
    if gameCounter > 0:
        print_both("Would you like to keep the same bet amount?")
        keep_bet = input()
        o.write("\n"+keep_bet)
        while str.upper(keep_bet) not in ('Y','N','YES','NO'):
            print_both("incorrect value, please enter Y,N,YES, or NO")
            keep_bet = input()
            o.write("\n"+keep_bet)
        if str.upper(keep_bet) in ('N','NO'):
            print_both("please choose your bet value (1,2,5, or 10)")
            init_bet = input()
            o.write("\n"+init_bet)
            while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
                print_both("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
                init_bet = input()
                o.write("\n"+init_bet)
    else:
        print_both("please choose your bet value (1,2,5, or 10)")
        init_bet = input()
        o.write("\n"+init_bet)
        while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
            print_both("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
            init_bet = input()
            o.write("\n"+init_bet)
    
        
    if init_bet == '':
        bet = 2.00
    elif str.lower(init_bet) == 'one':
        bet = 1.00
    elif str.lower(init_bet) == 'two':
        bet = 2.00
    elif str.lower(init_bet) == 'five':
        bet = 5.00
    elif str.lower(init_bet) == 'ten':
        bet = 10.00
    else:
        bet = float(init_bet)
        
    while bet > bank:
        print_both("Error, bank amount too low, please lower your bet")
        print_both("please choose your bet value (1,2,5, or 10)")
        init_bet = input()
        o.write("\n"+init_bet)
        while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
            print_both("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
            init_bet = input()
            o.write("\n"+init_bet)
        if init_bet == '':
            bet = 2.00
        elif str.lower(init_bet) == 'one':
            bet = 1.00
        elif str.lower(init_bet) == 'two':
            bet = 2.00
        elif str.lower(init_bet) == 'five':
            bet = 5.00
        elif str.lower(init_bet) == 'ten':
            bet = 10.00
        else:
            bet = float(init_bet)
    
    
    #BREAK OUT INTO ITS OWN FUNCTION FOR HOUSE DRAW
    #Agent does not see house values until they stay, hit blackjack, or bust
    #The House Draw is the initial hand for the dealer
    house_draw = []
    #re-shuffling each time to ensure randomness in draw
    random.shuffle(deck)
    #Using pop to remove the last value in the deck to ensure that it cannot be selected again
    house_draw.append(deck.pop(random.randrange(0,len(deck))))
    if sum(deck) < 1:
        #re-create deck
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)
    
    random.shuffle(deck)
    house_draw.append(deck.pop(random.randrange(0,len(deck))))
    if sum(deck) < 1:
        #re-create deck
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)
    
    
    if sum(house_draw) == 21:
        print_both("initial house cards: "+str(house_draw[0])+" + "+str(house_draw[1]))
        print_both("House Blackjack, Check your draw... if you have blackjack it is a push, if you do not it is a draw")
    elif sum(house_draw) == 22:
        #because it is possible to draw 2 aces in a single hand, we want to force one of those aces to be a 1 (since ace value by default is 11, but can be 1)
        house_draw[1] = 1
        print_both("initial house cards: "+str(house_draw[0])+" + ??")
    else:
        print_both("initial house cards: "+str(house_draw[0])+" + ??")
    
    #BREAK OUT INTO ITS OWN FUNCTION FOR AGENT DRAW
    #The Agent Draw is the initial hand for the Agent
    agent_draw = []
    random.shuffle(deck)
    agent_draw.append(deck.pop(random.randrange(0,len(deck))))
    if sum(deck) < 1:
        #re-create deck
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)
    
    random.shuffle(deck)
    agent_draw.append(deck.pop(random.randrange(0,len(deck))))
    if sum(deck) < 1:
        #re-create deck
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)
    
    
    #setting variable for agent choice of "Hit" or "Stay"
    agent_choice = "Hit" #Scenario if the agent always hit
    
    #setting variable for agent choice for converting ace value to 1 "Y" or "N"
    agent_choice_ace = "Y" #Scenario if the agent always converted ace to 1
    
    #Initializing agent blackjack status. 
    blackjack_status = 'N'
    
    #Initializing agent bust status.
    bust = 'N'
    
    #START GAME AGENT CHOICE LOGIC
    if sum(agent_draw) == 22:
        agent_draw[1] = 1
    
    print_both("initial agent cards: "+str(agent_draw[0])+" + "+str(agent_draw[1]))
    
    if sum(house_draw) == 21:
        print("") 
    elif sum(agent_draw) == 21:
        print_both("Blackjack! Let's see what the house has")
        blackjack_status = 'Y' #updating to 'Y' because agent_draw has blackjack
    else:
        #The following nested if-else statements check for whether the agent would like to hit or stay
        #There are 16 layers currently based off of 3 decks: 
            #There are 12 possible aces in the deck and if the initial draw is an ace and a 2 then the rest of the aces are drawn and then remaining 2s until 21, that is 16 possible hands
        agent_choice = ''
        endloop = 'N'
        while str.lower(agent_choice) != 'stay' and bust == 'N' and endloop == 'N':
            if 21-sum(agent_draw) < 10:
                odds = round((1-((21-sum(agent_draw))/13))*100,2)
            else:
                odds = 0
            print_both("Current hand value: "+str(sum(agent_draw))+" There is a "+str(odds)+"% chance of going over if you hit")
            print_both("Would you like to Hit or Stay?")
            agent_choice = input()
            o.write("\n"+agent_choice)
            while str.lower(agent_choice) not in ('hit','stay'):
                print_both("incorrect value, please enter hit or stay")
                agent_choice = input()
                o.write("\n"+agent_choice)
            if str.lower(agent_choice) == "stay":
                print("") 
            elif str.lower(agent_choice) == "hit":
                if len(deck) < 1:
                    #re-create deck
                    deck = Blackjack_func.Deck().deck()
                    random.shuffle(deck)
                agent_draw.append(deck.pop(random.randrange(0,len(deck))))
                print_both("You drew a(n) "+str(agent_draw[len(agent_draw)-1]))
                try:
                    agent_draw.index(11)
                    print_both("Total with ace as 11: "+str(sum(agent_draw)))
                    print_both("Total with ace as 1: "+str(sum(agent_draw)-10))
                    print_both("Would you like to change your ace value to a 1?")
                    agent_choice_ace = input()
                    o.write("\n"+agent_choice_ace)
                    while str.upper(agent_choice_ace) not in ('Y','N','YES','NO'):
                        print_both("incorrect value, please enter Y,N,YES, or NO")
                        agent_choice_ace = input()
                        o.write("\n"+agent_choice_ace)
                    if str.upper(agent_choice_ace) in ('Y', 'YES'):
                        agent_draw[agent_draw.index(11)] = 1
                except Exception as e:
                    print("") 
                if sum(agent_draw) == 21:
                    endloop = 'Y'
                    print_both("You've hit the max without going over! Let's see what the house has")
                elif sum(agent_draw) > 21:
                    bust = 'Y'
            if sum(deck) < 1:
                #re-create deck
                deck = Blackjack_func.Deck().deck()
                random.shuffle(deck)
        if sum(agent_draw) > 21:
            bust = 'Y'

    #STOP GAME AGENT CHOICE LOGIC
    
    #house rules state that dealer must draw until they reach at least 17. if 17 is reached they must stay
    if blackjack_status == 'N' and bust == 'N':
        while sum(house_draw) < 17:
            if len(deck) < 1:
                deck = Blackjack_func.Deck().deck()
                random.shuffle(deck)
            house_draw.append(deck.pop(random.randrange(0,len(deck))))
            if sum(house_draw) > 21:
                try:
                    house_draw.index(11)
                    house_draw[house_draw.index(11)] = 1
                except:
                    print("") 
            if sum(deck) < 1:
                #re-create deck
                deck = Blackjack_func.Deck().deck()
                random.shuffle(deck)
    
    print_both("House total: "+str(sum(house_draw)))
    print_both("Agent total: "+str(sum(agent_draw)))
    
        #START GAME REWARD LOGIC
    if bust == 'Y':
        print_both("bust! you lose this round")
        bank = bank-bet
        losses = losses+1
        Reward = -1*bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == 21 and sum(agent_draw) == 21:
        print_both("Push, you get your original bet back")
        ties = ties+1
        Reward = 0
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == 21 and sum(agent_draw) != 21:
        print_both("you lose this round")
        bank = bank-bet
        losses = losses+1
        Reward = -1*bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'Y':
        print_both("Blackjack! You win!")
        bank = bank+(bet*2)
        wins = wins +1
        Reward = 2*bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'N':
        print_both("You win!")
        bank = bank+bet
        wins = wins +1
        Reward = bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(agent_draw) > 21:
        print_both("bust! You lose this round")
        bank = bank-bet
        losses = losses+1
        Reward = -1*bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == sum(agent_draw):
        print_both("Push, you get your original bet back")
        ties = ties+1
        Reward = 0
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) < sum(agent_draw):
        print_both("you win!")
        bank = bank+bet
        wins = wins +1
        Reward = bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(house_draw) < 21 and sum(house_draw) > sum(agent_draw):
        print_both("you lose")
        bank = bank-bet
        losses = losses+1
        Reward = -1*bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) > 21 and sum(agent_draw) < 21:
        print_both("you win!")
        bank = bank+bet
        wins = wins +1
        Reward = bet
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    #END GAME REWARD LOGIC
        
    #print_both(sum(deck))
    if sum(deck) < 1:
        #re-create deck
        deck = Blackjack_func.Deck().deck()
        random.shuffle(deck)

    
    gameCounter += 1
    if blackjack_status == 'Y':
        blackjackcounter += 1
    #largest gain
    if bank > max_bank:
        max_bank = bank
    #longest winning streak
    
    print_both("current bank amount: $"+str(bank))
    RoundRewards.append(Reward)
    print_both("Continue Playing?")
    AgentContinue = input()
    o.write("\n"+AgentContinue)
    while str.upper(AgentContinue) not in ('Y','N','YES','NO'):
        print_both("incorrect value, please enter Y,N,YES, or NO")
        AgentContinue = input()
        o.write("\n"+AgentContinue)
    
    #End While Loop

grouper = (win_df.win != win_df.win.shift()).cumsum()
win_df['streak'] = win_df.groupby(grouper).cumsum()

if str.upper(AgentContinue) in ('N', 'NO'):
    print_both("You have chosen not to continue playing")
    print_both("Ending bank value: $"+str(bank))
    print_both("total games played: "+str(gameCounter))
    print_both("total blackjacks: "+str(blackjackcounter))
    print_both(f"total wins so far: {wins}")
    print_both(f"Perecentage wins: {(wins/gameCounter) * 100}%")
    print_both(f"Perecentage wins (excluding ties): {(wins/(gameCounter-ties)) * 100}%")
    print_both("total rewards: "+str(sum(RoundRewards)))
    print_both(f"wins: {wins} losses: {losses} ties: {ties}")
    print_both("maximum gain during playing: $"+str(max_bank-100.00))
    print_both("maximum winning streak: "+str(win_df['streak'].max()))

if bank < 1.00:
    print_both("Game Over, no money left in the bank")
    print_both("total games played: "+str(gameCounter))
    print_both("total blackjacks: "+str(blackjackcounter))
    print_both(f"Perecentage wins: {(wins/gameCounter) * 100}%")
    print_both(f"Perecentage wins (excluding ties): {(wins/(gameCounter-ties)) * 100}%")
    print_both("total rewards: "+str(sum(RoundRewards)))
    print_both(f"wins: {wins} losses: {losses} ties: {ties}")
    print_both("maximum gain during playing: $"+str(max_bank-100.00))
    print_both("maximum winning streak: "+str(win_df['streak'].max()))
    #AI cannot continue if bank < minimum bet
    
o.close()
print("Press 'Enter' when you are ready to close the application")
input()

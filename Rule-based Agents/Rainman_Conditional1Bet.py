# import sys
# import numpy
# import matplotlib
import pandas as pd
# import sklearn
#import tensorforce
#import kerasRL
import os
import Blackjack_func
import random
from datetime import datetime


initdeck = Blackjack_func.Deck()
deck = initdeck.deck()

#create a counter to keep track of how many games were played
gameCounter = 0

#choose the number of times to loop and instantiate the value which will be
loops = 10000
test = 0

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

o = open('logs/'+str(os.path.basename(__file__)).replace('.py','')+datetime.now().strftime("%Y%m%d_%H%M%S")+'.log','w')




#currently utilizing a while loop for testing. If Bank goes below 1.00 or deck goes below a summed value of 60, stop
#When the deck class is created, we can create a nested while loop
#The outer loop will check for bank value, the inner loop will check for deck size and re-shuffle when deck goes below a summed value of 60
while bank >= 1.00 and str.upper(AgentContinue) in ('Y','YES') and test < loops:
    
    #Agent choice each new turn, currently set to default value for testing
    if gameCounter > 0:
        print("Would you like to keep the same bet amount?")
        keep_bet = 'y'
        while str.upper(keep_bet) not in ('Y','N','YES','NO'):
            print("incorrect value, please enter Y,N,YES, or NO")
            keep_bet = 'y'
        if str.upper(keep_bet) in ('N','NO'):
            print("please choose your bet value (1,2,5, or 10)")
            init_bet = "1"
            while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
                print("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
                init_bet = "1"
    else:
        print("please choose your bet value (1,2,5, or 10)")
        init_bet = "1"
        while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
            print("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
            init_bet = "1"
    
        
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
        print("Error, bank amount too low, please lower your bet")
        print("please choose your bet value (1,2,5, or 10)")
        init_bet = "1"
        while str.lower(init_bet) not in ('','1','2','5','10','one','two','five','ten'):
            print("incorrect value, please press enter or input 1, 2, 5, 10, one, two, five, or ten")
            init_bet = "1"
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
    if len(deck) < 1:
        #re-create deck
        deck = initdeck.deck()
    
    random.shuffle(deck)
    house_draw.append(deck.pop(random.randrange(0,len(deck))))
    if len(deck) < 1:
        #re-create deck
        deck = initdeck.deck()
    
    
    if sum(house_draw) == 21:
        print("initial house cards: "+str(house_draw[0])+" + "+str(house_draw[1]))
        print("House Blackjack, Check your draw... if you have blackjack it is a push, if you do not it is a draw", file=o)
    elif sum(house_draw) == 22:
        #because it is possible to draw 2 aces in a single hand, we want to force one of those aces to be a 1 (since ace value by default is 11, but can be 1)
        house_draw[1] = 1
        print("initial house cards: "+str(house_draw[0])+" + ??", file=o)
    else:
        print("initial house cards: "+str(house_draw[0])+" + ??", file=o)
    
    #BREAK OUT INTO ITS OWN FUNCTION FOR AGENT DRAW
    #The Agent Draw is the initial hand for the Agent
    agent_draw = []
    random.shuffle(deck)
    agent_draw.append(deck.pop(random.randrange(0,len(deck))))
    if len(deck) < 1:
        #re-create deck
        deck = initdeck.deck()
    
    random.shuffle(deck)
    agent_draw.append(deck.pop(random.randrange(0,len(deck))))
    if len(deck) < 1:
        #re-create deck
        deck = initdeck.deck()
    
    
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
    
    print("initial agent cards: "+str(agent_draw[0])+" + "+str(agent_draw[1]), file=o)
    print(sum(agent_draw))
    
    if sum(house_draw) == 21 and sum(agent_draw) == 21:
        print("") #Unsure if this should be converted to a break. The logic needs to be in place so that resulting logic can work properly
    elif sum(house_draw) == 21 and sum(agent_draw) != 21:
        print("") #Unsure if this should be converted to a break. The logic needs to be in place so that resulting logic can work properly
    elif sum(agent_draw) == 21:
        print("Blackjack! Let's see what the house has", file=o)
        blackjack_status = 'Y' #updating to 'Y' because agent_draw has blackjack
    else:
        #The following nested if-else statements check for whether the agent would like to hit or stay
        #There are 16 layers currently based off of 3 decks: 
            #There are 12 possible aces in the deck and if the initial draw is an ace and a 2 then the rest of the aces are drawn and then remaining 2s until 21, that is 16 possible hands
        agent_choice = ''
        while str.lower(agent_choice) != 'stay' and sum(agent_draw) < 21 and bust == 'N':
            print("Current hand value: "+str(sum(agent_draw))+" Would you like to Hit or Stay?", file=o)
            if sum(agent_draw) < 17:
                agent_choice = 'hit'
            else:
                agent_choice = 'stay'
            while str.lower(agent_choice) not in ('hit','stay'):
                print("incorrect value, please enter hit or stay")
                if sum(agent_draw) < 17:
                    agent_choice = 'hit'
                else:
                    agent_choice = 'stay'
            if str.lower(agent_choice) == "stay":
                print("")
            elif str.lower(agent_choice) == "hit":
                if len(deck) < 1:
                    #re-create deck
                    deck = initdeck.deck()
                agent_draw.append(deck.pop(random.randrange(0,len(deck))))
                print("You drew a "+str(agent_draw[len(agent_draw)-1]), file=o)
                try:
                    agent_draw.index(11)
                    print("Would you like to change your ace to a 1?")
                    agent_choice_ace = 'y'
                    while str.upper(agent_choice_ace) not in ('Y','N','YES','NO'):
                        print("incorrect value, please enter Y,N,YES, or NO")
                        agent_choice_ace = 'y'
                    if str.upper(agent_choice_ace) in ('Y', 'YES'):
                        agent_draw[agent_draw.index(11)] = 1
                except:
                    print("")
                if sum(agent_draw) == 21:
                    print("You've hit the max without going over! Let's see what the house has", file=o)
                elif sum(agent_draw) > 21:
                    bust = 'Y'
            if len(deck) < 1:
                #re-create deck
                deck = initdeck.deck()

    #STOP GAME AGENT CHOICE LOGIC
    
    #house rules state that dealer must draw until they reach at least 17. if 17 is reached they must stay
    if blackjack_status == 'N' and bust == 'N':
        while sum(house_draw) < 17:
            if len(deck) < 1:
                deck = initdeck.deck()
            house_draw.append(deck.pop(random.randrange(0,len(deck))))
            if sum(house_draw) > 21:
                try:
                    house_draw.index(11)
                    house_draw[house_draw.index(11)] = 1
                except:
                    print("")
            if len(deck) < 1:
                #re-create deck
                deck = initdeck.deck()
    
    print("House total: "+str(sum(house_draw)), file=o)
    print("Agent total: "+str(sum(agent_draw)), file=o)
    
    #START GAME REWARD LOGIC
    if bust == 'Y':
        print("bust! you lose this round", file=o)
        bank = bank-bet
        losses = losses+1
        Reward = -1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == 21 and sum(agent_draw) == 21:
        print("Push, you get your original bet back", file=o)
        ties = ties+1
        Reward = 1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == 21 and sum(agent_draw) != 21:
        print("you lose this round", file=o)
        bank = bank-bet
        losses = losses+1
        Reward = -1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'Y':
        print("Blackjack! You win!", file=o)
        bank = bank+(bet*2)
        wins = wins +1
        Reward = 5
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'N':
        print("You win!", file=o)
        bank = bank+bet
        wins = wins +1
        Reward = 3
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(agent_draw) > 21:
        print("bust! You lose this round", file=o)
        bank = bank-bet
        losses = losses+1
        Reward = -1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) == sum(agent_draw):
        print("Push, you get your original bet back", file=o)
        ties = ties+1
        Reward = 1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) < sum(agent_draw):
        print("you win!", file=o)
        bank = bank+bet
        wins = wins +1
        Reward = 3
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    elif sum(house_draw) < 21 and sum(house_draw) > sum(agent_draw):
        print("you lose", file=o)
        bank = bank-bet
        losses = losses+1
        Reward = -1
        win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
    elif sum(house_draw) > 21 and sum(agent_draw) < 21:
        print("you win!", file=o)
        bank = bank+bet
        wins = wins +1
        Reward = 3
        win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
    #END GAME REWARD LOGIC
        
    #print(sum(deck))
    if len(deck) < 1:
        #re-create deck
        deck = initdeck.deck()

    
    gameCounter += 1
    test += 1
    #largest gain
    if bank > max_bank:
        max_bank = bank
    #longest winning streak
    
    print("current bank amount: $"+str(bank), file=o)
    RoundRewards.append(Reward)
    print("Continue Playing?")
    AgentContinue = 'y'
    while str.upper(AgentContinue) not in ('Y','N','YES','NO'):
        print("incorrect value, please enter Y,N,YES, or NO")
        AgentContinue = 'y'
    
    #End While Loop

grouper = (win_df.win != win_df.win.shift()).cumsum()
win_df['streak'] = win_df.groupby(grouper).cumsum()

if str.upper(AgentContinue) in ('N', 'NO'):
    print("You have chosen not to continue playing")
    print("total games played: "+str(gameCounter))
    print(f"total wins so far: {wins}")
    print(f"Perecentage wins: {(wins/gameCounter) * 100}%")
    print(f"Perecentage wins (excluding ties): {(wins/(gameCounter-ties)) * 100}%")
    print("total rewards: "+str(sum(RoundRewards)))
    print(f"wins: {wins} losses: {losses} ties: {ties}")
    print("maximum gain during playing: $"+str(max_bank-100.00))
    print("maximum winning streak: "+str(win_df['streak'].max()))

if bank < 1.00:
    print("Game Over, no money left in the bank", file=o)
    print("total games played: "+str(gameCounter), file=o)
    print(f"Perecentage wins: {(wins/gameCounter) * 100}%", file=o)
    print(f"Perecentage wins (excluding ties): {(wins/(gameCounter-ties)) * 100}%", file=o)
    print("total rewards: "+str(sum(RoundRewards)), file=o)
    print(f"wins: {wins} losses: {losses} ties: {ties}", file=o)
    print("maximum gain during playing: $"+str(max_bank-100.00), file=o)
    print("maximum winning streak: "+str(win_df['streak'].max()), file=o)
    #AI cannot continue if bank < minimum bet
 
if test == loops:
    print("Simulation complete", file=o)
    print("total games played: "+str(gameCounter), file=o)
    print(f"total wins so far: {wins}", file=o)
    print(f"Perecentage wins: {(wins/gameCounter) * 100}%", file=o)
    print(f"Perecentage wins (excluding ties): {(wins/(gameCounter-ties)) * 100}%", file=o)
    print("total rewards: "+str(sum(RoundRewards)), file=o)
    print(f"wins: {wins} losses: {losses} ties: {ties}", file=o)
    print("maximum gain during playing: $"+str(max_bank-100.00), file=o)
    print("maximum winning streak: "+str(win_df['streak'].max()), file=o)

o.close()
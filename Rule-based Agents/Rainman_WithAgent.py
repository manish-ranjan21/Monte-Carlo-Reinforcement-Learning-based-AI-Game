# import sys
# import numpy
# import matplotlib
import pandas as pd
import gym
from gym import spaces
import os
import Blackjack_func
import random
from datetime import datetime

#reward_options = {"lose_1":-1, "tie_1":0, "win_1":1, "blackjack_1": 2,"lose_2":-2, "tie_2":0, "win_2":2, "blackjack_2": 4,"lose_5":-5, "tie_5":0, "win_5":5, "blackjack_5": 10,"lose_10":-10, "tie_10":0, "win_10":10, "blackjack_10": 20}
    
#There are 4 different state spaces identified: hit/stay, ace conversion, continue play, and bet
# hit = 0, stand = 1
action_space_hitstay = spaces.Discrete(2)

# convert to 1 = 0, keep as 11 = 1
action_space_ace = spaces.Discrete(2)

# continue = 0, end = 1
action_space_continue = spaces.Discrete(2)

# $1 = 0, $2 = 1, $5 = 2, $10 = 3
action_space_bet = spaces.Discrete(4)


total_rewards = 0
NUM_EPISODES = 100


for _ in range(NUM_EPISODES):
    #create a counter to keep track of how many games were played
    gameCounter = 0
    
    ## Number of wins and losses
    wins = 0
    losses = 0
    ties = 0
    
    #From proposal, we decided that the user would start out with $100 in the bank
    bank = 100.00
    max_bank = bank
    
    win_df = pd.DataFrame({"win":[]})

    ##Agent Reward tracker
    RoundRewards = []
    
    #Initiatlizing agent continue playing
    AgentContinue = 'Y'
    episode_reward = 0
    
    #Start Environment Logic
    while bank >= 1.00 and str.upper(AgentContinue) in ('Y','YES'):
        
        if gameCounter == 0:
            deck = Blackjack_func.Deck().deck()
            random.shuffle(deck)
            
        bet = action_space_bet.sample()
        
        if bet == 0:
            bet = 1.00
        elif bet == 1:
            bet = 2.00
        elif bet == 2:
            bet = 5.00
        elif bet == 3:
            bet = 10.00
            
        while bet > bank:
            print("Error, bank amount too low, please lower your bet")
            bet = action_space_bet.sample()
            if bet == 0:
                bet = 1.00
            elif bet == 1:
                bet = 2.00
            elif bet == 2:
                bet = 5.00
            elif bet == 3:
                bet = 10.00
        
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
            print("initial house cards: "+str(house_draw[0])+" + "+str(house_draw[1]))
            print("House Blackjack, Check your draw... if you have blackjack it is a push, if you do not it is a draw")
        elif sum(house_draw) == 22:
            #because it is possible to draw 2 aces in a single hand, we want to force one of those aces to be a 1 (since ace value by default is 11, but can be 1)
            house_draw[1] = 1
            print("initial house cards: "+str(house_draw[0])+" + ??")
        else:
            print("initial house cards: "+str(house_draw[0])+" + ??")
        
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
        
        print("initial agent cards: "+str(agent_draw[0])+" + "+str(agent_draw[1]))
        print(sum(agent_draw))
        
        if sum(house_draw) == 21 and sum(agent_draw) == 21:
            print("") #Unsure if this should be converted to a break. The logic needs to be in place so that resulting logic can work properly
        elif sum(house_draw) == 21 and sum(agent_draw) != 21:
            print("") #Unsure if this should be converted to a break. The logic needs to be in place so that resulting logic can work properly
        elif sum(agent_draw) == 21:
            print("Blackjack! Let's see what the house has")
            blackjack_status = 'Y' #updating to 'Y' because agent_draw has blackjack
        else:
            #The following nested if-else statements check for whether the agent would like to hit or stay
            #There are 16 layers currently based off of 3 decks: 
                #There are 12 possible aces in the deck and if the initial draw is an ace and a 2 then the rest of the aces are drawn and then remaining 2s until 21, that is 16 possible hands
            agent_choice = ''
            while agent_choice != 1 and sum(agent_draw) < 21 and bust == 'N':
                print("Current hand value: "+str(sum(agent_draw))+" Would you like to Hit or Stay?")
                agent_choice = action_space_hitstay.sample()
                if agent_choice == 1:
                    print("")
                elif agent_choice == 0:
                    if len(deck) < 1:
                        #re-create deck
                        deck = Blackjack_func.Deck().deck()
                        random.shuffle(deck)
                    agent_draw.append(deck.pop(random.randrange(0,len(deck))))
                    print("You drew a "+str(agent_draw[len(agent_draw)-1]))
                    try:
                        agent_draw.index(11)
                        print("Would you like to change your ace to a 1?")
                        agent_choice_ace = action_space_ace.sample()
                        if agent_choice_ace == 0:
                            agent_draw[agent_draw.index(11)] = 1
                    except:
                        print("")
                    if sum(agent_draw) == 21:
                        print("You've hit the max without going over! Let's see what the house has")
                    elif sum(agent_draw) > 21:
                        bust = 'Y'
                if sum(deck) < 1:
                    #re-create deck
                    deck = Blackjack_func.Deck().deck()
                    random.shuffle(deck)
    
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
        
        print("House total: "+str(sum(house_draw)))
        print("Agent total: "+str(sum(agent_draw)))
        
            #START GAME REWARD LOGIC
        if bust == 'Y':
            print("bust! you lose this round")
            bank = bank-bet
            losses = losses+1
            Reward = -1*bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) == 21 and sum(agent_draw) == 21:
            print("Push, you get your original bet back")
            ties = ties+1
            Reward = 0
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) == 21 and sum(agent_draw) != 21:
            print("you lose this round")
            bank = bank-bet
            losses = losses+1
            Reward = -1*bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'Y':
            print("Blackjack! You win!")
            bank = bank+(bet*2)
            wins = wins +1
            Reward = 2*bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
        elif sum(house_draw) != 21 and sum(agent_draw) == 21 and blackjack_status == 'N':
            print("You win!")
            bank = bank+bet
            wins = wins +1
            Reward = bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
        elif sum(agent_draw) > 21:
            print("bust! You lose this round")
            bank = bank-bet
            losses = losses+1
            Reward = -1*bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) == sum(agent_draw):
            print("Push, you get your original bet back")
            ties = ties+1
            Reward = 0
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) < sum(agent_draw):
            print("you win!")
            bank = bank+bet
            wins = wins +1
            Reward = bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
        elif sum(house_draw) < 21 and sum(house_draw) > sum(agent_draw):
            print("you lose")
            bank = bank-bet
            losses = losses+1
            Reward = -1*bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[0]})])
        elif sum(house_draw) > 21 and sum(agent_draw) < 21:
            print("you win!")
            bank = bank+bet
            wins = wins +1
            Reward = bet
            win_df = pd.concat([win_df,pd.DataFrame({"win":[1]})])
        #END GAME REWARD LOGIC
            
        #print(sum(deck))
        if sum(deck) < 1:
            #re-create deck
            deck = Blackjack_func.Deck().deck()
            random.shuffle(deck)
    
        
        gameCounter += 1
        #largest gain
        if bank > max_bank:
            max_bank = bank
        #longest winning streak
        
        print("current bank amount: $"+str(bank))
        RoundRewards.append(Reward)
        print("Continue Playing?")
        AgentContinue = action_space_continue.sample()
        if AgentContinue == 0:
            AgentContinue = 'Y'
        elif AgentContinue == 1:
            AgentContinue = 'N'
        
        episode_reward += Reward
        #End While Loop

    total_rewards += episode_reward

    grouper = (win_df.win != win_df.win.shift()).cumsum()
    win_df['streak'] = win_df.groupby(grouper).cumsum()
    
    if ties == gameCounter:
        zeroties = gameCounter-1
    else:
        zeroties = ties
    
    if str.upper(AgentContinue) in ('N', 'NO'):
        print("You have chosen not to continue playing")
        print("total games played: "+str(gameCounter))
        print(f"total wins so far: {wins}")
        print(f"Perecentage wins: {(wins/gameCounter) * 100}%")
        print(f"Perecentage wins (excluding ties): {(wins/(gameCounter-zeroties)) * 100}%")
        print("total rewards: "+str(sum(RoundRewards)))
        print(f"wins: {wins} losses: {losses} ties: {ties}")
        print("maximum gain during playing: $"+str(max_bank-100.00))
        print("maximum winning streak: "+str(win_df['streak'].max()))
    
    if bank < 1.00:
        print("Game Over, no money left in the bank")
        print("total games played: "+str(gameCounter))
        print(f"Perecentage wins: {(wins/gameCounter) * 100}%")
        print(f"Perecentage wins (excluding ties): {(wins/(gameCounter-zeroties)) * 100}%")
        print("total rewards: "+str(sum(RoundRewards)))
        print(f"wins: {wins} losses: {losses} ties: {ties}")
        print("maximum gain during playing: $"+str(max_bank-100.00))
        print("maximum winning streak: "+str(win_df['streak'].max()))
        #AI cannot continue if bank < minimum bet
        
avg_reward = total_rewards/NUM_EPISODES
print("Average Reward without training: "+str(avg_reward))
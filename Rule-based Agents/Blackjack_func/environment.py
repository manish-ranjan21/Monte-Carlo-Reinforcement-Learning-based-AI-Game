import gym
from gym import spaces
from .deck import Deck

class BlackjackEnv(gym.Env):
    
    def __init__(self):
        super(BlackjackEnv, self).__init__()
        
        # Initialize the blackjack deck.
        self.deck = Deck().deck()
        random.shuffle(deck)
        
        self.player_hand = []
        self.dealer_hand = []
        
        self.reward_options = {"lose_1":-1, "tie_1":0, "win_1":1, "blackjack_1": 2,"lose_2":-2, "tie_2":0, "win_2":2, "blackjack_2": 4,"lose_5":-5, "tie_5":0, "win_5":5, "blackjack_5": 10,"lose_10":-10, "tie_10":0, "win_10":10, "blackjack_10": 20}
        
        # hit = 0, stand = 1
        self.action_space_hitstay = spaces.Discrete(2)
        
        # convert to 1 = 0, keep as 11 = 1
        self.action_space_ace = spaces.Discrete(2)
        
        # continue = 0, end = 1
        self.action_space_continue = spaces.Discrete(2)
        
        # $1 = 0, $2 = 1, $5 = 2, $10 = 3
        self.action_space_bet = spaces.Discrete(4)
        '''
        First element of tuple is the range of possible hand values for the player. (3 through 20)
        This is the possible range of values that the player will actually have to make a decision for.
        Any player hand value 21 or above already has automatic valuations, and needs no input from an
        AI Agent. 
        Second element of the tuple is the range of possible values for the dealer's upcard. (2 through 11)
        '''
        
        self.observation_space = spaces.Tuple((spaces.Discrete(18), spaces.Discrete(10)))
        
        self.done = False
        
    def _take_action(self, action, ):
        if action == 0: # hit
            self.player_hand.append(self.bj_deck.deal())
        
        if 
        # re-calculate the value of the player's hand after any changes to the hand.
        self.player_value = player_eval(self.player_hand)
        
    def bet(self, action):
        if action == 0:
            bet = 1
        elif action == 1:
            bet = 2
        elif action == 2:
            bet = 5
        elif action == 3:
            bet = 10
        
        return bet
    
    def hitstay(self, action, bet, ace, cont):
        self._take_action(action)
        
        # End the episode/game is the player stands or has a hand value >= 21.
        self.done = action == 1 or self.player_value >= 21
        
        # rewards are 0 when the player hits and is still below 21, and they
        # keep playing.
        rewards = 0
        
        if self.done:
            # CALCULATE REWARDS
            if self.player_value > 21: # above 21, player loses automatically.
                if bet
                rewards = self.reward_options["lose"]
            elif self.player_value == 21: # blackjack! Player wins automatically.
                rewards = self.reward_options["win"]
            else:
                ## Begin dealer turn phase.

                dealer_value, self.dealer_hand, self.bj_deck = dealer_turn(self.dealer_hand, self.bj_deck)

                ## End of dealer turn phase

                #------------------------------------------------------------#

                ## Final Compare

                if dealer_value > 21: # dealer above 21, player wins automatically
                    rewards = self.reward_options["win"]
                elif dealer_value == 21: # dealer has blackjack, player loses automatically
                    rewards = self.reward_options["lose"]
                else: # dealer and player have values less than 21.
                    if self.player_value > dealer_value: # player closer to 21, player wins.
                        rewards = self.reward_options["win"]
                    elif self.player_value < dealer_value: # dealer closer to 21, dealer wins.
                        rewards = self.reward_options["lose"]
                    else:
                        rewards = self.reward_options["tie"]
        
        self.balance += rewards
        
        
        # Subtract by 1 to fit into the possible observation range.
        # This makes the possible range of 3 through 20 into 1 through 18
        player_value_obs = self.player_value - 2
        
        # get the value of the dealer's upcard, this value is what the agent sees.
        # Subtract by 1 to fit the possible observation range of 1 to 10.
        upcard_value_obs = dealer_eval([self.dealer_upcard]) - 1
        
        # the state is represented as a player hand-value + dealer upcard pair.
        obs = np.array([player_value_obs, upcard_value_obs])
        
        return obs, rewards, self.done, {}
    
    def reset(self): # resets game to an initial state
        # Add the player and dealer cards back into the deck.
        self.bj_deck.cards += self.player_hand + self.dealer_hand

        # Shuffle before beginning. Only shuffle once before the start of each game.
        self.bj_deck.shuffle()
         
        self.balance = INITIAL_BALANCE
        
        self.done = False
        
        # returns the start state for the agent
        # deal 2 cards to the agent and the dealer
        self.player_hand = [self.bj_deck.deal(), self.bj_deck.deal()]
        self.dealer_hand = [self.bj_deck.deal(), self.bj_deck.deal()]
        self.dealer_upcard = self.dealer_hand[0]
        
        # calculate the value of the agent's hand
        self.player_value = player_eval(self.player_hand)
        
        # Subtract by 1 to fit into the possible observation range.
        # This makes the possible range of 2 through 20 into 1 through 18
        player_value_obs = self.player_value - 2
            
        # get the value of the dealer's upcard, this value is what the agent sees.
        # Subtract by 1 to fit the possible observation range of 1 to 10.
        upcard_value_obs = dealer_eval([self.dealer_upcard]) - 1
        
        # the state is represented as a player hand-value + dealer upcard pair.
        obs = np.array([player_value_obs, upcard_value_obs])
        
        return obs
    
env = BlackjackEnv()

total_rewards = 0
NUM_EPISODES = 1000

for _ in range(NUM_EPISODES):
    env.reset()
    
    episode_reward = 0
    while env.done == False:
        bet = env.action_space_bet.sample()
        action = env.action_space_hitstay.sample()
        ace = env.action_space_ace.sample()
        cont = env.action_space_continue.sample()
        
        new_state, reward, done, desc = env.hitstay(action)
        
        episode_reward += reward
        
    total_rewards += episode_reward
    
avg_reward = total_rewards/NUM_EPISODES
print("Average Reward without training: "+str(avg_reward))
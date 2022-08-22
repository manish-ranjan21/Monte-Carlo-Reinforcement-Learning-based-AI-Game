# Penn State AI801 Team9 BlackJack Project
## Scripts:
### Interactive Script:
#### Rainman_Interactive
##### About
This script allows users to play Blackjack on their own and maintain a reward system to see how they would do as the AI.
##### How To Play
1. download the repository
2. Open the Rainman_Interactive.py script
3. Enter your initial bet (1, 2, 5, or 10)
4. After reviewing your initial hand, choose if you would like to hit or stay
    1. If the drawn card is an ace, choose if you would like to convert to a 1 or leave as 11
5. If the value is still under 21 after hitting, choose again (and so on)
6. After the game has concluded, you will be given the option to continue playing or end.
7. After ending the game, a summary will be provided

### Monte-Carlo Approaches:
#### Monte_Carlo
##### About
This script is based off of https://towardsdatascience.com/playing-blackjack-using-model-free-reinforcement-learning-in-google-colab-aa2041a2c13d
It uses a pre-defined blackjack OpenGym environment. You can alter the Q-learning variables at the beginning of the script (see ipynb file)

#### adithyasolai_Blackjack
##### About
This script is based off of https://github.com/adithyasolai/Monte-Carlo-Blackjack
At the beginning of the script, you can set the number of training iterations (currently set to 1,000,000), the number of episodes (games), and initial bank and number of decks. The initial bank does not have much impact in this scenario, but number of decks could have a positive impact on the number of blackjacks (since there are more aces in the deck).
This script must be run in Spyder.

### Rule-based Agent Scripts
#### Rainman_WithAgent
##### About
This script was set up as an OpenGym Environment and runs using a discrete space approach for each of the actions:
- hit/stay (discrete space of 2)
- bet (discrete space of 4)
- convert ace (discrete space of 2)
- continue playing (discrete space of 2)

#### Rainman_AlwaysHit
##### About
1. There are 4 different scripts where the agent choice is always hit (request an additional card be added to the hand). Due to the agent choice being defaulted to hit, the ace conversion is always set to yes (if an ace is drawn, convert it to a 1 as opposed to an 11). Each script is aligned to a different bet amount (1,2,5,10). The full game results are stored in a log file
2. Bet = $1 Test Result
    1. After playing 169 games, the agent went bankrupt. It had a winning percentage of 16.57% and total agent reward of -31. It never gained more than the initial bank and had a maximum winning streak of 2
3. Bet = $2 Test Results
    1. After playing 86 games, the agent went bankrupt. It had a winning percentage of 16.28% and total agent reward of -14. It never gained more than the initial bank and had a maximum winning streak of 2
4. Bet = $5 Test Results
    1. After playing 24 games, the agent went bankrupt. It had a winning percentage of 8.33% and total agent reward of -16. It had a maximum gain of $5 more than the initial bank and had a maximum winning streak of 1
5. Bet = $10 Test Results
    1. After playing 10 games, the agent went bankrupt. It had a winning percentage of 0 and total agent reward of -10. It never gained more than the initial bank and never had a winning streak because it did not win a single game

#### Rainman_AlwaysStay
##### About
1.	There are 4 different scripts where the agent choice is always stay (maintain the dealt hand and compare to that of the dealer). Due to the agent choice being defaulted to stay, the ace conversion is always set to no (if an ace is drawn, keep the value as 11). Each script is aligned to a different bet amount (1,2,5,10). The full game results are stored in a log file
2.	Bet = $1 Test Result
    1.	After playing 726 games, the agent went bankrupt. It had a winning percentage of 38.57% and total agent reward of 526. It had a maximum gain of $4 and had a maximum winning streak of 10
3.	Bet = $2 Test Results
    1.	After playing 333 games, the agent went bankrupt. It had a winning percentage of 38.14% and total agent reward of 233. It never gained more than the initial bank and had a maximum winning streak of 5
4.	Bet = $5 Test Results
    1.	After playing 163 games, the agent went bankrupt. It had a winning percentage of 39.88% and total agent reward of 123. It had a maximum gain of $25 more than the initial bank and had a maximum winning streak of 6
5.	Bet = $10 Test Results
    1.	After playing 104 games, the agent went bankrupt. It had a winning percentage of 41.35% and total agent reward of 84. It had a maximum gain of $70 more than the initial bank and had a maximum winning streak of 4

#### Rainman_Conditional
##### About
1.	There are 4 different scripts where the agent choice is conditional. If the hand is less than 17, then hit, else stay. This is somewhat like the nature of the dealer; however, the player has a higher likelihood of losing due to always having to draw first. The ace conversion is defaulted to yes, but one could argue that this could also have a conditional filter applied here as well. Each script is aligned to a different bet amount (1,2,5,10). The full game results are stored in a log file
2.	Bet = $1 Test Result
    1.	After playing 2817 games, the agent went bankrupt. It had a winning percentage of 41.68% and total agent reward of 2617. It had a maximum gain of $5 more than the initial bank and had a maximum winning streak of 8
3.	Bet = $2 Test Results
    1.	After playing 2076 games, the agent went bankrupt. It had a winning percentage of 42.05% and total agent reward of 1976. It had a maximum gain of $14 more than the initial bank and had a maximum winning streak of 8
4.	Bet = $5 Test Results
    1.	After playing 179 games, the agent went bankrupt. It had a winning percentage of 38.55% and total agent reward of 139. It had a maximum gain of $25 more than the initial bank and had a maximum winning streak of 5
5.	Bet = $10 Test Results
    1.	After playing 197 games, the agent went bankrupt. It had a winning percentage of 40.10% and total agent reward of 177. It had a maximum gain of $130 more than the initial bank and had a maximum winning streak of 6

#### Rainman_BankOptimizationConditional
##### About
1.	There are 4 different scripts where the agent choice is conditional, but if a limit is reached on the original bank ($5, $10, $25, and $50 respectively). If the hand is less than 17, then hit, else stay. This is somewhat like the nature of the dealer; however, the player has a higher likelihood of losing due to always having to draw first. The ace conversion is defaulted to yes, but one could argue that this could also have a conditional filter applied here as well. Each script is aligned to a different bet amount (1,2,5,10). The full game results are stored in a log file
2.	Bet = $1 Test Result
    1.	After playing 61 games, the agent reached their goal of a $5 increase. It had a winning percentage of 44.26% and total agent reward of 71. It had a maximum winning streak of 4
3.	Bet = $2 Test Results
    1.	After playing 290 games, the agent reached their goal of a $10 increase. It had a winning percentage of 43.10% and total agent reward of 300. It had a maximum winning streak of 6
4.	Bet = $5 Test Results
    1.	After playing 16 games, the agent reached their goal of a $25 increase. It had a winning percentage of 62.5% and total agent reward of 26. It had a maximum winning streak of 5
5.	Bet = $10 Test Results
    1.	After playing 57 games, the agent reached their goal of a $50 increase. It had a winning percentage of 47.37% and total agent reward of 67. It had a maximum winning streak of 7

#### Rainman_AllowNegativeConditional
##### About
1.	There are 4 different scripts where the agent choice is conditional but will continue to play even when the bank goes negative until the 10000 round limit is reached. If the hand is less than 17, then hit, else stay. This is somewhat like the nature of the dealer; however, the player has a higher likelihood of losing due to always having to draw first. The ace conversion is defaulted to yes, but one could argue that this could also have a conditional filter applied here as well. Each script is aligned to a different bet amount (1,2,5,10). The full game results are stored in a log file
2.	Bet = $1 Test Result
    1.	The agent ended with a bank of -$596. It had a winning percentage of 39.76% and total agent reward of 8608. It had a maximum gain of $4 more than the initial bank and had a maximum winning streak of 9
3.	Bet = $2 Test Results
    1.	The agent ended with a bank of -$1022. It had a winning percentage of 40.21% and total agent reward of 8878. It had a maximum gain of $20 more than the initial bank and had a maximum winning streak of 9
4.	Bet = $5 Test Results
    1.	The agent ended with a bank of -$2620. It had a winning percentage of 40.17% and total agent reward of 8912. It had a maximum gain of $30 more than the initial bank and had a maximum winning streak of 10
5.	Bet = $10 Test Results
    1.	The agent ended with a bank of -$5320. It had a winning percentage of 40.13% and total agent reward of 8916. It had a maximum gain of $80 more than the initial bank and had a maximum winning streak of 9

#### Rainman_Randomized
##### About
1.	This is a completely random choice blackjack game. The only consistent part of this script is the continuation of playing is always set to yes. The full game results are stored in a log file.
2.	Test Results
    1.	After playing 28 games, the agent went bankrupt. It had a winning percentage of 21.43% and total agent reward of 0. It never gained more than the initial bank and had a maximum winning streak of 2

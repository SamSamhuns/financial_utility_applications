'''
Utility Python program to generate a Value Realization Model.
It uses a simple model to predict the probability of a high value or a
low value for a stock given the sequence of buys(asks being lifted) or sells(bids being hit).
The script will prompt the user to enter a sequence of buy(s)/sell(s) with trade prices like `bbssbs` or `BSBSBB`.
Buy/sell sequences can also be entered through a text file containing these sequences as
the first command line argument to the script_name.
'''
import os
import sys
import matplotlib.pyplot as plt

# class to hold all the probability tree information and related probabilities
class trade_prob_class:
    def __init__(self, value_high, value_low ):
        # IMPORTANT all probabilities are joint in a strutured probability tree
        #                               -Buy
        #                  - Informed --
        #          - Low--              -Sell     -- Buy
        #        -         - Uninformed - - - - -
        # Value -                       -Buy      -- Sell
        #        -         - informed --
        #          - High--             -Sell     -- Buy
        #                  - Uninformed - - - - -
        #                                         -- Sell
        ##########################################################################################################################

        self.value_high_prob = value_high               # Prob that the stock value is high at the end of the day
        self.value_low_prob = value_low                 # Prob that the stock value is low at the end of the day

        self.informed_given_low = 0.1                   # Prob that the trader is informed given the stock val is low
        self.uninformed_given_low = 0.4                 # Prob that the trader is uninformed given the stock val is low
        self.informed_given_high = 0.1                  # Prob that the trader is informed given the stock val is high
        self.uninformed_given_high = 0.4                # Prob that the trader is uinformed given the stock val is high

        self.buy_given_informed_low = 0                 # Prob of a buy given the trader is informed given the stock val is low
        self.sell_given_informed_low = 0.1              # Prob of a sell given the trader is informed given the stock val is low
        self.buy_given_uninformed_low = 0.2             # Prob of a buy given the trader is uninformed given the stock val is low
        self.sell_given_uninformed_low = 0.2            # Prob of a sell given the trader is uninformed given the stock val is low
        self.buy_given_informed_high = 0.1              # Prob of a buy given the trader is informed given the stock val is high
        self.sell_given_informed_high = 0               # Prob of a sell given the trader is informed given the stock val is high
        self.buy_given_uninformed_high = 0.2            # Prob of a buy given the trader is uninformed given the stock val is high
        self.sell_given_uninformed_high = 0.2           # Prob of a sell given the trader is uninformed given the stock val is high


# function to parse and load buy/sell sequences into a string trade_seq_str_holder
def f_trade_seq_str_read ( fp, trade_seq_str_holder ):
    for seq in fp:
        seq = seq.lower().strip()
        seq = seq.replace( ' ', '' )
        trade_seq_str_holder += seq
    return trade_seq_str_holder

# printing information on model
print("\nValue here is the end of day closing price unknown to everyone except informed traders.")
print("At the start of the day, the final value of the stock is unknown and has a 50/50 chance of being low or high")
print("Informed traders will always buy if the actual value is high and always sell if it's low.")
print("Uninformed traders have 50% chance of buying or selling regardless of the stock's final value.")


# if no args are entered
if len(sys.argv) == 1:
    trade_seq_str = (input('Enter the trade sequence (Format bssbssbbb) :')).lower().replace(' ', '')
# if a file containing the buy sell sequences are entered
elif len(sys.argv) == 2:
    f_trade_seq_str = open(sys.argv[1], 'r')
    trade_seq_str = f_trade_seq_str_read( f_trade_seq_str, trade_seq_str )
    f_trade_seq_str.close()
else:
    print('Usage VRM.py <Optional-f_trade_seq_str.txt>')
    sys.exit()

# trade seq error checking for invalid inputs
for trade in trade_seq_str:
    if trade != 'b' and trade != 's':
        print('Invalid sequence of buys/sells ( Usage b = buy, s = sell ):')
        sys.exit()

print('\nThe main sequence of high/low value probabilities for all the trades is generated as high_low_prob chart.')
print('The flowcharts showing the sequencing of random events for each trade are generated in a fig_output folderself. \
\nMake sure there are no folders in the fig_output_folder.')

# creating a output folder
output_folder_path = 'fig_output'
if not os.path.exists(output_folder_path):
    os.makedirs( output_folder_path)
os.chdir(output_folder_path)

# generating a list of all old files in the output_folder_path directory
old_file_list = os.listdir('./')
for file in old_file_list:
    os.remove(file)

# In the beginning the probability of a high or low closing stock value is 50/50
trade_prob_obj = trade_prob_class(0.5, 0.5)
informed_prop = 0                                                                             # Proportion of informed traders

# making sure a valid informed user proportion has been entered
while True:
    informed_prop = float(input("\nEnter the assumed proportion of informed traders in the market (i.e. 0.0 to 1.0):"))
    if informed_prop <= 1.0 and informed_prop >= 0.0:
        break
    print('Incorrect propertions entered. Try again.')

uninformed_prop = 1 - informed_prop                                                           # Proportion of uninformed traders

trade_seq_array = [['Open', trade_prob_obj.value_high_prob, trade_prob_obj.value_low_prob]]   #

for trade in trade_seq_str:
    # if next trade is a buy
    if trade == 'b':

    # if it is a sell
    else:



print( informed_prop )
print( trade_seq_str )

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
import numpy as np
import matplotlib.pyplot as plt

# printing information on model
print("\nValue here is the end of day closing price unknown to everyone except informed traders.")
print("At the start of the day, the final value of the stock is unknown and has a 50/50 chance of being low or high")
print("Informed traders will always buy if the actual value is high and always sell if it's low.")
print("Uninformed traders have 50% chance of buying or selling regardless of the stock's final value.\n")

# uninformed traders always have a 50% chance of buying or selling given regardless of the value
prob_uninformed_buy_sell = 0.5
# informed traders will always buy if value is high and sell if value is low
prob_informed_buy_if_high = 1.0
prob_informed_sell_if_high = 0
prob_informed_buy_if_low = 0
prob_informed_sell_if_low = 1.0

# class to hold all the probability tree information and related probabilities
class trade_prob_tree:
    def __init__(self, value_high, value_low ):
        # IMPORTANT all probabilities are joint in a strutured probability tree
        #                                         --Buy                       #
        #                  - Uninformed - - - - -                             #
        #          - Low--              -Buy      --Sell                      #
        #        -         - Informed --                                      #
        #       -                       -Sell                                 #
        # Value -                                                             #
        #       -                       -Buy                                  #
        #        -         - informed --                                      #
        #          - High--             -Sell     --Buy                       #
        #                  - Uninformed - - - - -                             #
        #                                         --Sell                      #
        #######################################################################

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

# if no args are entered
if len(sys.argv) == 1:
    trade_seq_str = (input('Enter the trade sequence (Format bssbssbbb) :')).lower().replace(' ', '')
# if a file containing the buy sell sequences are entered
elif len(sys.argv) == 2:
    f_trade_seq_str = open(sys.argv[1], 'r')
    trade_seq_str = f_trade_seq_str_read( f_trade_seq_str, trade_seq_str )
    f_trade_seq_str.close()
else:
    print('Usage main_VRM.py <Optional-f_trade_seq_str.txt>')
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
main_tree = trade_prob_tree(0.5, 0.5)                                                         # Creating a trade_prob_tree object
informed_prop = 0                                                                             # Proportion of informed traders

# making sure a valid informed user proportion has been entered
while True:
    informed_prop = float(input("\nEnter the assumed proportion of informed traders in the market (i.e. 0.0 to 1.0):"))
    if informed_prop <= 1.0 and informed_prop >= 0.0:
        break
    print('Incorrect propertions entered. Try again.')

uninformed_prop = 1 - informed_prop                                                           # Proportion of uninformed traders


# array to hold sequences of trades and the respective probabilities of a high or low price
# At the open, the high and low value probabilities are both 50/50
trade_type = 'Open'
trade_seq_array = [[trade_type, main_tree.value_high_prob, main_tree.value_low_prob]]         # [ trade_type, value_high, value_low ]

for trade in trade_seq_str:

    # if next trade is a buy
    if trade == 'b':
        trade_type = 'Buy'
        # using rules of conditional probability
        denominator_prob = (main_tree.buy_given_informed_low + main_tree.buy_given_informed_high \
        + main_tree.buy_given_uninformed_low + main_tree.buy_given_uninformed_high )

        # Calculate the probability for the stock to end up with a low or a high value
        # given an ask was lifted in the previous trade (Buy)
        main_tree.value_low_prob = (main_tree.buy_given_informed_low + \
        main_tree.buy_given_uninformed_low) / denominator_prob

        main_tree.value_high_prob = (main_tree.buy_given_informed_high + \
        main_tree.buy_given_uninformed_high) / denominator_prob

    # if it is a sell
    else:
        trade_type = 'Sell'
        # using rules of conditional probability
        denominator_prob = (main_tree.sell_given_informed_low + main_tree.sell_given_informed_high \
        + main_tree.sell_given_uninformed_low + main_tree.sell_given_uninformed_high )

        # Calculate the probability for the stock to end up with a low or a high value
        # given a bit was hit in the previous trade (Sell)
        main_tree.value_low_prob = (main_tree.sell_given_informed_low + \
        main_tree.sell_given_uninformed_low) / denominator_prob

        main_tree.value_high_prob = (main_tree.sell_given_informed_high + \
        main_tree.sell_given_uninformed_high) / denominator_prob

    # Update the probablities for all the different branches in the probability tree
    main_tree.informed_given_low = main_tree.value_low_prob * informed_prop
    main_tree.uninformed_given_low = main_tree.value_low_prob * uninformed_prop
    main_tree.informed_given_high = main_tree.value_high_prob * informed_prop
    main_tree.uninformed_given_high = main_tree.value_high_prob * uninformed_prop

    main_tree.buy_given_informed_low = prob_informed_buy_if_low * main_tree.informed_given_low
    main_tree.sell_given_informed_low = prob_informed_sell_if_low * main_tree.informed_given_low
    main_tree.buy_given_uninformed_low = prob_uninformed_buy_sell * main_tree.uninformed_given_low
    main_tree.sell_given_uninformed_low = prob_uninformed_buy_sell * main_tree.uninformed_given_low
    main_tree.buy_given_informed_high = prob_informed_buy_if_high * main_tree.informed_given_high
    main_tree.sell_given_informed_high = prob_informed_sell_if_high * main_tree.informed_given_high
    main_tree.buy_given_uninformed_high = prob_uninformed_buy_sell * main_tree.uninformed_given_high
    main_tree.sell_given_uninformed_high = prob_uninformed_buy_sell * main_tree.uninformed_given_high

    # Add the probability to the trade_seq_array
    trade_seq_array.append([ trade_type, round(main_tree.value_high_prob, 5), round(main_tree.value_low_prob,5)])

# Open a new file to store the probabilities of a high or a low value given different types of trades
buy_sell_prob_output = open('high_low_probs_output.txt', 'w')
# print the header in the file
print( ('%s \t %s \t %s') % ( 'Trade type', 'High Value Prob', 'Low Value Prob'), file=buy_sell_prob_output )
# print all the probablities into an output file
for trade_arr in trade_seq_array:
    print( trade_arr[0], trade_arr[1] , trade_arr[2], file=buy_sell_prob_output, sep='\t\t' )

buy_sell_prob_output.close()
# generate a numpy array for holding the high/low probability information
trade_arr_numpy = np.array( [ [i, trade_seq_array[i][1] , trade_seq_array[i][2]] for i in range(len(trade_seq_array)) ])

# Generate bar graphs to show the probablities of a high or low price given the sequence of buys and sells
# mananging the graph labels

width = 0.35                # width of prob bars
ind = trade_arr_numpy[:,0]  # generating the x axix number lables
fig, ax = plt.subplots()    # creating ax and fig object
high_bar = ax.bar(ind - width/2, trade_arr_numpy[:,1], width, color='green', label='High Value probability')
low_bar = ax.bar(ind + width/2, trade_arr_numpy[:,2], width, color='#bb0000', label='Low Value probability')
# getting the x ticks of buys and sells
x_label_ticks = np.array( [ trade_seq_array[i][0] for i in range(len(trade_seq_array)) ] )

ax.set_title('Probability of a High or Low final price after buys/sells')
ax.set_ylabel('Probability')
ax.set_xlabel('Trades (Buy = ask was lifted, Sell = bid was hit)')
ax.set_xticks(ind)
ax.set_xticklabels( x_label_ticks )
ax.legend()

plt.savefig('high_low_prob_output.png')
plt.show()

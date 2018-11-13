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

# function to parse and load buy/sell sequences into a string trade_seq_holder
def f_trade_seq_read ( fp, trade_seq_holder ):
    for seq in fp:
        seq = seq.lower().strip()
        seq = seq.replace( ' ', '' )
        trade_seq_holder += seq
    return trade_seq_holder

trade_seq = ''
# if no args are entered
if len(sys.argv) == 1:
    trade_seq = (input('Enter the trade sequence (Format bssbssbbb) :')).lower().replace(' ', '')
# if a file containing the buy sell sequences are entered
elif len(sys.argv) == 2:
    f_trade_seq = open(sys.argv[1], 'r')
    trade_seq = f_trade_seq_read( f_trade_seq, trade_seq )
    f_trade_seq.close()
else:
    print('Invalid number of argument(s) supplied: Usage VRM.py <Optional-f_trade_seq.txt>')
    sys.exit()

# trade seq error checking for invalid inputs
for trade in trade_seq:
    if trade != 'b' and trade != 's':
        print('Invalid sequence of buys/sells ( Usage b = buy, s = sell ):')
        sys.exit()

# printing information on model
print("\nValue here is the end of day closing price unknown to everyone except informed traders.")
print("At the start of the day, the final value of the stock is unknown and has a 50/50 chance of being low or high")
print("Informed traders will always buy if the actual value is high and always sell if it's low.")
print("Uninformed traders have 50% chance of buying or selling regradless of the stock's final value.")

# making sure a valid informed user proportion has been entered
informed_prop = 0
while True:
    informed_prop = float(input("\nEnter the assumed proportion of informed traders in the market (i.e. 0.0 to 1.0):"))
    if informed_prop <= 1.0 and informed_prop >= 0.0:
        break
    print('Incorrect propertions entered. Try again.')

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



print( informed_prop )
print( trade_seq )

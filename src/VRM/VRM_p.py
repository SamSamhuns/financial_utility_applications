'''
Utility Python program to generate a Value Realization Model.
It uses a simple model to predict the probability of a high value or a
low value for a stock given the sequence of buys(asks being lifted) or sells(bids being hit).
The script will prompt the user to enter a sequence of buy(s)/sell(s) with trade prices like `bbssbs` or `BSBSBB`.
Buy/sell sequences can also be entered through a text file containing these sequences as
the first command line argument to the script_name.
'''
import sys
import matplotlib.pyplot as plt

trade_seq = ''
if len(sys.argv) == 1:
    trade_seq = (input('Enter the trade sequence (Format bssbssbbb) :')).lower()
elif len(sys.argv) == 2:
    f_trade_seq = open(sys.argv[1], 'r')
    for seq in f_trade_seq:
        seq = seq.lower().strip()
        trade_seq += seq
    f_trade_seq.close()
else:
    print('Invalid number of argument(s) supplied: Usage VRM.py <Optional-f_trade_seq.txt>')
    sys.exit()
    
print( trade_seq )

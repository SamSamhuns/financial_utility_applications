'''
Script to parse security returns CSV file
The CSV files must be generated from yahoo-finance ( Using an API or a CSV download )
CSV Format: Date, Open, High, Low, Close, Adj, Close, Volume
'''
import sys
import numpy as np
import pandas as pd
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        print('Usage main_RAV.py <yahoo_finance_returns_CSV>')
        sys.exit()
    sp500 = pd.read_csv( sys.argv[1] )

    # changing the 'Date' column to a pandas series datetime object and setting it as df index
    sp500['Date'] = sp500['Date'].astype('datetime64[ns]')
    sp500.set_index( sp500['Date'], inplace=True )
    dtime_interval = sp500.index[1] - sp500.index[0]
    if dtime_interval.days in {1,3}:
        #Data is on a daily basis
        pass
    elif dtime_interval.days in {365,366}:
        #Data is on a yearly basis
        pass

    elif dtime_interval.days in {28,29,30,31}:
        #Data is on a monthly basis
        pass
    else:
        print("Data time intervals incorrect")
        sys.exit()


if __name__ == '__str__':
    main()

'''
Script to parse security returns CSV file
The CSV files must be generated from yahoo-finance ( Using an API or a CSV download )
CSV Format: Date, Open, High, Low, Close, Adj, Close, Volume
'''
import sys
import csv
import numpy as np
import pandas as pd
from datetime import datetime

def monthly_return( eticker ):
    eticker['Monthly Returns'] = eticker['Adj Close'].pct_change() * 100        # getting the monthly return and converting it a percent return
    eticker['12 MMA'] = eticker['Monthly Returns'].rolling( window=12 ).mean()  # Get the 12 month moving average returns

    summary = eticker.describe()
    annul_return = eticker['Monthly Returns'].mean() * 12
    annul_volatility = eticker['Monthly Returns'].std() * np.sqrt(12)
    sharpe_ratio = 0
    if len(sys.argv) == 3:
        sharpe_ratio = (annul_return - float(sys.argv[2])) / annul_volatility
    else:
        sharpe_ratio = annul_return / annul_volatility
    calc_output_fname = (sys.argv[1].split('.'))[0]+' calculated.csv'
    summary_output_fname = (sys.argv[1].split('.'))[0]+' summary.csv'
    eticker.to_csv(calc_output_fname)
    summary.to_csv(summary_output_fname)

    with open(summary_output_fname, 'a') as sfile:
        sum_writer = csv.writer(sfile, delimiter=',')

        sum_writer.writerow(['Annualized Return', annul_return])
        sum_writer.writerow(['Annualized Volatility', annul_volatility])
        sum_writer.writerow(["Sharpe's Ratio", sharpe_ratio])
    sfile.close()


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage main_RAV.py <yahoo_finance_returns_CSV> <Optional_risk_free_rate>')
        sys.exit()
    ticker = pd.read_csv( sys.argv[1] )

    # changing the 'Date' column to a pandas series datetime object and setting it as the df index
    ticker['Date'] = ticker['Date'].astype('datetime64[ns]')
    ticker.set_index( ticker['Date'], inplace=True )
    # Calcuting the time interval between sucessive data points
    dtime_interval = ticker.index[1] - ticker.index[0]

    if dtime_interval.days in {1,3}:
        #Data is on a daily basis
        pass
    elif dtime_interval.days in {7}:
        #Data is on a weekly basis
        pass
    elif dtime_interval.days in {28,29,30,31}:
        #Data is on a monthly basis
        monthly_return(ticker)
    else:
        print("Data time intervals incorrect")
        sys.exit()

if __name__ == '__main__':
    main()

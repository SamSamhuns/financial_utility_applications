'''
Script to parse security returns CSV file
The CSV files must be generated from yahoo-finance ( Using an API or a CSV download )
CSV Format: Date, Open, High, Low, Close, Adj, Close, Volume
'''
# Author: Samridha Man Shrestha
# 2018-11-22
# Using Python 3

import sys
import csv
import numpy as np
import pandas as pd


def calc_summary_gen(eticker, annul_factor):
    summary = eticker.describe()

    annul_return = eticker.iloc[:, 7].mean() * annul_factor
    annul_volatility = eticker.iloc[:, 7].std() * np.sqrt(annul_factor)
    sharpe_ratio = 0
    # check if the optional risk free rate has been entered
    if len(sys.argv) == 3:
        sharpe_ratio = (annul_return - float(sys.argv[2])) / annul_volatility
    else:
        sharpe_ratio = annul_return / annul_volatility
    # sys.argv[1] is the CSV file name
    calc_output_fname = (sys.argv[1].split('.'))[0] + ' calculated.csv'
    summary_output_fname = (sys.argv[1].split('.'))[0] + ' summary.csv'
    eticker.to_csv(calc_output_fname)
    summary.to_csv(summary_output_fname)

    # opening the summary_output_fname to append the annualize stats
    with open(summary_output_fname, 'a') as sfile:
        sum_writer = csv.writer(sfile, delimiter=',')

        sum_writer.writerow(['Annualized Return', annul_return])
        sum_writer.writerow(['Annualized Volatility', annul_volatility])
        sum_writer.writerow(["Sharpe's Ratio", sharpe_ratio])
    sfile.close()


def monthly_returns(eticker):
    # getting the monthly return and converting it a percent return
    eticker['Monthly Returns'] = eticker['Adj Close'].pct_change() * 100
    eticker['12 MMA'] = eticker['Monthly Returns'].rolling(
        window=12).mean()  # Get the 12 month moving average returns

    # the annulaizetion factor for monthly returns is 12 (12 trading months in a year)
    calc_summary_gen(eticker, 12)


def daily_returns(eticker):
    eticker['Daily Returns'] = eticker['Adj Close'].pct_change() * 100
    eticker['10 DMA'] = eticker['Daily Returns'].rolling(
        window=10).mean()    # 10 day moving average
    eticker['30 DMA'] = eticker['Daily Returns'].rolling(
        window=30).mean()    # 30 day moving average

    # the annulaizetion factor for monthly returns is 252 (252 trading days in a year)
    calc_summary_gen(eticker, 252)


def weekly_returns(eticker):
    eticker['Weekly Returns'] = eticker['Adj Close'].pct_change() * 100
    eticker['4 WMA'] = eticker['Weekly Returns'].rolling(
        window=4).mean()     # 4 weeks moving average

    # the annulaizetion factor for weekly returns is 52 (52 trading weeks in a year)
    calc_summary_gen(eticker, 52)


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage main_RAV.py <yahoo_finance_returns_CSV> <Optional_risk_free_rate>')
        sys.exit()
    ticker = pd.read_csv(sys.argv[1])

    # changing the 'Date' column to a pandas series datetime object and setting it as the df index
    ticker['Date'] = ticker['Date'].astype('datetime64[ns]')
    ticker.set_index(ticker['Date'], inplace=True)
    # Calcuting the time interval between sucessive data points
    dtime_interval = ticker.index[1] - ticker.index[0]

    if dtime_interval.days in {1, 3}:
        # Data is on a daily basis
        daily_returns(ticker)
    elif dtime_interval.days in {7}:
        # Data is on a weekly basis
        weekly_returns(ticker)
    elif dtime_interval.days in {28, 29, 30, 31}:
        # Data is on a monthly basis
        monthly_returns(ticker)
    else:
        print("Data time intervals incorrect")
        sys.exit()


if __name__ == '__main__':
    main()

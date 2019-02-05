# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import sys

# Utility Python program for calculating Net Present Value of cash flows over a yearly period
# DCF Calculations for yearly cash flows
# All cash flows must be presented on a yearly basis in the form of a CSV file as described below
# discount rate has to be entered separately.

# Author: Samridha Man Shrestha
# 2018-11-12
# Using Python 3
# import matplotlib as mpl
# mpl.use('Agg')


# Function to calculate present value of cash flow
# rate is in % per year and time is in years
def presentVal(futureVal, rate, time):
    return futureVal / ((1 + (rate / 100))**time)

#  CSV file format
#  Note that current year is stated as 0
#  year, cash_flow
#  0,    -30000
#  1,    1500
#  2,    1600


def main():
    if len(sys.argv) != 3:
        print("Usage: python main_DCF.py <DISCOUNT RATE> <CSV FILE>")
        sys.exit()
    # Error check
    try:
        fp = open(sys.argv[2], 'r')
        # Discount rate entered as a percentage
        d_rate = float(sys.argv[1])
    except IOError:
        print(sys.argv[2], " does not exist." )
        print("Usage: python main_DCF.py <DISCOUNT RATE> <CSV FILE>")
        sys.exit()
    except ValueError:
        print(sys.argv[1], " must be a number without %." )
        print("Usage: python main_DCF.py <DISCOUNT RATE> <CSV FILE>")
        sys.exit()

    # Generate header, a list containing the first two elems of the CSV file
    header = fp.readline().strip().split(',')
    npv = 0                                                     # Net Present Value
    cashFlowList = []

    # loop to go through the CSV file parsing each line to separate the years and cash flow
    # into a two dimensional array cashFlowList
    for line in fp:
        line = line.strip().split(',')
        cashFlowTemp = []
        for i in range(len(header)):
            cashFlowTemp.append(int(line[i]))
        cashFlowList.append(cashFlowTemp)
        npv += presentVal(cashFlowTemp[1], d_rate, cashFlowTemp[0])

    npCF = np.array(cashFlowList)

    # Creating a bar chart showing the cash flows overtime
    plt.title("Cash Flows over time: Given a NPV of %.2f and yearly rate of %.2f%%" % (
        npv, d_rate))
    plt.xlabel('Years (0 = current year )')
    plt.ylabel('Cash flow ($)')
    plt.bar(npCF[:, 0], npCF[:, 1], alpha=0.9, width=0.2)
    plt.savefig('cash_flow_fig.png')

    plt.show()
    fp.close()


if __name__ == "__main__":
    main()

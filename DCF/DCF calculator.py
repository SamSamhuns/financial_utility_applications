# coding: utf-8

'''
Utility Python program for calculating Net Present Value of cash flows over a yearly period
DCF Calculations for yearly cash flows
All cash flows must be presented on a yearly basis in the form of a CSV file as described below
discount rate has to be entered separately.
'''
# Author: Samridha Man Shrestha
# 2018-11-12
# Must have numpy and matplotlib installed in host system
# Using Python 3
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate present value of cash flow
# rate is in % per year and time is in years
def presentVal ( futureVal, rate, time ):
    return futureVal / ((1+(rate/100))**time)

#  Name the csv data file cd.csv which must be in the same directory as this .py file
#  CSV file format
#  Note that current year is stated as 0
#  year, cash_flow
#  0,    -30000
#  1,    1500
#  2,    1600

fp = open('cf.csv', 'r')
d_rate = int(input("Enter discount rate per year: "))             # Discount rate entered as a percentage

header = fp.readline().strip().split(',')
npv = 0 # Net Present Value
cashFlowList = []

for line in fp:
    line = line.strip().split(',')
    cashFlowTemp = []
    for i in range(len(header)):
        cashFlowTemp.append( int(line[i]) )
    cashFlowList.append(cashFlowTemp)
    npv += presentVal(cashFlowTemp[1], d_rate, cashFlowTemp[0])

print("The NPV is %.2f" % (npv))

npCF = np.array(cashFlowList)

# Creating a bar chart showing the cash flows overtime
plt.title("Cash Flows over time")
plt.xlabel('Years (0 = current year )')
plt.ylabel('Cash flow ($)')
plt.bar(npCF[:,0], npCF[:,1], alpha=0.9, width=0.2 )

plt.show()
fp.close()

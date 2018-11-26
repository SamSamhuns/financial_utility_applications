'''
Script to download and save security returns CSV file
The CSV files are downloaded from yahoo-finance through their downloads API page
CSV Format: Date, Open, High, Low, Close, Adj, Close, Volume
'''
# Author: Samridha Man Shrestha
# 2018-11-26
# Using Python 3
import sys
import time
import requests

session = requests.Session()


def get_cookie_crumb():
    crumb = None
    cookie = None
    # This query sends a GET request to the yahoo finance page to get session cookie and crumb
    # Querying the yahoo finance quote page for GSPC
    response = session.get('http://finance.yahoo.com/quote/^GSPC')

    if response.ok:
        cookie = response.cookies
        # print(response.content)
        # print(response.cookies.items())
    else:
        print('GET request unsuccessful: HTTP status', response.status_code)
        sys.exit()

    alines = str(response.content)
    cs = alines.find('CrumbStore')
    cr = alines.find('crumb', cs + 10)
    cl = alines.find(':', cr + 5)
    q1 = alines.find('"', cl + 1)
    q2 = alines.find('"', q1 + 1)
    crumb = alines[q1 + 1:q2]

    # print(crumb, cookie )
    return {'cookie': cookie, 'crumb': crumb}


def get_sec_data(ticker, begindate, enddate, dtype):
    cookie, crumb = None, None
    cc_result = get_cookie_crumb()
    cookie = cc_result['cookie']
    crumb = cc_result['crumb']

    # time.mktime() takes format ( tm_year, tm_month, tm_day, tm_hr, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    tm_year, tm_month, tm_day, = (int(begindate[0:4]), int(
        begindate[4:6]), int(begindate[6:8])
    t_begin=time.mktime(tm_year, tm_month, tm_day, 4, 0, 0, 0, 0, 0))
    t_end = time.mktime(tm_year, tm_month, tm_day, 18, 0, 0, 0, 0, 0))

    # loading up the parameters for the historical data get request to yahoo finance
    param={}
    param['period1']=int(t_begin)
    param['period2']=int(t_end)
    param['interval']='1d'
    if dtype == 'quote':
        param['events']='history'
    elif dtype == 'dividend':
        param['events']='div'
    elif dtype == 'split':
        param['events']='split'
    param['crumb']=crumb

    url='http://query1.finance.yahoo.com/v7/finance/download/{}?'.format(
        ticker)
    resp2=session.get(url, params = param, cookies = cookie)

    # Printing useful information
    # print(crumb, cookie)
    print(resp2.status_code)
    print(resp2.content)


def main():
    if len(sys.argv) != 5 and (sys.argv[4]).lower() != 'quote' and (sys.argv[4]).lower() != 'split' and (sys.argv[4]).lower() != 'dividend':
        print("Usage:security.csv <TICKER> <START_DATE_YYYYMMDD> <END_DATE_YYYYMMDD> <DATA_quote/dividend/split>")
        sys.quit()

    ticker=(sys.argv[1]).upper()
    start_date=int(sys.argv[2].replace(' ', '').replace('-', ''))
    end_date=int(sys.argv[3].replace(' ', '').replace('-', ''))
    data_type=(sys.argv[4]).lower()
    get_sec_data(ticker, start_date, end_date, data_type)

# FORMAT example for func args ( 'DJI', '20170515', '20170526', 'quote')


main()

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

    full_resp = str(response.content)
    cs = full_resp.find('CrumbStore')
    cr = full_resp.find('crumb', cs + 10)
    cl = full_resp.find(':', cr + 5)
    q1 = full_resp.find('"', cl + 1)
    q2 = full_resp.find('"', q1 + 1)
    crumb = full_resp[q1 + 1:q2]

    # print(crumb, cookie )
    return {'cookie': cookie, 'crumb': crumb}


def get_sec_data(ticker, begindate, enddate, dtype, interval):
    cookie, crumb = None, None
    cc_result = get_cookie_crumb()
    cookie = cc_result['cookie']
    crumb = cc_result['crumb']

    # time.mktime() takes format ( tm_year, tm_month, tm_day, tm_hr, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
    t_begin = time.mktime((int(begindate[0:4]), int(begindate[4:6]), int(begindate[6:8]), 4, 0, 0, 0, 0, 0))
    t_end = time.mktime((int(enddate[0:4]), int(enddate[4:6]), int(enddate[6:8]), 18, 0, 0, 0, 0, 0))

    # loading up the parameters for the historical data get request to yahoo finance
    param={}
    param['period1']=int(t_begin)
    param['period2']=int(t_end)
    param['interval']='1mo'
    if dtype == 'quote':
        param['events']='history'
    elif dtype == 'dividend':
        param['events']='div'
    elif dtype == 'split':
        param['events']='split'
    param['crumb']=crumb

    url='http://query1.finance.yahoo.com/v7/finance/download/{}?'.format(
        ticker)
    resp2=session.get(url, params=param, cookies=cookie)

    # Printing useful information
    # print(crumb, cookie)
    # print( url, param )
    print(resp2.status_code)
    print(resp2.content)


def main():
    if len(sys.argv) != 5 and (sys.argv[4]).lower() not in {'quote', 'split', 'dividend'} and (sys.argv[5] not in {'1d', '1wk', '1mo'}):
        print("Usage:security.csv <TICKER> <START_DATE_YYYYMMDD> <END_DATE_YYYYMMDD> <DATA_quote/dividend/split> <interval_1d/1wk/1mo>")
        sys.exit()

    ticker=(sys.argv[1]).upper()
    start_date=sys.argv[2].replace(' ', '').replace('-', '')
    end_date=sys.argv[3].replace(' ', '').replace('-', '')
    data_type=(sys.argv[4]).lower()
    get_sec_data(ticker, start_date, end_date, data_type, interval)

# FORMAT example for func args ( 'DJI', '20170515', '20170526', 'quote', '1mo')
main()

import sys
import time
import requests

session = requests.Session()
response = session.get('http://finance.yahoo.com/quote/^GSPC')

if response.ok:
    rtn = response.cookies.get_dict()
    # print(response.content)
    print(rtn)
    print ( response.cookies.items())
else:
    print('Unsuccessful GET request')
    sys.exit()

ticker, begindate, enddate = 'DJI', '20170515', '20170526'

t_begin = time.mktime((int(begindate[0:4]), int(begindate[4:6]), int(begindate[6:8]), 4, 0, 0, 0, 0, 0))
t_end = time.mktime((int(enddate[0:4]), int(enddate[4:6]), int(enddate[6:8]), 18, 0, 0, 0, 0, 0))

param = dict()

alines = str(response.content)
cs = alines.find('CrumbStore')
cr = alines.find('crumb', cs + 10)
cl = alines.find(':', cr + 5)
q1 = alines.find('"', cl + 1)
q2 = alines.find('"', q1 + 1)
crumb = alines[q1 + 1:q2]

print(crumb)

param['period1'] = int(t_begin)
param['period2'] = int(t_end)
param['interval'] = '1d'
param['events'] = 'history'
param['crumb'] = crumb


url = 'http://query1.finance.yahoo.com/v7/finance/download/{}?'.format(ticker)
print(rtn , response.cookies)
print("THE URL IS:", url, param)
req2 = session.get(url, params=param, cookies=response.cookies)

print (req2.status_code  )
print (req2.content)

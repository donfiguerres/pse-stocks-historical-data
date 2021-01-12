import os.path
import sys
import csv
import requests
import time
import json
from datetime import datetime

requestpath = 'https://edge.pse.com.ph/common/DisclosureCht.ax'

headers = {
    'Origin': 'https://edge.pse.com.ph', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'en-US,en;q=0.9', 
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Content-Type': 'application/json', 
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://edge.pse.com.ph/companyPage/stockData.do?cmpy_id=29&security_id=146',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
    }

payload = {
    "cmpy_id":"164",
    "security_id":"249",
    "startDate":"01-01-2020",
    "endDate":"01-11-2021"
    }

with open('finalstocks.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        if count < 234 and count > 240:
            count += 1
            continue
        companyFile = open('historicaldata/'+row['companyName']+'.csv', 'w')
        print(row['companyId'], row['securityId'], row['companyName'])
        
        payload['cmpy_id'] = row['companyId']
        payload['security_id'] = row['securityId']

        r = requests.post(requestpath, json=payload, headers=headers)
        hist_data = json.loads(r.content)
        hist_values = hist_data['chartData']

        company_hist_file = csv.writer(companyFile)
        company_hist_file.writerow(['Date', 'Value', 'Open', 'Close', 'High', 'Low']) 

        for item in hist_values: 
            print(item)
            date_object = datetime.strptime(item['CHART_DATE'],'%b %d, %Y 00:00:00')
            shortdate = date_object.strftime("%d/%m/%y")
            company_hist_file.writerow([shortdate, item['VALUE'], item['OPEN'], item['CLOSE'], item['HIGH'], item['LOW']]) 
        # why the need for a delay?
        time.sleep(5)

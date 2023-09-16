import json
import requests
import pandas as pd
import datetime 

verbose = True

page = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex')
futures = json.loads(page.content)

ct = int(datetime.datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())*1000

all_data_df = pd.DataFrame()
for i in futures:
    print(i["symbol"])
    if i["symbol"][-4:] == 'BUSD': continue
    page = requests.get('https://fapi.binance.com/fapi/v1/fundingRate', params={'symbol': i["symbol"], 'startTime': ct - 24*3600*1000 - 8*3600*1000})
    try:
        df = pd.DataFrame(json.loads(page.content)[:-1])
        df = df.astype({'fundingRate': 'float64'})
    except:
        print("Could not parse data for symnbol " + i["symbol"])
        continue

    all_data_df = all_data_df.append(df)



rawdata_csv = "funding_fees_raw.csv"
all_data_df.to_csv(rawdata_csv, index = False)
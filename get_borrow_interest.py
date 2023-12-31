import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from utils.prepare_env import get_api_key
import pandas as pd
import datetime

config_logging(logging, logging.DEBUG)

api_key, api_secret = get_api_key()

client = Client(api_key, api_secret)

assets = client.margin_all_assets()

all_data_df = pd.DataFrame()

ct = int(datetime.datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())*1000

for asset in assets:
    if not asset['isBorrowable']: continue
    ticker = asset['assetName']
    print(ticker)
    interest_rate = client.margin_interest_rate_history(asset=ticker, vipLevel=1, startTime=ct - 24*3600*1000 - 1, recvWindow=30000)
    df = pd.DataFrame(interest_rate)
    df = df.astype({'dailyInterestRate': 'float64'})
    all_data_df = all_data_df.append(df)

rawdata_csv = "borrow_interest_raw.csv"
all_data_df.to_csv(rawdata_csv, index = False)    
from enum import Enum, auto
from binance.client import Client
from os import environ
from dotenv import load_dotenv
import sys

load_dotenv()

class Binance:
    client = Client
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        print(self.client.get_server_time())

    def get_orders(self, symbol: str):
        return self.client.get_all_orders(symbol=symbol, limit=10)

class Currency(Enum):
    BTC = "BTC"
    ETH = "ETH"
    TWD = "TWD"
    USD = "USD"
    DAI = "DAI"
    USDC = "USDC"
    USDT = "USDT"

    @classmethod
    def choices(cls):
        result = tuple((i.name+j.name, i.name+j.name) for i in cls for j in cls if i != j)
        print(result)
        return result

class Record:
    id: int = 0
    market: Currency = ""
    

if __name__ == "__main__":
    client = Binance(environ.get("API_KEY"), environ.get("API_SECRET"))
    print([(v["price"], v["side"], v["executedQty"], v["cummulativeQuoteQty"], v["type"]) for v in client.get_orders(sys.argv[1]) if v['status'] == 'FILLED'])
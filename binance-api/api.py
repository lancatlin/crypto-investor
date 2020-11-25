from typing import Dict
from enum import Enum, auto
from binance.client import Client
from os import environ
from dotenv import load_dotenv
import sys

load_dotenv()

class Binance:
    client = Client
    def __init__(self, api_key: str, api_secret: str):
        self.client = Client(api_key, api_secret)

    def get_orders(self, symbol: str):
        data = self.client.get_all_orders(symbol=symbol, limit=10)
        return [Record(v) for v in data if v['status'] == 'FILLED']

    def get_balances(self):
        info = self.client.get_account()
        return info['balances']
    
    def assets(self):
        return [v['asset'] for v in self.get_balances() if float(v['free']) + float(v['locked']) != 0]

def all_symbols(currencies):
    result = tuple(f"{i}{j}" for i in currencies for j in currencies if i != j)
    print(result)
    return result

class Record:
    id: int = 0
    side: bool = False
    symbol: str = ""
    executed_qty: float = 0
    cummulative_quote_qty: float = 0

    def __init__(self, table: Dict[str, str]):
        self.id = int(table["orderId"])
        self.symbol = table["symbol"]
        self.executed_qty = float(table["executedQty"])
        self.cummulative_quote_qty = float(table["cummulativeQuoteQty"])


    def price(self) -> float:
        return self.cummulative_quote_qty / self.executed_qty
    
    def __str__(self):
        return "id: {}, symbol: {}, executedQty: {}, quote: {}, price: {}".format(self.id, self.symbol, self.executed_qty, self.cummulative_quote_qty, self.price())
    
my_currencies = ['BTC', 'ETH', 'LTC', 'EOS', 'XRP', 'USDC', 'USDT']

if __name__ == "__main__":
    client = Binance(environ.get("API_KEY"), environ.get("API_SECRET"))
    print(client.assets())
    print([str(v) for v in client.get_orders(sys.argv[1])])
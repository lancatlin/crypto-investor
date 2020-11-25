from typing import Dict, List, Optional
from enum import Enum, auto
from binance.client import Client # type: ignore
from os import environ
from dotenv import load_dotenv
import sys
from record import Record

load_dotenv()

class Binance:
    client = Client
    __symbols: Optional[List[str]] = None

    def __init__(self, api_key: Optional[str], api_secret: Optional[str]):
        self.client = Client(api_key, api_secret)

    def get_orders(self, symbol: str):
        data = self.client.get_all_orders(symbol=symbol, limit=10)
        return [Record(v) for v in data if v['status'] == 'FILLED']

    def assets(self) -> List[str]:
        return [v['asset'] for v in self.client.get_account()['balances'] \
            if float(v['free']) + float(v['locked']) != 0]

    def symbols(self) -> List[str]:
        if self.__symbols is not None:
            return self.__symbols
        return [v for v in all_symbols(self.assets()) \
            if self.client.get_symbol_info(v) is not None]

    def records(self) -> List[Record]:
        records: List[Record] = []
        for symbol in self.symbols():
            records += self.get_orders(symbol)
        return records


def all_symbols(currencies: List[str]):
    return tuple(f"{i}{j}" for i in currencies for j in currencies if i != j)

if __name__ == "__main__":
    client = Binance(environ.get("API_KEY"), environ.get("API_SECRET"))
    for record in client.records():
        print(record)
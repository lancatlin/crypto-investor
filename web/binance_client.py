from typing import Dict, List, Optional, Generator
from binance.client import Client # type: ignore
from web.models import Record

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

    def symbols(self) -> Generator[str, None, None]:
        if self.__symbols is not None:
            return self.__symbols
        for v in all_symbols(self.assets()):
            if self.client.get_symbol_info(v) is not None:
                yield v

    def records(self) -> Generator[Record, None, None]:
        for symbol in self.symbols():
            for r in self.get_orders(symbol):
                yield r


def all_symbols(currencies: List[str]):
    return tuple(f"{i}{j}" for i in currencies for j in currencies if i != j)

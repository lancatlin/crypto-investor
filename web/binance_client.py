from typing import Dict, List, Generator
from binance.client import Client # type: ignore
from web.models import Record, User

class Binance:
    client: Client = None
    __symbols: List[str] = None
    user: User = None

    def __init__(self, user: User):
        self.user = user
        self.client = Client(user.api_key, user.api_secret)

    def get_orders(self, symbol: str):
        data = self.client.get_all_orders(symbol=symbol)
        return [self.create_record(v) for v in data if v['status'] == 'FILLED']

    def assets(self) -> List[str]:
        return [v['asset'] for v in self.client.get_account()['balances'] \
            if float(v['free']) + float(v['locked']) != 0]

    def symbols(self) -> Generator[str, None, None]:
        if self.__symbols is not None:
            for symbol in self.__symbols:
                yield symbol
            return
        symbols = []
        for v in all_symbols(self.assets()):
            if self.client.get_symbol_info(v) is not None:
                symbols.append(v)
                yield v
        self.__symbols = symbols

    def records(self) -> Generator[Record, None, None]:
        for symbol in self.symbols():
            for r in self.get_orders(symbol):
                yield r

    def create_record(self, table: Dict[str, str]) -> Record:
        return Record.objects.create(
            id = int(table['orderId']),
            isSell = table['side'] == 'SELL',
            symbol = table['symbol'],
            executed_qty = float(table['executedQty']),
            cummulative_quote_qty = float(table['cummulativeQuoteQty']),
            user=self.user,
        )

def all_symbols(currencies: List[str]):
    return tuple(f"{i}{j}" for i in currencies for j in currencies if i != j)

from typing import Dict, List, Generator, Tuple
from binance.client import Client # type: ignore
from web.models import Record, User
from datetime import datetime, timezone

class Binance:
    client: Client = None
    __symbols: List[str] = None
    user: User = None

    def __init__(self, user: User):
        self.user = user
        self.client = Client(user.api_key, user.api_secret)

    def records(self) -> Generator[Tuple[Record, bool], None, None]:
        for symbol in self.symbols():
            for r in self.get_orders(symbol):
                yield r

    def symbols(self) -> Generator[str, None, None]:
        if self.__symbols is not None:
            for symbol in self.__symbols:
                yield symbol
            return
        symbols = []
        for v in all_symbols(self.assets()):
            if self.client.get_symbol_info(v.replace('/', '')) is not None:
                symbols.append(v)
                yield v
        self.__symbols = symbols

    def assets(self) -> List[str]:
        return [v['asset'] for v in self.client.get_account()['balances'] \
            if float(v['free']) + float(v['locked']) != 0]

    def get_orders(self, symbol: str) -> List[Tuple[Record, bool]]:
        data = self.client.get_all_orders(symbol=symbol.replace('/', ''))
        return [self.create_record(v, symbol) for v in data if v['status'] == 'FILLED']

    def create_record(self, table: Dict[str, str], symbol: str) -> Record:
        updates = {
            'is_sell': table['side'] == 'SELL',
            'symbol': symbol,
            'executed_qty': float(table['executedQty']),
            'cummulative_quote_qty': float(table['cummulativeQuoteQty']),
            'user': self.user,
            'time': datetime.fromtimestamp(int(table['time']) / 1000, tz=timezone.utc),
        }
        return Record.objects.get_or_create(
            id = int(table['orderId']),
            defaults=updates,
        )

    def price(self, symbol: str) -> float:
        print(symbol)
        try:
            data = self.client.get_avg_price(symbol=symbol+'USDT')
            return float(data['price'])
        except:
            return 1

def all_symbols(currencies: List[str]):
    return tuple(f"{i}/{j}" for i in currencies for j in currencies if i != j)

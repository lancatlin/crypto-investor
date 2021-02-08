from typing import List, Dict
from django.test import TestCase
from django.utils import timezone
from .binance_client import Binance
from .models import User, Record, calculate_profit
from dotenv import load_dotenv
from os import environ
from datetime import datetime

class BinanceTestCase(TestCase):
    client: Binance = None
    def setUp(self):
        load_dotenv()
        api_key = environ.get("API_KEY")
        api_secret = environ.get("API_SECRET")
        user = User.objects.create(api_key=api_key, api_secret=api_secret)
        self.client = Binance(user)
    
    def test_find_records(self):
        for record in self.client.records():
            print(record)
        print([i for i in self.client.symbols()])

class ProfitTest(TestCase):
    records: List[Record] = []
    prices: Dict[str, float] = {}
    user: User = None

    def setUp(self):
        self.user = User.objects.create(username='test_profit')
        self.records = [
            self.record(
                symbol="BTC/USDC",
                is_sell=True,
                executed_qty=1,
                cummulative_quote_qty=20000,
            ),
            self.record(
                symbol="BTC/USDC",
                is_sell=False,
                executed_qty=1,
                cummulative_quote_qty=18000,
            ),
            self.record(
                symbol='BTC/ETH',
                is_sell=True,
                executed_qty=1,
                cummulative_quote_qty=40,
            ),
            self.record(
                symbol="ETH/USDC",
                is_sell=False,
                executed_qty=1,
                cummulative_quote_qty=400,
            ),
        ]
        self.prices = {
            'BTC': 20000,
            'USDC': 1,
            'ETH': 500,
        }

    def record(self, **kwargs):
        return Record.objects.create(
            user=self.user,
            time=timezone.now(),
            **kwargs,
        )
    
    def test_profit(self):
        prices = lambda k: self.prices[k]
        profit = calculate_profit(self.records, prices)
        print(profit.__dict__)
        assert profit.profit == 2100, 'Profit not correct'
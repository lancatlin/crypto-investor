# Create your models here.
from typing import Dict, List, Callable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
#from .binance_client import Binance

class User(AbstractUser):
    api_key = models.CharField(max_length=128)
    api_secret = models.CharField(max_length=128)

class Record(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_sell: bool = models.BooleanField()
    symbol: str = models.CharField(max_length=64)
    executed_qty: float = models.FloatField()
    cummulative_quote_qty: float = models.FloatField()
    time = models.DateTimeField()

    def price(self) -> float:
        return self.cummulative_quote_qty / self.executed_qty
    
    def __str__(self) -> str:
        return f"id: {self.id}, symbol: {self.symbol}, executedQty: {self.executed_qty}, quote: {self.cummulative_quote_qty}, price: {self.price()}"
    
# Profit records the profit in a period
class Profit:
    cost: float = 0
    income: float = 0
    profit: float = 0
    rate: float = 0
    currencies: Dict[str, float] = {}

    def __init__(self, cost, income, currencies, prices):
        value = [
            sum([v * prices(k) for k, v in currencies.items() if v > 0]),
            sum([-v * prices(k) for k, v in currencies.items() if v < 0]),
        ]
        self.cost = cost + value[1]
        self.income = income + value[0]
        self.currencies = currencies
        self.value = sum(value)
        self.profit = self.income - self.cost
        self.rate = self.income / self.cost * 100 - 100

def calculate_profit(records: List[Record], prices: Callable[[str], float]) -> Profit:
    cost: float = 0
    income: float = 0
    pool: Dict[str, float] = {}

    for record in records:
        c: List[str] = record.symbol.split('/', 2)
        if all(is_coin(k) for k in c):
            # omit stable coin to stable coin
            continue
        [pool.setdefault(k, 0) for k in c if not is_coin(k)]
        if not record.is_sell:
            pool[c[0]] += record.executed_qty
            if is_coin(c[1]):
                cost += record.cummulative_quote_qty
            else:
                pool[c[1]] -= record.cummulative_quote_qty
        else:
            pool[c[0]] -= record.executed_qty
            if is_coin(c[1]):
                income += record.cummulative_quote_qty
            else:
                pool[c[1]] += record.cummulative_quote_qty
    
    return Profit(cost, income, pool, prices)

def is_coin(c: str) -> bool:
    return 'USD' in c or c == 'DAI'
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

    def __init__(self, cost, income, currencies):
        self.cost = cost
        self.income = income
        self.profit = income - cost
        self.rate = income / cost
        self.currencies = currencies

def calculate_profit(records: List[Record], prices: Callable[[str], float]) -> Profit:
    cost: Dict[str, float] = {}
    income: Dict[str, float] = {}

    for record in records:
        c: List[str] = record.symbol.split('/', 2)
        for k in c:
            cost.setdefault(k, 0)
            income.setdefault(k, 0)
        if not record.is_sell:
            income[c[0]] += record.executed_qty
            cost[c[1]] += record.cummulative_quote_qty
        else:
            income[c[0]] -= record.executed_qty
            income[c[1]] += record.cummulative_quote_qty
    
    total_cost = sum([cost[k] * prices(k) for k in cost.keys()])
    total_value = sum([income[k] * prices(k) for k in income.keys()])
    currencies = {k: income[k] - cost[k] for k in cost.keys()}
    return Profit(total_cost, total_value, currencies)

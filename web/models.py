# Create your models here.
from typing import Dict
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    api_key = models.CharField(max_length=128)
    api_secret = models.CharField(max_length=128)

class Record(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    isSell: bool = models.BooleanField()
    symbol: str = models.CharField(max_length=64)
    executed_qty: float = models.FloatField()
    cummulative_quote_qty: float = models.FloatField()

    def __init__(self, table: Dict[str, str]):
        self.id = int(table['orderId'])
        self.isSell = table['side'] == 'SELL'
        self.symbol = table['symbol']
        self.executed_qty = float(table['executedQty'])
        self.cummulative_quote_qty = float(table['cummulativeQuoteQty'])

    def price(self) -> float:
        return self.cummulative_quote_qty / self.executed_qty
    
    def __str__(self) -> str:
        return f"id: {self.id}, symbol: {self.symbol}, executedQty: {self.executed_qty}, quote: {self.cummulative_quote_qty}, price: {self.price()}"
    
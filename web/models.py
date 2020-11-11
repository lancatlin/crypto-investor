from django.db import models
from enum import Enum, auto
# Create your models here.

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

class Record(models.Model):
    SELL = "SELL"
    BUY = "BUY"
    side_choices = [
        (SELL, "Sell"),
        (BUY, "Buy")
    ]

    id = models.IntegerField()
    symbol = models.CharField(max_length=255, choices=Currency.choices())
    time = models.DateTimeField()
    price = models.FloatField()
    side = models.Choices(choices = side_choices)


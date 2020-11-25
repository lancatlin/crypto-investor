from django.db import models
# Create your models here.


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


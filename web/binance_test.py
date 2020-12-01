from django.test import TestCase
from web.binance_client import Binance
from dotenv import load_dotenv
from os import environ

class BinanceTestCase(TestCase):
    def setUp(self):
        load_dotenv()
        api_key = environ.get("API_KEY")
        api_secret = environ.get("API_SECRET")
        print(f"{api_key}, {api_secret}")
        self.client = Binance(api_key, api_secret)
    
    def test_find_records(self):
        for record in self.client.records():
            print(record)

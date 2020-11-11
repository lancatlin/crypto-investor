from binance.client import Client
from os import environ
from dotenv import load_dotenv

load_dotenv()

class BinanceClient:
    client = Client
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        print(self.client.get_server_time())

    def get_orders(self, symbol: str):
        return self.client.get_all_orders(symbol=symbol, limit=10)

if __name__ == "__main__":
    client = BinanceClient(environ.get("API_KEY"), environ.get("API_SECRET"))
    print(client.get_orders("BTCUSDC"))
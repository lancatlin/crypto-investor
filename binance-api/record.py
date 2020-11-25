from typing import Dict

class Record:
    id: int = 0
    side: bool = False
    symbol: str = ""
    executed_qty: float = 0
    cummulative_quote_qty: float = 0

    def __init__(self, table: Dict[str, str]):
        self.id = int(table["orderId"])
        self.symbol = table["symbol"]
        self.executed_qty = float(table["executedQty"])
        self.cummulative_quote_qty = float(table["cummulativeQuoteQty"])

    def price(self) -> float:
        return self.cummulative_quote_qty / self.executed_qty
    
    def __str__(self) -> str:
        return f"id: {self.id}, symbol: {self.symbol}, executedQty: {self.executed_qty}, quote: {self.cummulative_quote_qty}, price: {self.price()}"
    
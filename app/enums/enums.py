from enum import Enum,unique

@unique
class ActiveStocks(Enum):
    TESLA = "TSLA"
    NVIDIA = "NVDA"
    ALPHABET = "GOOG"
    APPLE = "AAPL"
    AMAZON = "AMZN"
    MICROSOFT = "MSFT"
    META = "META"
    NETFLIX = "NFLX"
    AMD = "AMD"
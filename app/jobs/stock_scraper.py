from ..models import StockData
from ..helpers import add_records_to_database
from ..services.stock_scraper import fetch_stock_news, fetch_stock_price
from ..services.pinecone_vectorizer import get_pinecone_index, upsert_documents
import datetime
import jsonpickle

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

URLS = {
    "yahoo_finance": "https://finance.yahoo.com/quote/{stock_symbol}/news?p={stock_symbol}",
    "market_watch": "https://www.marketwatch.com/investing/stock/{stock_symbol}",
    "cnbc_trader_talk": "https://www.cnbc.com/trader-talk/",
    "yahoo_topic": "https://finance.yahoo.com/topic/stock-market-news/"
}

def scrape_stocks(app):
    with app.app_context():
        stock_symbols = ['TSLA', 'NVDA', 'GOOG', 'AAPL', 'AMZN', 'MSFT', 'META', 'NFLX', 'AMD']
        stock_data_objects = []

        for symbol in stock_symbols:
            print(f"Fetching data for {symbol}...")
            news = fetch_stock_news(symbol)
            price = fetch_stock_price(symbol)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            stock_data = f"""
            Stock News of {symbol} on {timestamp}\n

            The stock price is ${price}.\n
            """

            news_content = [data['content'] for data in news]

            stock_data += "\n".join(f"{content}" for content in news_content)

            scraped_data = StockData(name=symbol+timestamp, news=stock_data, stock_metadata=jsonpickle.encode({'stock_symbol': symbol, 'timestamp': timestamp}))
            stock_data_objects.append(scraped_data)

        upsert_documents([(data.name, data.news, data.deserialize_stock_metadata()) for data in stock_data_objects])
        add_records_to_database(stock_data_objects)

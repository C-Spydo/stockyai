from pinecone import Pinecone
from ..models import StockData
from ..extensions import session
from datetime import datetime, timedelta
from ..constants import PINECONE_INDEX_HOST

def clean_stock_table(app):
    with app.app_context():
        pc = Pinecone()
        index = pc.Index(host=PINECONE_INDEX_HOST)

        cutoff_time = datetime.now() - timedelta(hours=12)
        
        query = session.query(StockData).filter(StockData.created_at < cutoff_time)

        stock_data_list = query.all()
        stock_names = [stock.name for stock in stock_data_list]

        for name in stock_names:
            for ids in index.list(prefix=name):
                index.delete(ids=ids)

        query.delete(synchronize_session=False)
        session.commit()
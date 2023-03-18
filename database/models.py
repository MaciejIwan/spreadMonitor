from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Spread(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(DateTime)
    binance_best_bid = Column(Float)
    binance_best_ask = Column(Float)
    okx_best_bid = Column(Float)
    okx_best_ask = Column(Float)
    bid_diff = Column(Float)
    ask_diff = Column(Float)

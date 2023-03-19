import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import timedelta

# create the SQLAlchemy engine
engine = create_engine('sqlite:///nazwa_pliku_bazy_danych.sqlite')

# create a base class for declarative ORM models
Base = declarative_base()

# define the ORM model for the "data" table
class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    currency = Column(String)
    exchange = Column(String)
    bin_best_bid = Column(Float)
    bin_best_ask = Column(Float)
    okx_best_bid = Column(Float)
    okx_best_ask = Column(Float)

# create the tables in the database, if they don't already exist
Base.metadata.create_all(engine)

# create a session factory to interact with the database
Session = sessionmaker(bind=engine)

# create a session object to interact with the database
session = Session()

# retrieve all rows from the "data" table
rows = session.query(Data).all()

# convert the rows to a pandas DataFrame
data = pd.DataFrame.from_records([row.__dict__ for row in rows])

# set the DataFrame index to the "timestamp" column
data.set_index('timestamp', inplace=True)

# calculate the bid-ask spread for both exchanges
data['bin_spread'] = data['bin_best_ask'] - data['bin_best_bid']
data['okx_spread'] = data['okx_best_ask'] - data['okx_best_bid']

# calculate the potential profit for an arbitrage trade
data['potential_profit'] = data['bin_best_bid'] * 0.993 - data['okx_best_ask'] * 1.003

# filter the data to only include potential arbitrage opportunities
arbitrage_data = data[data['potential_profit'] > 0]

# group the data by hour and count the number of arbitrage opportunities
arbitrage_counts = arbitrage_data.resample('H')['potential_profit'].count()

# calculate the mean time between arbitrage opportunities
mean_time_between_arbitrage = timedelta(hours=1) / arbitrage_counts.mean()

# calculate the mean potential profit for an arbitrage trade
mean_potential_profit = arbitrage_data['potential_profit'].mean()

# print the results
print(f"Number of arbitrage opportunities per hour: {arbitrage_counts.mean():.2f}")
print(f"Mean time between arbitrage opportunities: {mean_time_between_arbitrage}")
print(f"Mean potential profit for an arbitrage trade: {mean_potential_profit:.2f}")

# plot the bid-ask spread and potential profit over time
data[['bin_spread', 'okx_spread', 'potential_profit']].plot(figsize=(10, 7))

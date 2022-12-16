from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime,Float,String, UniqueConstraint, create_engine

Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    __table_args__ = (UniqueConstraint("station_id", "date", name="date_station_cx"),)
    id=Column(Integer,primary_key=True)
    station_id = Column(String)
    date = Column(DateTime)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precip = Column(Float)

class Yield(Base):
    __tablename__ = "yields"
    year = Column(String, primary_key=True)
    yields = Column(Integer)

class summaryWeather(Base):
    __tablename__ = "summary_weather"
    __table_args__ = (UniqueConstraint("station_id", "year", name="year_station_cx"),)
    id=Column(Integer,primary_key=True)
    station_id = Column(String)
    year = Column(String)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precip = Column(Float)

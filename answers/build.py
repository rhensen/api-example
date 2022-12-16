from models import Weather, Yield, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
import csv 
import datetime


engine = create_engine('sqlite:///database.db')
conn=engine.connect()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
start=datetime.datetime.now()
print(f'--LOG: Start Time: {start}')

dir_list = os.listdir('wx_data')
ids=[x.replace('.txt', "")for x in dir_list]

for file in dir_list: 
    with open(f'wx_data/{file}') as txt_file:
        data = csv.reader(txt_file, delimiter="\t")
        data = list(data)
        def make_weather_row(day):
            weather=Weather(station_id=file.replace('.txt', ""),
                date= datetime.datetime.strptime(day[0], '%Y%m%d'),
                max_temp= int(day[1]),
                min_temp= int(day[2]),
                precip= int(day[3]))
            return(weather)
        data_full=[make_weather_row(day) for day in data]
        try:
            session = Session()
            session.add_all(data_full)
            session.commit()
        except: 
            pass

with open(f'yld_data/US_corn_grain_yield.txt') as txt_file:
        data = csv.reader(txt_file, delimiter="\t")
        data = list(data)
        for day in data:
            try:
                yields=Yield(
                year= int(day[0]),
                yields= int(day[1]))
                session = Session()
                session.add(yields)
                session.commit()
            except:
                pass
end=datetime.datetime.now()
print(f'--LOG: End Time: {end}')
print(f'--LOG: Total Upload Time: {end-start}')
print(f'--LOG: Number of Weather Rows Uploaded: { conn.execute("select count(*) from weather").scalar() }')
print(f'--LOG: Number of Yield Rows Uploaded: { conn.execute("select count(*) from yields").scalar() }')
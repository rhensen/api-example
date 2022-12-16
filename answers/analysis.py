from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import summaryWeather,Base

engine = create_engine('sqlite:///database.db')
conn=engine.connect()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

clean_null_precip="""
update weather set precip = null where precip = -9999;
"""
conn.execute(clean_null_precip)

clean_null_max_temp="""
update weather set max_temp = null where max_temp= -9999;
"""
conn.execute(clean_null_max_temp)

clean_null_min_temp="""
update weather set min_temp = null where min_temp= -9999;
"""
conn.execute(clean_null_min_temp)
create_summary_table="""
SELECT station_id, strftime("%Y", date) as year, AVG(max_temp)/10 as avg_max_temp,AVG(min_temp)/10 as avg_min_temp,SUM(precip)/100 as total_precip from weather group BY station_id, strftime("%Y", date);
"""
resultSet=conn.execute(create_summary_table).all()
def make_weather_row(row):
            weather=summaryWeather(station_id=row[0],year=int(row[1]),
                avg_max_temp= row[2],
                avg_min_temp= row[3],
                total_precip= row[4])
            return(weather)
data_full=[make_weather_row(row) for row in resultSet]
session = Session()
session.add_all(data_full)
session.commit()
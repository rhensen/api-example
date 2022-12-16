from flask import  jsonify, request
from app import app
import sqlalchemy as db
import json 
engine = db.create_engine('sqlite:///database.db')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    conn=engine.connect()
    min_date= request.args.get('min_date', type = str, default='1984-01-01')
    max_date= request.args.get('max_date', type = str,default='2015-01-01')
    limit= request.args.get('limit', type = int,default=500)
    page= request.args.get('page', type = int,default=1)
    station_id= request.args.get('station_id', type = str)
    start=limit*(page-1)
    end=limit*(page)
    query=f"""
        SELECT * FROM weather where date > '{min_date}' and date < '{max_date}'
        and id>{start} and id <= {end}
        """
    if station_id:
        query="".join([query,f"and station_id= '{station_id}'"])
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = (row[0], row[1], row[2], row[3], row[4], row[5])
        rowarray_list.append(t)
    response = jsonify(rowarray_list)
    conn.close()
    return response, 200

@app.route('/api/yield', methods=['GET'])
def get_yield():
    conn=engine.connect()
    min_year= request.args.get('min_year', type = str, default='1984-01-01')
    max_year= request.args.get('max_year', type = str,default='2015-01-01')
    limit= request.args.get('limit', type = int,default=500)
    page= request.args.get('page', type = int,default=1)
    station_id= request.args.get('station_id', type = str)
    start=limit*(page-1)
    end=limit*(page)
    query=f"""
        SELECT * FROM yields where year > '{min_year}' and year < '{max_year}'
        """
    if station_id:
        query="".join([query,f"and station_id= '{station_id}'"])
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = (row[0], row[1])
        rowarray_list.append(t)
    response = jsonify(rowarray_list)
    conn.close()
    return response, 200

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    conn=engine.connect()
    min_year= request.args.get('min_year', type = int, default=1984)
    max_year= request.args.get('max_year', type = int,default=2015)
    limit= request.args.get('limit', type = int,default=500)
    page= request.args.get('page', type = int,default=1)
    station_id= request.args.get('station_id', type = str)
    start=limit*(page-1)
    end=limit*(page)
    query=f"""
        SELECT * FROM summary_weather where year > '{min_year}' and year < '{max_year}'
        and id>{start} and id <= {end}
        """
    if station_id:
        query="".join([query,f"and station_id= '{station_id}'"])
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = (row[0], row[1], row[2], row[3], row[4], row[5])
        rowarray_list.append(t)
    response = jsonify(rowarray_list)
    conn.close()
    return response, 200

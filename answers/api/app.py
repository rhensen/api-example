from flask import Flask, jsonify, request
from waitress import serve
import logging
import sqlalchemy as db
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = Flask(__name__)

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
        with t as(SELECT ROW_NUMBER() OVER() AS row_number,* FROM weather where date >= '{min_date}'  and date <= '{max_date}')
        select row_number,station_id,date,min_temp,max_temp,precip from t where row_number> {start} and row_number<{end}
        """
    if station_id:
        query="".join([query,f"and station_id= '{station_id}'"])
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = {'id':row[0], 'station_id':row[1], 'date':row[2], 'min_temp':row[3], 'max_temp':row[4], 'precip':row[5]}
        rowarray_list.append(t)
    response = jsonify(rowarray_list)
    conn.close()
    return response, 200

@app.route('/api/yield', methods=['GET'])
def get_yield():
    conn=engine.connect()
    min_year= request.args.get('min_year', type = int, default=1984)
    max_year= request.args.get('max_year', type = int,default=2015)
    query=f"""
        SELECT * FROM yields where year >= {min_year} and year <= {max_year}
        """
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = {'year':row[0],'yield': row[1]}
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
        with t as(SELECT ROW_NUMBER() OVER() AS row_number,* FROM summary_weather where year >= {min_year} and year <= {max_year})
        select row_number,station_id,year,avg_max_temp,avg_min_temp,total_precip from t where row_number> {start} and row_number<{end}
        """
    if station_id:
        query="".join([query,f"and station_id= '{station_id}'"])
    data = conn.execute(query).fetchall()
    rowarray_list = []
    for row in data:
        t = {'id':row[0], 'station_id':row[1], 'year':row[2], 'avg_max_temp_celsius':row[3], 'avg_min_temp_celsius':row[4], 'total_precip_cm':row[5]}

        rowarray_list.append(t)
    response = jsonify(rowarray_list)
    conn.close()
    return response, 200


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

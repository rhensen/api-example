# Code Challenge

# steps to run locally 

## setup

```cd ~/code-challenge ```

```pip install requirements.txt```

## build the database

```python3 answers/build.py```

## perform analysis 

```python3 answers/analysis.py```

## launch API to http://0.0.0.0:8080

```python3 answers/api/app.py```



## query structure: 

### GET .../api/weather/stats
#### optional query parameters: 
min_year (ex: 2008)

max year (ex: 2010)

station_id

page (defaults to page 1)

limit (defaults to page 500)


ex: 
```
http://0.0.0.0:8080/api/weather/stats?min_year=2000&max_year=2003&station_id=USC00115326
```

### GET .../api/weather
#### optional query parameters: 
min_date (ex: 2000-01-03) 

max_date (ex: 2008-01-03)

station_id ("USC00110072")

page (defaults to page 1)

limit (defaults to page 500)

### GET.../api/yield
#### optional query parameters: 

min_year (ex: 2008)

max year (ex: 2010)




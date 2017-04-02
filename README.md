# Dark Sky Python

Python 3 wrapper for the Dark Sky Weather API. This should provide a lightweight library which is feature-complete with the API.

[Powered by Dark Sky](https://darksky.net/poweredby/)

## Simple Usage
```python
import forecast

API_KEY = "API KEY"
LAT = <LATITUDE>
LON = <LONGITUDE>

f = forecast.Forecast(API_KEY, LAT, LON) # Generates forecast object
```

From here, you can access all the data provided in the response.

Eg.
```python
current = f.currently
print(current.summary)
```

Eg. to get the forecast in 1 hour:
```python
hourly = f.hourly
print(hourly[hourly.starttime + 3600].summary)
```

## TODO
* Improve fetching datapoints from minutely and hourly datablocks
* Write unit tests
* Improve README
* Make into proper package (implement __init__.py)
* Add requirements.txt
* Implement dedicated classes for Alerts and Flags
* Parse headers to provide easy access to more useful information (current way involves manually parsing the header)

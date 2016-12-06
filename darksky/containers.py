#! /usr/bin/python3

# pylint: disable=C0411; Pylint bug trying to order imports incorrectly

from datastore import Datapoint, Datablock
from exceptions import NoDataError
import forecast as f

# TODO: Consider being able to call all the weather objects without having
# to manually create a forecast object first.

class Currently(Datapoint):
    """
    An object to encapsulate the Currently data point.
    Uses a f.Forecast object to instantiate itself.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "currently" not in forecast:
            raise NoDataError("Currently datapoint does not exist.")

        super().__init__(forecast.data.get("currently"))

    # TODO: Define __repr__ and __str__


class Minutely(Datablock):
    """
    An object to encapsulate the Minutely data block.
    Uses a f.Forecast object to instantiate itself.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "minutely" not in forecast:
            raise NoDataError("Minutely datablock does not exist.")

        super().__init__(forecast.data.get("minutely"))

    # TODO: Define __repr__ and __str__

class Hourly(Datablock):
    """
    An object to encapsulate the Hourly data block.
    Uses a f.Forecast object to instantiate itself.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "hourly" not in forecast:
            raise NoDataError("Hourly datablock does not exist.")

        super().__init__(forecast.data.get("hourly"))

    # TODO: Define __repr__ and __str__

class Daily(Datablock):
    """
    An object to encapsulate the Daily data block.
    Uses a f.Forecast object to instantiate itself.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "daily" not in forecast:
            raise NoDataError("Daily datablock does not exist.")

        super().__init__(forecast.data.get("daily"))

    # TODO: Define __repr__ and __str__

class Alerts:
    """
    An object to encapsulate the Alerts object.
    Uses a Forecast object to instantiate itself.
    """
    pass

class Flags:
    """
    An object to encapsulate the Flags object.
    Uses a Forecast object to instantiate itself.
    """
    pass

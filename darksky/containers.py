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

    def __repr__(self):
        return "<Currently data point at time {} with {} attributes>"\
                 .format(str(self.time), len(self.attributes))


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

    def __repr__(self):
        return "<Minutely data block with start time {} and {} datapoints>"\
                 .format(str(self.starttime), len(self))

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

    def __repr__(self):
        return "<Hourly data block with start time {} and {} datapoints>"\
                 .format(str(self.starttime), len(self))

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

    def __repr__(self):
        return "<Daily data block with start time {} and {} datapoints>"\
                 .format(str(self.starttime), len(self))

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

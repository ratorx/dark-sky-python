#! /usr/bin/python3

# pylint: disable=C0411; Pylint bug trying to order imports incorrectly

from .datastore import Datapoint, Datablock
from .exceptions import NoDataError
from . import forecast as f

class Currently(Datapoint):
    """
    Represents the Currently Datapoint in the Forecast response.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "currently" not in forecast:
            raise NoDataError("Currently datapoint does not exist.")

        super().__init__(forecast.data.get("currently"))

    def __repr__(self):
        return "<Currently data point at time {} with {} attributes>" \
                 .format(str(self.time), len(self.attributes))


class Minutely(Datablock):
    """
    Represents the Minutely Datablock in the Forecast response.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "minutely" not in forecast:
            raise NoDataError("Minutely datablock does not exist.")

        super().__init__(forecast.data.get("minutely"))

    def __repr__(self):
        return "<Minutely data block with start time {} and {} datapoints>" \
                 .format(str(self.starttime), len(self))

class Hourly(Datablock):
    """
    Represents the Hourly Datablock in the Forecast response.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object")
        elif "hourly" not in forecast:
            raise NoDataError("Hourly datablock does not exist.")

        super().__init__(forecast.data.get("hourly"))

    def __repr__(self):
        return "<Hourly data block with start time {} and {} datapoints>" \
                 .format(str(self.starttime), len(self))

class Daily(Datablock):
    """
    Represents the Daily Datablock in the Forecast response.
    """
    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object.")
        elif "daily" not in forecast:
            raise NoDataError("Daily datablock does not exist.")

        super().__init__(forecast.data.get("daily"))

    def __repr__(self):
        return "<Daily data block with start time {} and {} datapoints>" \
                 .format(str(self.starttime), len(self))

class Alerts(Datapoint):
    """
    Represents the Alerts object from the Forecast response.

    Refer to https://darksky.net/dev/docs/response under Alerts for
    documentation.
    """

    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object.")
        elif "alerts" not in forecast:
            raise NoDataError("Alerts Array does not exist.")

        super().__init__(forecast.data.get("alerts"))

    def __repr__(self):
        return "<Alerts object for {}>".format(self.title)



class Flags(Datapoint):
    """
    Represents the Flags object from the Forecast response.

    Refer to https://darksky.net/dev/docs/response under Flags for
    documentation.
    """

    def __init__(self, forecast):
        if not isinstance(forecast, f.Forecast):
            raise TypeError("Not a Forecast object.")
        elif "flags" not in forecast:
            raise NoDataError("Flags object does not exist.")

        super().__init__(forecast.data.get("flags"))

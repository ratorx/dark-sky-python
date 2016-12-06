#! /usr/bin/python3
from time import struct_time, mktime

from exceptions import NoDataError

class Datapoint:
    """
    Converts a datapoint dictionary into a usable datapoint

    Guaranteed to contain:
    time - A UNIX time at which the datapoint begins

    Other fields are not guaranteed to exist. Will throw
    AttributeError if field is not found

    Refer to https://darksky.net/dev/docs/response
    under the Data Point Object.

    """

    # Required
    _time = None

    def __init__(self, datapoint):
        if not isinstance(datapoint, dict):
            raise NoDataError("Not a valid data source.")

        try:
            self._time = int(datapoint["time"])
        except (KeyError, TypeError):
            raise NoDataError("Not a valid data source.")

        self.__dict__ = datapoint

    def __getattr__(self, name): # Necessary to avoid pylint errors
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name + "does not exist.")

    @property
    def time(self):
        return self._time

    @property
    def attributes(self):
        return set(self.__dict__.keys())


class Datablock:
    """
    Converts a datablock dictionary into usable data blocks.

    datapoints - A dictionary of Datapoint objects hashed by time
    summary - A human-readable summary of this datablock
    icon - A machine-readable summary of this datablock
    """

    # Required
    _datapoints = None

    # Optional
    _summary = None
    _icon = None


    def __init__(self, datablock):
        if not isinstance(datablock, dict):
            raise NoDataError("Not a valid data source.")

        self._datapoints = dict()
        try:
            for datapoint in datablock["data"]:
                self._datapoints[datapoint["time"]] = Datapoint(datapoint)
        except KeyError:
            raise NoDataError("Not a valid data source.")

        self._summary = datablock.get("summary", "No summary found.")
        self._icon = datablock.get("icon", "none")

    def __iter__(self):
        return iter(self.datapoints)

    @property
    def datapoints(self):
        return self._datapoints

    @property
    def summary(self):
        return self._summary

    @property
    def icon(self):
        return self._icon

    def get_datapoint(self, time):
        """
        Returns the datapoint at a given time

        Arguments:
        time - A struct_time object or an int time measure in seconds
               since the epoch.
        """

        if isinstance(time, struct_time):
            time = mktime(time)
        elif not isinstance(time, int):
            raise TypeError("time must be an int or struct_time object.")

        try:
            return self.datapoints[time]
        except KeyError:
            raise NoDataError("The data for the given time is not available.")

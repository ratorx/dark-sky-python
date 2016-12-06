#! /usr/bin/python3
from time import struct_time, mktime

from exceptions import NoDataError

class Datapoint:
    """
    Wraps a datapoint dictionary into an object

    Guaranteed to contain:
    time - A UNIX time at which the datapoint begins (int)

    Other fields are not guaranteed to exist. Will throw
    AttributeError if field is not found

    Refer to https://darksky.net/dev/docs/response
    under the Data Point Object.

    """

    def __init__(self, datapoint):
        if not isinstance(datapoint, dict):
            raise NoDataError("Not a valid data source.")

        self.__dict__ = datapoint

    def __getattr__(self, name): # Necessary to avoid pylint errors
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name + "does not exist.")

    def __contains__(self, name):
        return name in self.__dict__.keys()

    def __repr__(self):
        return "<Data point with time {} and {} attributes>"\
                 .format(str(self.time), len(self.attributes))

    def __iter__(self):
        return iter(self.__dict__)

    @property
    def attributes(self):
        return set(self.__dict__.keys())

    def items(self):
        return self.__dict__.items()


class Datablock:
    """
    Converts a datablock dictionary into usable data blocks.

    datapoints - A dictionary of Datapoint objects hashed by time (dict)
    summary - A human-readable summary of this datablock (string)
    icon - A machine-readable summary of this datablock (string)
    """

    # Required
    _datapoints = None
    _starttime = None
    _interval = None

    # Optional
    _summary = None
    _icon = None


    def __init__(self, datablock):
        if not isinstance(datablock, dict):
            raise NoDataError("Not a valid data source.")

        self._datapoints = []
        self._starttime = datablock["data"][0]["time"]
        self._interval = datablock["data"][1]["time"] - self.starttime
        try:
            for datapoint in datablock["data"]:
                self._datapoints.append(Datapoint(datapoint))
        except KeyError:
            raise NoDataError("Not a valid data source.")

        self._summary = datablock.get("summary", "No summary found.")
        self._icon = datablock.get("icon", "none")

    def __len__(self):
        return len(self._datapoints)

    def __iter__(self):
        return iter(self._datapoints)

    def __getitem__(self, time):
        """
        Returns the datapoint at a given time. If time is in range of
        the datablock, it will be rounded down to the nearest
        available datapoint.

        Arguments:
        time - A struct_time object or an int time measure in seconds
               since the epoch.
        """

        if isinstance(time, struct_time):
            time = mktime(time)
        elif not isinstance(time, int):
            raise TypeError("time must be an int or struct_time object.")

        index = self.index(time)
        if index < 0 or index >= len(self._datapoints):
            return self._datapoints[index]

    def __contains__(self, time):
        """
        Returns a boolean value which determines if a given time has a
        datapoint. If time is in range of the datablock, it will be
        rounded down to the nearest available datapoint

        Arguments:
        time - A struct_time object or an int time measure in seconds
               since the epoch.
        """

        if isinstance(time, struct_time):
            time = mktime(time)
        elif not isinstance(time, int):
            raise TypeError("time must be an int or struct_time object.")

        return time >= self.starttime and time <= self.endtime

    @property
    def summary(self):
        return self._summary

    @property
    def icon(self):
        return self._icon

    @property
    def starttime(self):
        return self._starttime

    @property
    def endtime(self):
        return self._starttime + self._interval * len(self._datapoints)

    def index(self, time):
        """
        Returns the list index of the weather datapoint with time
        rounded down to the nearest datapoint time.

        Arguments:
        time - int representing seconds since the epoch
        """
        return int((time - self.starttime) / self._interval)

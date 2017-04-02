#! /usr/bin/python3
from time import struct_time, mktime

from exceptions import NoDataError

class Datapoint:
    """
    A generic class to wrap each datapoint in the API response.

    Guaranteed Attribute:
    time - A UNIX time at which the datapoint begins (int)

    Other fields are not guaranteed to exist. Will throw
    AttributeError if field is not found

    Refer to https://darksky.net/dev/docs/response
    under Data Point Object for list of possible attributes.
    """

    def __init__(self, datapoint):
        if not isinstance(datapoint, dict):
            raise NoDataError("Not a valid data source.")

        self.__dict__ = datapoint

    def __getattr__(self, name): # Necessary to avoid pylint errors
        return self.__dict__.get(name)

    def __contains__(self, name):
        return name in self.__dict__.keys()

    def __repr__(self):
        return "<Data point at time {} with {} attributes>" \
                 .format(str(self.time), len(self.attributes))

    def __iter__(self):
        return iter(self.__dict__)

    def attributes(self):
        return set(self.__dict__.keys())

    def items(self):
        return self.__dict__.items()


class Datablock:
    """
    A class to wrap Datablocks from the API response

    Attributes:
    datapoints - A dictionary of Datapoint objects hashed by time (dict)
    summary - A human-readable summary of this datablock (string)
    icon - A machine-readable summary of this datablock (string)
    starttime - The UNIX time that the first Datapoint was recorded (int)
    endtime - The UNIX time that the last Datapoint ends (int)

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
        """
        Returns the number of Datapoints in the Datablock.
        """
        return len(self._datapoints)

    def __iter__(self):
        """
        Returns an iterable over the Datapoints in the Datablock.
        """
        return iter(self._datapoints)

    def __getitem__(self, n):
        """
        Returns the datapoint at a given time. If time is in range of
        the datablock, it will be rounded down to the nearest
        available datapoint.

        Arguments:
        n - Number of intervals from the starttime
        """

        index = self.index(self.starttime + n * self.interval)
        if index < 0 or index >= len(self._datapoints):
            return self._datapoints[index]

    def __contains__(self, time):
        """
        Returns a boolean value which represents whether a given time is
        in range of the Datablock.

        Note: Reason that __getitem__ and __contains__ take different
        arguments is because each simplifies use in its own way. To check
        if a given n is in the block is simple, whereas its more useful
        to check if a given time is in range.

        Arguments:
        time - Query time (struct_time OR int)
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
    def interval(self):
        return self._interval

    @property
    def endtime(self):
        return self._starttime + self._interval * len(self._datapoints)

    def index(self, time):
        """
        Returns the list index of the weather datapoint with time
        rounded down to the nearest datapoint time.

        Arguments:
        time - Query time (int)
        """
        return int((time - self.starttime) / self._interval)

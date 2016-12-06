#! /usr/bin/python3

# pylint: disable=C0411; Pylint bug trying to order imports incorrectly

from datastore import Datapoint, Datablock

class Currently(Datapoint):
    """
    An object to encapsulate the Currently data point
    """
    pass

class Minutely(Datablock):
    """
    An object to encapsulate the Minutely data block
    """
    pass

class Hourly(Datablock):
    """
    An object to encapsulate the Hourly data block
    """
    pass

class Daily(Datablock):
    """
    An object to encapsulate the Daily data block
    """
    pass

class Alerts:
    """
    An object to encapsulate the Alerts object
    """
    pass

class Flags:
    """
    An object to encapsulate the Flags object
    """
    pass

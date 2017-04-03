#! /usr/bin/python3

# pylint: disable=R0913; Required because of optional arguments
# pylint: disable=R0902; Required to maintain all optional arguments
# pylint: disable=C0411; Pylint bug trying to order imports incorrectly

import requests

from . import containers as c
from .exceptions import InvalidParameterError


class Forecast:
    """
    A class to handle the URL generation for the API call and request
    parsing of the API object.

    Required arguments:
    key - API key of user (string)
    lat - Latitude of forecast location (float)
    lng - Longitude of forecast location (float)

    Optional arguments:
    exclude - Containers to exclude from forecast request (list)
    ALLOWED: "currently", "minutely", "hourly", "daily", "alerts", "flags"
    DEFAULT: None

    extend - Containers to provide extended information for (list)
    ALLOWED: "hourly"
    DEFAULT: None

    lang - Language of summaries (string)
    ALLOWED: Visit https://darksky.net/dev/docs/forecast for allowed
             languages
    DEFAULT: "en"

    units - Units of weather data (string)
    ALLOWED: "auto", "ca", "uk2", "us", "si"
    DEFAULT: "auto"

    Data:
    request - Request object from the API response (Request)
    data - Dictionary containing the returned forcast request (dict)
    """

    # Required Variables
    _key = None
    _lat = None
    _lng = None

    # Optional Data Modification Variables
    _exclude = None # Default is None
    ALLOWED_EXCLUDES = frozenset(["currently", "minutely", "hourly", "daily", \
                                 "alerts", "flags"])
    _extend = None # Default is None
    ALLOWED_EXTENDS = frozenset(["hourly"]) # Allows for future API endpoints

    _lang = None # Default is English
    ALLOWED_LANGS = frozenset(["ar", "az", "be", "bs", "ca", "cs", "de", "el",\
                              "en", "es", "et", "fr", "hr", "hu", "id", "it", \
                              "is", "kw", "nb", "nl", "pl", "pt", "ru", "sk", \
                              "sl", "sr", "sv", "tet", "tr", "uk", \
                              "x-pig-latin", "zh", "zh-tw"])

    _units = None # Default is auto
    ALLOWED_UNITS = frozenset(["auto", "ca", "uk2", "us", "si"])

    _request = None # Provided to troubleshoot api issues
    _data = None

    def __init__(self, key, lat, lng, exclude=None, extend=None, lang=None, \
                 units=None):
        # Required Parameters
        self.key = key
        self.lat = lat
        self.lng = lng
        self.exclude = exclude
        self.extend = extend
        self.lang = lang
        self.units = units

        # Get Data JSON object
        self._request = self.get_request()
        self._data = self.request.json()

    def __contains__(self, name):
        """
        Returns a boolean value which represents whether the returned
        object contains the named container

        Arguments:
        name - The name of the container to check for
        ALLOWED: "currently", "minutely", "hourly", "daily", "alerts",
                 "flags"
        """
        if name not in self.ALLOWED_EXCLUDES or name not in self.data.keys():
            return False
        else:
            return True

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = str(value)

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, lat):
        self._lat = float(lat)

    @property
    def lng(self):
        return self._lng

    @lng.setter
    def lng(self, lng):
        self._lng = float(lng)

    @property
    def exclude(self):
        return self._exclude

    @exclude.setter
    def exclude(self, exclude):
        if exclude is None:
            pass
        elif set(exclude).issubset(self.ALLOWED_EXCLUDES):
            self._exclude = exclude
        else:
            raise InvalidParameterError(str(set(exclude)-self.ALLOWED_EXCLUDES)
                                        + " are not supported by exclude")

    @property
    def extend(self):
        return self._extend

    @extend.setter
    def extend(self, extend):
        if extend is None:
            pass
        elif set(extend).issubset(self.ALLOWED_EXTENDS):
            self._extend = extend
        else:
            raise InvalidParameterError(str(set(extend)-self.ALLOWED_EXTENDS)
                                        + " are not supported by extend")

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        if lang is None:
            self._lang = "en"
        elif lang in self.ALLOWED_LANGS:
            self._lang = lang
        else:
            raise InvalidParameterError(str(lang) + " is not an API language")

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        if units is None:
            self._units = "auto"
        elif units in self.ALLOWED_UNITS:
            self._units = units
        else:
            raise InvalidParameterError(str(units)+" are not supported units.")

    @property
    def data(self):
        return self._data

    @property
    def request(self):
        return self._request

    @property
    def timezone(self):
        """
        Get timezone from JSON object.
        """
        return self.data.get("timezone")

    @property
    def currently(self):
        """
        Returns the Currently object for this forecast.
        """
        return c.Currently(self)

    @property
    def minutely(self):
        """
        Returns the Minutely object for this forecast.
        """
        return c.Minutely(self)

    @property
    def hourly(self):
        """
        Returns the Hourly object for this forecast.
        """
        return c.Hourly(self)

    @property
    def daily(self):
        """
        Returns the Daily object for this forecast.
        """
        return c.Daily(self)

    @property
    def alerts(self):
        """
        Returns the Alerts object for this forecast.
        """
        return c.Alerts(self)

    @property
    def flags(self):
        """
        Returns the Flags object for this forecast.
        """
        return c.Flags(self)

    def get_url(self):
        """
        Generates the URL from the instance.
        """
        url = "https://api.darksky.net/forecast/{}/{},{}?lang={}&units={}"\
                .format(str(self.key),
                        str(self.lat),
                        str(self.lng),
                        self.lang,
                        self.units)
        addons = ""
        if self.exclude is not None:
            addons += "&exclude=" + ",".join(self.exclude)
        if self.extend is not None:
            addons += "&extend=" + ",".join(self.extend)

        return url + addons

    def get_request(self):
        """
        Returns the JSON forcecast request as a Request object.
        """
        url = self.get_url()
        r = requests.get(url)
        r.raise_for_status()
        return r

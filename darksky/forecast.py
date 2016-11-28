#! /usr/bin/python3

# pylint: disable=R0913; Required because of optional arguments
# pylint: disable=R0902; Required to maintain all optional arguments
# pylint: disable=C0411; Pylint bug trying to order imports incorrectly

import requests

from exceptions import InvalidParameterError


class Forecast:
    """
    This handles the API calls and url-building required to fetch a
    weather forcast. The resulting object can be passed into any of datablocks
    or datapoints in order to instantiate it.
    """

    # Required Variables
    key = None
    lat = None
    lng = None

    # Optional Data Modification Variables
    exclude = None # Default is None
    ALLOWED_EXCLUDES = frozenset(["currently", "minutely", "hourly", "daily", \
                                 "alerts", "flags"])
    extend = None # Default is None
    ALLOWED_EXTENDS = frozenset(["hourly"]) # Allows for future API endpoints

    lang = None # Default is English
    ALLOWED_LANGS = frozenset(["ar", "az", "be", "bs", "ca", "cs", "de", "el", \
                              "en", "es", "et", "fr", "hr", "hu", "id", "it", \
                              "is", "kw", "nb", "nl", "pl", "pt", "ru", "sk", \
                              "sl", "sr", "sv", "tet", "tr", "uk", \
                              "x-pig-latin", "zh", "zh-tw"])

    units = None # Default is auto
    ALLOWED_UNITS = frozenset(["auto", "ca", "uk2", "us", "si"])

    data = None

    def __init__(self, key, lat, lng, exclude=None, extend=None, lang=None, \
                 units=None):
        # Required Parameters
        self.key = str(key)
        self.lat = float(lat)
        self.lng = float(lng)

        # Optional
        if exclude is None:
            pass
        elif set(exclude).issubset(self.ALLOWED_EXCLUDES):
            self.exclude = exclude
        else:
            raise InvalidParameterError(str(set(exclude) - self.ALLOWED_EXCLUDES) + \
                                        " are not supported by exclude")

        if extend is None:
            pass
        elif set(extend).issubset(self.ALLOWED_EXTENDS):
            self.extend = extend
        else:
            raise InvalidParameterError(str(set(extend) - self.ALLOWED_EXTENDS) + \
                                        " are not supported by extend")

        if lang is None:
            self.lang = "en"
        elif lang in self.ALLOWED_LANGS:
            self.lang = lang
        else:
            raise InvalidParameterError(str(lang) + " is not an API language")

        if units is None:
            self.units = "auto"
        elif units in self.ALLOWED_UNITS:
            self.units = units
        else:
            raise InvalidParameterError(str(units) + " is not an API language")

        # Get Data JSON object
        self.data = self.get_json()

    def get_url(self):
        """
        Uses the state of the object to build the API request URL
        """
        url_base = "https://api.darksky.net/forecast/{}/{},{}" \
                        .format(str(self.key), str(self.lat), str(self.lng))
        addons = "?lang={}&units={}".format(self.lang, self.units)

        if self.exclude is not None:
            addons += "&exclude=" + ",".join(self.exclude)
        if self.extend is not None:
            addons += "&extend=" + ",".join(self.extend)

        return url_base + addons

    def get_json(self):
        """
        Returns the JSON forcecast
        """
        url = self.get_url()
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def has_currently(self):
        """
        Checks if the request returned Currently data
        """
        return self.data.get("currently") is not None

    def has_minutely(self):
        """
        Checks if the request returned Minutely data
        """
        return self.data.get("minutely") is not None

    def has_hourly(self):
        """
        Checks if the request returned Hourly data
        """
        return self.data.get("hourly") is not None

    def has_alerts(self):
        """
        Checks if the request returned any Alerts
        """
        return self.data.get("alerts") is not None

    def has_flags(self):
        """
        Checks if the request returned any Flags
        """
        return self.data.get("flags") is not None

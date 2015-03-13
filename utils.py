__author__ = 'atrament'
__all__ = ['is_iso_date', 'mkdatetime', "is_iso_time", "mktimedelta"]

import re as _re
import datetime as _datetime
from config import DATETIME_PATTERN as _DATETIME_PATTERN


def is_iso_date(d):
    """:returns True if d is a string representing an iso date or datetime, False otherwise"""
    if not isinstance(d, str):  # can't regex on non-string elements
        return False
    return bool(_re.match(_DATETIME_PATTERN, d))


def is_iso_time(d, fetch=False):
    if not isinstance(d, str):  # can't regex on non-string elements
        return False
    match = _re.findall("\d{1,2}:\d{2}(?::\d{2})*(?:.\d{1,6})*", d)
    if fetch and bool(match):
        return match[0]
    return bool(match)


def mkdatetime(iso):
    """makes a datetime object from given string
    :returns datetime.datetime object"""
    if not isinstance(iso, str):
        raise TypeError("Argument for mkdatetime must be a string.")
    if not is_iso_date(iso):
        raise ValueError("Argument for mkdatetime must be iso datetime format")
    return _datetime.datetime(*map(int, _re.findall("\d+", iso)))


def mktimedelta(iso):
    if not isinstance(iso, str):
        raise TypeError("Argument for mktimedelta must be a string.")
    if not is_iso_time(iso):
        raise ValueError("Argument for mktimedelta must be iso datetime or time format")
    time = is_iso_time(iso, fetch=True)
    time = list(map(int, _re.findall("\d+", time)))
    args = dict(zip("hours minutes seconds microseconds".split(),
                    time))
    return _datetime.timedelta(**args)

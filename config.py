__author__ = 'atrament'

import re as _re


DEFAULT_TASKS_CHARACTERISTICS = dict(map(lambda i: (i, None), "duration,due,progress,title,label".split(',')))

HOURS_PER_DAY = 7
DAYSTART = 8  # number of hours efore the start of the day (if you work from 8:00, enter 8)

DATETIME_PATTERN = _re.compile("^\d{4}-\d{2}-\d{2}(T[0-2]\d:[0-5]\d(:[0-5]\d|$)|$)")

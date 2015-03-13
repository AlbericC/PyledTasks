from utils import is_iso_time, mktimedelta

__author__ = 'atrament'
__all__ = ['Task']

from utils import *
from config import DEFAULT_TASKS_CHARACTERISTICS as _DEFAULT_TASKS_CHARACTERISTICS, HOURS_PER_DAY, DAYSTART
import datetime


class Task():
    def __init__(self, **kwargs):
        """Make a new task.

        Tasks definitions may be incomplete and are defined with keywords.
        default keywords and values are :

        {'due': None,
         'duration': None,
         'label': None,
         'progress': None,
         'title': None}

        :param kwargs: known characteristics of the task.
        They will be set to self.characteristics in the form key=value for each kwarg
        """
        self._defined = dict(_DEFAULT_TASKS_CHARACTERISTICS)
        self._defined.update(kwargs)
        self.clean_dates()
        self._parent = None

    def clean_dates(self):
        for k, v in self._defined.items():
            if is_iso_date(v):
                self._defined[k] = mkdatetime(v)
            elif is_iso_time(v):
                self._defined[k] = mktimedelta(v)

    def subtask(self, other, delete=False):
        """add other as a sub task of self.
        if delete==True, removes task from subtasks."""
        if not isinstance(other, self.__class__):
            raise TypeError("Must nest tasks only")
        if self._defined.get("subtasks") is None:
            self._defined["subtasks"] = []
        if delete:
            if other.parent is self:
                del other.parent  # make subtask forget parent if needed
                # forget subtask
                self._defined["subtasks"].remove(other)
        else:
            # make subtask forget previous parent
            del other.parent
            # make subtask register self as parent
            other.parent = self
            # register other as subtask
            self._defined["subtasks"].append(other)

    @property
    def timeleft(self):
        if not isinstance(self.due, datetime.datetime):
            return None
        else:
            return self.due - datetime.datetime.now()

    def workdaysleft(self):
        """returns working time available to complete task on time
        :returns dict {'remaining': datetime.timedelta, 'days': int} or None if no due date is set"""

        one_day = datetime.timedelta(hours=HOURS_PER_DAY)
        fulldays = self.timeleft//one_day
        remains = self.timeleft-fulldays*one_day
        return {"days": fulldays, "remaining": remains}

    def earlyend(self):
        """returns earliest possible datetime of completion or None if no duration is set.
        """
        if not self.duration:
            return None
        progress = self.progress if self.progress else 0
        remainingwork = self.duration*(1-progress)
        one_day = datetime.timedelta(hours=HOURS_PER_DAY)
        days, remains = remainingwork // one_day, remainingwork % one_day
        # noinspection PyUnresolvedReferences
        return datetime.datetime.now() + datetime.timedelta(days, remains.seconds, hours=DAYSTART)

    def _unparent(self):
        if self._parent:
            # make parent unregister self as parent
            self._parent.subtask(self, delete=True)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        former = self.parent
        self._parent = value
        if former:
            former.subtask(self, delete=True)  # old parent forgets.

    @parent.deleter
    def parent(self):
        self.parent = None

    @property
    def characteristic(self):
        return self._defined

    def set(self, attribute, value):
        """set a domain-specific aspect of the task, such as duration, due, progress..."""
        if not isinstance(attribute, str):
            raise TypeError("attributes must be designated by string label, recieved %s" % attribute)
        self._defined[attribute] = value

    def __getattr__(self, item):
        # if attribute not in instance __dict__, finds it in _defined characts
        if any(is_iso_date(d) for d in self._defined.values()):
            self.clean_dates()
        return self._defined.get(item, None)

#! /usr/bin/python3

import datetime
from task import Task
from sys import argv

__author__ = 'atrament'

"""Main PyledTasks executable"""


if __name__ == '__main__':
    """main app"""
    keywords = "show add"
    if any(w in "-h --help help".split() for w in argv) or not any(w in keywords for w in argv):
        print("""
PyledTasks: A simple task management system for PhD students and researchers

usage: pyledtasks [options] [actions]

actions available:
help          - display this help message and quit
list          - display a list of tasks and quit
show T        - display details on task T, where T is a number.
                (can be found with 'list')
progress T N  - update progress of T to N%, N being from 0 to 100
add [args]    - enter a task creation interface
                if args are given, they apply to the new task instead
                (see characteristics)
                if the "=" sign is not used, the order of arguments is:
                    due,duration,label
set T args    - change the characteristics of a task
watch T files - associate a watcher to the files stated: using this file will
                increment time spent on the task. This allows for statistical
                processing and progress estimation (but does not update
                progress by itself)

characteristics of tasks:
                due         - due date to which the task must be completed
                title       - name of the task
                label       - description of the task
                duration    - estimate in hours:minutes[:seconds] of the work
                              time needed to complete the task
                parent      - id # of the parent task to the one created

options:
-h
--help          display this help message and quit
-w              use the watch deamon

examples:

pyledtasks add title=Thesis due=2019-03-31 duration=1500:00 label="Write it !"
pyledtasks add 2019-03-31 1500:00 Write the thesis essay
pyledtasks set 5 due 2019-06-25
""")
    # load tasks from file
        # make empty file if needed
    # prompt tasks
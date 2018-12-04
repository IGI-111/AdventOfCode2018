#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
import re
from datetime import datetime

class Event:
    SHIFT = 1
    SLEEP = 2
    WAKE = 3

    def __init__(self, line):
        m = re.search("\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.*)", line)
        self.date = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M')
        message = m.group(2)

        if message == "wakes up":
            self.type = Event.WAKE
        elif message == "falls asleep":
            self.type = Event.SLEEP
        else:
            m = re.search("Guard #(\d+) begins shift", message)
            self.type = Event.SHIFT
            self.guard = int(m.group(1))


with open("4.txt") as file:
    events = sorted([Event(line) for line in file], key=lambda e: e.date)

    guard_tally = {}
    current_guard = None
    last_asleep = None
    for event in events:
        if event.type == Event.SHIFT:
            current_guard = event.guard
            if event.guard not in guard_tally:
                guard_tally[event.guard] = [0] * 60
        elif event.type == Event.SLEEP:
            last_asleep = event.date
        elif event.type == Event.WAKE:
            for i in range(last_asleep.minute, event.date.minute):
                guard_tally[current_guard][i] += 1
            last_asleep = None

    best_guard = None
    best_guard_total = None
    best_minute = None
    for (guard, minutes) in guard_tally.items():
        if best_guard_total == None or sum(minutes) > best_guard_total:
            best_guard = guard
            best_guard_total = sum(minutes)
            best_minute = minutes.index(max(minutes))
    print(best_guard * best_minute)

    best_guard = None
    best_minute = None
    best_minute_total = None
    for (guard, minutes) in guard_tally.items():
        if best_minute_total == None or max(minutes) > best_minute_total:
            best_guard = guard
            best_minute_total = max(minutes)
            best_minute = minutes.index(max(minutes))
    print(best_guard * best_minute)


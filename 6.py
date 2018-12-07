#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from functools import reduce
import time


class Graph:
    def __init__(self, file):
        self.before = {}
        self.after = {}

        for line in file:
            m = re.search(
                "Step (\w+) must be finished before step (\w+) can begin.", line
            )
            # a => b
            a = m.group(1)
            b = m.group(2)

            if not a in self.before:
                self.before[a] = set()
            if not a in self.after:
                self.after[a] = set()
            if not b in self.before:
                self.before[b] = set()
            if not b in self.after:
                self.after[b] = set()

            self.before[b].add(a)
            self.after[a].add(b)

    def entry_points(self):
        return {p for p in self.before if len(self.before[p]) == 0}


def time_value(quantum, val):
    return 1 + quantum + ord(val) - ord("A")


with open("6.txt") as file:
    graph = Graph(file)
    done = []
    available = sorted(graph.entry_points())

    while len(available) > 0:
        execute = next(a for a in available if graph.before[a].issubset(done))
        done.append(execute)
        available.remove(execute)

        available = sorted(graph.after[execute].difference(done).union(available))

    print("".join(done))

    quantum = 60
    worker_count = 5

    done = []
    available = sorted(graph.entry_points())
    current_task = [None] * worker_count
    time_left = [0] * worker_count

    chrono = 0
    while len(available) > 0 or any(t != None for t in current_task):
        for i in range(0, worker_count):
            if time_left[i] == 0 and current_task[i] != None:
                done.append(current_task[i])
                available = sorted(
                    graph.after[current_task[i]].difference(done).union(available)
                )
                current_task[i] = None

            if current_task[i] == None:
                try:
                    current_task[i] = next(
                        a for a in available if graph.before[a].issubset(done)
                    )
                    available.remove(current_task[i])
                    time_left[i] = time_value(quantum, current_task[i])
                except StopIteration:
                    continue

            time_left[i] -= 1
        chrono += 1

    print(chrono - 1)

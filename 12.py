#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import deque


class Automaton:
    def __init__(self, file):
        m = re.search("initial state: ([#\\.]*)", next(file))
        state_str = m.group(1)
        self.state = [c == "#" for c in iter(state_str)]
        self.origin = 0
        next(file)
        self.rules = {}
        for line in file:
            m = re.search("([#\\.]*) => ([#\\.])", line)
            pattern = tuple([c == "#" for c in iter(m.group(1))])
            output = m.group(2) == "#"
            self.rules[pattern] = output

        self.speed = 0
        self.history = deque([None, None])

    def tick_one(self):
        self.history.popleft()
        self.history.append(self.state)

        oldorigin = self.origin

        buffer_size = 3
        self.origin += buffer_size
        self.state = [False] * buffer_size + self.state + [False]* buffer_size

        next_state = [False] * len(self.state)
        for i in range(0, len(next_state)):
            pattern = tuple(self.state[i - 2 : i + 3])
            next_state[i] = self.rules[pattern] if pattern in self.rules else False
        self.state = next_state

        while not self.state[buffer_size]:
            self.state.pop(0)
            self.origin -= 1
        while not self.state[-buffer_size-1]:
            self.state.pop()

        self.speed = self.origin - oldorigin

    def tick(self, n):
        for i in range(0, n):
            print(i)
            print(self)
            print(self.history[0] == self.history[1])
            print("origin", self.origin)
            print("speed", self.speed)
            if self.history[0] != None and self.history[0] == self.history[1]:
                    self.origin += (n - i) * self.speed
                    break
            self.tick_one()

    def __repr__(self):
        return "".join(["#" if c else "." for c in self.state])

    def count_pot_indices(self):
        res = 0
        for i in range(0, len(self.state)):
            if self.state[i]:
                res += i - self.origin
        return res


with open("12.txt") as file:
    automaton = Automaton(iter(file))
    automaton.tick(20)

    print(automaton.count_pot_indices())

with open("12.txt") as file:
    automaton = Automaton(iter(file))
    automaton.tick(50000000000)
    print(automaton.count_pot_indices())

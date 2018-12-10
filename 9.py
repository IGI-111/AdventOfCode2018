#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import deque

class Marble:
    def __init__(self, val, before, after):
        self.val = val
        self.before = before
        self.after = after

    @staticmethod
    def initial_marble():
        m = Marble(0, None, None)
        m.before = m
        m.after = m
        return m

    def insert_after(self, val):
        after = self.after
        new = Marble(val, self, after)
        self.after = new
        after.before = new

    def remove_before(self):
        before = self.before
        before_before = self.before.before

        self.before = before_before
        before_before.after = self
        del before


def parse_line(line):
    m = re.search("(\d+) players; last marble is worth (\d+) points", line)
    return (int(m.group(1)), int(m.group(2)))

def run_game(player_count, last_marble):
    scores = [0] * player_count
    current_marble = Marble.initial_marble()
    current_player = 0

    for i in range(1, last_marble + 1):
        if i % 23 == 0:
            for _ in range(0, 6):
                current_marble = current_marble.before
            scores[current_player] += i + current_marble.before.val
            current_marble.remove_before()
        else:
            current_marble = current_marble.after
            current_marble.insert_after(i)
            current_marble = current_marble.after

        current_player = (current_player + 1) % player_count
    return scores


with open("9.txt") as file:
    for line in file:
        (player_count, last_marble) = parse_line(line)
        print(max(run_game(player_count, last_marble)))
        print(max(run_game(player_count, 100*last_marble)))


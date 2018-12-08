#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

PATTERNS = [unit + unit.upper() for unit in string.ascii_lowercase] + [
    unit.upper() + unit for unit in string.ascii_lowercase
]


def react(polymer):
    prev = None
    while prev == None or prev != len(polymer):
        prev = len(polymer)
        for pattern in PATTERNS:
            polymer = polymer.replace(pattern, "")
    return polymer


with open("5.txt") as file:
    for polymer in file:
        polymer = polymer.strip()

        print(len(react(polymer)))

        shortest = None
        for unit in string.ascii_lowercase:
            without = polymer.translate({ord(i): None for i in unit + unit.upper()})
            l = len(react(without))
            if shortest == None or l < shortest:
                shortest = l
        print(shortest)

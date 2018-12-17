#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def parse_file(file):
    coords = set()
    for match in re.finditer("([xy])=(\d+), [xy]=(\d+)..(\d+)", file.read()):
        if match.group(1) == "x":
            x = int(match.group(2))
            for y in range(int(match.group(3)), int(match.group(4)) + 1):
                coords.add((x, y))
        else:
            y = int(match.group(2))
            for x in range(int(match.group(3)), int(match.group(4)) + 1):
                coords.add((x, y))
    return coords

class Field:
    def __init__(self, solid_coordinates):
        min_x = min(c[0] for c in solid_coordinates)
        max_x = max(c[0] for c in solid_coordinates)
        min_y = min(c[1] for c in solid_coordinates)
        max_y = max(c[1] for c in solid_coordinates)
        print(solid_coordinates)

        self.width = max_x - min_x + 3
        self.height = max_y - min_y + 1
        self.field = ['.'] * self.width * self.height

        for c in solid_coordinates:
            print(c,(c[0]-min_x+1), (c[1] - min_y) , (c[0]-min_x+1) + (c[1] - min_y-1) * self.width)
            self.field[(c[0]-min_x+1) + (c[1] - min_y) * self.width] = '#'

        self.source = 500 - min_x+1

    def __repr__(self):
        res = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x + y * self.width
                res += self.field[pos]
            res += "\n"
        return res

    def drop(self):
        current = self.source
        blocked_right = False
        blocked_left = False
        while not (blocked_left and blocked_right):
            self.field[current] = '|'

            if current + self.width >= len(self.field):
                return

            if self.field[current + self.width] in "|.":
                current += self.width
                blocked_right = False
                blocked_left = False
            elif not blocked_left and self.field[current -1] in "|.":
                current -= 1
            elif not blocked_right and self.field[current +1] in "|.":
                current += 1

            if self.field[current -1] not in "|.":
                blocked_left = True
            if self.field[current +1] not in "|.":
                blocked_right = True
        self.field[current] = '~'


field = Field(parse_file(open("17.txt")))
print(field)
while True:
    input()
    field.drop()
    print(field)


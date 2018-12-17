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

        self.width = max_x - min_x + 3
        self.height = max_y - min_y + 1
        self.field = ["."] * self.width * self.height

        for c in solid_coordinates:
            self.field[(c[0] - min_x + 1) + (c[1] - min_y) * self.width] = "#"

        self.source = 500 - min_x + 1

    def __repr__(self):
        res = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x + y * self.width
                res += self.field[pos]
            res += "\n"
        return res

    def drop(self, origin):
        drops = [origin]

        while len(drops) > 0:
            drop = drops.pop()

            # drop down
            while (
                drop + self.width < len(self.field)
                and self.field[drop + self.width] in "|."
            ):
                self.field[drop] = "|"
                drop += self.width

            # outside
            if drop + self.width >= len(self.field):
                self.field[drop] = "|"
                continue

            filling = True
            while filling:
                right = drop
                while (
                    self.field[right + 1] in "|."
                    and self.field[right + 1 + self.width] not in "|."
                ):
                    right += 1
                right_open = self.field[right + 1] in "|."

                left = drop
                while (
                    self.field[left - 1] in "|."
                    and self.field[left - 1 + self.width] not in "|."
                ):
                    left -= 1
                left_open = self.field[left - 1] in "|."

                if not (right_open or left_open):
                    for i in range(left, right + 1):
                        self.field[i] = "~"
                    drop -= self.width
                else:
                    filling = False
                    for i in range(left, right + 1):
                        self.field[i] = "|"
                    if right_open:
                        drops.append(right + 1)
                    if left_open:
                        drops.append(left - 1)

    def wet_count(self):
        return len([x for x in self.field if x in "|~"])

    def still_count(self):
        return len([x for x in self.field if x in "~"])

field = Field(parse_file(open("17.txt")))
field.drop(field.source)
print(field.wet_count())
print(field.still_count())

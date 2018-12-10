#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Point:
    def __init__(self, line):
        m = re.search(
            "position=<\s*(-?\d+)\s*,\s*(-?\d+)\s*> velocity=<\s*(-?\d+)\s*,\s*(-?\d+)\s*>",
            line,
        )
        self.x = int(m.group(1))
        self.y = int(m.group(2))
        self.dx = int(m.group(3))
        self.dy = int(m.group(4))

    def tick(self):
        self.x += self.dx
        self.y += self.dy


class Grid:
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        min_x = min(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_x = max(p.x for p in self.points)
        max_y = max(p.y for p in self.points)

        width = max_x + 1 - min_x
        height = max_y + 1 - min_y

        field = [" "] * width * height
        for p in self.points:
            field[(p.x - min_x) + (p.y - min_y) * width] = "#"
        field = "".join(field)

        chunks, chunk_size = len(field), len(field) // height
        lines = [field[i : i + chunk_size] for i in range(0, chunks, chunk_size)]
        return "\n".join(lines)

    def height(self):
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)
        return max_y + 1 - min_y

    def tick(self):
        for p in self.points:
            p.tick()


with open("10.txt") as file:
    time = 0
    grid = Grid([Point(line) for line in file])
    while grid.height() > 10:
        grid.tick()
        time +=1
    print(grid)
    print(time)

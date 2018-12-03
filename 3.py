#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Fabric:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [0] * width * height

    def cut_one(self, x, y):
        self.field[y * self.width + x] += 1

    def overlap_surf(self):
        total = 0
        for s in self.field:
            if s > 1:
                total += 1
        return total


class Cut:
    def __init__(self, line):
        m = re.search("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
        self.id = int(m.group(1))
        self.left = int(m.group(2))
        self.top = int(m.group(3))
        self.width = int(m.group(4))
        self.height = int(m.group(5))

    def cut(self, fabric):
        for x in range(self.left, self.left + self.width):
            for y in range(self.top, self.top + self.height):
                fabric.cut_one(x, y)

    def has_overlap(self, cut):
        return (
            self.left < cut.left + cut.width
            and self.left + self.width > cut.left
            and self.top < cut.top + cut.height
            and self.top + self.height > cut.top
        )


with open("3.txt") as file:
    fabric = Fabric(1000, 1000)
    for line in file:
        c = Cut(line)
        c.cut(fabric)
    print(fabric.overlap_surf())

with open("3.txt") as file:
    cuts = [Cut(line) for line in file]
    for cut in cuts:
        if not any(cut.has_overlap(c) and cut.id != c.id for c in cuts):
            print(cut.id)
            break

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Fabric:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [0] * width * height

    def cut(self, cut):
        for x in range(cut.left, cut.right):
            for y in range(cut.top, cut.bottom):
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
        width = int(m.group(4))
        height = int(m.group(5))
        self.bottom = self.top + height
        self.right = self.left + width

    def overlaps(self, cut):
        return (
            self.left < cut.right
            and self.right > cut.left
            and self.top < cut.bottom
            and self.bottom > cut.top
        )

    def __equals__(self, cut):
        return self.id == cut.id


with open("3.txt") as file:
    fabric = Fabric(1000, 1000)
    for line in file:
        fabric.cut(Cut(line))
    print(fabric.overlap_surf())

with open("3.txt") as file:
    cuts = [Cut(line) for line in file]
    for cut in cuts:
        if not any(cut.overlaps(c) and cut != c for c in cuts):
            print(cut.id)
            break

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class Field:
    def __init__(self, file):
        self.width = len(next(file)) - 1
        file.seek(0)
        self.height = sum(1 for line in file)
        file.seek(0)

        self.field = ["."] * self.width * self.height
        i = 0
        for line in file:
            for c in iter(line.strip("\n")):
                if c in set("#.|"):
                    self.field[i] = c
                else:
                    print("Invalid character: {}".format(c))
                    quit()
                i += 1
        self.seen = {}

    def __repr__(self):
        res = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x + y * self.width
                res += self.field[pos]
            res += "\n"
        return res

    def tick_one(self):
        if tuple(self.field) in self.seen:
            self.field = self.seen[tuple(self.field)]
            return

        next_field = self.field.copy()
        for i in range(0, len(self.field)):
            if self.field[i] == '.' and self.adj(i).count('|') >= 3:
                next_field[i] = '|'
            elif self.field[i] == '|' and self.adj(i).count('#') >= 3:
                next_field[i] = '#'
            elif self.field[i] == '#' and not (self.adj(i).count('#') >= 1 and self.adj(i).count('|') >= 1):
                next_field[i] = '.'

        self.seen[tuple(self.field)] = next_field
        self.field = next_field
    def tick(self, n):
        for i in range(0, n):
            if tuple(self.field) in self.seen:
                # build cycle
                cycle = [ tuple(self.field) ]
                cur = tuple(self.seen[tuple(self.field)])
                while cur != cycle[0]:
                    cycle.append(cur)
                    cur = tuple(self.seen[cur])

                remaining = n-i-1
                self.field = self.seen[cycle[remaining % len(cycle)]]
                return
            self.tick_one()



    def adj(self, pos):
        x = pos % self.width
        y = math.floor(pos/self.width)

        res = []
        if y >= 1 and x >= 1:
            res.append(self.field[x-1 + (y-1) * self.width])
        if y >= 1:
            res.append(self.field[x + (y-1) * self.width])
        if y >= 1 and x < self.width-1:
            res.append(self.field[x+1 + (y-1) * self.width])
        if x >= 1:
            res.append(self.field[x-1 + (y) * self.width])
        if x < self.width-1:
            res.append(self.field[x+1 + (y) * self.width])
        if y < self.height-1 and x >= 1:
            res.append(self.field[x-1 + (y+1) * self.width])
        if y < self.height-1:
            res.append(self.field[x + (y+1) * self.width])
        if y < self.height-1 and x < self.width-1:
            res.append(self.field[x+1 + (y+1) * self.width])
        return res


field = Field(open("18.txt"))
field.tick(10)
print(field.field.count('|') * field.field.count('#'))

field = Field(open("18.txt"))
field.tick(1000000000)
print(field.field.count('|') * field.field.count('#'))

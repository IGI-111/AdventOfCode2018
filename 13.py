#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import floor

class Track:
    def __init__(self, file, raise_collisions=True):
        self.raise_collisions = raise_collisions
        self.track = []
        self.carts = []

        self.width = len(next(file)) - 1
        file.seek(0)
        self.height = sum(1 for line in file)
        file.seek(0)

        i = 0
        for line in file:
            for c in iter(line.strip("\n")):
                if c in set("-|/\\ +"):
                    self.track.append(c)
                elif c in set("<>"):
                    self.carts.append(Cart(c, i))
                    self.track.append("-")
                elif c in set("^v"):
                    self.carts.append(Cart(c, i))
                    self.track.append("|")
                else:
                    print("Invalid character: {}".format(c))
                    quit()
                i += 1

    def __repr__(self):
        res = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x + y * self.width
                carts = [c for c in self.carts if c.pos == pos]
                if len(carts) > 0:
                    res += carts[0].direction
                else:
                    res += self.track[pos]
            res += "\n"
        return res

    def tick(self):
        self.carts.sort(key=lambda x: x.pos)
        to_destroy = []
        for c in self.carts:
            c.advance(self.track, self.width, self.carts)
            for other in self.carts:
                if c != other and c.pos == other.pos:
                    if self.raise_collisions:
                        raise Collision(c.pos)
                    else:
                        to_destroy.append(c)
                        to_destroy.append(other)
        for c in to_destroy:
            self.carts.pop(self.carts.index(c))

    def collisions(self):
        res = set()
        for c in self.carts:
            for other in self.carts:
                if other != c and other.pos == c.pos:
                    res.add(c.pos)
        return res

class Collision(BaseException):
    def __init__(self, pos):
        self.pos = pos

class Cart:
    def __init__(self, direction, pos):
        self.direction = direction
        self.pos = pos
        self.next_turn = "left"

    def advance(self, track, width, carts):
        increments = {"<": -1, ">": 1, "^": -width, "v": width}
        incr = increments[self.direction]
        next_pos = self.pos + incr

        if track[next_pos] == "\\":
            turns = {">": "v", "<": "^", "^": "<", "v": ">"}
            self.direction = turns[self.direction]
        elif track[next_pos] == "/":
            turns = {">": "^", "<": "v", "^": ">", "v": "<"}
            self.direction = turns[self.direction]
        elif track[next_pos] == "+":
            self.turn()

        self.pos = next_pos


    def turn(self):
        turn_directions = {
            "left": {">": "^", "<": "v", "^": "<", "v": ">"},
            "straight": {">": ">", "<": "<", "^": "^", "v": "v"},
            "right": {">": "v", "<": "^", "^": ">", "v": "<"},
        }

        self.direction = turn_directions[self.next_turn][self.direction]

        turn_sequence = {"left": "straight", "straight": "right", "right": "left"}
        self.next_turn = turn_sequence[self.next_turn]


with open("13.txt") as file:
    track = Track(file)
    try:
        while True:
            track.tick()
    except Collision as c:
        print("{},{}".format(c.pos % track.width, floor(c.pos / track.width)))
with open("13.txt") as file:
    track = Track(file, False)
    while len(track.carts) > 1:
        track.tick()

    last_cart = track.carts[0]
    print("{},{}".format(last_cart.pos % track.width, floor(last_cart.pos / track.width)))

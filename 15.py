#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import itertools


class Field:
    def __init__(self, file, elf_power=3):
        self.width = len(next(file)) - 1
        file.seek(0)
        self.height = sum(1 for line in file)
        file.seek(0)

        self.field = ["."] * self.width * self.height
        self.hp = {}
        self.ap = {}
        self.rounds = 0

        i = 0
        for line in file:
            for c in iter(line.strip("\n")):
                if c in set("#."):
                    self.field[i] = c
                elif c == "G":
                    self.field[i] = c
                    self.hp[i] = 200
                    self.ap[i] = 3
                elif c == "E":
                    self.field[i] = c
                    self.hp[i] = 200
                    self.ap[i] = elf_power
                else:
                    print("Invalid character: {}".format(c))
                    quit()
                i += 1

    def shortest_path(self, start, goal):
        distances = {n: 1 for n in self.neighbors(goal) if self.passable_terrain(n)}
        distances[goal] = 0
        closed_set = {goal}
        open_set = {n for n in self.neighbors(goal) if self.passable_terrain(n)}
        while len(open_set) > 0:
            current_generation = open_set
            open_set = set()
            for current in current_generation:
                closed_set.add(current)

                for neighbor in self.neighbors(current):
                    if neighbor not in closed_set and self.passable_terrain(neighbor):
                        distances[neighbor] = distances[current] + 1
                        open_set.add(neighbor)
        steps = []
        current = start
        while current != goal:
            possible_steps = [
                n
                for n in self.neighbors(current)
                if self.passable_terrain(n) and n in distances
            ]
            if len(possible_steps) == 0:
                return None
            best_distance = min([distances[x] for x in possible_steps])
            best_steps = [s for s in possible_steps if distances[s] == best_distance]
            chosen = min(best_steps)
            steps.append(chosen)
            current = chosen

        return steps

    def passable_terrain(self, pos):
        return self.field[pos] == "."

    def neighbors(self, pos):
        res = []
        if pos > self.width:
            res.append(pos - self.width)
        if pos > 0:
            res.append(pos - 1)
        if pos < self.height * self.width - 1:
            res.append(pos + 1)
        if pos < (self.height - 1) * self.width:
            res.append(pos + self.width)
        return res

    def heuristic_distance(self, a, b):
        (ax, ay) = self.to_cart(a)
        (bx, by) = self.to_cart(b)
        return abs(ax - bx) + abs(ay - by)

    def __repr__(self):
        res = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x + y * self.width
                res += self.field[pos]
            res += "\n"
        return res

    def to_cart(self, pos):
        return (pos % self.width, math.floor(pos / self.width))

    def from_cart(self, x, y):
        return x + y * self.width

    def elves(self):
        return [pos for pos in range(0, len(self.field)) if self.field[pos] == "E"]

    def goblins(self):
        return [pos for pos in range(0, len(self.field)) if self.field[pos] == "G"]

    def move(self, unit):
        targets = self.goblins() if self.field[unit] == "E" else self.elves()
        in_range = list(
            filter(self.passable_terrain, sum(map(self.neighbors, targets), []))
        )
        reachable = list(
            filter(lambda t: self.shortest_path(unit, t) != None, in_range)
        )
        paths = list(map(lambda t: self.shortest_path(unit, t), reachable))
        distances = list(map(len, paths))
        if len(distances) == 0:
            return unit
        best_distance = min(distances)
        nearest = list(
            filter(
                lambda t: len(self.shortest_path(unit, t)) == best_distance, reachable
            )
        )

        chosen = min(nearest)

        best_path = self.shortest_path(unit, chosen)
        self.field[best_path[0]] = self.field[unit]
        self.field[unit] = "."
        self.hp[best_path[0]] = self.hp[unit]
        del self.hp[unit]
        self.ap[best_path[0]] = self.ap[unit]
        del self.ap[unit]

        return best_path[0]

    def in_attack_range(self, unit):
        targets = self.goblins() if self.field[unit] == "E" else self.elves()
        return any(self.heuristic_distance(t, unit) == 1 for t in targets)

    def attack(self, unit):
        targets = list(
            filter(
                lambda t: self.heuristic_distance(t, unit) == 1,
                self.goblins() if self.field[unit] == "E" else self.elves(),
            )
        )
        best_hp = min([self.hp[t] for t in targets])
        best_targets = [t for t in targets if self.hp[t] == best_hp]
        chosen_target = min(best_targets)

        self.hp[chosen_target] -= self.ap[unit]
        if self.hp[chosen_target] <= 0:
            self.field[chosen_target] = "."
            del self.hp[chosen_target]
            del self.ap[chosen_target]

    def tick(self):
        units = [pos for pos in range(0, len(self.field)) if self.field[pos] in "EG"]
        for unit in units:
            if self.field[unit] not in "EG":
                continue
            if not self.in_attack_range(unit):
                unit = self.move(unit)
            if self.in_attack_range(unit):
                self.attack(unit)

            if self.winner() is not None:
                if unit == units[-1]:
                    self.rounds += 1
                return
        self.rounds += 1

    def winner(self):
        if len(self.goblins()) == 0:
            return "E"
        elif len(self.elves()) == 0:
            return "G"
        else:
            return None


field = Field(open("15.txt"))
while field.winner() is None:
    # print(field)
    field.tick()
print(field.rounds * sum(field.hp.values()))


elf_power = 3
elf_deaths = True
while elf_deaths:
    elf_deaths = False
    elf_power += 1
    field = Field(open("15.txt"), elf_power)

    elf_count = len(field.elves())
    while field.winner() is None:
        field.tick()
        if len(field.elves()) < elf_count:
            elf_deaths = True
            break
        # print(field)
print(field.rounds * sum(field.hp.values()))

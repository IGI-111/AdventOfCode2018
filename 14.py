#!/usr/bin/env python
# -*- coding: utf-8 -*-

def iterate(recipes, current):
    new_recipes = map(int, iter(str(recipes[current[0]] + recipes[current[1]])))
    for r in new_recipes:
        recipes.append(r)
    current[0] = (current[0] + 1 + recipes[current[0]]) % len(recipes)
    current[1] = (current[1] + 1 + recipes[current[1]]) % len(recipes)

number = int(next(open("14.txt")))

recipes = [3, 7]
current = [0, 1]
while len(recipes) < number + 10:
    iterate(recipes, current)
print("".join(map(str, recipes[number:])))

pattern = list(map(int, iter(str(number))))
recipes = [3, 7]
current = [0, 1]

prev_len = len(recipes)
res = None
while res == None:
    iterate(recipes, current)
    for i in range(prev_len-len(pattern), len(recipes)-len(pattern)):
        if recipes[i:i+len(pattern)] == pattern:
            res = i
            break
    prev_len = len(recipes)
print(res)

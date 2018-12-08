#!/usr/bin/env python
# -*- coding: utf-8 -*-


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


with open("5.txt") as file:
    points = []
    for line in file:
        [x, y] = map(lambda s: int(s.strip()), line.strip().split(","))
        points.append((x, y))

    dim_x = 1 + max(map(lambda x: x[0], points))
    dim_y = 1 + max(map(lambda x: x[1], points))

    field = [-1] * dim_x * dim_y
    for y in range(0, dim_y):
        for x in range(0, dim_x):
            dists = dict()
            for i in range(0, len(points)):
                d = dist(points[i], (x, y))
                if d in dists:
                    dists[d] = -1
                else:
                    dists[d] = i
            field[x + y * dim_x] = dists[min(dists)]

    sizes = {p: 0 for p in range(-1, len(points))}
    for val in field:
        sizes[val] += 1

    # remove borders
    for x in range(0, dim_x):
        sizes[field[x]] = 0
        sizes[field[x + dim_x * (dim_y - 1)]] = 0
    for y in range(0, dim_y):
        sizes[field[dim_x * y]] = 0
        sizes[field[dim_x - 1 + dim_x * y]] = 0
    sizes[-1] = 0
    print(max(sizes.values()))

    close_count = 0
    for y in range(0, dim_y):
        for x in range(0, dim_x):
            total_dist = sum([dist(p, (x,y)) for p in points])
            if total_dist < 10000:
                close_count += 1
    print(close_count)



#!/usr/bin/env python
# -*- coding: utf-8 -*-


def compute_power(serial_number, x, y):
    rack_id = x + 10
    return int(str(rack_id * (y * rack_id + serial_number))[-3]) - 5


def max_subarray(array):
    return (0, 0)


width = 300
height = 300

serial_number = int(next(open("11.txt")))

matrix = [0] * width * height
for y in range(0, height):
    for x in range(0, width):
        matrix[x + y * width] = compute_power(serial_number, x + 1, y + 1)

prefix_sums = [0] * width * height
for x in range(0, width):
    prefix_sums[x] = matrix[x]
for y in range(1, height):
    for x in range(0, width):
        prefix_sums[x + y * width] = (
            prefix_sums[x + (y - 1) * width] + matrix[x + y * width]
        )

best_square = None
best_square_val = None
for y in range(0, height - 2):
    for x in range(0, width - 2):
        first_row = (
            prefix_sums[x + (y - 1) * width : x + 3 + (y - 1) * width]
            if y > 0
            else [0] * 3
        )
        last_row = prefix_sums[x + (y + 2) * width : x + 3 + (y + 2) * width]

        square_val = sum([last_row[i] - first_row[i] for i in range(0, 3)])
        if best_square_val == None or square_val > best_square_val:
            best_square = (x, y)
            best_square_val = square_val
print("{},{}".format(best_square[0] + 1, best_square[1] + 1))

best_square = None
best_square_val = None
for y in range(0, height):
    for yl in range(y + 1, height):
        size = yl - y
        for x in range(0, width - size + 1):
            first_row = (
                prefix_sums[x + (y - 1) * width : x + size + (y - 1) * width]
                if y > 0
                else [0] * size
            )
            last_row = prefix_sums[
                x + (y + size - 1) * width : x + size + (y + size - 1) * width
            ]
            square_val = sum([last_row[i] - first_row[i] for i in range(0, size)])

            if best_square_val == None or square_val > best_square_val:
                best_square = (x, y, size)
                best_square_val = square_val
print("{},{},{}".format(best_square[0] + 1, best_square[1] + 1, best_square[2]))

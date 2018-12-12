#!/usr/bin/env python
# -*- coding: utf-8 -*-


def compute_power(serial_number, x, y):
    rack_id = x + 10
    return int(str(rack_id * (y * rack_id + serial_number))[-3]) - 5


def summed_area(sums, width, x, y, size):
    a = sums[x - 1 + (y - 1) * width] if x > 0 else 0
    b = sums[x + size - 1 + (y - 1) * width] if y > 0 else 0
    c = sums[x - 1 + (y + size - 1) * width] if x > 0 else 0
    d = sums[x + size - 1 + (y + size - 1) * width]
    return d - b - c + a


width = 300
height = 300

serial_number = int(next(open("11.txt")))

matrix = [0] * width * height
for y in range(0, height):
    for x in range(0, width):
        matrix[x + y * width] = compute_power(serial_number, x + 1, y + 1)

sums = [0] * width * height
for y in range(0, height):
    for x in range(0, width):
        sums[x + y * width] = (
            (sums[x - 1 + y * width] if x > 0 else 0)
            + (sums[x + (y - 1) * width] if y > 0 else 0)
            - (sums[x - 1 + (y - 1) * width] if x > 0 and y > 0 else 0)
            + matrix[x + y * width]
        )

best_square = None
best_square_val = None
for y in range(0, height - 2):
    for x in range(0, width - 2):
        square_val = summed_area(sums, width, x, y, 3)
        if best_square_val == None or square_val > best_square_val:
            best_square = (x, y)
            best_square_val = square_val
print("{},{}".format(best_square[0] + 1, best_square[1] + 1))

best_square = None
best_square_val = None
for size in range(1, 300):
    for y in range(0, height - size + 1):
        for x in range(0, width - size + 1):
            square_val = summed_area(sums, width, x, y, size)
            if best_square_val == None or square_val > best_square_val:
                best_square = (x, y, size)
                best_square_val = square_val
print("{},{},{}".format(best_square[0] + 1, best_square[1] + 1, best_square[2]))

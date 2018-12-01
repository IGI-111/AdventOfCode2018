#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open("1.txt") as f:
    total = 0
    for line in f:
        total += int(line.strip())
    print(total)

with open("1.txt") as f:
    changes = [int(line.strip()) for line in f]

    seen = set()
    total = 0
    while total not in seen:
        for c in changes:
            seen.add(total)
            total += c
            if total in seen: break
    print(total)


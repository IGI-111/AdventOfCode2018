#!/usr/bin/env python
# -*- coding: utf-8 -*-

def checksum(s):
    counts = {}
    for c in s:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    return (int(2 in counts.values()), int(3 in counts.values()))

with open("2.txt") as file:
    counts = (0, 0)
    for line in file:
        c = checksum(line.strip())
        counts = (counts[0] + c[0], counts[1] + c[1])
    print(counts[0] * counts[1])

def same(a, b):
    assert len(a) == len(b)
    res = ""
    for i in range(0, len(a)):
        if a[i] == b[i]:
            res += a[i]
    return res

with open("2.txt") as file:
    ids = [line.strip() for line in file]
    
    for i in range(0, len(ids)):
        a = ids[i]
        for b in ids[i+1:]:
            s = same(a, b)
            if len(s) == len(a) - 1:
                print s

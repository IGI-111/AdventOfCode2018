#!/usr/bin/env python
# -*- coding: utf-8 -*-

d = 0
running = True
while running:
    e = d | 65536
    d = 2176960
    while True:
        b = e & 255
        d = d + b
        d = d & 16777215
        d = d * 65899
        d = d & 16777215
        if 256 > e:
            print(d)
            running = False
            break
        e = e // 256

seen = set()
prev = None
d = 0
running = True
while running:
    e = d | 65536
    d = 2176960
    while True:
        b = e & 255
        d = d + b
        d = d & 16777215
        d = d * 65899
        d = d & 16777215
        if 256 > e:
            if d in seen:
                print(prev)
                running = False
            prev = d
            seen.add(d)
            break
        e = e // 256

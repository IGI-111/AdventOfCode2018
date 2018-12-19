#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def run_ins(ins, regs):
    (opcode, a, b, c) = ins
    if opcode == "addr":
        regs[c] = regs[a] + regs[b]
    elif opcode == "addi":
        regs[c] = regs[a] + b
    elif opcode == "mulr":
        regs[c] = regs[a] * regs[b]
    elif opcode == "muli":
        regs[c] = regs[a] * b
    elif opcode == "banr":
        regs[c] = regs[a] & regs[b]
    elif opcode == "bani":
        regs[c] = regs[a] & b
    elif opcode == "borr":
        regs[c] = regs[a] | regs[b]
    elif opcode == "bori":
        regs[c] = regs[a] | b
    elif opcode == "setr":
        regs[c] = regs[a]
    elif opcode == "seti":
        regs[c] = a
    elif opcode == "gtir":
        regs[c] = 1 if a > regs[b] else 0
    elif opcode == "gtri":
        regs[c] = 1 if regs[a] > b else 0
    elif opcode == "gtrr":
        regs[c] = 1 if regs[a] > regs[b] else 0
    elif opcode == "eqir":
        regs[c] = 1 if a == regs[b] else 0
    elif opcode == "eqri":
        regs[c] = 1 if regs[a] == b else 0
    elif opcode == "eqrr":
        regs[c] = 1 if regs[a] == regs[b] else 0
    else:
        print("Illegal opcode: {}".format(opcode))


def parse_program(file):
    program = []
    for match in re.finditer("(\w+) (\d+) (\d+) (\d+)", file.read()):
        (opcode, a, b, c) = match.groups()
        program.append((opcode, int(a), int(b), int(c)))

    file.seek(0)
    match = re.search("#ip (\d+)", file.read())
    ip = int(match.group(1))
    return (ip, program)


(ip, program) = parse_program(open("19.txt"))
regs = [0] * 6

while regs[ip] >= 0 and regs[ip] < len(program):
    run_ins(program[regs[ip]], regs)
    regs[ip] += 1
print(regs[0])

num = 10551378
c = 1
for i in range(2, num+1):
    if num % i == 0:
        c += i
print(c)

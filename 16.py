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


def possible_opcodes(before_regs, ins, after_regs):
    matching_opcodes = set()
    for opcode in [
        "addr",
        "addi",
        "mulr",
        "muli",
        "banr",
        "bani",
        "borr",
        "bori",
        "setr",
        "seti",
        "gtir",
        "gtri",
        "gtrr",
        "eqir",
        "eqri",
        "eqrr",
    ]:
        regs = before_regs.copy()
        ins = (opcode, ins[1], ins[2], ins[3])
        run_ins(ins, regs)
        if regs == after_regs:
            matching_opcodes.add(opcode)
    return matching_opcodes


def parse_tests(file):
    res = []
    for match in re.finditer(
        "Before:\s*\[(.*)\]\s(.*)\sAfter:\s*\[(.*)\]", file.read()
    ):
        (before, ins, after) = match.groups()
        before = list(map(int, before.split(",")))
        ins = tuple(map(int, ins.split()))
        after = list(map(int, after.split(",")))

        res.append((before, ins, after))
    return res


def parse_program(file):
    m = re.search("(\d+\s\d+\s\d+\s\d+\n){2,}", file.read())
    return list(
        map(lambda ins: tuple(map(int, ins.split())), m.group(0).strip().split("\n"))
    )


tests = parse_tests(open("16.txt"))
matching_three = 0
for (before, ins, after) in tests:
    if len(possible_opcodes(before, ins, after)) >= 3:
        matching_three += 1
print(matching_three)

tests = parse_tests(open("16.txt"))
opcodes = {}
for (before, ins, after) in tests:
    opcode = ins[0]
    if opcode in opcodes:
        opcodes[opcode] = opcodes[opcode].intersection(
            possible_opcodes(before, ins, after)
        )
        if len(opcodes[opcode]) == 1:
            for other in opcodes:
                if other != opcode:
                    opcodes[other] = opcodes[other].difference(opcodes[opcode])
    else:
        opcodes[opcode] = possible_opcodes(before, ins, after)
for opcode in opcodes:
    opcodes[opcode] = next(iter(opcodes[opcode]))

print(opcodes)

regs = [0] * 4
program = parse_program(open("16.txt"))
for ins in program:
    real_ins = (opcodes[ins[0]], ins[1], ins[2], ins[3])
    run_ins(real_ins, regs)
print(regs[0])

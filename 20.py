#!/usr/bin/env python
# -*- coding: utf-8 -*-

def parse_expr(expr):
    options = tuple()
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i] == '(':
            open_paren = i
            depth = 0
            for j in range(open_paren, len(expr)):
                if expr[j] == '(':
                    depth += 1
                elif expr[j] == ')':
                    depth -= 1
                if depth == 0:
                    close_paren = j
                    break
            tokens.append(parse_expr(expr[open_paren+1:close_paren]))
            i = close_paren+1
        elif expr[i] == '|':
            options += (tokens, )
            tokens = []
            i += 1
        else:
            tokens.append(expr[i])
            i += 1
    options += (tokens,)
    return options

def build_graph(options, graph, start):
    for option in options:
        current = start
        for token in option:
            if type(token) == str:
                if token == 'N':
                    after = (current[0], current[1] - 1)
                elif token == 'S':
                    after = (current[0], current[1] + 1)
                elif token == 'E':
                    after = (current[0] + 1, current[1])
                elif token == 'W':
                    after = (current[0] - 1, current[1])

                graph[current].add(after)
                if after in graph:
                    graph[after].add(current)
                else:
                    graph[after] = {current}
                current = after
            else:
                build_graph(token, graph, current)

def distances(graph):
    openSet = {(0, 0)}
    far = {(0, 0): 0}
    closedSet = set()

    while openSet != set():
        nextOpenSet = set()
        for val in openSet:
            closedSet.add(val)
            for neigh in graph[val].difference(closedSet):
                far[neigh] = far[val] + 1
                nextOpenSet.add(neigh)
        openSet = nextOpenSet
    return far



expr = open("20.txt").read().strip()[1:-1]
options = parse_expr(expr)
graph = { (0,0): set() }
build_graph(options, graph, (0, 0))
dists = distances(graph)
print(max(dists.values()))
print(len([x for x in dists.values() if x >= 1000]))

#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node:
    def __init__(self, data):
        self.child_len = data.pop(0)
        self.meta_len = data.pop(0)
        self.children = []
        for i in range(0, self.child_len):
            self.children.append(Node(data))
        self.meta = [data.pop(0) for _ in range(0, self.meta_len)]

    def rec_sum(self):
        return sum(self.meta) + sum([c.rec_sum() for c in self.children])

    def value(self):
        if self.child_len == 0:
            return sum(self.meta)
        else:
            return sum(
                [
                    self.children[n - 1].value()
                    for n in self.meta
                    if n > 0 and n <= self.child_len
                ]
            )


with open("8.txt") as file:
    for line in file:
        data = list(map(int, line.split()))
        tree = Node(data)
        print(tree.rec_sum())
        print(tree.value())

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from random import shuffle

SEPARATOR = ";"
STATS_FILE = "stats.txt"
EDGES_FILE = "edges.csv"
SHUFFLED_EDGES = "edges_shuffled.csv"

def get_stats(filename):
    d = {}
    with open(filename, "r") as f:
        for line in f:
            number = int(line.split(" ")[-1])
            if "Node" in line:
                d["nodes"] = number
            if "Edge" in line:
                d["edges"] = number

    return d


def get_shuffled_map(count):
    keys = list(range(1, count + 1))
    values = list(range(1, count + 1))
    shuffle(values)

    mapping = {}
    for k, v in zip(keys, values):
        mapping[k] = v

    return mapping


def make_shuffled_edges(edge_dir, shuffled_map):
    source_edges = os.path.join(edge_dir, EDGES_FILE)
    target_edges = os.path.join(edge_dir, SHUFFLED_EDGES)

    with open(source_edges, "r") as f_e:
        with open(target_edges, "w") as f_s:
            for line in f_e:
                items = line.split(SEPARATOR)
                items[1] = str(shuffled_map[int(items[1])])
                items[2] = str(shuffled_map[int(items[2])])

                f_s.write(SEPARATOR.join(items))


def main():

    if len(sys.argv) > 1:
        edge_dir = sys.argv[1]
    else:
        edge_dir = ""

    stats = get_stats(os.path.join(edge_dir, STATS_FILE))
    shuffled_map = get_shuffled_map(stats["nodes"])
    make_shuffled_edges(edge_dir, shuffled_map)


if __name__ == "__main__":
    main()

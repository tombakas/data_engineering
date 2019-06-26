#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

import numpy as np


EDGE_TYPES = [
    "acted_in",
    "directed",
    "directed_in",
    "has_genre",
    "worked_with"
]


def parse_args():

    parser = argparse.ArgumentParser(description="Generate adjacency matrices")
    parser.add_argument("-e", "--edge-dir", required=True, help="Directory with edges")

    args = parser.parse_args()
    return args


def get_counts(filename):
    counts = {}
    with open(filename, "r") as f:
        for line in f:
            if "Node" in line:
                counts["node"] = int(line.split(":")[-1])
            if "Edge" in line:
                counts["edge"] = int(line.split(":")[-1])

    return counts


def populate_matrices(m, filename):
    with open(filename, "r") as f:
        for line in f:
            items = line.split(";")

            edge = items[-1].strip()
            source = int(items[1]) - 1
            target = int(items[2]) - 1
            edge_idx = EDGE_TYPES.index(edge)

            m[edge_idx][source][target] = 1

            if edge == "worked_with":
                m[edge_idx][target][source] = 1


def save_matrices(m, edge_dir):
    edge_dir = os.path.join(edge_dir, "edges")
    if not (os.path.exists(edge_dir)):
        os.mkdir(edge_dir)

    for i, edge in enumerate(EDGE_TYPES):
        filename = os.path.join(edge_dir, edge + ".csv")
        np.savetxt(filename, m[i], fmt="%d")


def main():
    args = parse_args()
    edge_dir = args.edge_dir

    counts = get_counts(os.path.join(edge_dir, "stats.txt"))

    dim = counts["node"]
    matrices = [np.zeros((dim, dim,), dtype=np.int8) for edge in EDGE_TYPES]

    populate_matrices(matrices, os.path.join(edge_dir, "edges.csv"))
    save_matrices(matrices, edge_dir)


if __name__ == "__main__":
    main()

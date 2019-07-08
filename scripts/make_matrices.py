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
    parser.add_argument("-f", "--edge-file", default="edges.csv", help="Edge file name")
    parser.add_argument("-m", "--merged", default=False, action="store_true", help="Merge matrices")
    parser.add_argument("-s", "--shuffled", default=False, action="store_true", help="Shuffled edges")

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


def populate_matrices(m, filename, merged=False):
    with open(filename, "r") as f:
        for line in f:
            items = line.split(";")

            source = int(items[1]) - 1
            target = int(items[2]) - 1
            edge = items[-1].strip()

            if merged:
                edge_idx = 0
            else:
                edge_idx = EDGE_TYPES.index(edge)

            m[edge_idx][source][target] = 1

            if edge == "worked_with":
                m[edge_idx][target][source] = 1


def save_matrices(m, edge_dir, edge_subdir="edges", merged=False):
    edge_dir = os.path.join(edge_dir, edge_subdir)
    if not (os.path.exists(edge_dir)):
        os.mkdir(edge_dir)

    if merged:
        filename = os.path.join(edge_dir, "matrix_merged.csv")
        np.savetxt(filename, m[0], fmt="%d")
    else:
        for i, edge in enumerate(EDGE_TYPES):
            filename = os.path.join(edge_dir, edge + ".csv")
            np.savetxt(filename, m[i], fmt="%d")


def main():
    args = parse_args()
    edge_dir = args.edge_dir

    counts = get_counts(os.path.join(edge_dir, "stats.txt"))

    dim = counts["node"]
    if args.merged:
        matrices = [np.zeros((dim, dim,), dtype=np.int8)]
    else:
        matrices = [np.zeros((dim, dim,), dtype=np.int8) for edge in EDGE_TYPES]

    populate_matrices(matrices, os.path.join(edge_dir, args.edge_file), args.merged)

    if args.shuffled:
        save_matrices(matrices, edge_dir, "edges_shuffled", args.merged)
    else:
        save_matrices(matrices, edge_dir, "edges", args.merged)



if __name__ == "__main__":
    main()

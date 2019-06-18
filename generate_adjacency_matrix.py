#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import sys

import numpy as np

from collections import defaultdict


ACTORS = "generated_data/actors.csv"
ACTOR_EDGES = "generated_data/actor_edges.csv"


def read_data(filename):
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames[:]
        fieldnames.pop(0)
        data = {item["ID"]: {fieldname: item[fieldname] for fieldname in fieldnames} for item in reader}
    return data


def main():
    actors = read_data(ACTORS)
    actors = sorted(actors.keys())
    total_actors = len(actors)

    actor_edges = read_data(ACTOR_EDGES)
    actor_edge_sets = defaultdict(set)

    i = 1
    for actor in actors:
        print("\rIterating over actors: {:>6.2f}%".format(i / total_actors * 100), end="", flush=True)
        for pair_dict in actor_edges.values():
            pair_values = list(pair_dict.values())
            if actor in pair_values:
                pair_values.remove(actor)
                actor_edge_sets[actor].add(pair_values[0])
        i += 1
    print(" Done.")

    adj = np.zeros((total_actors, total_actors,))

    for i, actor in enumerate(actors):
        for j in range(total_actors):
            paired_actor = actors[j]
            print("\rBuilding matrix: {:>6.2f}%".format(i / float(total_actors) * 100), end="", flush=True)
            if paired_actor in actor_edge_sets[actor]:
                adj[i][j] = 1
    print(" Done.")

    np.save("./matrix.npy", adj)
    print("Matrix saved to \"matrix.npy\"")


if __name__ == "__main__":
    main()

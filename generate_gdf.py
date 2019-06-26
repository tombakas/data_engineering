#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse


def parse_args():

    parser = argparse.ArgumentParser(description="Generate adjacency matrices")
    parser.add_argument("-e", "--edge-dir", required=True, help="Directory with edges")

    args = parser.parse_args()
    return args


def generate_gdf(target_dir):
    target_file = os.path.join(target_dir, "graph.gdf")
    edges_file = os.path.join(target_dir, "edges.csv")
    nodes_file = os.path.join(target_dir, "nodes.csv")

    with open(target_file, "w") as f:
        f.write("nodedef>name VARCHAR,label VARCHAR,class VARCHAR\n")
        with open(nodes_file, "r") as n_f:
            for line in n_f:
                items = [item.strip() for item in line.split(";")]
                f.write(",".join([items[0], items[4], items[2]]) + "\n")

        f.write("edgedef>node1 VARCHAR,node2 VARCHAR,label VARCHAR, directed BOOLEAN\n")
        with open(edges_file, "r") as n_f:
            for line in n_f:
                items = [item.strip() for item in line.split(";")]
                f.write(",".join([items[1], items[2], items[4], "true"]) + "\n")


def main():
    args = parse_args()
    edge_dir = args.edge_dir
    generate_gdf(edge_dir)


if __name__ == "__main__":
    main()

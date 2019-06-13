#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

from itertools import combinations

SOURCE_DATA_DIR = "./source_data"
GENERATEC_DATA_DIR = "./generated_data"

MOVIE_FILE = os.path.join(GENERATEC_DATA_DIR, "movie_info.json")


def node_build(data, type_name):
    output = []
    for k, v in data.items():
        output.append(f"{v},Node Label,{type_name},Name,\"{k}\"\n")

    return output


def main():
    with open(MOVIE_FILE, "r") as f:
        data = json.loads(f.read())

    top_id = 1

    films = {}
    actors = {}
    genres = {}
    directors = {}

    # build film ids
    for item in data:
        if item["title"] not in films:
            films[item["title"]] = top_id
            top_id += 1

    # build actor ids
    for item in data:
        for actor in item["top_cast"]:
            if actor not in actors:
                actors[actor] = top_id
                top_id += 1

    # build director ids
    for item in data:
        for director in item["directors"]:
            if director not in directors:
                directors[director] = top_id
                top_id += 1

    # build director ids
    for item in data:
        genres_l = json.loads(item["genres"].replace("'", "\""))
        for genre in genres_l:
            if genre["name"] not in genres:
                genres[genre["name"]] = top_id
                top_id += 1

    film_nodes = node_build(films, "film")
    actor_nodes = node_build(actors, "actor")
    genre_nodes = node_build(genres, "genre")
    director_nodes = node_build(directors, "director")
    worked_with = set()
    directed_in = set()
    worked_in = set()

    nodes_groups = [film_nodes, actor_nodes, genre_nodes, director_nodes]

    with open(os.path.join(GENERATEC_DATA_DIR, "nodes.csv"), "a") as f:
        for node_group in nodes_groups:
            for node in node_group:
                f.write(node)

    top_edge = 1
    with open(os.path.join(GENERATEC_DATA_DIR, "edges.csv"), "w") as f:
        for item in data:
            film_id = films[item["title"]]
            genres_l = json.loads(item["genres"].replace("'", "\""))
            genre_ids = [genre["id"] for genre in genres_l]

            # Acted in
            actor_ids = []
            for actor in item["top_cast"]:
                actor_id = actors[actor]
                actor_ids.append(actor_id)
                f.write(f"{top_edge},{actor_id},{film_id},Edge Label,acted_in\n")
                top_edge += 1

                # Worked in set build
                for genre_id in genre_ids:
                    pair = [actor_id, genre_id]
                    s = f"{pair[0]}_{pair[1]}"
                    worked_in.add(s)
                # /Worked in set build
            # /Acted in

            # Worked with set build
            for c in combinations(actor_ids, 2):
                actor_pair = sorted(c)
                first, second = actor_pair[0], actor_pair[1]
                worked_with.add(f"{first}_{second}")
            # /Worked with set build

            # Directed
            for director in item["directors"]:
                director_id = directors[director]
                f.write(f"{top_edge},{director_id},{film_id},Edge Label,directed\n")
                top_edge += 1

                # Directed in set build
                for genre_id in genre_ids:
                    pair = [director_id, genre_id]
                    s = f"{pair[0]}_{pair[1]}"
                    directed_in.add(s)
                # /Directed in set build
            # /Directed

            # Has genre
            for genre_id in genre_ids:
                f.write(f"{top_edge},{film_id},{genre_id},Edge Label,has_genre\n")
                top_edge += 1
            # /Has genre

        # Directed in
        for pair in directed_in:
            first, second = pair.split("_")
            f.write(f"{top_edge},{first},{second},Edge Label,directed_in\n")
            top_edge += 1
        # /Directed in

        # Worked with
        for pair in worked_with:
            first, second = pair.split("_")
            f.write(f"{top_edge},{first},{second},Edge Label,worked_with\n")
            top_edge += 1
        # /Worked with


if __name__ == "__main__":
    main()

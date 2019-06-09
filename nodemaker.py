#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json

GENERATEC_DATA_DIR = "./generated_data"


def node_build(data, type_name):
    output = []
    for k, v in data.items():
        output.append(f"{v},Node Label,{type_name},Name,\"{k}\"")
        return output


def main():
    with open("./movies_2.json", "r") as f:
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

    films = node_build(films, "film")
    actors = node_build(actors, "actor")
    genres = node_build(genres, "genre")
    directors = node_build(directors, "director")

    nodes_groups = [films, actors, genres, directors]

    with open(os.path.join(GENERATEC_DATA_DIR, "nodes.csv"), "a") as f:
        for node_group in nodes_groups:
            for node in node_group:
                f.write(node)

    top_edge = 1
    with open(os.path.join(GENERATEC_DATA_DIR, "edges.csv"), "a") as f:
        for item in data:
            film_id = films[item["title"]]

            for actor in item["top_cast"]:
                actor_id = actors[actor]
                f.write(f"{top_edge},{actor_id},{film_id},Edge Label,acted_in")
                top_edge += 1

            for director in item["directors"]:
                director_id = directors[director]
                f.write(f"{top_edge},{director_id},{film_id},Edge Label,directed")
                top_edge += 1

            genres_l = json.loads(item["genres"].replace("'", "\""))
            for genre in genres_l:
                genre_id = genres[genre["name"]]
                f.write(f"{top_edge},{film_id},{genre_id},Edge Label,has_genre")
                top_edge += 1

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import csv
import sys
import json

from json.decoder import JSONDecodeError
from time import time

SOURCE_DATA_DIR = "./source_data"
GENERATEC_DATA_DIR = "./generated_data"

MOVIE_FILE = os.path.join(SOURCE_DATA_DIR, "movies_metadata.csv")
CREDIT_FILE = os.path.join(SOURCE_DATA_DIR, "credits.csv")

TOTAL_ACTORS = 4

BUDGET_THRESHOLD = 1e8


def check_file_presence():
    source_files = [MOVIE_FILE, CREDIT_FILE]

    for file in source_files:
        if not os.path.exists(file):
            print(f"Can't find {file} file")
            sys.exit(1)


def get_csv_data(filename, as_list=True):
    if as_list:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            data = [row for row in reader]
        return data

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = {}
        data = {item["id"]: item for item in reader}
    return data


def filter_data(data, column, threshold):
    filtered_data = []
    for item in data:
        try:
            if int(item[column]) >= threshold:
                filtered_data.append(item)
        except ValueError:
            pass

    return filtered_data


def fix_json_data(input_data, idx=None):
    def replace_quotes(input_data):
        return input_data.replace("'", '"')

    def replace_nones(input_data):
        return input_data.replace("None", "null")

    data = replace_quotes(input_data)
    data = replace_nones(data)

    data = re.sub('^"|"$', "", data)

    pattern = re.compile(': "([^:]+?"[^:]*?)+",')
    nested_quotes = re.finditer(pattern, data)
    if nested_quotes:
        for item in nested_quotes:
            s, e = item.span()

            s += 3
            e -= 2

            text = data[s:e]
            text = text.replace('"', "'")

            data = data[:s] + text + data[e:]

    pattern = re.compile('""[^,]+?""')
    inside_double = re.finditer(pattern, data)
    if inside_double:
        s_offset = 0
        e_offset = 0

        for item in inside_double:
            s, e = item.span()

            s = s + s_offset
            e = e + e_offset

            text = data[s:e]
            text = '"' + text[2:-2].replace('"', "'") + '"'

            data = data[:s] + text + data[e:]

            s_offset += s_offset - 2
            e_offset += e_offset - 2

    return data


def force_parse_json(input_data):
    bad_char = re.compile("char [0-9]+")

    for x in range(1000):
        try:
            json_data = json.loads(input_data)
            break
        except JSONDecodeError as e:
            if "Invalid \escape" in e.msg:
                idx = int(re.search(bad_char, str(e)).group().split(" ")[1])
                input_data = input_data[: idx - 1] + input_data[idx + 1 :]
            else:
                idx = int(re.search(bad_char, str(e)).group().split(" ")[1])
                input_data = input_data[: idx - 1] + "'" + input_data[idx:]
            if x == 999:
                print(input_data)
                sys.exit(1)

    return json_data


def extract_details(movie, credits):
    cast_str = fix_json_data(credits["cast"])
    crew_str = fix_json_data(credits["crew"])

    crew = force_parse_json(crew_str)
    cast = force_parse_json(cast_str)

    if crew is not None and cast is not None:
        top_three_cast = []
        for member in cast:
            if member["order"] in list(range(TOTAL_ACTORS)):
                top_three_cast.append(member["name"])

        directors = []
        for member in crew:
            if member["department"] == "Directing" and member["job"] == "Director":
                directors.append(member["name"])

        return {"top_cast": top_three_cast, "directors": directors}


def build_aggregated_movie_json(movie_data, credit_data):
    output = []
    for movie in movie_data:
        details = credit_data.get(movie["id"])
        movie_info = {"title": movie["title"], "genres": movie["genres"]}
        if details:
            getted = extract_details(movie, details)
            if getted:
                movie_info.update(getted)
                output.append(movie_info)

    return output


def write_data_to_file(data, filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write(json.dumps(data))
    else:
        print(f"{filename} already exists")


def main():
    check_file_presence()

    # read in all data from movies_metadata.csv
    movie_data = get_csv_data(MOVIE_FILE)
    # only keep films with budget above 10^7 (or whatever BUDGET_THRESHOLD is)
    movie_data = filter_data(movie_data, "budget", BUDGET_THRESHOLD)

    # read in all credits data from credits.csv
    credit_data = get_csv_data(CREDIT_FILE, as_list=False)

    output = build_aggregated_movie_json(movie_data, credit_data)
    write_data_to_file(
        output, os.path.join(GENERATEC_DATA_DIR, f"{int(time())}movie_info.json")
    )


if __name__ == "__main__":
    main()

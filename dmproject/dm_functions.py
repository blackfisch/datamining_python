#!/usr/bin/env python3
"""
This module contains all function that actually manipulate the data to display it.
Some of these functions get imported and called from main.py.

Docstrings are always written as a command ("Do This, Return That") as per PEP 257
"""
import re
import matplotlib.pyplot as plotter
import pandas

#pylint: disable=line-too-long
RE_PATH = r'^(\(entrance\)|\/(((album|board|category-file-list|category-article-list)\/?\d+)|[^\/?]+(\/[^\d\/]+[^?\/]+)?\/)|\/)'


def draw_pie(reader):
    """Take the reader object and input the data to the plotter."""
    labels = []
    values = []

    for row in reader:
        lbl, val = row
        labels.append(lbl)
        values.append(val)

    _, axes_object = plotter.subplots()

    axes_object.pie(values, labels=labels, autopct='%1.2f', startangle=90)
    axes_object.axis('equal')


def analyze_pagepath(reader):
    """Take the reader object and process data for the plotter."""

    traffic = {}
    forum_traffic = {}
    dl_traffic = {}

    for path, users in reader:
        subpath = re.match(r'^\/[^\/?=\n]*\/?', path)
        if subpath is None:
            continue

        users = int(users)
        subpath = subpath.group(0).replace('/index.html', '/')

        if ("/acp/" in path or "/moderation" in path):
            continue

        # general traffic stats
        if subpath in traffic.keys():
            traffic[subpath] += users
        else:
            traffic[subpath] = users

        # site traffic analysis
        match = re.match(r'\/forum\/board\/([^\/]*)\/', path)
        if match:
            # forum category
            match = match.group(1)

            if subpath in forum_traffic.keys():
                forum_traffic[match] += users
            else:
                forum_traffic[match] = users
        else:
            match = re.match(
                r'\/downloads\/category-file-list\/([^\/]*)\/', path)
            if match:
                # downloads category
                match = match.group(1)

                if subpath in dl_traffic.keys():
                    dl_traffic[match] += users
                else:
                    dl_traffic[match] = users

    _, axes_traffic = plotter.subplots()
    # filter -> dict comprehension
    traffic = {k: v for k, v in traffic.items() if v > 50}
    axes_traffic.barh(list(traffic.keys()), list(traffic.values()), 0.5)

    _, axes_forum_traffic = plotter.subplots()
    # filter -> dict comprehension
    forum_traffic = {k: v for k, v in forum_traffic.items() if v > 5}
    axes_forum_traffic.barh(list(forum_traffic.keys()),
                            list(forum_traffic.values()), 0.5)

    _, axes_dl_traffic = plotter.subplots()
    # filter -> dict comprehension
    dl_traffic = {k: v for k, v in dl_traffic.items() if v > 5}
    axes_dl_traffic.barh(list(dl_traffic.keys()),
                         list(dl_traffic.values()), 0.5)


def analyze_previous_pagepath(reader):
    """Take the reader object and process data for the plotter."""
    data = {
        "path": [],
        "prev": [],
        "users": []
    }

    for path, prev_path, users in reader:
        path = re.match(RE_PATH, path).group(0)
        prev_path = re.match(RE_PATH, prev_path).group(0)
        users = int(users)

        if ("/acp/" in path or "/moderation" in path or "/acp/" in prev_path or "/moderation" in prev_path):
            continue

        data['path'].append(path)
        data['prev'].append(prev_path)
        data['users'].append(users)

    data_frame = pandas.DataFrame.from_dict(data)

    tab = pandas.crosstab(
        index=data_frame['path'],
        columns=data_frame['prev'],
        values=data_frame['users'],
        aggfunc=sum
    ).fillna(0).apply(lambda r: r/r.sum(), axis=1)

    tab.plot.bar()

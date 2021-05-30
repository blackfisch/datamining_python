#!/usr/bin/env python3
import csv
import os
import matplotlib.pyplot as plotter

work_dir = os.getcwd()


def draw_pie(reader):
    labels = []
    values = []

    for row in reader:
        lbl, val = row
        labels.append(lbl)
        values.append(val)

    figureObject, axesObject = plotter.subplots()

    axesObject.pie(values, labels=labels, autopct='%1.2f', startangle=90)
    axesObject.axis('equal')


for file_name in ('usergender_users', 'useragebracket_users', 'continent_users'):

    with open(os.path.join(work_dir, f'data/{file_name}.csv'), 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)

        draw_pie(reader)

plotter.show()

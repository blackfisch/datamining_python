#!/usr/bin/env python3
"""
This is the main File that gets executed by the user.

The first line is a 'shebang' telling the OS what interpreter to use.

Following the shebang - this docstring is the file description which should 
contain an explanation what this script does.
This project follows PEP8 guidelines on code styling almost exactly.
The tool 'pylint' can be used as a linter for all files in this project.

After the docstring the imports are organized, one module per line and import statement.
First all the default modules, then third-party or own modules.
Dependencies can be installed with the packer manager pip. To install matplotlip and pandas use:
    > pip install matplotlib pandas
After that, either restart VSCode or do the following steps:
    > Press F1
    > Enter "Python: Restart Language Server"
    > Press ENTER to execute and restart the server
    > all modules should now be recognized

Specific functions from a package can also be imported with the 'from'-keyword.

In Python there is no need for functions everything gets executed as written.
Functions and Classes can and should be used to structure the code better.
"""
import csv
import os
import matplotlib.pyplot as plotter

# import specific functions from package
from dmproject.dm_functions import draw_pie, analyze_pagepath, analyze_previous_pagepath


WORK_DIR = os.getcwd()

FILES_FNC = {
    'usergender_users': draw_pie,
    'useragebracket_users': draw_pie,
    'continent_users': draw_pie,
    'pagepath_users': analyze_pagepath,
    'pagepath-previouspagepath_users': analyze_previous_pagepath
}

for (file_name, fnc) in FILES_FNC.items():
    with open(os.path.join(WORK_DIR, f'data/{file_name}.csv'), 'r') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        next(reader)

        fnc(reader)

plotter.show()

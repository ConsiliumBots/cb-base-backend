"""
Normally in django, to import views a and b,
you would have to write down this code in this init:
from .a import a
from .b import b
__all__ = ['a', 'b']
This code does that automatically so you don't have to specify
each new view being added.
"""

from os import listdir
from os.path import isfile, join
import pathlib

# get path
path = pathlib.Path(__file__).parent.resolve()
path = str(path)

# get all files from folder
files = [f for f in listdir(path) if isfile(join(path, f))]

# save all views
all_views = []

# for each file, import file
for file in files:
    if '__init__' not in file:
        view = file.replace(".py", '')
        all_views.append(f'{view}')
        command = f'from .{view} import {view}'
        exec(command)

exec(f'__all__ = {all_views}')

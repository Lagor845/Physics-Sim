import os
from importlib import import_module
from inspect import getmembers,isclass

scripts = []
for file in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "\\scripts"):
    if file.endswith(".py"):
        imported_script = import_module(f"scripts.{file.replace(".py","")}")
        desired_class = getmembers(imported_script,isclass)
        module = desired_class[0][1]()
        scripts.append(module)
from filehandling import *

options = readFile("options", emptyOptions)
for i in options.keys():
    exec(i + " = " + str(options[i]))

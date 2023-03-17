# - get inputs from var and con files
# - get most constrained variable and least constrained value
# - imlpement backtracking and forward checking

import sys

var_file = sys.argv[1]
con_file = sys.argv[2]
procedure = sys.argv[3]

variables = []
constraints = []

def readFile():
    file1 = open(var_file, "r")
    for x in file1:
        nums_str = x[3:]
        variables.append(list(map(int, nums_str.split())))

    file2 = open(con_file, "r")
    for x in file2:
        constraints.append(x.strip())

def backtracking():
    pass

def forwardChecking():
    pass


readFile()
print(variables)
print(constraints)

if procedure == "none":
    backtracking()
elif procedure == "fc":
    forwardChecking()
else:
    print("Not valid input")

# - get inputs from var and con files
# - get most constrained variable and least constrained value
# - imlpement backtracking and forward checking

import sys

var_file = sys.argv[1]
con_file = sys.argv[2]
procedure = sys.argv[3]


variables = {}
constraints = []

def readFile():
    file1 = open(var_file, "r")
    for x in file1:
        var = x[0:1]
        nums_str = x[3:]
        variables[var] = (list(map(int, nums_str.split())))

    file2 = open(con_file, "r")
    for x in file2:
        constraints.append(x.strip())

def mostConstrainedVar():

    pass

def leastConstringVal():
    pass

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


"""
function rec_bactracking (assignment, csp):
    if assignment == complete:
        return assignment
    select var: from unassigned-variables(Variables[csp], assignment, csp)
    for each value in Order-Domain-Values(var, assignment, csp) do:
        if value is consistent with assignment:
            add {var = value} to assignment
            result = Recursive-Backtracking(assignment, csp)
            if result != failure
                return result
            remove {var = value} from assignment
    return failure
"""

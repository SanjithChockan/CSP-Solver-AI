# - get inputs from var and con files
# - get most constrained variable and least constrained value
# - imlpement backtracking and forward checking

import sys
from collections import OrderedDict

var_file = sys.argv[1]
con_file = sys.argv[2]
procedure = sys.argv[3]

variables = {}
constraints = []
line_counter = 0

def readFile():
    file1 = open(var_file, "r")
    for x in file1:
        var = x[0:1]
        nums_str = x[3:]
        variables[var] = (list(map(int, nums_str.split())))

    file2 = open(con_file, "r")
    for x in file2:
        constraints.append(x.strip())


def most_constrained_var(unassigned_variables, current_constraints):

    # Get keys with the smallest domains
    min_val = min([len(unassigned_variables[key]) for key in unassigned_variables])
    min_keys = []
    for key in unassigned_variables:
        if len(unassigned_variables[key]) == min_val:
            min_keys.append(key)

    if len(min_keys) == 1:
        return [min_keys[0], unassigned_variables[min_keys[0]]]

    var_involved_count = {}
    # Implement degree heurist to check how many constrains the keys are involved in
    for key in min_keys:
        count = 0
        for const in current_constraints:
            if key in const:
                count += 1
        var_involved_count[key] = count
    
    # Get keys with the smallest count
    max_count = max([var_involved_count[key] for key in var_involved_count])
    res = []
    for key in var_involved_count:
        if var_involved_count[key] == max_count:
            res.append(key)
    
    res.sort()
    return [res[0], unassigned_variables[res[0]]]

def least_constring_val(var_and_domain, unassigned_variables, current_constraints):
    count_dict = {}
    
    var, domain = var_and_domain
    for d in domain:
        count_dict[d] = 0
        for unassigned_var in unassigned_variables:
            for const in current_constraints:
                if var in const and  unassigned_var in const:
                    
                    for b in unassigned_variables[unassigned_var]:
                        const_list = const.split(" ")
                        var_and_value = {}

                        if var == const_list[0]:
                            var_and_value[ "first_var"] = d
                            var_and_value[ "second_var"] = b
                        else:
                            var_and_value[ "first_var"] = b
                            var_and_value[ "second_var"] = d
                        
                        if const_list[1] == '!':
                            if var_and_value[ "first_var"] != var_and_value[ "second_var"]:
                                count_dict[d] += 1
                        elif const_list[1] == '>':
                            if var_and_value[ "first_var"] > var_and_value[ "second_var"]:
                                count_dict[d] += 1
                        elif const_list[1] == '<':
                            if var_and_value[ "first_var"] < var_and_value[ "second_var"]:
                                count_dict[d] += 1
                        elif const_list[1] == '=':
                            if var_and_value[ "first_var"] == var_and_value[ "second_var"]:
                                count_dict[d] += 1
                    
    sorted_count_dict = OrderedDict(sorted(count_dict.items(), key=lambda x:x[1], reverse=True))
    return sorted_count_dict.keys()
     
def is_complete(assignment):
    for a in assignment:
        if assignment[a] == None:
            return False
    return True


def assignment_consistent(assignment, val, ordered_var, overall_constraints, assignment_order):
    var, domain = ordered_var
    for a in assignment:
        if assignment[a] != None:
            for const in overall_constraints:
                if a in const and var in const:
                    const_list = const.split(" ")
                    var_and_value = {}

                    if var == const_list[0]:
                        var_and_value[ "first_var"] = val
                        var_and_value[ "second_var"] = assignment[a]
                    else:
                        var_and_value[ "first_var"] = assignment[a]
                        var_and_value[ "second_var"] = val
                    
                    global line_counter
                    if const_list[1] == '!':
                        if not(var_and_value[ "first_var"] != var_and_value[ "second_var"]):
                            assignment[var] = val
                            line_counter += 1
                            print(f"{line_counter}. {print_in_order(assignment, assignment_order)}  failure")
                            assignment[var] = None
                            return False
                    elif const_list[1] == '>':
                        if not(var_and_value[ "first_var"] > var_and_value[ "second_var"]):
                            assignment[var] = val
                            line_counter += 1
                            print(f"{line_counter}. {print_in_order(assignment, assignment_order)}  failure")
                            assignment[var] = None
                            return False
                    elif const_list[1] == '<':
                        if not(var_and_value[ "first_var"] < var_and_value[ "second_var"]):
                            assignment[var] = val
                            line_counter += 1
                            print(f"{line_counter}. {print_in_order(assignment, assignment_order)}  failure")
                            assignment[var] = None
                            return False
                    elif const_list[1] == '=':
                        if not(var_and_value[ "first_var"] == var_and_value[ "second_var"]):
                            assignment[var] = val
                            line_counter += 1
                            print(f"{line_counter}. {print_in_order(assignment, assignment_order)}  failure")
                            assignment[var] = None
                            return False
    return True

def print_in_order(assignment, assignment_order):
    res = []
    for ao in assignment_order:
        res.append(f"{ao}={assignment[ao]}")
    combined_str = ", ".join(res)
    return(combined_str)

def backtracking(assignment, variables, constraints, overall_constraints, assignment_order):

    if is_complete(assignment):
        global line_counter
        print(f"{line_counter+1}. {print_in_order(assignment, assignment_order)}  solution")
        return assignment
    
    ordered_var = most_constrained_var(variables, constraints)
    
    # update current unassigned variables and current constraints
    del variables[ordered_var[0]]
    current_constraints = []
    for c in constraints:
        if ordered_var[0] not in c:
            current_constraints.append(c)

    order_domain_values = least_constring_val(ordered_var, variables, constraints)
    assignment_order.append(ordered_var[0])

    for val in order_domain_values:
        if assignment_consistent(assignment, val, ordered_var, overall_constraints, assignment_order):
            assignment[ordered_var[0]] = val
    
            result = backtracking(assignment.copy(), variables.copy(), current_constraints.copy(), overall_constraints, assignment_order.copy())
            
            if result != "FAILURE":
                return result


            assignment[ordered_var[0]] = None

    return "FAILURE"

def forwardChecking():
    pass

readFile()

vars = variables.keys()
assignment = {}
for v in vars:
    assignment[v] = None

backtracking(assignment, variables, constraints, constraints.copy(), [])





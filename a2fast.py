import random
import time
import copy

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################


# A clause consists of a set of symbols, each of which is negated
# or not. A clause where
# clause.symbols = {"a": 1, "b": -1, "c": 1}
# corresponds to the statement: a OR (NOT b) OR c .
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# A SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.
class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

    # Takes as input an assignment to symbols and returns True or
    # False depending on whether the instance is satisfied.
    # Input:
    # - assignment: Dictionary of the format {symbol: sign}, where sign
    #       is either 1 or -1.
    # Output: True or False
    def is_satisfied(self, assignment):
        ###########################################
        # Start your code
        if len(self.clauses) == 0:
            return True
        for clause in self.clauses:
            if len(clause.symbols) == 0:
                return False
            check = 0
            for symbol in clause.symbols:
                for asign in assignment:
                    if symbol == asign:
                        if clause.symbols[symbol]*assignment[asign] == 1:
                            check = 1
            if check == 0:
                return False
        return True

    def popularSymbol(self):
        popularity = {} 
        for symbol in self.symbols:
            popularity[symbol] = 0
        for clause in self.clauses:
            for symbol in clause.symbols:
                popularity[symbol] += 1
        popular = 0
        for n in range(len(popularity)):
            if popularity[self.symbols[n]] > popularity[self.symbols[popular]]:
                popular = n
        popular = self.symbols[popular] 
        return popular

    def popInClause(self, clauseI):
        popularity = {}
        popularI = [] 
        for symbol in self.clauses[clauseI].symbols:
            popularity[symbol] = 0
            popularI.append(symbol)
        for clause in self.clauses:
            for symbol in clause.symbols:
                if symbol in popularI:
                    popularity[symbol] += 1
        popular = popularI[0]
        for n in popularI:
            if popularity[n] > popularity[popular]:
                popular = n
        return popular

    def smallestClause(self):
        small = 0
        for n in range(len(self.clauses)):
            if len(self.clauses[n].symbols) < len(self.clauses[small].symbols):
                small = n
        return small

def solve_dpll(instance):
    ###########################################
    # Start your code
    assignment = {}
    if instance.is_satisfied(assignment):
        return assignment
   
    n = 0
    while n in range(len(instance.clauses)):
        if len(instance.clauses[n].symbols) == 0:
            return False                           
        elif len(instance.clauses[n].symbols) == 1:
            unitName = list(instance.clauses[n].symbols.keys())[0]
            unitValue = instance.clauses[n].symbols[unitName]
            assignment[unitName] = unitValue
            instance = (simplify(instance, unitName, unitValue))
            n = -1
        n = n + 1
    
    n = 0


    while n < len(instance.symbols):                                  #Pure literal elimination step
        i = 0
        match = 0
        while(i < len(instance.clauses)):
            if match != 2:
                for a in list(instance.clauses[i].symbols.keys()):
                    if a == instance.symbols[n]:
                        if match == 0:
                            match = instance.clauses[i].symbols[a]
                        elif instance.clauses[i].symbols[a] == match:
                            pass
                        else:
                            match = 2                                   #assign 2 to match if this variable have different polarity
                i = i + 1                                               #in SAT instance
            else:
                break                                              

        if match != 2 and match != 0:                                              # eliminate variable if it occur only with one polarity
            assignment[instance.symbols[n]] = match
            instance = simplify(instance, instance.symbols[n], match)
            n = n - 1
        n = n + 1 


    if instance.is_satisfied(assignment):
        return assignment

    small = instance.smallestClause()
    if len(instance.symbols) < 203:
                                                                      #technique of solving an instance(trying to solve "smalles" clause)
        name = instance.popInClause(small)
        value = instance.clauses[small].symbols[name]
        

        trySatisfy = solve_dpll(simplify(instance, name, value*(-1)))        #assigning values to symbols from the smallest clause
        if type(trySatisfy) == dict:                                         #as smalles clause is the most "difficult" to satisfy
            assignment[name] = value*(-1)                                    #(I assign value*(-1) because this can help to find "wrong" solutions faster(and most of "solutions" are "wrong"))
            assignment.update(trySatisfy)
            return assignment
        
        else:
            tryBetter = solve_dpll(simplify(instance, name, value))             
            if type(tryBetter) == dict:                                         
                assignment[name] = value
                assignment.update(tryBetter)
                return assignment
    elif len(instance.symbols) > 789:                                                                   #if instance have 203 symbols or more, use other technique
        for n in instance.clauses:
            symb = []
            for s in n.symbols:
                symb.append(s)
                string = str(s)
                string += "\n"
                s1 = ""
            for i in instance.clauses:
                for symbol in i.symbols:
                    if symbol in symb:
                        string += str(i)
                        string += "\n"
                        for s in i.symbols:
                            if s not in symb:
                                symb.append(s)
                        break
                s1 += str(i)
                s1 += "\n"
            if len(symb) < len(instance.symbols):
                inst1 = SatInstance()
                inst2 = SatInstance()
                inst1.from_str(string)
                inst2.from_str(s1)
                True1 = solve_dpll(simplify(inst1, inst1.symbols[0], 1))
                if type(True1) == dict:
                    True2 = solve_dpll(simplify(inst2, inst2.symbols[0], 1))
                    if type(True2) == dict:
                        assignment[inst1.symbols[0]] = 1
                        assignment[inst2.symbols[0]] = 1
                        assignment.update(True1)
                        assignment.update(True2)
                        return assignment
                    False2 = solve_dpll(simplify(inst2, inst2.symbols[0], -1))
                    if type(False2) == dict:
                        assignment[inst1.symbols[0]] = 1
                        assignment[inst2.symbols[0]] = -1
                        assignment.update(True1)
                        assignment.update(False2)
                        return assignment
                    else:
                        return False
                False1 = solve_dpll(simplify(inst1, inst1.symbols[0], -1))
                if type(True1) == dict:
                    True2 = solve_dpll(simplify(inst2, inst2.symbols[0], 1))
                    if type(True2) == dict:
                        assignment[inst1.symbols[0]] = -1
                        assignment[inst2.symbols[0]] = 1
                        assignment.update(False1)
                        assignment.update(True2)
                        return assignment
                    False2 = solve_dpll(simplify(inst2, inst2.symbols[0], -1))
                    if type(False2) == dict:
                        assignment[inst1.symbols[0]] = -1
                        assignment[inst2.symbols[0]] = -1
                        assignment.update(False1)
                        assignment.update(False2)
                        return assignment
                    else:
                        return False
        popular = instance.popularSymbol()                                  #(try to assign value to a symbol which occur most times in instance)
        tryTrue = solve_dpll(simplify(instance, popular, 1))
        if type(tryTrue) == dict:
            assignment[popular] = 1
            assignment.update(tryTrue)
            return assignment
        tryFalse = solve_dpll(simplify(instance, popular, -1))
        if type(tryFalse) == dict:
            assignment[popular] = -1
            assignment.update(tryFalse)
            return assignment
    else:
        popular = instance.popularSymbol()                                  #(try to assign value to a symbol which occur most times in instance)
        tryTrue = solve_dpll(simplify(instance, popular, 1))
        if type(tryTrue) == dict:
            assignment[popular] = 1
            assignment.update(tryTrue)
            return assignment
        tryFalse = solve_dpll(simplify(instance, popular, -1))
        if type(tryFalse) == dict:
            assignment[popular] = -1
            assignment.update(tryFalse)
            return assignment


    return False





def simplify(instance, var, value):                                     #Given a SAT inctance, variable name and value simplify SAT instance
    updated = SatInstance()                                             #by assigning given value to all ocurances of a given variable,
                                                                        #deleting this variable from set of symbols, and deleting all clauses                                             
    updated.from_str(instance.__str__())                                #satisfyed by a given variable with a given value
    n = 0
    while(n < len(updated.clauses)):
        for symbol in updated.clauses[n].symbols:
            if symbol == var:
                if (updated.clauses[n].symbols[symbol] * value) == 1:
                    del updated.clauses[n]
                    n = n - 1
                    break
                else:
                    del updated.clauses[n].symbols[symbol]
                    n = n - 1
                    break
        n = n + 1

    for eSymbol in range(len(updated.symbols)):
        if updated.symbols[eSymbol] == var:
            del updated.symbols[eSymbol]
            break
    return updated


with open("bonus_instances.txt", "r") as input_file:
    instance_strs = input_file.read()

instance_strs = instance_strs.split("\n\n")
with open("bonus_assignments1.txt", "w") as output_file:
    for instance_str in instance_strs:
        if instance_str.strip() == "":
            continue
        instance = SatInstance()
        instance.from_str(instance_str)
        print(len(instance.symbols))
        assignment = solve_dpll(instance)
        print(instance.is_satisfied(assignment))
        for symbol_index, (symbol,sign) in enumerate(assignment.items()):
            if symbol_index != 0:
                output_file.write(" ")
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            output_file.write(token)
        output_file.write("\n")

# CIS 473/573
# CIS 473/573
# Homework #4
# Daniel Lowd
# February 2021
#
# TEMPLATE CODE
import itertools

# List of variable cardinalities is global, for convenience.
# NOTE: This is not a good software engineering practice in general.
# However, the autograder code currently uses it to set the variable 
# ranges directly without reading in a full model file, so please keep it
# here and use it when you need variable ranges!
var_ranges = []


#
# FACTOR CLASS -- EDIT HERE!
#

class Factor(dict):
    def __init__(self, scope_, vals_):
        self.scope = scope_
        self.vals = vals_
        self.stride = dict()
        temp = [0]*len(self.scope)
        temp[0] = 1
        for i in range(1, len(self.scope)):
            temp[i] = var_ranges[self.scope[i-1]] * temp[i-1]
        for j in range(len(self.scope)):
            self.stride[self.scope[j]] = temp[j]

        # TODO -- ADD EXTRA INITIALIZATION CODE IF NEEDED

    def __mul__(self, other):
        """Returns a new factor representing the product."""
        # TODO -- PUT YOUR MULTIPLICATION CODE HERE!
        j = 0
        k = 0
        new_scope = []

        for item1 in self.scope:
            new_scope.append(item1)
        for item2 in other.scope:
            if item2 not in new_scope:
                new_scope.append(item2)
        assignment = [0]*len(var_ranges)
        # calculating rows of factor table
        count = 1
        for item in new_scope:
            count *= var_ranges[item]

        new_vals = [0]*count

        for l in range(len(var_ranges)):
            assignment[l] = 0
        for i in range(count):
            new_vals[i] = self.vals[j] * other.vals[k]
            for y in new_scope:
                assignment[y] += 1
                if assignment[y] == var_ranges[y]:
                    assignment[y] = 0
                    if y in self.stride:
                        j -= (var_ranges[y]-1)*self.stride[y]
                    if y in other.stride:
                        k -= (var_ranges[y]-1)*other.stride[y]
                else:
                    if y in self.stride:
                        j += self.stride[y]
                    if y in other.stride:
                        k += other.stride[y]
                    break

        return Factor(new_scope, new_vals)


    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __repr__(self):
        """Return a string representation of a factor."""
        rev_scope = self.scope[::-1]
        val = "x" + ", x".join(str(s) for s in rev_scope) + "\n"
        itervals = [range(var_ranges[i]) for i in rev_scope]
        for i,x in enumerate(itertools.product(*itervals)):
            val = val + str(x) + " " + str(self.vals[i]) + "\n"
        return val

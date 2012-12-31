###
### template of code for Problem 4 of Problem Set 2, Fall 2008
###


bestSoFar = 0     # variable that keeps track of largest number
                  # of McNuggets that cannot be bought in exact quantity
packages = (7,11,13)   # variable that contains package sizes

def is_solvable(packages, n):
    x, y, z = packages
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if x*a + y*b + z*c == n:
                    return 1
    return 0

for n in range(1, 150):   # only search for solutions up to size 150
    ## complete code here to find largest size that cannot be bought
    ## when done, your answer should be bound to bestSoFar
    if not is_solvable(packages, n):
        bestSoFar = n
    #else:
    #    counter = 0
    #if counter == 6:
    #    bestSoFar = n - 6
    #    break

print bestSoFar

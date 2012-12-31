# Problem Set 4
# Name: 
# Collaborators: 
# Time: 

#
# Problem 1
#

def nestEggFixed(salary, save, growthRate, years):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: the annual percent increase in your investment account (an
      integer between 0 and 100).
    - years: the number of years to work.
    - return: a list whose values are the size of your retirement account at
      the end of each year.
    """
    assert years >= 0, "years must be a positive integer."
    savings_record = [0] * years
    if years >= 1:
        for year in range(years):
            savings_record[year] = savings_record[year-1] * (1 + 0.01*growthRate) + salary*save*0.01

    return savings_record
    # if years <= 1:
    #     return salary * save * 0.01 * years
    # else:
    #     return salary * save * 0.01 + nestEggFixed(salary, save, growthRate, years-1) * (1 + growthRate * 0.01)

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]

    # TODO: Add more test cases here.

#
# Problem 2
#

def nestEggVariable(salary, save, growthRates):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: a list of the annual percent increases in your investment
      account (integers between 0 and 100).
    - return: a list of your retirement account value at the end of each year.
    """
    assert len(growthRates) >= 0, "years must be a positive integer."
    savings_record = [0]*len(growthRates)
    if len(growthRates) >= 1:
        for i in range(len(growthRates)):
            savings_record[i] = savings_record[i-1] * (1 + 0.01*growthRates[i]) + salary*save*0.01

    return savings_record


def testNestEggVariable():
    salary      = 10000
    save        = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]

    # TODO: Add more test cases here.

#
# Problem 3
#

def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    assert len(growthRates) >= 0, "years must be a positive integer."
    savings_record = [savings] * len(growthRates)
    if len(growthRates) >= 1:
        for i in range(len(growthRates)):
            savings_record[i] = savings_record[i-1] * (1 + 0.01*growthRates[i]) - expenses

    return savings_record

def testPostRetirement():
    savings     = 5266.26
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 1229.95548986
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print savingsRecord
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]

    # TODO: Add more test cases here.

#
# Problem 4
#

def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates, epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """
    savings = nestEggVariable(salary, save, preRetireGrowthRates)[-1]
    low = 0
    high = savings
    guess = (low + high)/2.0
##    while abs(postRetirement(savings, postRetireGrowthRates, guess)[-1]) > epsilon:
##        savings_left = postRetirement(savings, postRetireGrowthRates, guess)[-1]
##        print 'guess: ', guess, 'savings_left: ', savings_left
##        if savings_left > 0:
##            low = guess
##        else:
##            high = guess
##        guess = (low + high)/2.0
##    print 'Estimate: ', guess
##    return guess
    return _find(savings, postRetireGrowthRates, epsilon, low, high)

# Binary search, recursively
def _find(savings, postRetireGrowthRates, epsilon, low, high):
    guess = (low + high)/2.0
    savings_left = postRetirement(savings, postRetireGrowthRates, guess)[-1]
    print 'guess: ', guess, 'savings_left: ', savings_left
    if abs(savings_left) < epsilon:
        return guess
    elif savings_left > 0:
        low = guess
        return _find(savings, postRetireGrowthRates, epsilon, low, high)
    else:
        high = guess
        return _find(savings, postRetireGrowthRates, epsilon, low, high)


def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print expenses
    # Output should have a value close to:
    # 1229.95548986

    # TODO: Add more test cases here.

if __name__ == '__main__':
    #testNestEggFixed()
    #testNestEggVariable()
    #testPostRetirement()
    testFindMaxExpenses()

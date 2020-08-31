import sys
import math
import copy
from gurobipy import *

from task import Task
from meal import Meal

def createInvervalsForDays(availablePeriods):
    availableIntervals = {}

    for day in availablePeriods.keys():
        availableIntervals[day] = createInvervals(availablePeriods[day][0], availablePeriods[day][1])
    
    return availableIntervals


def createInvervals(startTime, endTime):
    interval = 15
    startTime = startTime.split(':')
    endTime = endTime.split(':')

    intervals = {}
    intervalId = 1
    hour = int(startTime[0])
    minute = int(startTime[1])
    
    while hour < int(endTime[0]):
        iterator = 0
        while minute < 60:
            intervals[(hour, minute)] = intervalId
            minute += interval
            iterator += 1
            intervalId += 1

        if (minute > 60):
            minute = 15
        else:
            minute = 0

        hour += 1

    iterator = 0
    while minute < int(endTime[1]):
        intervals[(hour, minute)] = intervalId
        minute += interval
        iterator += 1
        intervalId += 1

    return intervals


def createBusyIntervals(busyPeriods):
    busyIntervals = {}

    busyIntervalId = 1
    for day in busyPeriods.keys():
        tempIntervals = []
        for period in busyPeriods[day].keys():
            tempIntervals.append(createInvervals(busyPeriods[day][period][0], busyPeriods[day][period][1]))

        intervals = []
        busyIntervals[day] = {}
        for interval in tempIntervals:
            for key in interval.keys():
                busyIntervals[day][key] = busyIntervalId
            busyIntervalId += 1

    return busyIntervals


def readFile(lines):
    numberOfDays = int(lines[0])
    iterator = 1
    
    D = {}
    while iterator <= numberOfDays:
        availablePeriod = lines[iterator].strip('\n').split(' ')
        D[availablePeriod[0]] = (availablePeriod[1], availablePeriod[2])
        iterator += 1
    
    U = createInvervalsForDays(D)
    daysId = {}

    i = 1
    for day in D.keys():
        D[day] = i
        daysId[i] = day
        i += 1

    numberOfBusyPeriods = int(lines[iterator])
    iterator += 1
    busyPeriods = {}
    busyPeriodId = 1
    while iterator <= (numberOfDays + numberOfBusyPeriods + 1):
        busyPeriodsPerDay = lines[iterator].strip('\n').split(' ')
        
        periods = {}
        periodsIterator = 2
        for i in range(int(busyPeriodsPerDay[1])):
            periods[i + 1] = (busyPeriodsPerDay[periodsIterator], busyPeriodsPerDay[periodsIterator + 1])
            periodsIterator += 2
        
        busyPeriods[busyPeriodsPerDay[0]] = periods
        iterator += 1

    busyIntervals = createBusyIntervals(busyPeriods)

    A = {}
    E = {}
    c = {}
    b = {}

    intervals = U

    numberOfTasks = int(lines[iterator])
    iterator += 1
    tasks = {}
    while iterator <= (numberOfDays + numberOfBusyPeriods + numberOfTasks + 2):
        line = lines[iterator].strip('\n').split(' ')
        
        daysItMustBeDone = []
        numberOfDaysItMustBeDone = int(line[2])
        for i in range(numberOfDaysItMustBeDone):
            daysItMustBeDone.append(line[i + 3])

        itMustBeDoneBeforeBusyInterval = False
        busyIntervalThatTheTaskMustBeDoneBefore = 0
        if (line[int(line[2]) + 4] != '-1'):
            itMustBeDoneBeforeBusyInterval = True
            interval = line[int(line[2]) + 6].split(':')
            busyIntervalThatTheTaskMustBeDoneBefore = (line[int(line[2]) + 5], (int(interval[0]), int(interval[1])))

        A[line[0]] = None
        E[line[0]] = daysItMustBeDone
        c[line[0]] = int(line[1]) * 4
        b[line[0]] = int(line[int(line[2]) + 3]) * 4 

        tasks[line[0]] = Task(line[0], int(line[1]) * 4, daysItMustBeDone, int(line[int(line[2]) + 3]) * 4,
                              itMustBeDoneBeforeBusyInterval, busyIntervalThatTheTaskMustBeDoneBefore)
        iterator += 1

    N = {}
    m = {}
    h = {}

    for task in tasks.keys():
        if (tasks[task].busyIntervalThatTheTaskMustBeDoneBefore != 0):
            N[task] = None
            m[task] = U[tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[0]][(tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[1][0], tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[1][1])]
            h[task] = D[tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[0]]

    R = {}
    t = {}
    y = {}

    numberOfMeals = int(lines[iterator])
    iterator += 1
    meals = {}
    while iterator <= (numberOfDays + numberOfBusyPeriods + numberOfTasks + numberOfMeals + 3):
        line = lines[iterator].strip('\n').split(' ')

        R[line[0]] = int(int(line[3]) / 15)

        t[line[0]] = {}
        y[line[0]] = {}

        meals[line[0]] = Meal(line[0], line[1], line[2], line[3])

        for day in U.keys():
            startInterval = meals[line[0]].possibleIntervals[0]
            endInterval = meals[line[0]].possibleIntervals[-1]
            t[line[0]][day] = U[day][(int(startInterval[0]), (int(startInterval[1])))]
            y[line[0]][day] = U[day][(int(endInterval[0]), (int(endInterval[1])))]

        iterator += 1

    L = A.copy()

    for meal in R.keys():
        L[meal] = None

    I = copy.deepcopy(U)

    for day in busyIntervals.keys():
        for interval in busyIntervals[day].keys():
            del I[day][interval]

    return D, U, A, E, c, b, N, m, h, R, t, y, L, I, busyIntervals, daysId


def getVariables(model, L, U, D):
    x = {}
    for day in D.keys():
        x[day] = {}
        for interval in U[day].values():
            x[day][interval] = {}
            for task in L.keys():
                x[day][interval][task] = model.addVar(vtype=GRB.BINARY, name='x_' + str(day) + '_' + str(interval) + '_' + str(task))

    return x


def setConstraints(model, x, D, I, L, c, A, R, t, y, E, O, b, U, N, h, m, daysId):
    # Restrição (2) OK
    for day in D.keys():
        for interval in I[day].keys():
            model.addConstr(quicksum(x[day][I[day][interval]][task] for task in L.keys()) <= 1)

    # Restrição (3) OK
    for task in A.keys():
        model.addConstr(quicksum(x[day][interval][task] for day in D.keys() for interval in I[day].values()) == c[task])
    
    # Restrição (4)
    for task in A.keys():
        for day in E[task]:
            model.addConstr(quicksum(x[day][interval][task] for interval in U[day].values()) >= b[task])

    # Restrição (5)
    for task in N.keys():
        model.addConstr((c[task] - quicksum(x[daysId[day]][interval][task] for day in range(1, h[task]) for interval in I[day].values()) - quicksum(x[daysId[h[task]]][interval][task] for interval in range(1, m[task]))) == 0)

    # Restrição (6) OK
    for day in D.keys():
        for meal in R.keys():
            model.addConstr(quicksum(x[day][interval][meal] for interval in range(t[meal][day], y[meal][day] + 1)) == R[meal])

    # Restrição (7) OK
    for task in A.keys():
        for day in E[task]:
            model.addConstr(quicksum(x[day][interval][task] for interval in I[day].values()) >= 1)

    # Restrição (8)
    for day in O.keys():
        model.addConstr(quicksum(x[day][U[day][interval]][task] for interval in O[day].keys() for task in L.keys()) == 0, name='qwertyuiokjhgfdsdfhjgfdertyjk,mnb')


def main():
    fileName = ''.join(sys.argv[1:])
    file = open(fileName, "r")
    lines = file.readlines()

    D, U, A, E, c, b, N, m, h, R, t, y, L, I, O, daysId = readFile(lines)

    model = Model()

    x = getVariables(model, L, U, D)

    model.setObjective(quicksum(x[day][interval][task] for task in L.keys() for day in D.keys() for interval in I[day].values()), GRB.MINIMIZE)

    setConstraints(model, x, D, I, L, c, A, R, t, y, E, O, b, U, N, h, m, daysId)
    
    model.write("saida-modelo.lp")
    
    model.optimize()

    vars = model.getVars()

    for var in vars:
        print(var)


if __name__ == "__main__":
    main()
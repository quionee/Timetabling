class Heuristic:

    def __init__(self, intervals, busyIntervals, tasks, meals):
        self.intervals = intervals
        self.busyIntervals = busyIntervals
        self.tasks = tasks
        self.meals = meals


    def heuristic(self):
        self.assignMeals()
        self.sortTasks()

        for task in self.tasks.keys():
            if (self.tasks[task].daysItMustBeDone != []):
                for day in self.tasks[task].daysItMustBeDone:
                    consecutiveIntervals = 0
                    itHasConsecutiveMinimumWorkload = False
                    intervals = []
                    for interval in self.intervals[day].keys():
                        if (self.intervals[day][interval] == 0):
                            consecutiveIntervals += 1
                            intervals.append(interval)
                        else:
                            consecutiveIntervals = 0
                            intervals = []

                        if (consecutiveIntervals == self.tasks[task].consecutiveMinimumWorkload):
                            itHasConsecutiveMinimumWorkload = True
                            break
                    
                    if itHasConsecutiveMinimumWorkload:
                        for interval in intervals:
                            self.intervals[day][interval] = task
            else:
                for day in self.intervals.keys():
                    if (self.tasks[task].workload < self.tasks[task].totalWorkload):
                        consecutiveIntervals = 0
                        itHasConsecutiveMinimumWorkload = False
                        intervals = []
                        for interval in self.intervals[day].keys():
                            if (self.intervals[day][interval] == 0):
                                consecutiveIntervals += 1
                                intervals.append(interval)
                            else:
                                consecutiveIntervals = 0
                                intervals = []

                            if (consecutiveIntervals == self.tasks[task].consecutiveMinimumWorkload):
                                itHasConsecutiveMinimumWorkload = True
                                break
                        
                        if itHasConsecutiveMinimumWorkload:
                            for interval in intervals:
                                self.intervals[day][interval] = task
                                self.tasks[task].workload += 1

        print('\n\n\n---------- Intervals considering Busy Intervals ----------\n')
        for day in self.intervals.keys():
            print(day, ':', self.intervals[day], '\n')


    def assignMeals(self):
        for day in self.intervals.keys():
            for meal in self.meals.keys():
                possibleIntervalPos = 0
                consecutiveIntervals = 0
                while consecutiveIntervals < self.meals[meal].duration:
                    if (self.intervals[day][self.meals[meal].possibleIntervals[possibleIntervalPos]] == 0):
                        consecutiveIntervals += 1
                    else:
                        consecutiveIntervals = 0
                    
                    possibleIntervalPos += 1
                
                possibleIntervalPos -= 1
                while consecutiveIntervals > 0:
                    self.intervals[day][self.meals[meal].possibleIntervals[possibleIntervalPos]] = meal

                    consecutiveIntervals -= 1
                    possibleIntervalPos -= 1
        
    def sortTasks(self):
        tasks = {}
        for task in self.tasks.keys():
            tasks[(len(self.tasks[task].daysItMustBeDone), task)] = None
        
        sortedTasks = {}
        while len(tasks) > 0:
            numberMaxTask = [max(tasks)[0], max(tasks)[1]]
            sortedTasks[numberMaxTask[1]] = self.tasks[numberMaxTask[1]]
            del tasks[(numberMaxTask[0], numberMaxTask[1])]

        self.tasks = sortedTasks
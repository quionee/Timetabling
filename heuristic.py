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
            currentIntervals = self.intervals
            if (self.tasks[task].daysItMustBeDone != []):
                currentIntervals = self.tasks[task].daysItMustBeDone

            while self.tasks[task].workload < self.tasks[task].totalWorkload:
                for day in currentIntervals:
                    consecutiveIntervals = 0
                    itHasConsecutiveMinimumWorkload = False
                    intervals = []
                    
                    for interval in self.intervals[day].keys():
                        if (self.intervals[day][interval] == 0):
                            consecutiveIntervals += 1
                            intervals.append(interval)
                        elif ((consecutiveIntervals > 0) and ((str(self.intervals[day][interval]).split('_')[0] == 'Refeição'))):
                            if ((str(self.intervals[day][self.meals[self.intervals[day][interval]].possibleIntervals[-1]]).split('_')[0] != 'Refeição') and self.moveIntervalsForward(day, interval, self.intervals[day][interval])):
                                consecutiveIntervals += 1
                                intervals.append(interval)
                        else:
                            consecutiveIntervals = 0
                            intervals = []
                        
                        if (consecutiveIntervals == self.tasks[task].consecutiveMinimumWorkload):
                            itHasConsecutiveMinimumWorkload = True
                            break
                        
                    if (self.tasks[task].itMustBeDoneBeforeBusyInterval):
                        if ((self.tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[0] == day) and (self.tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[1] == interval)):
                            break
                            
                    if itHasConsecutiveMinimumWorkload:
                        for interval in intervals:
                            self.intervals[day][interval] = task
                        
                        self.tasks[task].workload += consecutiveIntervals

                    if (self.tasks[task].workload == self.tasks[task].totalWorkload):
                        break
                    
                    if (self.tasks[task].itMustBeDoneBeforeBusyInterval and (self.tasks[task].busyIntervalThatTheTaskMustBeDoneBefore[0] == day)):
                        break


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


    def moveIntervalsForward(self, day, interval, meal):
        newIntervals = []
        for i in range(len(self.meals[meal].possibleIntervals)):
            if (str(self.intervals[day][self.meals[meal].possibleIntervals[i]]) == meal):
                newIntervals.append(i + 1)
        try:
            self.intervals[day][self.meals[meal].possibleIntervals[newIntervals[-1]]] = meal
            self.intervals[day][self.meals[meal].possibleIntervals[newIntervals[0] - 1]] = 0
        except IndexError:
            return False


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
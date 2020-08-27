class Heuristic:

    def __init__(self, intervals, busyIntervals, tasks, meals):
        self.intervals = intervals
        self.busyIntervals = busyIntervals
        self.tasks = tasks
        self.meals = meals


    def heuristic(self):
        # 1. Definir os invervalos possíveis para os dias OK
        # 2. Preencher os horários ocupados OK
        # 3. Alocar os horários de refeição a partir dos primeiros intervalos
        #    livres (dentro do escopo possível para refeições). OK
        # 4. Ordenar de forma descrescente as atividades por quantidade de dias que ela DEVE ser realizada. OK
        # 5. Para todas as atividades a serem alocadas, fazer:
        #     (a) Se atividade tem dias específicos para ser realizada, para cada dia (aleatoriamente)
        #         possível pela atividade, fazer:
        #         i. Alocar a carga horária mínima consecutiva a partir do primeiro intervalo livre do dia.
        #     (b) Se a carga horária total da atividade dividida pela quantidades de dias em que ela pode
        #         ser alocada for maior que a carga horária mínima consecutiva, repetir passo (a).

        self.assignMeals()
        self.sortTasks()

        print('\n\n\n---------- Intervals considering Busy Intervals ----------\n')
        for day in self.intervals.keys():
            print(day, ':', self.intervals[day], '\n')

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










    # def test(self):
    #     print('\n\n---------- Busy Intervals ----------\n')
    #     for day in self.busyIntervals.keys():
    #         print(day, ':', self.busyIntervals[day])

    #     print('\n\n\n---------- Intervals considering Busy Intervals ----------\n')
    #     for day in self.intervals.keys():
    #         print(day, ':', self.intervals[day], '\n')

    #     print('\n\n---------- Tasks ----------\n')
    #     for task in self.tasks.keys():
    #         print(self.tasks[task].name, ':', self.tasks[task].workload, self.tasks[task].daysItMustBeDone, self.tasks[task].consecutiveMinimumWorkload, self.tasks[task].itMustBeDoneBeforeBusyInterval, self.tasks[task].busyIntervalThatTheTaskMustBeDoneBefore)

    #     print('\n\n\n---------- Meals ----------\n')
    #     for meal in self.meals.keys():
    #         print(meal, ':', self.meals[meal].possibleIntervals, self.meals[meal].duration)
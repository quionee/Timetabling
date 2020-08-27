class Task:

    def __init__(self, name, workload, daysItMustBeDone, consecutiveMinimumWorkload,
                 itMustBeDoneBeforeBusyInterval, busyIntervalThatTheTaskMustBeDoneBefore):
        self.name = name
        self.workload = 0
        self.totalWorkload = workload
        self.daysItMustBeDone = daysItMustBeDone
        self.consecutiveMinimumWorkload = consecutiveMinimumWorkload
        self.itMustBeDoneBeforeBusyInterval = itMustBeDoneBeforeBusyInterval
        self.busyIntervalThatTheTaskMustBeDoneBefore = busyIntervalThatTheTaskMustBeDoneBefore


    def checkConsecutiveMinimumWorkload():
        print('yeah')

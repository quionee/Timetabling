class Task:
    def __init__(self, name, workload, daysItMustBeDone, consecutiveMinimumWorkload,
                 itMustBeDoneBeforeBusyInterval, busyIntervalThatTheTaskMustBeDoneBefore):
        self.name = name
        self.workload = workload
        self.daysItMustBeDone = daysItMustBeDone
        self.consecutiveMinimumWorkload = consecutiveMinimumWorkload
        self.itMustBeDoneBeforeBusyInterval = itMustBeDoneBeforeBusyInterval
        self.busyIntervalThatTheTaskMustBeDoneBefore = busyIntervalThatTheTaskMustBeDoneBefore

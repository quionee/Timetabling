class Meal:

    def __init__(self, startTimeLimit, endTimeLimit, duration):
        self.possibleIntervals = self.createPossibleIntervals(startTimeLimit, endTimeLimit)
        self.duration = int(int(duration) / 15)


    def createPossibleIntervals(self, startTimeLimit, endTimeLimit):
        interval = 15
        startTimeLimit = startTimeLimit.split(':')
        endTimeLimit = endTimeLimit.split(':')

        possibleIntervals = []
        hour = int(startTimeLimit[0])
        minute = int(startTimeLimit[1])
        
        while hour < int(endTimeLimit[0]):
            iterator = 0
            while minute < 60:
                possibleIntervals.append((hour, minute))
                minute += interval
                iterator += 1

            if (minute > 60):
                minute = 15
            else:
                minute = 0

            hour += 1

            iterator = 0

        while minute < int(endTimeLimit[1]):
            possibleIntervals.append((hour, minute))
            minute += interval
            iterator += 1

        return possibleIntervals
    

    # def itsWhithinTheScope(self):


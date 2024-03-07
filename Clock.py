
import time
import datetime
from ClockDriver import ClockDriver

class ClockController(object):
    def __init__(self):
        self.clockDriver :  ClockDriver = None

    def digitToSevenSeg(self, digit):
        if digit == None:
            return [0] * 7
        elif digit == 0:
            return [1, 1, 1, 1, 1, 1, 0]
        elif digit == 1:
            return [0, 1, 1, 0, 0, 0, 0]
        elif digit == 2:
            return [1, 1, 0, 1, 1, 0, 1]
        elif digit == 3:
            return [1, 1, 1, 1, 0, 0, 1]
        elif digit == 4:
            return [0, 1, 1, 0, 0, 1, 1]
        elif digit == 5:
            return [1, 0, 1, 1, 0, 1, 1]
        elif digit == 6:
            return [1, 0, 1, 1, 1, 1, 1]
        elif digit == 7:
            return [1, 1, 1, 0, 0, 0, 0]
        elif digit == 8:
            return [1] * 7
        elif digit == 9:
            return [1, 1, 1, 1, 0, 1, 1]
        else:
            return [0, 0, 0, 0, 0, 0, 1]

    def setDigit(self, digit, val):
        segs = self.digitToSevenSeg(val)
        for i in range(7):
            self.clockDriver.setSegment(digit, i, segs[i])

    def setTime(self):
        now = datetime.datetime.now()
        h = now.hour
        m = now.minute
        s = now.second

        self.setDigit('oneSec', s % 10)
        self.setDigit('tenSec', s // 10)
        self.setDigit('oneMin', m % 10)
        self.setDigit('tenMin', m // 10)
        self.setDigit('oneHour', h % 10)
        self.setDigit('tenHour', h // 10)


if __name__ == "__main__":
    this = ClockController()
    while True:
        this.clear()
        this.setSegment(23, True)
        this.setSegment(31, True)
        this.setTime()
        this.output()

        #We want to sleep until just after the next second
        now = datetime.datetime.now()
        delayus = 1e6 - now.microsecond
        delay = delayus / float(1e6)
        time.sleep(delay)

from ClockDriver import ClockDriver
import RPi.GPIO as GPIO

# 00: 1hr G
# 01: 1hr F
# 02: 1hr A
# 03: 1hr B
# 04: 1hr C
# 05: 1hr D
# 06: 1hr E
# 07: PM
# 08: 10hr G
# 09: 10hr F
# 10: 10hr A
# 11: 10hr B
# 12: 10hr C
# 13: 10hr D
# 14: 10hr E
# 15: AM
# 16: 1min G
# 17: 1min F
# 18: 1min A
# 19: 1min B
# 20: 1min C
# 21: 1min D
# 22: 1min E
# 23: minute-second colon
# 24: 10min G
# 25: 10min F
# 26: 10min A
# 27: 10min B
# 28: 10min C
# 29: 10min D
# 30: 10min E
# 31: hour-minute colon
# 32: 1sec G
# 33: 1sec F
# 34: 1sec A
# 35: 1sec B
# 36: 1sec C
# 37: 1sec D
# 38: 1sec E
# 39: unused?
# 40: 10sec G
# 41: 10sec F
# 42: 10sec A
# 43: 10sec B
# 44: 10sec C
# 45: 10sec D
# 46: 10sec E
# 47: unused?


class IvationDriver(ClockDriver):
    def __init__(self):
        ClockDriver.__init__()
        self.clockPin = 20
        self.dataPin = 21
        self.latchPin = 16
        self.otherPin = 19

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.clockPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.dataPin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.otherPin, GPIO.OUT, initial=GPIO.HIGH)

        self.data = [0] * 6

        self.oneSecIndices = [34, 35, 36, 37, 38, 33, 32]
        self.tenSecIndices = [42, 43, 44, 45, 46, 41, 40]
        self.oneMinIndices = [18, 19, 20, 21, 22, 17, 16]
        self.tenMinIndices = [26, 27, 28, 29, 30, 25, 24]
        self.oneHourIndices = [2, 3, 4, 5, 6, 1, 0]
        self.tenHourIndices = [10, 11, 12, 13, 14, 9, 8]

    def clear(self):
        self.data = [0] * 6

    def _setSegmentByIndex(self, segIndex, val):
        block = segIndex // 8
        bit = segIndex % 8
        if val:
            self.data[block] |= (1 << bit)
        else:
            self.data[block] &= ~(1 << bit)

    def _outputByte(self, theByte):
        for i in range(8):
            val = bool((theByte >> i) & 1)
            GPIO.output(self.dataPin, not val)
            GPIO.output(self.clockPin, True)
            GPIO.output(self.clockPin, False)

    def writeOutputs(self):
        #GPIO.output(self.otherPin, True)
        #time.sleep(0.007)

        for i in range(6):
            self.outputByte(self.data[i])
            #time.sleep(0.002)

        GPIO.output(self.latchPin, True)
        GPIO.output(self.latchPin, False)
        #time.sleep(0.001)
        GPIO.output(self.otherPin, True)
        GPIO.output(self.otherPin, False)
        #time.sleep(0.001)

    def setSegment(self, digit, segment, val):
        if digit == 'oneSec':
            self._setSegmentByIndex(self.oneSecIndices[segment], val)
        if digit == 'tenSec':
            self._setSegmentByIndex(self.tenSecIndices[segment], val)
        if digit == 'oneMin':
            self._setSegmentByIndex(self.oneMinIndices[segment], val)
        if digit == 'tenMin':
            self._setSegmentByIndex(self.tenMinIndices[segment], val)
        if digit == 'oneHour':
            self._setSegmentByIndex(self.oneHourIndices[segment], val)
        if digit == 'tenHour':
            self._setSegmentByIndex(self.tenHourIndices[segment], val)
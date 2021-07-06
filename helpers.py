# Helper class to make chart marker generation easier
# e.x: a=NiceScale(min, max)
# a.maxPoint, a.maxTicks, a.minPoint, a.niceMin, a.niceMax, a.tickSpacing

import math
import bpy
class HelperClass:
    def remap(self, x, oMin, oMax, nMin, nMax):
        if oMin == oMax:
            print("range is 0!")
            return None

        if nMin == nMax:
            print("range is 0!")
            return None

        # check for reversed input
        reverseInput = False
        oldMin = min( oMin, oMax )
        oldMax = max( oMin, oMax )
        if not oldMin == oMin:
            reverseInput = True

        # check for reversed output
        reverseOutput = False   
        newMin = min( nMin, nMax )
        newMax = max( nMin, nMax )
        if not newMin == nMin:
            reverseOutput = True

        portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
        if reverseInput:
            portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

        result = portion + newMin
        if reverseOutput:
            result = newMax - portion

        return result

class NiceScale:
    def __init__(self, minv,maxv):
        self.maxTicks = 6
        self.tickSpacing = 0
        self.lst = 10
        self.niceMin = 0
        self.niceMax = 0
        self.minPoint = minv
        self.maxPoint = maxv
        self.calculate()

    def calculate(self):
        self.lst = self.niceNum(self.maxPoint - self.minPoint, False)
        self.tickSpacing = self.niceNum(self.lst / (self.maxTicks - 1), True)
        self.niceMin = math.floor(self.minPoint / self.tickSpacing) * self.tickSpacing
        self.niceMax = math.ceil(self.maxPoint / self.tickSpacing) * self.tickSpacing

    def niceNum(self, lst, rround):
        self.lst = lst
        exponent = 0 # exponent of range
        fraction = 0 # fractional part of range
        niceFraction = 0 # nice, rounded fraction

        exponent = math.floor(math.log10(self.lst));
        fraction = self.lst / math.pow(10, exponent);

        if (self.lst):
            if (fraction < 1.5):
                niceFraction = 1
            elif (fraction < 3):
                niceFraction = 2
            elif (fraction < 7):
                niceFraction = 5;
            else:
                niceFraction = 10;
        else :
            if (fraction <= 1):
                niceFraction = 1
            elif (fraction <= 2):
                niceFraction = 2
            elif (fraction <= 5):
                niceFraction = 5
            else:
                niceFraction = 10

        return niceFraction * math.pow(10, exponent)

    def setMinMaxPoints(self, minPoint, maxPoint):
          self.minPoint = minPoint
          self.maxPoint = maxPoint
          self.calculate()

    def setMaxTicks(self, maxTicks):
        self.maxTicks = maxTicks;
        self.calculate()

#class generate text
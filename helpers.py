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

    # xSize,ySize,zSize,x_axis_size, y_axis_size, z_axis_size, obj_dimensions, cylWidth, axisPadding, axisMat, False)
    def generateAxis(self,xMax,yMax,zMax,xSize,ySize,zSize,pointDimensions,axisWidth,padding,axisMaterial):
        
        # Extra width needed for axis to wrap objects nicely
        extra_width_x = pointDimensions[0]/2
        extra_width_y = pointDimensions[1]/2
        extra_width_z = pointDimensions[2]/2

        # Generate X Axis Cylinder
        bpy.ops.mesh.primitive_cylinder_add(location=(xMax/2, -extra_width_y, - extra_width_z), radius=0.5)
        # world bpy.ops.mesh.primitive_cylinder_add(location=(0, min(yAxisFull) - extra_width_y, min(zAxisFull) - extra_width_z), radius=0.5)

        newXCyl = bpy.context.object  # define object
        bpy.context.object.rotation_euler = (0, 1.5708,0) # in radians (90 deg.)
        bpy.context.object.dimensions = [axisWidth, axisWidth, xSize * padding]
        bpy.context.object.data.materials.append(axisMaterial)  # Set mat selection

            # normal: bpy.ops.mesh.primitive_cylinder_add(location=(-x_padding, ySize/2, -z_padding), radius=0.5), radius=0.5)
            # wrapped
        bpy.ops.mesh.primitive_cylinder_add(
            location=(extra_width_x + xMax, yMax/2, -extra_width_z), radius=0.5)

        #world bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding, 0, min(zAxisFull) - z_padding), radius=0.5)

        newYCyl = bpy.context.object # define object
        bpy.context.object.rotation_euler = (0,1.5708,1.5708) # in radians
        bpy.context.object.dimensions = [axisWidth, axisWidth, ySize * padding]
        bpy.context.object.data.materials.append(axisMaterial)  # Set mat selection

        bpy.ops.mesh.primitive_cylinder_add(location=(-extra_width_x, -extra_width_y, zMax/2 - axisWidth*0.245), radius=0.5)
        #world bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding ,min(yAxisFull) - y_padding,-axisWidth*0.245), radius=0.5)

        newZCyl = bpy.context.object # define object
        # account for axis size to line up XYZ cylinder edges
        zSize = zSize + axisWidth/2
        # Set max Z value + abs(min) to Z size
        bpy.context.object.dimensions = [axisWidth, axisWidth, zSize * padding]
        bpy.context.object.data.materials.append(axisMaterial)  # Set mat selection
        
        final_axis = newXCyl, newYCyl, newZCyl
        return final_axis

    def generateAxisWorldSpace(self, xArray, yArray, zArray, xSize, ySize, zSize, pointDimensions, axisWidth, padding, axisMaterial):

        # Extra width needed for axis to wrap objects nicely
        extra_width_x = pointDimensions[0]/2
        extra_width_y = pointDimensions[1]/2
        extra_width_z = pointDimensions[2]/2

        # Generate X Axis Cylinder
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0, min(yArray) - extra_width_y, min(zArray) - extra_width_z), radius=0.5)

        newXCyl = bpy.context.object  # define object
        bpy.context.object.rotation_euler = (
            0, 1.5708, 0)  # in radians (90 deg.)
        bpy.context.object.dimensions = [axisWidth, axisWidth, xSize * padding]
        bpy.context.object.data.materials.append(
            axisMaterial)  # Set mat selection
        
        # Generate Y Axis Cylinder
        bpy.ops.mesh.primitive_cylinder_add(
            location=(min(xArray) - extra_width_x, 0, min(zArray) - extra_width_z), radius=0.5)

        newYCyl = bpy.context.object  # define object
        bpy.context.object.rotation_euler = (0, 1.5708, 1.5708)  # in radians
        bpy.context.object.dimensions = [axisWidth, axisWidth, ySize * padding]
        bpy.context.object.data.materials.append(axisMaterial)
        
        # Generate Z Axis Cylinder
        bpy.ops.mesh.primitive_cylinder_add(location=(min(
            xArray) - extra_width_x, min(yArray) - extra_width_y, -axisWidth*0.245), radius=0.5)

        newZCyl = bpy.context.object  # define object
        # account for axis size to line up XYZ cylinder edges
        zSize = zSize + axisWidth/2
        # Set max Z value + abs(min) to Z size
        bpy.context.object.dimensions = [axisWidth, axisWidth, zSize * padding]
        bpy.context.object.data.materials.append(
            axisMaterial)  # Set mat selection

        final_axis = newXCyl, newYCyl, newZCyl
        return final_axis


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

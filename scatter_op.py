import bpy
import csv
import os

class OT_Scatter(bpy.types.Operator):
    bl_idname = "view3d.do_scatter"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    csvMax = 8 # Length of csv columns
    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        default='*.csv;'
        )
    # X, Y, Z inputs
    bpy.types.Scene.my_tool_Xs = bpy.props.IntProperty(
        name = 'X-Loc',
        default = 0,
        min = 0,
        max = csvMax
    )

    bpy.types.Scene.my_tool_Ys = bpy.props.IntProperty(
        name = 'Y-Loc',
        default = 1,
        min = 0,
        max = csvMax
    )

    bpy.types.Scene.my_tool_Zs = bpy.props.IntProperty(
        name = 'Z-Loc',
        default = 2,
        min = 0,
        max = csvMax

    )
    bpy.types.Scene.dupeObj = bpy.props.StringProperty()    # Dupe obj selector
    bpy.types.Scene.dupe_enable = bpy.props.BoolProperty(   # Enable dupe checkbox
        name="Use dupe object",
        default = False
        )
    bpy.types.Scene.axis_enable = bpy.props.BoolProperty(   # Enable axis generation
        name="Generate axis",
        default = False
        )

    def execute(self, context):
        if(self.filepath.endswith('.csv')): # File is CSV
            csvFile = self.filepath
            # TODO: Generate axis on fileload (add inputs for x and y) & add axis labels
            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                xProp = bpy.context.scene.my_tool_Xs # X val
                yProp = bpy.context.scene.my_tool_Ys
                zProp = bpy.context.scene.my_tool_Zs 
                clone_dup = bpy.context.scene.dupe_enable   # Dupe bool
                axis_gen = bpy.context.scene.axis_enable # Generate aixs bool
                dupe_object_str = bpy.context.scene.dupeObj # Dupe object name
                next(reader) # Skip headers
                # Define axis arrays
                zAxisFull = []
                xAxisFull = []
                yAxisFull = []
                cylWdith = 0.15 # Width of axis cylinders
                axisPadding = 1.2 # extra length for axis
                for row in reader:
                    # Graph values
                    currentX = row[xProp]
                    currentY = row[yProp]
                    currentZ = row[zProp]
                    # Graph value arrays
                    zAxisFull.append(float(currentZ)) # Append each Z value to the array
                    xAxisFull.append(float(currentX))
                    yAxisFull.append(float(currentY))
                    csvMax = len(row) # set max value for column select
                    # Clone dupe process
                    if clone_dup:
                        dupeObject = bpy.data.objects[dupe_object_str] # Dupe input
                        newDupeObject = dupeObject.data.copy() # Cloned dupe
                        #newDupeObject.active_material = dupeObject.active_material.copy() # TODO: Add boolean checkbox to allow individual mats
                        clonedObj = bpy.data.objects.new("dupe_object_str", newDupeObject) # new obj
                        clonedObj.location = (float(row[xProp]), float(row[yProp]), float(row[zProp])) # Update clone location
                        bpy.context.collection.objects.link(clonedObj)
                        bpy.context.collection.objects.update # Update scene
                    else:   # Default cube if unchecked
                        newCube = bpy.ops.mesh.primitive_cube_add(location=(float(row[xProp]),float(row[yProp]),float(row[zProp])))
                        bpy.context.object.dimensions = [0.4,0.4,0.4]
                # Axis generation
                if axis_gen:
                    newZCyl = bpy.ops.mesh.primitive_cylinder_add(location=(0,0,0), radius=0.5) # Make axis cylinder mesh
                    bpy.context.object.dimensions = [cylWdith,cylWdith,(max(zAxisFull) + abs(min(zAxisFull))) * axisPadding]   # Set max Z value + abs(min) to Z size
                    bpy.ops.object.transform_apply(location = True, scale = True, rotation = True) # Apply scale

                    newXCyl = bpy.ops.mesh.primitive_cylinder_add(location=(0,0,0), radius=0.5)
                    bpy.context.object.rotation_euler = (0,1.5708,0) # in radianss
                    bpy.context.object.dimensions = [cylWdith,cylWdith,(max(xAxisFull) + abs(min(xAxisFull))) * axisPadding]
                    bpy.ops.object.transform_apply(location = True, scale = True, rotation = True) # Apply scale

                    newYCyl = bpy.ops.mesh.primitive_cylinder_add(location=(0,0,0), radius=0.5)
                    bpy.context.object.rotation_euler = (0,1.5708,1.5708) # in radianss
                    bpy.context.object.dimensions = [cylWdith,cylWdith,(max(yAxisFull) + abs(min(yAxisFull))) * axisPadding]
                    bpy.ops.object.transform_apply(location = True, scale = True, rotation = True) # Apply scale
        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):   # File select
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
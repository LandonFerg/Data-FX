import bpy
import csv
import os

class OT_Scatter(bpy.types.Operator):
    bl_idname = "view3d.do_stuff"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    csvMax = 8 #Length of csv columns
    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        default='*.csv;'
        )
    # X, Y, Z inputs #
    bpy.types.Scene.my_tool_Xs = bpy.props.IntProperty(
        name = 'X-Loc',
        default = 0,
        min = 0,
        max = csvMax
    )

    bpy.types.Scene.my_tool_Ys = bpy.props.IntProperty(
        name = 'Y-Loc',
        default = 0,
        min = 0,
        max = csvMax
    )

    bpy.types.Scene.my_tool_Zs = bpy.props.IntProperty(
        name = 'Z-Loc',
        default = 0,
        min = 0,
        max = csvMax

    )
    bpy.types.Scene.dupeObj = bpy.props.StringProperty()    # Dupe obj selector
    bpy.types.Scene.dupe_enable = bpy.props.BoolProperty(   # Enable dupe checkbox
        name="Use dupe object",
        default = False
        )

    def execute(self, context):
        if(self.filepath.endswith('.csv')): # File is CSV
            csvFile = self.filepath
            # TODO: Generate axis on fileload
            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                xProp = bpy.context.scene.my_tool_Xs # X val
                yProp = bpy.context.scene.my_tool_Ys # Y val
                zProp = bpy.context.scene.my_tool_Zs # Z val
                clone_dup = bpy.context.scene.dupe_enable   # Dupe bool
                dupe_object_str = bpy.context.scene.dupeObj # Dupe string
                next(reader) # Skip headers
                for row in reader:
                    currentX = row[xProp]
                    currentY = row[yProp]
                    currentZ = row[zProp]
                    csvMax = len(row) # set max value for column select
                    
                    if clone_dup:
                        dupeObject = bpy.data.objects[dupe_object_str] # Dupe inpit
                        newDupeObject = dupeObject.data.copy() # Cloned dupe
                        #newDupeObject.active_material = dupeObject.active_material.copy() # Clone material FIXME
                        clonedObj = bpy.data.objects.new("dupe_object_str", newDupeObject) # new obj
                        clonedObj.location = (float(row[xProp]), float(row[yProp]), float(row[zProp])) # Update clone location
                        bpy.context.collection.objects.link(clonedObj)
                        bpy.context.collection.objects.update # Update scene
                    else:   # Default cube if unchecked
                        newCube = bpy.ops.mesh.primitive_cube_add(location=(float(row[xProp]),float(row[yProp]),float(row[zProp])))
                        bpy.context.object.dimensions = [0.4,0.4,0.4]
        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):   # File select
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
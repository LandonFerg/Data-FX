import bpy
import csv
import os

class OT_Load_CSV(bpy.types.Operator):
    bl_idname = "view3d.do_stuff"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    csvMax = 100 #Length of csv columns
    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        default='*.csv;'
        )
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
    

    def execute(self, context):
        if(self.filepath.endswith('.csv')): # File is CSV
            csvFile = self.filepath

            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                xProp = bpy.context.scene.my_tool_Xs # Column X value
                yProp = bpy.context.scene.my_tool_Ys
                zProp = bpy.context.scene.my_tool_Zs
                next(reader) # Skip headers
                for row in reader:
                    currentX = row[xProp]
                    currentY = row[yProp]
                    currentZ = row[zProp]

                    csvMax = len(row)
                    newCube = bpy.ops.mesh.primitive_cube_add(location=(float(row[xProp]),float(row[yProp]),float(row[zProp])))
                    bpy.context.object.dimensions = [0.2,0.2,0.2]
        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):   # File select
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
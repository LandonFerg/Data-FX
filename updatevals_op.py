import bpy
import csv
import os
from bpy.props import FloatVectorProperty
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import IntProperty, EnumProperty, StringProperty, PointerProperty

class OT_UpdateVals(bpy.types.Operator):
    bl_idname = "view3d.load_vals"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"

    def execute(self, context):
        csv_file = bpy.context.scene.file_select
        if not csv_file:
            print("Error: No file selected")
            self.report({'ERROR_INVALID_INPUT'}, "File field is empty")
            return{'CANCELLED'}

        if(csv_file.endswith('.csv')):
            with open (csv_file, 'rt') as f:
                reader = csv.reader(f)
                headers = next(reader)
            
            for h in headers:
                print(h)

        return {'FINISHED'}


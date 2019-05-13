import bpy
import csv
import os

class OT_Load_CSV(bpy.types.Operator):
    bl_idname = "view3d.do_stuff"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        default='*.csv;'
        )
    

    def execute(self, context):
        if(self.filepath.endswith('.csv')): # File is CSV
            csvFile = self.filepath

            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                next(reader) # Skip headers
                for row in reader:
                    print(row[0])

        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        return {'FINISHED'}

    def invoke(self, context, event):   # File select
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
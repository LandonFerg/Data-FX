import bpy

class OT_Load_CSV(bpy.types.Operator):
    bl_idname = "view3d.do_stuff"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    filepath = bpy.props.StringProperty(
        subtype="FILE_PATH",
        default='*.csv;'
        )
    

    def execute(self, context):
        if(self.filepath.endswith('.csv')):
            print(self.filepath)
            # Do something with file
        else:
            print("Error: File not a CSV type")

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
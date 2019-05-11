import bpy

class Load_CSV(bpy.types.Operator):
    bl_idname = "view3d.do_stuff"
    bl_label = "CSV OP"
    bl_description = "Loads CSV"

    def execute(self, context):
        # Code here
        print("Hello World")
        return {'FINISHED'}
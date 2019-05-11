import bpy

class Main_Panel(bpy.types.Panel):
    bl_idname = "Main_Panel"
    bl_label = "DataFX"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row
        row.operator('view3d.do_stuff', text = "Do Stuff")


import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
)
class Scatter_Panel(bpy.types.Panel):
    bl_idname = "SCATTER_PT_Panel"
    bl_label = "Scatter Plot"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row4 = layout.row()
        row4.prop(context.scene, "file_select")

        # Col vals
        col = layout.split().column(align=True)
        col.label(text="CSV Columns")

        value_row_x = layout.row()
        value_row_x.label(text="X Axis: ")
        value_row_x.prop(context.scene, "header_dropdown_X", text="")

        value_row_y = layout.row()
        value_row_y.label(text="Y Axis: ")
        value_row_y.prop(context.scene, "header_dropdown_Y", text="")

        value_row_z = layout.row()
        value_row_z.label(text="Z Axis: ")
        value_row_z.prop(context.scene, "header_dropdown_Z", text="")

        row5 = layout.row()
        row5.prop(context.scene, 'dupe_enable')

        row6 = layout.row()
        row6.prop_search(context.scene, "dupeObj", context.scene, "objects")

        # Disable dupeObj if checkbox is false
        if bpy.context.scene.dupe_enable == False:
            row6.enabled = False
        elif bpy.context.scene.dupe_enable == True:
            row6.enabled = True
        
        row7 = layout.row()
        row7.prop(context.scene, 'axis_enable')

        row8 = layout.row()
        row8.prop(context.scene, 'axis_color')

        row9 = layout.row()
        row9.prop(context.scene, 'label_enable')

        row = layout.row()
        mainOp = row.operator('view3d.do_scatter', text = "Generate")

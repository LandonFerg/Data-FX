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

        row = layout.row()
        row.prop(context.scene, "scatter_file_select")

        # Col vals
        col = layout.split().column(align=True)
        col.label(text="CSV Columns")

        value_row_x = layout.row()
        value_row_x.label(text="X Axis: ")
        value_row_x.prop(context.scene, "scatter_dropdown_X", text="")

        value_row_y = layout.row()
        value_row_y.label(text="Y Axis: ")
        value_row_y.prop(context.scene, "scatter_dropdown_Y", text="")

        value_row_z = layout.row()
        value_row_z.label(text="Z Axis: ")
        value_row_z.prop(context.scene, "scatter_dropdown_Z", text="")

        row = layout.row()
        row.prop(context.scene, 'dupe_enable')

        row8 = layout.row()
        row8.prop_search(context.scene, "dupeObj", context.scene, "objects")

        # Disable dupeObj if checkbox is false
        if bpy.context.scene.dupe_enable == False:
            row8.enabled = False
        elif bpy.context.scene.dupe_enable == True:
            row8.enabled = True

        row = layout.row()
        row.prop(context.scene, 'axis_color')

        row = layout.row()
        row.prop(context.scene, 'size_enable')

        size_row = layout.row()
        size_row.prop(context.scene, 'graph_size_x')
        size_row.prop(context.scene, 'graph_size_y')
        size_row.prop(context.scene, 'graph_size_z')

        if bpy.context.scene.size_enable == False:
            size_row.enabled = False
        elif bpy.context.scene.size_enable == True:
            size_row.enabled = True

        row = layout.row()
        row.prop(context.scene, 'label_enable')

        row = layout.row()
        row.prop(context.scene, 'axis_enable')

        layout.row()

        row = layout.row()
        mainOp = row.operator('view3d.do_scatter', text = "Generate")

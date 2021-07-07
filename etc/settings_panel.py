import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
)

class Settings_Panel(bpy.types.Panel):
    bl_idname = "SCATTER_PT_PANEL"
    bl_label = "Global Settings"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    ### Global Settings ###
    bpy.types.Scene.graph_size_x = bpy.props.IntProperty(
        name="X",
        min=1,
        default=5
    )
    bpy.types.Scene.graph_size_y = bpy.props.IntProperty(
        name="Y",
        min=1,
        default=5
    )
    bpy.types.Scene.graph_size_z = bpy.props.IntProperty(
        name="Z",
        min=1,
        default=5
    )
    bpy.types.Scene.size_enable = bpy.props.BoolProperty(   # Enable custom graph size
        name="Graph size",
        description="Enables a custom graph size. (When disabled, values are pulled from the data)",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        # Col vals
        headerRow = layout.split().column(align=True)
        headerRow.label(text="Graph Scaling")

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
        row.label(text="Graph Appearence")

        row = layout.row()
        row.prop(context.scene, 'axis_color')

        row = layout.row()
        row.prop(context.scene, 'label_enable')

        row = layout.row()
        row.prop(context.scene, 'axis_enable')

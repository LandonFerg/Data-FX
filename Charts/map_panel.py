import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
)

class Map_Panel(bpy.types.Panel):
    bl_idname = "MAP_PT_Panel"
    bl_label = "Mapping Plot"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row1 = layout.row()
        row1.prop(context.scene, "map_file_select")
        
        # Map properties
        col = layout.split().column(align=True)
        col.label(text="Map Selection")
        placeholder = context.scene.placeholder

        # Csv defs
        value_row_x = layout.row()
        value_row_x.label(text="Latitude: ")
        value_row_x.prop(context.scene, "map_dropdown_lat", text="")

        value_row_y = layout.row()
        value_row_y.label(text="Longitude: ")
        value_row_y.prop(context.scene, "map_dropdown_lon", text="")


        row = layout.row()
        col.prop(placeholder, "dropdown_box", text="Map type: ")

        bottom_row = layout.row()
        mainOp = bottom_row.operator('view3d.do_map', text="Generate")

# from https://blender.stackexchange.com/questions/170219/python-panel-dropdownlist-and-integer-button
class PlaceholderProperties(PropertyGroup):
    inc_dec_int: IntProperty(
        name="Incr-Decr", min=1, default=4, description="Tooltip for Incr-Decr"
    )
    dropdown_box: EnumProperty(
        items=(
            ("0", "Globe", ""),
        ),
        name="Description for the Elements",
        default="0",
        description="Tooltip for the Dropdownbox",
    )

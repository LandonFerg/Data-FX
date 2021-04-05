import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
    FloatVectorProperty,
)

class OT_Map_Plot(bpy.types.Operator):
    bl_idname = "view3d.do_map"
    bl_label = "Generate Map"
    bl_description = "Generates Map"

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}

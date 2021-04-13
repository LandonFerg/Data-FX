import bpy
import math
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
        world_size = 2
        print("Hello World")
        self.make_world(world_size)
        lon = -95.7
        lat = 37.1
        self.calculate_cords(lon, lat, world_size/2)  # USA
        lat = 56.130
        lon = -106.346
        self.calculate_cords(lon, lat, world_size/2)  # CAN
       	lat = -25.274
        lon = 133.775
        self.calculate_cords(lon, lat, world_size/2)  # AUS
        bpy.ops.ed.undo_push()  # add to undo stack to prevent crashing
        return {'FINISHED'}

    def calculate_cords(self, lon, lat, radius):
        marker_size = 0.2
        phi = (90-lat)*(math.pi/ 180)

        theta = (lon+180)*(math.pi/180)
        x = -((radius) * math.sin(phi)*math.cos(theta))
        z = ((radius) * math.sin(phi)*math.sin(theta))
        y = ((radius) * math.cos(phi))

        map_point = bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32, ring_count=16, location=(x, y, z))

        bpy.context.object.dimensions = [marker_size, marker_size, marker_size]

        print("sphereical cordinates are: ", x, y, z)

    def make_world(self, _world_size):
        sphere_world = bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=(0, 0, 0))
        bpy.context.object.dimensions = [_world_size, _world_size, _world_size]
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.sphere_project()
        bpy.ops.object.editmode_toggle()




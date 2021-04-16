import bpy
import os
import csv
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

    bpy.types.Scene.map_file_select = bpy.props.StringProperty(
        name="File",
        default="",
        description="Data",
        maxlen=1024,
        subtype="FILE_PATH",
    )

    ### DROPDOWN ENUMS ###
    def populate_items(self, context): # Update dropdowns
        dropdown_items = [] # items enum
        csv_file = bpy.context.scene.map_file_select
        if not csv_file: # empty string check
            return ""
        if(csv_file.endswith('.csv')): # File is CSV
            with open (csv_file, 'rt') as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    count = 0
                    for h in headers: # push header vals to dropdown
                        identifier = str(h)
                        name = str(h)
                        tooltip = ""
                        number = count
                        dropdown_items.append((identifier, name, tooltip, number)) # append item tuple
                        count += 1
                    return dropdown_items

    bpy.types.Scene.map_dropdown_lat = bpy.props.EnumProperty(
        items=populate_items,
        name="",
        description="",
        default=None,
        update=None,
        get=None,
        set=None
    )

    bpy.types.Scene.map_dropdown_lon = bpy.props.EnumProperty(
        items=populate_items,
        name="",
        description="",
        default=None,
        update=None,
        get=None,
        set=None
    )

    def execute(self, context):
        selectedfile = bpy.context.scene.map_file_select  # Get our selected file
        world_size = 2
        print("Hello World")
        self.make_world(world_size)
        lat = 27.994402
        lon = -81.760254
        self.calculate_cords(lon, lat, world_size/2)
        
        bpy.ops.ed.undo_push()  # add to undo stack to prevent crashing
        return {'FINISHED'}

    def calculate_cords(self, lon, lat, radius):
        marker_size = 0.05

        latRad, lonRad = math.radians(lat), math.radians(lon)
        
        x = ((radius) * math.cos(latRad) * math.cos(lonRad))
        y = ((radius) * math.cos(latRad) * math.sin(lonRad))
        z = ((radius) * math.sin(latRad))

        map_point = bpy.ops.mesh.primitive_uv_sphere_add(
            segments=32, ring_count=16, location=(x, y, z))

        bpy.context.object.dimensions = [marker_size, marker_size, marker_size]

        print("sphereical cordinates are: ", x, y, z)

    def make_world(self, _world_size):
        sphere_world = bpy.ops.mesh.primitive_uv_sphere_add(segments=45, ring_count=28, location=(0, 0, 0), rotation=(0, 0, -0.1048))
        bpy.context.object.dimensions = [_world_size, _world_size, _world_size]
        bpy.ops.object.editmode_toggle()

        mat = bpy.data.materials.new(name="New_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        envImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
        envImage.image = bpy.data.images.load("//textures/world_tex.jpg")
        mat.node_tree.links.new(bsdf.inputs['Base Color'], envImage.outputs['Color'])
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.shade_smooth()

        ob = bpy.context.view_layer.objects.active

        # assign mat
        if ob.data.materials:
            ob.data.materials[0] = mat
        else:
            ob.data.materials.append(mat)




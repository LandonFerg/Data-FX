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
        if not selectedfile: # empty string check
            print("Error: No file selected")
            self.report({'ERROR_INVALID_INPUT'}, "File field is empty")
            return{'CANCELLED'}
        if(selectedfile.endswith('.csv')): # File is CSV
            csvFile = selectedfile
            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                header_row = next(reader) # skip headers
                
                # Get number values of header dropdown [0, 1, 2] (which axis is which)
                lat_number = header_row.index(bpy.context.scene.map_dropdown_lat)
                lon_number = header_row.index(bpy.context.scene.map_dropdown_lon)

                world_size = 2
                self.make_world(world_size)

                latitudes = []
                longitudes = []

                for row in reader:
                    currentLat = row[lat_number]
                    currentLon = row[lon_number]

                    self.calculate_cords(float(currentLon), float(currentLat), world_size/2)


        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        print("Hello World")
        
        bpy.ops.ed.undo_push()  # add to undo stack to prevent crashing
        return {'FINISHED'}

    def calculate_cords(self, lon, lat, radius):
        
        # New 'Points' collection
        if not bpy.data.collections.get("Points"):
            prop_collection = bpy.data.collections.new(name="Points")
            bpy.context.scene.collection.children.link(prop_collection)
        else:
            prop_collection = bpy.data.collections.get("Points")

        marker_size = 0.01

        latRad, lonRad = math.radians(lat), math.radians(lon)
        
        x = ((radius) * math.cos(latRad) * math.cos(lonRad))
        y = ((radius) * math.cos(latRad) * math.sin(lonRad))
        z = ((radius) * math.sin(latRad))

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=18, ring_count=12, location=(x, y, z))

        map_point = bpy.context.object
        map_point.dimensions = [marker_size, marker_size, marker_size] # size

        for coll in map_point.users_collection: # Remove from other collections
            coll.objects.unlink(map_point)

        prop_collection.objects.link(map_point) # Add to point collection


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




import bpy
import csv
import os
from bpy.props import FloatVectorProperty

from .helpers import helper_class

class OT_Scatter(bpy.types.Operator):
    bl_idname = "view3d.do_scatter"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    csvMax = 8 # Length of csv columns

    ### PANEL PROPERTIES & VARIABLES ###
    bpy.types.Scene.scatter_file_select = bpy.props.StringProperty(
        name="File",
        default="C:/Users/Lando/Downloads/test-csv - Sheet1 - Copy.csv",
        description="Data",
        maxlen=1024,
        subtype="FILE_PATH",
    )
    bpy.types.Scene.dupeObj = bpy.props.StringProperty()    # Dupe obj selector
    bpy.types.Scene.dupe_enable = bpy.props.BoolProperty(   # Enable dupe checkbox
        name="Use dupe object",
        default = False
        )
    bpy.types.Scene.axis_enable = bpy.props.BoolProperty(   # Enable axis generation
        name="Generate Axis",
        default = True
        )
    bpy.types.Scene.label_enable = bpy.props.BoolProperty(   # Enable label generation
        name="Use Labels",
        default = True
        )
    bpy.types.Scene.size_enable = bpy.props.BoolProperty(   # Enable custom graph size
        name="Graph size",
        description="Enables a custom graph size. (When disabled, values are pulled from the data)",
        default = True
        )
    bpy.types.Scene.graph_size_x = bpy.props.IntProperty(
        name="X",
        min=1,
        default = 5
    )
    bpy.types.Scene.graph_size_y = bpy.props.IntProperty(
        name="Y",
        min=1,
        default = 5
    )
    bpy.types.Scene.graph_size_z = bpy.props.IntProperty(
        name="Z",
        min=1,
        default = 5
    )
    bpy.types.Scene.axis_color = FloatVectorProperty(
        name="Axis color",
        subtype='COLOR',
        default=(0.012, 0.012, 0.012),
        min=0.0, max=1.0,
        description="color picker"
        )

    ### DROPDOWN ENUMS ###
    def populate_items(self, context): # Update dropdowns
        dropdown_items = [] # items enum
        csv_file = bpy.context.scene.scatter_file_select
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

    # TODO: make these enums a class https://docs.blender.org/api/current/bpy.props.html
    bpy.types.Scene.scatter_dropdown_X = bpy.props.EnumProperty(
            items=populate_items,
            name="",
            description="",
            default=None,
            update = None,
            get=None,
            set=None
    )
    bpy.types.Scene.scatter_dropdown_Y = bpy.props.EnumProperty(
            items=populate_items,
            name="",
            description="",
            default=None,
            update = None,
            get=None,
            set=None
    )
    bpy.types.Scene.scatter_dropdown_Z = bpy.props.EnumProperty(
            items=populate_items,
            name="",
            description="",
            default=None,
            update = None,
            get=None,
            set=None
    )

    def execute(self, context):
        helper = helper_class()
        selectedfile = bpy.context.scene.scatter_file_select # Get our selected file
        if not selectedfile: # empty string check
            print("Error: No file selected")
            self.report({'ERROR_INVALID_INPUT'}, "File field is empty")
            return{'CANCELLED'}
        if(selectedfile.endswith('.csv')): # File is CSV
            csvFile = selectedfile
            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                obj_dimensions = [0.4,0.4,0.4] # var to keep track of dims to compensate for origin
                clone_dup = bpy.context.scene.dupe_enable   # Dupe bool
                axis_gen = bpy.context.scene.axis_enable # Generate aixs bool
                label_gen = bpy.context.scene.label_enable
                dupe_object_str = bpy.context.scene.dupeObj # Dupe object name
                setAxisColor = bpy.context.scene.axis_color # axis color
                size_enable = bpy.context.scene.size_enable
                graph_size_x = bpy.context.scene.graph_size_x
                graph_size_y = bpy.context.scene.graph_size_y
                graph_size_z = bpy.context.scene.graph_size_z
                header_row = next(reader) # skip headers
                csvContents = list(csv.reader(f)) # add data to list so we can loop more than once

                # Get header values from the header dropdown
                x_number = header_row.index(bpy.context.scene.scatter_dropdown_X)
                y_number = header_row.index(bpy.context.scene.scatter_dropdown_Y)
                z_number = header_row.index(bpy.context.scene.scatter_dropdown_Z)

                # Apply our selected header values
                xProp = x_number
                yProp = y_number
                zProp = z_number

                # Define axis arrays
                zAxisFull = []
                xAxisFull = []
                yAxisFull = []

                # Define max graph values (for blender world space)
                xSize = graph_size_x
                ySize = graph_size_y
                zSize = graph_size_z

                cylWidth = 0.15 # Width of axis cylinders
                axisPadding = 1 # extra length for axis
                # define obj_dimensions for origin calculations
                if clone_dup and dupe_object_str:
                    dupeObject = bpy.data.objects[dupe_object_str] # Dupe input
                    obj_dimensions = dupeObject.dimensions
                else:
                    obj_dimensions = [0.4,0.4,0.4]
                
                if not bpy.data.collections.get("Points"):
                    prop_collection = bpy.data.collections.new(name="Points")
                    bpy.context.scene.collection.children.link(prop_collection)
                else:
                    prop_collection = bpy.data.collections.get("Points")

                for row in csvContents:
                    # Graph values
                    currentX = row[xProp]
                    currentY = row[yProp]
                    currentZ = row[zProp]
                    # Graph value arrays
                    zAxisFull.append(float(currentZ))
                    xAxisFull.append(float(currentX))
                    yAxisFull.append(float(currentY))

                # store min and max of axes
                xMin, xMax = min(xAxisFull), max(xAxisFull)
                yMin, yMax = min(yAxisFull), max(yAxisFull)
                zMin, zMax = min(zAxisFull), max(zAxisFull)

                for row in csvContents:
                    csvMax = len(row) # set max value for column select
                    
                    # Remap values to size of chart in world space
                    newX = helper.remap(float(row[xProp]), xMin, xMax, 0, xSize)
                    newY = helper.remap(float(row[yProp]), yMin, yMax, 0, ySize)
                    newZ = helper.remap(float(row[zProp]), zMin, zMax, 0, zSize)

                    # Clone dupe process
                    if clone_dup and dupe_object_str:
                        dupeObject = bpy.data.objects[dupe_object_str] # Dupe input
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY') # center our origin
                        newDupeObject = dupeObject.data.copy() # Cloned dupe
                        #newDupeObject.active_material = dupeObject.active_material.copy() # TODO: Add boolean checkbox to allow individual mats
                        clonedObj = bpy.data.objects.new(name=dupe_object_str, object_data=newDupeObject) # new obj
                        if size_enable: # Check if we want a custom scale or not
                            clonedObj.location = (float(newX), float(newY), float(newZ)) # Update clone location
                        else:
                            clonedObj.location = (float(row[xProp]), float(row[yProp]), float(row[zProp])) # Update clone location
                        prop_collection.objects.link(clonedObj) # Add dupe to new collection
                        bpy.context.collection.objects.update # Update scene
                    else:   # Default ico_sphere if unchecked
                        if size_enable:
                            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(float(newX),float(newY),float(newZ)))
                        else:
                            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(float(row[xProp]),float(row[yProp]),float(row[zProp])))
                        prim = bpy.context.object;
                        bpy.context.object.dimensions = [0.4,0.4,0.4]
                        for coll in prim.users_collection: # Remove from other collections
                            coll.objects.unlink(prim)
                        prop_collection.objects.link(prim) # Add to point collection
                        bpy.context.collection.objects.update # Update scene

                # Axis generation based on default graph size
                if axis_gen:
                    # make sure our axis is at far left/right (assuming centered obj origins)
                    x_padding = obj_dimensions[0]/2
                    y_padding = obj_dimensions[1]/2
                    z_padding = obj_dimensions[2]/2

                    if size_enable:
                        x_axis_size = xSize + obj_dimensions[0]
                        y_axis_size = ySize + obj_dimensions[1]
                        z_axis_size = zSize + obj_dimensions[2]
                    else:
                        x_axis_size = (max(xAxisFull) + abs(min(xAxisFull))) + obj_dimensions[0]
                        y_axis_size = (max(yAxisFull) + abs(min(yAxisFull))) + obj_dimensions[1]
                        z_axis_size = (max(zAxisFull) + abs(min(zAxisFull))) + obj_dimensions[2]

                    axisMat = bpy.data.materials.new(name="AxisMat")
                    

                    # calculate position taking into account origin size
                    if size_enable:
                        bpy.ops.mesh.primitive_cylinder_add(location=(xSize/2, -y_padding, -z_padding), radius=0.5) # Generate axis cylinder
                    else:
                        bpy.ops.mesh.primitive_cylinder_add(location=(0, min(yAxisFull) - y_padding, min(zAxisFull) - z_padding), radius=0.5)

                    newXCyl = bpy.context.object # define object
                    bpy.context.object.rotation_euler = (0,1.5708,0) # in radians (90 deg.)
                    bpy.context.object.dimensions = [cylWidth,cylWidth, x_axis_size * axisPadding]
                    context.object.data.materials.append(axisMat) # Set mat selection

                    if size_enable:
                        bpy.ops.mesh.primitive_cylinder_add(location=(-x_padding, ySize/2, -z_padding), radius=0.5)
                    else:
                        bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding, 0, min(zAxisFull) - z_padding), radius=0.5)

                    newYCyl = bpy.context.object # define object
                    bpy.context.object.rotation_euler = (0,1.5708,1.5708) # in radians
                    bpy.context.object.dimensions = [cylWidth,cylWidth, y_axis_size * axisPadding]
                    context.object.data.materials.append(axisMat) # Set mat selection

                    if size_enable: # Use custom size
                        bpy.ops.mesh.primitive_cylinder_add(location=(-x_padding ,-y_padding, zSize/2 -cylWidth*0.245), radius=0.5)
                    else: # Wrap around data size
                        bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding ,min(yAxisFull) - y_padding,-cylWidth*0.245), radius=0.5)

                    newZCyl = bpy.context.object # define object
                    z_axis_size = z_axis_size + cylWidth/2 # account for axis size to line up XYZ cylinder edges
                    bpy.context.object.dimensions = [cylWidth,cylWidth, z_axis_size * axisPadding]   # Set max Z value + abs(min) to Z size
                    context.object.data.materials.append(axisMat) # Set mat selection
                    axisMat.diffuse_color = (setAxisColor.r, setAxisColor.g, setAxisColor.b, 1)

                if label_gen and axis_gen:
                    XFont = bpy.data.curves.new(type="FONT",name="X Font Curve")
                    XFont.body = str(header_row[xProp])
                    XFont.align_x="CENTER"
                    #LabelFont = bpy.data.fonts.load('C:/font/file/path') # TODO: Enable Font loading from custom stringprop
                    #XFont.font = Font
                    x_font_obj = bpy.data.objects.new("X_Header", bpy.data.curves["X Font Curve"])
                    bpy.context.scene.collection.objects.link(x_font_obj)
                    x_font_obj.location = (float(newXCyl.location[0]) + x_axis_size/2, float(newXCyl.location[1]), float(newXCyl.location[2]))
                    constraint = x_font_obj.constraints.new("TRACK_TO")
                    constraint.target = bpy.context.scene.camera
                    constraint.track_axis = "TRACK_Z"

                    YFont = bpy.data.curves.new(type="FONT",name="Y Font Curve")
                    YFont.body = str(header_row[yProp])
                    YFont.align_x="CENTER"
                    y_font_obj = bpy.data.objects.new("Y_Header", bpy.data.curves["Y Font Curve"])
                    bpy.context.scene.collection.objects.link(y_font_obj)
                    y_font_obj.location = (float(newYCyl.location[0]), float(newYCyl.location[1]) + y_axis_size/2, float(newYCyl.location[2]))
                    constraint = y_font_obj.constraints.new("TRACK_TO")
                    constraint.target = bpy.context.scene.camera
                    constraint.track_axis = "TRACK_Z"

                    ZFont = bpy.data.curves.new(type="FONT",name="Z Font Curve")
                    ZFont.body = str(header_row[zProp])
                    ZFont.align_x="CENTER"
                    z_font_obj = bpy.data.objects.new("Z_Header", bpy.data.curves["Z Font Curve"])
                    bpy.context.scene.collection.objects.link(z_font_obj)
                    z_font_obj.location = (float(newZCyl.location[0]), float(newZCyl.location[1]), float(newZCyl.location[2]) + z_axis_size/2)
                    constraint = z_font_obj.constraints.new("TRACK_TO")
                    constraint.target = bpy.context.scene.camera
                    constraint.track_axis = "TRACK_Z"


            bpy.ops.ed.undo_push() # add to undo stack to prevent crashing

        else:
            print("Error: File not a CSV type")
            self.report({'ERROR_INVALID_INPUT'}, "File not of type CSV")
            return{'CANCELLED'}

        return {'FINISHED'}

    # def generate_markers(self, minX, maxX,minY,maxY,minZ,maxZ):



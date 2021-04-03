import bpy
import csv
import os
from bpy.props import FloatVectorProperty    

class OT_Scatter(bpy.types.Operator):
    bl_idname = "view3d.do_scatter"
    bl_label = "Load CSV"
    bl_description = "Loads CSV"
    csvMax = 8 # Length of csv columns
    # File selector
    bpy.types.Scene.file_select = bpy.props.StringProperty(
        name="File",
        default="",
        description="Data",
        maxlen=1024,
        subtype="FILE_PATH",
    )
    # X, Y, Z inputs
    bpy.types.Scene.my_tool_Xs = bpy.props.IntProperty(
        name = '',
        default = 0,
        min = 0,
        max = csvMax
    )
    bpy.types.Scene.my_tool_Ys = bpy.props.IntProperty(
        name = '',
        default = 1,
        min = 0,
        max = csvMax
    )
    bpy.types.Scene.my_tool_Zs = bpy.props.IntProperty(
        name = '',
        default = 2,
        min = 0,
        max = csvMax
    )
    bpy.types.Scene.dupeObj = bpy.props.StringProperty()    # Dupe obj selector
    bpy.types.Scene.dupe_enable = bpy.props.BoolProperty(   # Enable dupe checkbox
        name="Use dupe object",
        default = False
        )
    bpy.types.Scene.axis_enable = bpy.props.BoolProperty(   # Enable axis generation
        name="Generate axis",
        default = True
        )
    bpy.types.Scene.label_enable = bpy.props.BoolProperty(   # Enable label generation
        name="Use Labels",
        default = True
        )
    bpy.types.Scene.axis_color = FloatVectorProperty(
        name="Axis color",
        subtype='COLOR',
        default=(0.012, 0.012, 0.012),
        min=0.0, max=1.0,
        description="color picker"
         )

    def execute(self, context):
        selectedfile = bpy.context.scene.file_select # Get our selected file
        if not selectedfile: # empty string check
            print("Error: No file selected")
            self.report({'ERROR_INVALID_INPUT'}, "File field is empty")
            return{'CANCELLED'}
        if(selectedfile.endswith('.csv')): # File is CSV
            csvFile = selectedfile
            # TODO: Generate axis on fileload (add inputs for x and y) & add axis labels
            with open (csvFile, 'rt') as f: # Iterate through CSV
                reader = csv.reader(f)
                xProp = bpy.context.scene.my_tool_Xs # X val
                yProp = bpy.context.scene.my_tool_Ys
                zProp = bpy.context.scene.my_tool_Zs
                obj_dimensions = [0.4,0.4,0.4] # var to keep track of dims to compensate for origin
                clone_dup = bpy.context.scene.dupe_enable   # Dupe bool
                axis_gen = bpy.context.scene.axis_enable # Generate aixs bool
                label_gen = bpy.context.scene.label_enable
                dupe_object_str = bpy.context.scene.dupeObj # Dupe object name
                setAxisColor = bpy.context.scene.axis_color # axis color
                
                header_row = next(reader)
                #next(reader) # Skip headers
                # Define axis arrays
                zAxisFull = []
                xAxisFull = []
                yAxisFull = []
                cylWidth = 0.15 # Width of axis cylinders
                axisPadding = 1 # extra length for axis

                # define obj_dimensions for origin calculations
                if clone_dup:
                    dupeObject = bpy.data.objects[dupe_object_str] # Dupe input
                    obj_dimensions = dupeObject.dimensions
                else:
                    obj_dimensions = [0.4,0.4,0.4]
                
                for row in reader:
                    # Graph values
                    currentX = row[xProp]
                    currentY = row[yProp]
                    currentZ = row[zProp]
                    # Graph value arrays
                    zAxisFull.append(float(currentZ)) # Append each Z value to the array
                    xAxisFull.append(float(currentX))
                    yAxisFull.append(float(currentY))
                    csvMax = len(row) # set max value for column select
                    # Clone dupe process
                    if clone_dup:
                        dupeObject = bpy.data.objects[dupe_object_str] # Dupe input
                        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY') # center our origin
                        newDupeObject = dupeObject.data.copy() # Cloned dupe
                        #newDupeObject.active_material = dupeObject.active_material.copy() # TODO: Add boolean checkbox to allow individual mats
                        clonedObj = bpy.data.objects.new("dupe_object_str", newDupeObject) # new obj
                        clonedObj.location = (float(row[xProp]), float(row[yProp]), float(row[zProp])) # Update clone location
                        bpy.context.collection.objects.link(clonedObj)
                        bpy.context.collection.objects.update # Update scene
                    else:   # Default ico_sphere if unchecked
                        newCube = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=(float(row[xProp]),float(row[yProp]),float(row[zProp])))
                        bpy.context.object.dimensions = [0.4,0.4,0.4]
                # Axis generation
                if axis_gen:

                    # make sure our axis is at far left/right (assuming centered obj origins)
                    x_padding = obj_dimensions[0]/2
                    y_padding = obj_dimensions[1]/2
                    z_padding = obj_dimensions[2]/2

                    axisMat = bpy.data.materials.new(name="AxisMat")
                    bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding ,min(yAxisFull) - y_padding,-cylWidth*0.245), radius=0.5) # Make axis cylinder mesh
                    newZCyl = bpy.context.object # define object
                    z_axis_size = (max(zAxisFull) + abs(min(zAxisFull))) + obj_dimensions[2] # calculate scale so its lined up with graph
                    z_axis_size = z_axis_size + cylWidth/2 # account for axis size to line up XYZ cylinder edges
                    bpy.context.object.dimensions = [cylWidth,cylWidth, z_axis_size * axisPadding]   # Set max Z value + abs(min) to Z size
                    context.object.data.materials.append(axisMat) # Set mat selection
                    axisMat.diffuse_color = (setAxisColor.r, setAxisColor.g, setAxisColor.b, 1)

                    # calculate position taking into account origin size
                    bpy.ops.mesh.primitive_cylinder_add(location=(0, min(yAxisFull) - y_padding, min(zAxisFull) - z_padding), radius=0.5)
                    newXCyl = bpy.context.object # define object
                    bpy.context.object.rotation_euler = (0,1.5708,0) # in radians (90 deg.)
                    x_axis_size = (max(xAxisFull) + abs(min(xAxisFull))) + obj_dimensions[0] # account for origins when sizing
                    bpy.context.object.dimensions = [cylWidth,cylWidth, x_axis_size * axisPadding]
                    context.object.data.materials.append(axisMat) # Set mat selection

                    bpy.ops.mesh.primitive_cylinder_add(location=(min(xAxisFull) - x_padding, 0, min(zAxisFull) - z_padding), radius=0.5)
                    newYCyl = bpy.context.object # define object
                    bpy.context.object.rotation_euler = (0,1.5708,1.5708) # in radians
                    y_axis_size = (max(yAxisFull) + abs(min(yAxisFull))) + obj_dimensions[1] # account for origins when sizing
                    bpy.context.object.dimensions = [cylWidth,cylWidth, y_axis_size * axisPadding]
                    context.object.data.materials.append(axisMat) # Set mat selection
                
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

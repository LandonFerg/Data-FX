import bpy

class PT_Main_Panel(bpy.types.Panel):
    bl_idname = "Main_Panel"
    bl_label = "DataFX"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        mainOp = row.operator('view3d.do_stuff', text = "Load-CSV")

        row2 = layout.row()
        row2.prop(context.scene, 'my_tool_col')


        #NOTES
        #row2 = layout.row()
        #row2.operator(another operator function)
        # OR row2.prop(context.scene, "float_input") | # Put this under ur operator --> float_input = bpy.props.FloatProperty( ... )
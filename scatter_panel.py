import bpy

class PT_Scatter_Panel(bpy.types.Panel):
    bl_idname = "Scatter_Panel"
    bl_label = "Scatter Plot"
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
        #row.label("Scatter Plot")

        '''row2 = layout.row()
        row2.prop(context.scene, 'my_tool_Xs')
        

        row3 = layout.row()
        row3.prop(context.scene, 'my_tool_Ys')

        row4 = layout.row()
        row4.prop(context.scene, 'my_tool_Zs')'''

        # Col test
        col = layout.split().column(align=True)
        col.label(text="CSV Columns")
        col.prop(context.scene, 'my_tool_Xs')
        col.prop(context.scene, 'my_tool_Ys')
        col.prop(context.scene, 'my_tool_Zs')

        row5 = layout.row()
        row5.prop(context.scene, 'dupe_enable')

        row6 = layout.row()
        row6.prop_search(context.scene, "dupeObj", context.scene, "objects")

        # Disable dupeObj if checkbox is false
        if bpy.context.scene.dupe_enable == False:
            row6.enabled = False
        elif bpy.context.scene.dupe_enable == True:
            row6.enabled = True
            
        #NOTES
        #row2 = layout.row()
        #row2.operator(another operator function)
        # OR row2.prop(context.scene, "float_input") | # Put this under ur operator --> float_input = bpy.props.FloatProperty( ... )
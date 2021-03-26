import bpy

class Scatter_Panel(bpy.types.Panel):
    bl_idname = "SCATTER_PT_Panel"
    bl_label = "Scatter Plot"
    bl_category = "DataFX"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # @classmethod 
    # def poll(cls, context):
    #     return (context.object is not None) -- makes panel dissappear if no object is selected

    def draw(self, context):
        layout = self.layout

        # Col vals
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
        
        row7 = layout.row()
        row7.prop(context.scene, 'axis_enable')

        row8 = layout.row()
        row8.prop(context.scene, 'axis_color')

        row = layout.row()
        mainOp = row.operator('view3d.do_scatter', text = "Load-CSV & Generate")

        

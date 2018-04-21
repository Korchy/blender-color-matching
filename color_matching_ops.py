# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


import bpy
from .color_matching import ColorMatching


class OutputWindow(bpy.types.Operator):
    bl_idname = 'colormatch.show_window'
    bl_label = 'OutputWindow'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}


class NCSMatch(bpy.types.Operator):
    bl_idname = 'colormatch.ncsmatch'
    bl_label = 'Search nearest NCS:'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        ColorMatching.clear()
        return {'FINISHED'}

    def invoke(self, context, event):
        ColorMatching.search_nearest_ncs_by_rgb(context.window_manager.colormatching_vars.source_color, context.window_manager.colormatching_vars.matching_count)
        matches = ColorMatching.matches()
        for i, match in enumerate(matches):
            context.window_manager.colormatching_colors.add()
            context.window_manager.colormatching_colors[i].dest_color[0] = match[0][0] / 255
            context.window_manager.colormatching_colors[i].dest_color[1] = match[0][1] / 255
            context.window_manager.colormatching_colors[i].dest_color[2] = match[0][2] / 255
        # show window
        return context.window_manager.invoke_props_dialog(self, width=700)

    def draw(self, context):
        matches = ColorMatching.matches()
        row = self.layout.row()
        for i, match in enumerate(matches):
            col = row.column()
            col.label(str(round(match[2] * 100, 2)) + ' %')
            col.prop(context.window_manager.colormatching_colors[i], 'dest_color', text='')
            col.label(match[1][0])
            col.label('CMYK ' + match[1][1])

    def check(self, context):
        return True

    def cancel(self, context):
        self.execute(context)


def register():
    bpy.utils.register_class(NCSMatch)


def unregister():
    bpy.utils.unregister_class(NCSMatch)

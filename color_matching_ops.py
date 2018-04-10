# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching
#
# Version history:
#   1.0. - Search for some nearest alternative system colors by RGB value


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
    bl_label = 'Search nearest NCS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # ColorMatching.clear_match_textures()
        return {'FINISHED'}

    def invoke(self, context, event):
        ColorMatching.search_nearest_ncs_by_rgb(context.window_manager.colormatching_vars.source_color, context.window_manager.colormatching_vars.matching_count)
        ColorMatching.create_match_textures()
        # show window
        return context.window_manager.invoke_props_dialog(self, width=700)

    def draw(self, context):
        matches = ColorMatching.matches()
        match_textures = ColorMatching.match_textures()
        if matches and match_textures:
            row = self.layout.row()
            for i, texture in enumerate(match_textures):
                col = row.column()
                col.template_preview(texture[1], show_buttons=False)
                # col.template_preview(bpy.data.textures['colormatch_texture' + str(i)], show_buttons=False)
                col.label('RGB: ' + str(matches[i][0]))
                col.label(matches[i][1][0])     # NCS

    def check(self, context):
        return True


def register():
    bpy.utils.register_class(NCSMatch)


def unregister():
    bpy.utils.unregister_class(NCSMatch)

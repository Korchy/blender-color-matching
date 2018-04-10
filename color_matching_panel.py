# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching
#
# Version history:
#   1.0. - Search for some nearest alternative system colors by RGB value


import bpy


class ColorMatchPanel(bpy.types.Panel):
    bl_idname = 'colormatch.panel'
    bl_label = 'ColorMatch'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'ColorMatch'

    def draw(self, context):
        self.layout.prop(context.window_manager.colormatching_vars, 'source_color')
        self.layout.operator('colormatch.ncsmatch', text='Search NCS (NCl)')


def register():
    bpy.utils.register_class(ColorMatchPanel)


def unregister():
    bpy.utils.unregister_class(ColorMatchPanel)

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

        # self.layout.template_preview(bpy.data.materials['Test0'], show_buttons=False, preview_id='1')
        # self.layout.template_preview(bpy.data.materials['Test1'], show_buttons=False, preview_id='2')

        # self.layout.template_ID_preview(context.active_object, "active_material")

        self.layout.template_ID_preview(context.active_object, "active_material")
        self.layout.template_ID_preview(context.window_manager, 'colormatching_vars')


def register():
    bpy.utils.register_class(ColorMatchPanel)


def unregister():
    bpy.utils.unregister_class(ColorMatchPanel)

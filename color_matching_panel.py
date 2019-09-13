# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class COLORMATCH_PT_Panel(Panel):
    bl_idname = 'COLORMATCH_PT_panel'
    bl_label = 'ColorMatch'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ColorMatch'

    def draw(self, context):
        self.layout.prop(context.window_manager.colormatching_vars, 'source_color')
        self.layout.operator('colormatch.color_match', text='Search NCS (NCl)').db = 'NCS'
        self.layout.operator('colormatch.color_match', text='Search RAL Classic').db = 'RAL_C'
        self.layout.operator('colormatch.color_match', text='Search RAL Design').db = 'RAL_D'
        self.layout.operator('colormatch.color_match', text='Search RAL Effect').db = 'RAL_E'


def register():
    register_class(COLORMATCH_PT_Panel)


def unregister():
    unregister_class(COLORMATCH_PT_Panel)

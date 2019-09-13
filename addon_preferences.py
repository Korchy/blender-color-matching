# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import AddonPreferences
from bpy.props import IntProperty
from bpy.utils import register_class, unregister_class


class COLORMATCH_addon_preferences(AddonPreferences):
    bl_idname = __package__

    # matching cound
    matching_count: IntProperty(
        name='Matching count',
        min=1,
        default=5,
        subtype='UNSIGNED'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'matching_count')


def register():
    register_class(COLORMATCH_addon_preferences)


def unregister():
    unregister_class(COLORMATCH_addon_preferences)

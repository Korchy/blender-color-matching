# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching

from .addon import Addon
from . import addon_preferences
from . import color_matching_panel
from . import color_matching_ops
from . import color_matching


bl_info = {
    'name': 'Color matching',
    'category': 'All',
    'author': 'Nikita Akimov',
    'version': (1, 3, 0),
    'blender': (2, 81, 0),
    'location': 'The 3D_View window - T-panel - the ColorMatching tab',
    'wiki_url': 'https://b3d.interplanety.org/en/blender-add-on-color-matching/',
    'tracker_url': 'https://b3d.interplanety.org/en/blender-add-on-color-matching/',
    'description': 'Search for some nearest alternative system colors by RGB value'
}


def register():
    if not Addon.dev_mode():
        addon_preferences.register()
        color_matching.register()
        color_matching_ops.register()
        color_matching_panel.register()
    else:
        print('It seems you are trying to use the dev version of the ' + bl_info['name'] + ' add-on. It may work not properly. Please download and use the release version!')


def unregister():
    if not Addon.dev_mode():
        color_matching_panel.unregister()
        color_matching_ops.unregister()
        color_matching.unregister()
        addon_preferences.unregister()


if __name__ == '__main__':
    register()

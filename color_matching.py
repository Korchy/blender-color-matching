# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


import bpy
import os
import json
import copy
from mathutils import Vector
from .b3d_lib_int.rgb import RGB


class ColorMatching:

    __ncs_database = None
    __ncs_database_file = os.path.join(os.path.dirname(__file__), 'ncs.json')

    __matches = []  # search results -> first element - rgb color
    __match_textures = []   # [[image1, texutre1], [image2, texture2], ...]

    @staticmethod
    def search_nearest_ncs_by_rgb(source_rgb, limit):
        # returns limit strings from ncs database file sorted by relevance to rgb
        __class__.clear()
        rgb = RGB.fromlist(source_rgb)
        db = __class__.ncs_db()
        rgb_vector = rgb.to_vector()
        __class__.__matches = copy.deepcopy(sorted(db, key=lambda x: (rgb_vector - Vector((x[0][0], x[0][1], x[0][2]))).length)[:limit])
        for ncs in __class__.__matches:
            ncs.append(RGB.relevance(rgb, RGB.fromlist(ncs[0])))

    @staticmethod
    def ncs_db():
        if not __class__.__ncs_database:
            with open(__class__.__ncs_database_file) as data:
                __class__.__ncs_database = json.load(data)
        return __class__.__ncs_database

    @staticmethod
    def matches():
        return __class__.__matches

    @staticmethod
    def matches_str():
        matches_str = ''
        if __class__.__matches:
            matches_str += '%\tRGB\tNCS\tHEX\tCMYK\n'
            for line in __class__.__matches:
                matches_str += '{:<7.2%}\t{:03d}-{:03d}-{:03d}\t{:<15}\t'.format(line[2], int(line[0][0]), int(line[0][1]), int(line[0][2]), line[1][0])
                matches_str += '{}\t{}'.format(line[1][2], '-'.join([a.zfill(3) for a in line[1][1].split('-')]))
                matches_str += '\n'
        return matches_str

    @staticmethod
    def match_textures():
        return __class__.__match_textures

    @staticmethod
    def create_match_textures():
        if __class__.__matches:
            for i, item in enumerate(__class__.__matches):
                img = bpy.data.images.new('colormatch_image' + str(i), 255, 255)
                img.generated_color[0] = item[0][0] / 255
                img.generated_color[1] = item[0][1] / 255
                img.generated_color[2] = item[0][2] / 255
                texture = bpy.data.textures.new('colormatch_texture' + str(i), type='IMAGE')
                texture.image = img
                __class__.__match_textures.append([img, texture])

    @staticmethod
    def clear_match_textures():
        if __class__.__match_textures:
            for item in __class__.__match_textures:
                bpy.data.images.remove(item[0], do_unlink=True)
                bpy.data.textures.remove(item[1], do_unlink=True)
        __class__.__match_textures = []

    @staticmethod
    def clear():
        __class__.__matches = []
        __class__.clear_match_textures()


class ColorMatchingVars(bpy.types.PropertyGroup):
    source_color = bpy.props.FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.8, 0.8, 1.0)
    )


class ColorMatchingStatic:
    matching_count = 5


class DestColorItem(bpy.types.PropertyGroup):
    dest_color = bpy.props.FloatVectorProperty(
         name='Color',
         subtype='COLOR',
         size=4,
         min=0.0,
         max=1.0,
         default=(0.8, 0.8, 0.8, 1.0)
     )


def register():
    bpy.utils.register_class(ColorMatchingVars)
    bpy.utils.register_class(DestColorItem)
    bpy.types.WindowManager.colormatching_vars = bpy.props.PointerProperty(type=ColorMatchingVars)
    bpy.types.WindowManager.colormatching_colors = bpy.props.CollectionProperty(type=DestColorItem)


def unregister():
    del bpy.types.WindowManager.colormatching_colors
    del bpy.types.WindowManager.colormatching_vars
    bpy.utils.unregister_class(DestColorItem)
    bpy.utils.unregister_class(ColorMatchingVars)

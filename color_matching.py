# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching


import bpy
from bpy.props import FloatVectorProperty, PointerProperty, CollectionProperty
from bpy.types import PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class
import os
import json
import copy
from mathutils import Vector
from .b3d_lib_int.rgb import RGB


class ColorMatching:

    _matches = []  # search results -> first element - rgb color
    _match_textures = []   # [[image1, texutre1], [image2, texture2], ...]

    @classmethod
    def search_by_rgb(cls, context, db, rgb, limit):
        cls.clear(context)
        if db == 'NCS':
            cls._matches = NCS_DB.search(rgb, limit)
        elif db == 'RAL_C':
            cls._matches = RAL_C_DB.search(rgb, limit)
        elif db == 'RAL_D':
            cls._matches = RAL_D_DB.search(rgb, limit)
        elif db == 'RAL_E':
            cls._matches = RAL_E_DB.search(rgb, limit)
        elif db == 'PANTONE':
            cls._matches = PANTONE_DB.search(rgb, limit)

    @classmethod
    def matches(cls):
        return cls._matches

    @classmethod
    def matches_str(cls, context, db):
        matches_str = ''
        if cls._matches:
            matches_str += '%\t\tRGB\t\t\t'+db+'\t\t\tHEX\t\tCMYK\n'
            for line in cls._matches:
                matches_str += '{:<7.2%}\t{:03d}-{:03d}-{:03d}\t{:<15}\t'.format(line[2], int(line[0][0]), int(line[0][1]), int(line[0][2]), line[1][0])
                matches_str += '{}\t{}'.format(line[1][3], '-'.join([a.zfill(3) for a in line[1][1].split('-')]))
                matches_str += '\n'
        return matches_str

    @classmethod
    def match_textures(cls):
        return cls._match_textures

    @classmethod
    def create_match_textures(cls):
        if cls._matches:
            for i, item in enumerate(cls._matches):
                img = bpy.data.images.new('colormatch_image' + str(i), 255, 255)
                matchcolor = RGB.fromlist(item[0]).as_linear()
                img.generated_color[0] = matchcolor[0]
                img.generated_color[1] = matchcolor[1]
                img.generated_color[2] = matchcolor[2]
                texture = bpy.data.textures.new('colormatch_texture' + str(i), type='IMAGE')
                texture.image = img
                cls._match_textures.append([img, texture])

    @classmethod
    def clear_match_textures(cls):
        if cls._match_textures:
            for item in cls._match_textures:
                bpy.data.images.remove(image=item[0], do_unlink=True)
                bpy.data.textures.remove(image=item[1], do_unlink=True)
        cls._match_textures = []

    @classmethod
    def clear(cls, context):
        cls._matches = []
        cls.clear_match_textures()


class ColorDB:

    # DB format: [[[RGB], [NCS/RAL/PANTONR, CMYK (C), CMYK (U), HTML]], [...], ...]
    _database = None
    _database_file = None

    @classmethod
    def db(cls):
        if not cls._database:
            with open(cls._database_file) as data:
                cls._database = json.load(data)
        return cls._database

    @classmethod
    def search(cls, rgb, limit):
        rgb_vector = rgb.as_vector()
        db = cls.db()
        rez = copy.deepcopy(sorted(db, key=lambda x: (rgb_vector - Vector((x[0][0], x[0][1], x[0][2]))).length)[:limit])
        for result in rez:
            result.append(RGB.relevance(rgb, RGB.fromlist(result[0])))
        return rez


class NCS_DB(ColorDB):

    _database_file = os.path.join(os.path.dirname(__file__), 'ncs.json')


class RAL_C_DB(ColorDB):

    _database_file = os.path.join(os.path.dirname(__file__), 'ral_c.json')


class RAL_D_DB(ColorDB):

    _database_file = os.path.join(os.path.dirname(__file__), 'ral_d.json')


class RAL_E_DB(ColorDB):

    _database_file = os.path.join(os.path.dirname(__file__), 'ral_e.json')


class PANTONE_DB(ColorDB):

    _database_file = os.path.join(os.path.dirname(__file__), 'pantone.json')


class ColorMatchingVars(PropertyGroup):

    source_color: FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.8, 0.8, 1.0)
    )


class DestColorItem(PropertyGroup):

    dest_color: FloatVectorProperty(
         name='Color',
         subtype='COLOR',
         size=4,
         min=0.0,
         max=1.0,
         default=(0.8, 0.8, 0.8, 1.0)
     )


def register():
    register_class(ColorMatchingVars)
    register_class(DestColorItem)
    WindowManager.colormatching_vars = PointerProperty(type=ColorMatchingVars)
    WindowManager.colormatching_colors = CollectionProperty(type=DestColorItem)


def unregister():
    del WindowManager.colormatching_colors
    del WindowManager.colormatching_vars
    unregister_class(DestColorItem)
    unregister_class(ColorMatchingVars)

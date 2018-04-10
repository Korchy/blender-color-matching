# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/blender-color-matching
#
# Version history:
#   1.0. - Search for some nearest alternative system colors by RGB value


import math
import re
from mathutils import Vector


class RGB:

    __r = None
    __g = None
    __b = None

    __relevance0 = math.sqrt(3)*255   # rgb colors relevance = 0 when compare 2 rgb colors (diagonal of the rgb-cube 255x255x255)

    def __init__(self, r, g, b):
        if isinstance(r, int) and r >= 0 and r <= 255 and isinstance(g, int) and g >= 0 and g <= 255 and isinstance(b, int) and b >= 0 and b <= 255:
            self.__r = r
            self.__g = g
            self.__b = b
        if isinstance(r, float) and r >= 0.0 and r <= 1.0 and isinstance(g, float) and g >= 0.0 and g <= 1.0 and isinstance(b, float) and b >= 0.0 and b <= 1.0:
            self.__r = 255 * r
            self.__g = 255 * g
            self.__b = 255 * b

    def __repr__(self):
        return "RGB({},{},{})".format(self.__r, self.__g, self.__b)

    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g

    @property
    def b(self):
        return self.__b

    @classmethod
    def fromstring(cls, rgb):
        if re.compile('^\d{1,3}-\d{1,3}-\d{1,3}$').match(rgb) is not None:
            # 123-123-123
            rgbarr = rgb.split('-')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        elif re.compile('^\d{1,3}.\d{1,3}.\d{1,3}$').match(rgb) is not None:
            # 123.123.123
            rgbarr = rgb.split('.')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        else:
            return None

    @classmethod
    def fromlist(cls, lst):
        # [0-255, 0-255, 0-255] or [0.0-1.0, 0.0-1.0, 0.0-1.0]
        return cls(lst[0], lst[1], lst[2])

    @staticmethod
    def relevance(rgb1, rgb2):
        if isinstance(rgb1, RGB) and isinstance(rgb2, RGB):
            relevancelengtn = (__class__.rgb_to_vector(rgb1) - __class__.rgb_to_vector(rgb2)).length
            return 1 - relevancelengtn / __class__.__relevance0
        else:
            return 0

    @staticmethod
    def rgb_to_vector(rgb):
        if isinstance(rgb, RGB):
            return Vector((rgb.r, rgb.g, rgb.b))

    def to_vector(self):
        return __class__.rgb_to_vector(self)

    @staticmethod
    def rgb_to_unit(rgb):
        if isinstance(rgb, RGB):
            return [rgb.r / 255, rgb.g / 255, rgb.b / 255]

    def to_unit(self):
        return __class__.rgb_to_unit(self)

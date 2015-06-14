from __future__ import division
import math
import FreeCAD
import Part
import Units
from FreeCAD import Vector


class PartialHexScrewISO4014(object):
    """
    Part thread hex head bolt.

        ------------    +--,-------.--+
           ^           /,-'         `-.\
           |         ,"`       y       `.
           |        /          ^         ".
           |       /           |           \
           |      /;           |           :\
         s |     + |           +------>    | +
           |      \:         O        x    ;/
           |       :                      ./
           |     |  \                    ."  |
           |     |   `.                ,/    |
           v     |     \'-.         ,-'/     |
        ---------|--    +--`-------'--+      |
                 |                           |
                 |<------------------------->|
                 |             e             |


        |<-k->|
        :_____:
        /     |
        |     |
        y     |____________________              ______
        |     |     ^              \/\/\/\/\/\/\/\  ^
        |     |     |              \\\\\\\\\\\\\\\) |
        +-----+-->  |ds            \\\\\\\\\\\\\\\| |d
       O|     |  z  |              \\\\\\\\\\\\\\\) |
        |     |_____v______________/\/\/\/\/\/\/\/__v__
        |     |                    |              |
        |     |                    |              |
        \_____|                    |<-----b------>|
              :                                   |
              |<------------length--------------->|
    """

    _PROPERTY_NAMES = (
        "size", "length"
    )

    def __init__(self, obj):
        size_list = list(iso_4014_1979_partial_hex_screw["sizes"].keys())
        # the size list needs to be sorted for the number after the "M...",
        # so it shows up properly in the drop-down of the property editor
        size_list.sort(
            cmp=lambda x, y: int(x[1:]) - int(y[1:])
        )
        obj.addProperty(
            "App::PropertyEnumeration", "size", "PartialHexScrewISO4014",
            "ISO size of the screw"
        ).size = size_list
        obj.addProperty(
            "App::PropertyLength", "length", "PartialHexScrewISO4014",
            "The length of the screw shaft"
        ).length = 15
        obj.Proxy = self

    def onChanged(self, part, prop):
        # only recalculate the shape if relevant properties are changed
        if prop in self._PROPERTY_NAMES:
            self.execute(part)

    def execute(self, part):
        data = iso_4014_1979_partial_hex_screw["sizes"][part.size]
        # the calculations are based on the ACII art picture above,
        # with the points starting from the far right point,
        # and ending with the same point to close the polygon
        y_distance = 0.5 * data["s_max"]
        angle = math.pi / 3
        head_radius = y_distance / math.sin(angle)
        x_distance = math.cos(angle) * head_radius
        points = [
            Vector(head_radius, 0, 0),
            Vector(x_distance, y_distance, 0),
            Vector(-x_distance, y_distance, 0),
            Vector(-head_radius, 0, 0),
            Vector(-x_distance, -y_distance, 0),
            Vector(x_distance, -y_distance, 0),
            Vector(head_radius, 0, 0),
        ]
        # create a polygon and transform it to a face too:
        hexagon = Part.Face(Part.makePolygon(points))
        # just an integer won't work here, must use units:
        k = data["k_nom"] * Units.MilliMetre
        head = hexagon.extrude(Vector(0, 0, k))
        shaft = Part.makeCylinder(
            0.5 * data["ds_max"], part.length + k,
            Vector(0, 0, 0), Vector(0, 0, 1)
        )
        part.Shape = head.fuse(shaft)


iso_4014_1979_partial_hex_screw = {
    "iso": "4014-1979",
    "thread": "partial",
    "head": "hex",
    "sizes": {
        "M3": {
            "d": 3,
            "thread_pitch": 0.5,
            "b1": 12,
            "b2": None,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.4,
            "ds_max": 3,
            "ds_min": 2.86,
            "k_nom": 2,
            "k_min_1": 1.8,
            "k_max_1": 2.12,
            "k_min_2": None,
            "k_max_2": None,
            "s_max": 5.5,
            "s_min": 5.32,
            "product_grade": "A",
            "deprecation": None,
        },
        "M4": {
            "d": 4,
            "thread_pitch": 0.7,
            "b1": 14,
            "b2": None,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.4,
            "ds_max": 4,
            "ds_min": 3.82,
            "k_nom": 2.8,
            "k_min_1": 2.68,
            "k_max_1": 2.92,
            "k_min_2": None,
            "k_max_2": None,
            "s_max": 7,
            "s_min": 6.78,
            "product_grade": "A",
            "deprecation": None,
        },
        "M5": {
            "d": 5,
            "thread_pitch": 0.8,
            "b1": 16,
            "b2": None,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.5,
            "ds_max": 5,
            "ds_min": 4.82,
            "k_nom": 3.5,
            "k_min_1": 3.35,
            "k_max_1": 3.65,
            "k_min_2": 3.26,
            "k_max_2": 3.74,
            "s_max": 8,
            "s_min": 7.78,
            "product_grade": "A",
            "deprecation": None,
        },
        "M6": {
            "d": 6,
            "thread_pitch": 1,
            "b1": 18,
            "b2": None,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.5,
            "ds_max": 6,
            "ds_min": 5.82,
            "k_nom": 4,
            "k_min_1": 3.85,
            "k_max_1": 4.15,
            "k_min_2": 3.76,
            "k_max_2": 4.24,
            "s_max": 10,
            "s_min": 9.78,
            "product_grade": "A",
            "deprecation": None,
        },
        "M8": {
            "d": 8,
            "thread_pitch": 1.25,
            "b1": 22,
            "b2": 28,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.6,
            "ds_max": 8,
            "ds_min": 7.78,
            "k_nom": 5.3,
            "k_min_1": 5.15,
            "k_max_1": 5.45,
            "k_min_2": 5.06,
            "k_max_2": 5.54,
            "s_max": 13,
            "s_min": 12.73,
            "product_grade": "A",
            "deprecation": None,
        },
        "M10": {
            "d": 10,
            "thread_pitch": 1.5,
            "b1": 26,
            "b2": 32,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.6,
            "ds_max": 10,
            "ds_min": 9.78,
            "k_nom": 6.4,
            "k_min_1": 6.22,
            "k_max_1": 6.58,
            "k_min_2": 6.11,
            "k_max_2": 6.69,
            "s_max": 16,
            "s_min": 15.73,
            "product_grade": "A",
            "deprecation": None,
        },
        "M12": {
            "d": 12,
            "thread_pitch": 1.75,
            "b1": 30,
            "b2": 36,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.6,
            "ds_max": 12,
            "ds_min": 11.73,
            "k_nom": 7.5,
            "k_min_1": 7.32,
            "k_max_1": 7.68,
            "k_min_2": 7.21,
            "k_max_2": 7.79,
            "s_max": 18,
            "s_min": 17.73,
            "product_grade": "A",
            "deprecation": None,
        },
        "M14": {
            "d": 14,
            "thread_pitch": 2,
            "b1": 34,
            "b2": 40,
            "b3": None,
            "min_washer_face": 0.15,
            "max_washer_face": 0.6,
            "ds_max": 14,
            "ds_min": 13.73,
            "k_nom": 8.8,
            "k_min_1": 8.62,
            "k_max_1": 8.98,
            "k_min_2": 8.51,
            "k_max_2": 9.09,
            "s_max": 21,
            "s_min": 20.67,
            "product_grade": "A",
            "deprecation": "avoid",
        },
        "M16": {
            "d": 16,
            "thread_pitch": 2,
            "b1": 38,
            "b2": 44,
            "b3": 57,
            "min_washer_face": 0.2,
            "max_washer_face": 0.8,
            "ds_max": 16,
            "ds_min": 15.73,
            "k_nom": 10,
            "k_min_1": 9.82,
            "k_max_1": 10.18,
            "k_min_2": 9.71,
            "k_max_2": 10.29,
            "s_max": 24,
            "s_min": 23.67,
            "product_grade": "A",
            "deprecation": None,
        },
        "M20": {
            "d": 20,
            "thread_pitch": 2.5,
            "b1": 46,
            "b2": 52,
            "b3": 65,
            "min_washer_face": 0.2,
            "max_washer_face": 0.8,
            "ds_max": 20,
            "ds_min": 19.67,
            "k_nom": 12.5,
            "k_min_1": 12.28,
            "k_max_1": 12.72,
            "k_min_2": 12.15,
            "k_max_2": 12.85,
            "s_max": 30,
            "s_min": 29.67,
            "product_grade": "A",
            "deprecation": None,
        },
        "M24": {
            "d": 24,
            "thread_pitch": 3,
            "b1": 54,
            "b2": 60,
            "b3": 73,
            "min_washer_face": 0.2,
            "max_washer_face": 0.8,
            "ds_max": 24,
            "ds_min": 23.67,
            "k_nom": 15,
            "k_min_1": 14.78,
            "k_max_1": 15.22,
            "k_min_2": 14.65,
            "k_max_2": 15.35,
            "s_max": 36,
            "s_min": 35.38,
            "product_grade": "A",
            "deprecation": None,
        },
        "M30": {
            "d": 30,
            "thread_pitch": 3.5,
            "b1": 66,
            "b2": 72,
            "b3": 85,
            "min_washer_face": 0.2,
            "max_washer_face": 0.8,
            "ds_max": 30,
            "ds_min": 29.67,
            "k_nom": 18.7,
            "k_min_1": None,
            "k_max_1": None,
            "k_min_2": 18.28,
            "k_max_2": 19.12,
            "s_max": 46,
            "s_min": 45,
            "product_grade": "B",
            "deprecation": None,
        },
        "M36": {
            "d": 36,
            "thread_pitch": 4,
            "b1": 78,
            "b2": 84,
            "b3": 97,
            "min_washer_face": 0.2,
            "max_washer_face": 0.8,
            "ds_max": 36,
            "ds_min": 35.61,
            "k_nom": 22.5,
            "k_min_1": None,
            "k_max_1": None,
            "k_min_2": 22.08,
            "k_max_2": 22.92,
            "s_max": 55,
            "s_min": 53.8,
            "product_grade": "B",
            "deprecation": None,
        },
    }
}

class Linedef:
    # 14 bytes = 2H x 7
    __slots__ = [
        'start_vertex_id',
        'end_vertex_id',
        'flags',
        'line_type',
        'sector_tag',
        'front_sidedef_id',
        'back_sidedef_id'
    ]



class Node:
    class Bbox:
        __slots__ = [
            "top",
            "bottom",
            "left",
            "right"
        ]
    __slots__ = [
        "x_partition",
        "y_partition",
        "dx_partition",
        "dy_partition",
        "bbox",
        "front_child_id",
        "back_child_id"
    ]
    def __init__(self):
        self.bbox = {"front": self.Bbox(), "back": self.Bbox() }



class SubSector:
    __slots__ = [
        "seg_counts",
        "first_seg_id"
    ]

class Seg:
    __slots__ = [
        "start_vertex_id",
        "end_vertex_id",
        "angle",
        "linedef_id",
        "direction",
        "offset"
    ]


class Thing:
    __slot__ = [
        "pos",
        "angle",
        "type",
        "flags"
    ]

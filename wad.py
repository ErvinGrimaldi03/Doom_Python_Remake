import os
import struct
from pygame.math import Vector2
from data_types import *

class Wad(object):
    def __init__(self, wad_path):
        self.wad_file = open(wad_path, "rb")
        self.header = self.read_header()
        self.directory = self.read_directory()

    def read_thing(self, offset):
        thing = Thing()
        read_2bytes = self.read_2bytes

        x = read_2bytes(offset, byte_format='h')
        y = read_2bytes(offset + 2, byte_format='h')

        thing.angle = read_2bytes(offset + 4 , byte_format='H')
        thing.type = read_2bytes(offset + 6, byte_format='H')
        thing.flags = read_2bytes(offset + 8, byte_format='H')
        thing.pos = Vector2(x, y)
        return thing

    def read_segment(self, offset):
        read_2_bytes = self.read_2bytes

        seg = Seg()
        seg.start_vertex_id = read_2_bytes(offset, byte_format='h')
        seg.end_vertex_id = read_2_bytes(offset + 2, byte_format='h')
        seg.angle = read_2_bytes(offset+4, byte_format='h')
        seg.linedef_id =read_2_bytes(offset+6, byte_format='h')
        seg.direction = read_2_bytes(offset+8, byte_format='h')
        seg.offset = read_2_bytes(offset+10, byte_format='h')
        return seg

    def read_sub_sector(self, offset):
        read_2bytes = self.read_2bytes

        sub_sector = SubSector()
        sub_sector.seg_count = read_2bytes(offset, byte_format='h')
        sub_sector.first_seg_id = read_2bytes(offset + 2, byte_format='h')

        return sub_sector

    def read_node(self, offset):
        read_2bytes = self.read_2bytes

        node = Node()
        node.x_partition = read_2bytes(offset, byte_format='h')
        node.y_partition = read_2bytes(offset + 2, byte_format='h')
        node.dx_partition = read_2bytes(offset + 4, byte_format='h')
        node.dy_partition = read_2bytes(offset + 6, byte_format='h')

        node.bbox["front"].top = read_2bytes(offset + 8, byte_format='h')
        node.bbox["front"].bottom = read_2bytes(offset + 10, byte_format='h')
        node.bbox["front"].left = read_2bytes(offset + 12, byte_format='h')
        node.bbox["front"].right = read_2bytes(offset + 14, byte_format='h')

        node.bbox["back"].top = read_2bytes(offset + 16, byte_format='h')
        node.bbox["back"].bottom = read_2bytes(offset + 18, byte_format='h')
        node.bbox["back"].left = read_2bytes(offset + 20, byte_format='h')
        node.bbox["back"].right = read_2bytes(offset + 22, byte_format='h')

        node.front_child_id = read_2bytes(offset + 24, byte_format="H")
        node.back_child_id = read_2bytes(offset + 26, byte_format="H")
        return node




    def read_header(self):
        return {
            "wad_type": self.read_toString(offset=0, num_bytes=4),
            "lump_count": self.read_4bytes(offset=4),
            "init_offset": self.read_4bytes(offset=8)
        }

    def read_directory(self):
        directory = []
        for i in range(self.header["lump_count"]):
            offset = self.header["init_offset"] + i * 16
            lump_info = {
                "lump_offset": self.read_4bytes(offset),
                "lump_size": self.read_4bytes(offset + 4),
                "lump_name": self.read_toString(offset=offset + 8, num_bytes=8)
            }
            directory.append(lump_info)
        return directory

    def read_vertex(self, offset):
        x = self.read_2bytes(offset, byte_format='h')
        y = self.read_2bytes(offset + 2, byte_format='h')
        return Vector2(x, y)

    def read_sector(self, offset):
        read_2bytes = self.read_2bytes
        read_string = self.read_toString
        sector = Sector()
        sector.floor_height = read_2bytes(offset, byte_format='h')
        sector.ceil_height = read_2bytes(offset+ 2, byte_format='h')
        sector.floor_texture = read_string(offset+ 4, num_bytes=8)
        sector.ceil_texture = read_string(offset+ 12, num_bytes=8)
        sector.light_level = read_2bytes(offset+ 20, byte_format='H')
        sector.type = read_2bytes(offset+ 22, byte_format='H')
        sector.tag = read_2bytes(offset+ 24, byte_format='H')
        return sector

    def read_sidedef(self, offset):
        # 30 bytes = 2h + 2h + 8c + 8c + 8c + 2H
        read_2_bytes = self.read_2bytes
        read_string = self.read_toString
        sidedef = Sidedef()
        sidedef.x_offset = read_2_bytes(offset, byte_format='h')
        sidedef.y_offset = read_2_bytes(offset + 2, byte_format='h')
        sidedef.upper_texture = read_string(offset + 4, num_bytes=8)
        sidedef.lower_texture = read_string(offset + 12, num_bytes=8)
        sidedef.middle_texture = read_string(offset + 20, num_bytes=8)
        sidedef.sector_id = read_2_bytes(offset + 28, byte_format='H')
        return sidedef

    def read_linedef(self, offset):
        read_2bytes = self.read_2bytes

        linedef = Linedef()
        linedef.start_vertex_id = read_2bytes(offset, byte_format='H')
        linedef.end_vertex_id = read_2bytes(offset + 2, byte_format='H')
        linedef.flags = read_2bytes(offset + 4, byte_format='H')
        linedef.line_type = read_2bytes(offset + 6, byte_format='H')
        linedef.sector_tag = read_2bytes(offset + 8, byte_format='H')
        linedef.front_sidedef_id = read_2bytes(offset + 10, byte_format='H')
        linedef.back_sidedef_id = read_2bytes(offset + 12, byte_format='H')
        return linedef

    def read_1byte(self, offset, byte_format='B'):
        return self.read_bytes(offset=offset, num_bytes=1, byte_format=byte_format)[0]

    def read_2bytes(self, offset, byte_format):
        return self.read_bytes(offset=offset, num_bytes=2, byte_format=byte_format)[0]

    def read_4bytes(self, offset, byte_format='i'):
        return self.read_bytes(offset=offset, num_bytes=4, byte_format=byte_format)[0]

    def read_toString(self, offset, num_bytes):
        return ''.join(b.decode("ascii") for b in self.read_bytes(offset, num_bytes, byte_format='c' * num_bytes) if
                       ord(b) != 0).upper()

    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)  # Start reading from offset
        buffer = self.wad_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)

    def close(self):
        self.wad_file.close()


class WadData(object):
    LUMP_INDICES = {
        "THINGS": 1, "LINEDEFS": 2, "SIDEDEFS": 3, "VERTEXES": 4, "SEGS": 5, "SSECTORS": 6, "NODES": 7, "SECTORS": 8,
        "REJECT": 9, "BLOCKMAP": 10
    }
    LINEDEF_FLAGS = {
        'BLOCKING': 1, 'BLOCK_MONSTERS': 2, 'TWO_SIDED': 4, 'DONT_PEG_TOP': 8,
        'DONT_PEG_BOTTOM': 16, 'SECRET': 32, 'SOUND_BLOCK': 64, 'DONT_DRAW': 128, 'MAPPED': 256
    }
    def __init__(self, engine, map_name):
        self.reader = Wad(engine.wad_path)

        self.map_name = map_name
        self.map_index = self.get_lump_index(lump_name=self.map_name)
        self.vertexes = self.get_lump_data(
            reader_func=self.reader.read_vertex,
            lump_index=self.map_index + self.LUMP_INDICES["VERTEXES"],
            num_bytes=4
        )
        self.linedefs = self.get_lump_data(
            reader_func=self.reader.read_linedef,
            lump_index = self.map_index + self.LUMP_INDICES['LINEDEFS'],
            num_bytes = 14
        )

        self.nodes = self.get_lump_data(
            reader_func=self.reader.read_node,
            lump_index=self.map_index + self.LUMP_INDICES['NODES'],
            num_bytes = 28
        )

        self.sub_sectors = self.get_lump_data(
            reader_func = self.reader.read_sub_sector,
            lump_index = self.map_index + self.LUMP_INDICES["SSECTORS"],
            num_bytes = 4
        )

        self.segments = self.get_lump_data(
            reader_func = self.reader.read_segment,
            lump_index = self.map_index + self.LUMP_INDICES["SEGS"],
            num_bytes = 12
        )

        self.things = self.get_lump_data(
            reader_func = self.reader.read_thing,
            lump_index = self.map_index + self.LUMP_INDICES["THINGS"],
            num_bytes = 10
        )

        self.sidedefs = self.get_lump_data(
            reader_func=self.reader.read_sidedef,
            lump_index=self.map_index + self.LUMP_INDICES['SIDEDEFS'],
            num_bytes=30
        )
        self.sectors = self.get_lump_data(
            reader_func=self.reader.read_sector,
            lump_index=self.map_index + self.LUMP_INDICES['SECTORS'],
            num_bytes=26
        )

        [print(i) for i in self.vertexes]
        self.update_data()
        self.reader.close()


    def update_data(self):
        self.update_linedefs()
        self.update_sidedefs()
        self.update_segs()

    def update_sidedefs(self):
        for sidedef in self.sidedefs:
            sidedef.sector = self.sectors[sidedef.sector_id]

    def update_linedefs(self):
        for linedef in self.linedefs:
            linedef.front_sidedef = self.sidedefs[linedef.front_sidedef_id]
            if linedef.back_sidedef_id == 0xFFFF:
                linedef.back_sidedef = None
            else:
                linedef.back_sidedef = self.sidedefs[linedef.back_sidedef_id]

    def update_segs(self):
        for seg in self.segments:
            seg.start_vertex = self.vertexes[seg.start_vertex_id]
            seg.end_vertex = self.vertexes[seg.end_vertex_id]
            seg.linedef = self.linedefs[seg.linedef_id]
            # ----------------------------------------------------- #
            if seg.direction:
                front_sidedef = seg.linedef.back_sidedef
                back_sidedef = seg.linedef.front_sidedef
            else:
                front_sidedef = seg.linedef.front_sidedef
                back_sidedef = seg.linedef.back_sidedef
            #
            seg.front_sector = front_sidedef.sector
            if self.LINEDEF_FLAGS['TWO_SIDED'] & seg.linedef.flags:
                seg.back_sector = back_sidedef.sector
            else:
                seg.back_sector = None
            # ----------------------------------------------------- #

            # convert angles from BAMS to degrees
            seg.angle = (seg.angle << 16) * 8.38190317e-8
            seg.angle = seg.angle + 360 if seg.angle < 0 else seg.angle

    @staticmethod
    def print_attrs(obj):
        for attr in obj.__slots__:
            print(eval(f'obj.{attr}'), end=' ')

    def get_lump_data(self, reader_func, lump_index, num_bytes, header_length=0):
        lump_info = self.reader.directory[lump_index]
        count = lump_info['lump_size'] // num_bytes
        data = []
        for i in range(count):
            offset = lump_info['lump_offset'] + i * num_bytes + header_length
            data.append(reader_func(offset))
        return data

    def get_lump_index(self, lump_name):
        for index, lump in enumerate(self.reader.directory):
            if lump_name in lump.values():
                return index

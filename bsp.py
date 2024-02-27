from settings import *

class BSP:
    SUB_SECTOR_IDENTIFIER = 0x8000  # 2**15 = 32768

    def __init__(self, engine):
        self.engine = engine
        self.player = engine.player
        self.nodes = engine.wad_data.nodes
        self.sub_sectors = engine.wad_data.sub_sectors
        self.segs = engine.wad_data.segments
        self.root_node_id = len(self.nodes) - 1

    def update(self):
        pass
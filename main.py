from wad import WadData
from settings import *
import pygame as pg
import sys
from map_render import MapRender
from player import Player
from bsp import BSP
from view_render import ViewRender
from seg_handler import SegHandler
class DoomEngine:
    def __init__(self, wad_path=r"C:\Users\grima\PycharmProjects\Doom_Python_Remake\WAV\DOOM.WAD"):
        self.wad_path = wad_path
        self.screen = pg.display.set_mode((WIN_RES))
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 1/60

        self.init()

    def init(self):
        self.wad_data = WadData(self, map_name="E3M1")
        self.map_render = MapRender(self)
        self.player = Player(self)
        self.bsp = BSP(self)
        self.seg_handler = SegHandler(self)
        self.view_render = ViewRender(self)



    def update(self):
        self.player.update()
        self.seg_handler.update()
        self.bsp.update()
        self.dt = self.clock.tick()
        pg.display.set_caption(f"{self.clock.get_fps()}")

    def draw(self):
        pg.display.flip()
        # self.screen.fill("black")
        # self.map_render.draw()


    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()



if __name__ == "__main__":
    Doom = DoomEngine()
    Doom.run()

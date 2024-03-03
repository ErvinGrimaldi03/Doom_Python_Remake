import math

from settings import *
from pygame.math import Vector2
import pygame as pg

class Player:
    def __init__(self, engine):
        self.engine = engine
        self.thing = engine.wad_data.things[0]
        self.pos = self.thing.pos
        self.angle = self.thing.angle
        self.height = PLAYER_HEIGHT
        self.DIAG_MOVE_CORR = 1 / math.sqrt(2)

    def get_player_hight(self):
        self.height = self.engine.bsp.get_sub_sectors_height() + PLAYER_HEIGHT

    def update(self):
        self.get_player_hight()
        self.control()

    def control(self):
        speed = PLAYER_SPEED * self.engine.dt
        rot_speed = PLAYER_ROTATION_SPEED * self.engine.dt

        key_state = pg.key.get_pressed()
        if key_state[pg.K_LEFT]:
            self.angle += rot_speed
        if key_state[pg.K_RIGHT]:
            self.angle -= rot_speed

        inc = Vector2(0)
        if key_state[pg.K_a]:
            inc += Vector2(0, speed).rotate(self.angle)
        if key_state[pg.K_d]:
            inc += Vector2(0, -speed).rotate(self.angle)
        if key_state[pg.K_w]:
            inc += Vector2(speed, 0).rotate(self.angle)
        if key_state[pg.K_s]:
            inc += Vector2(-speed, 0).rotate(self.angle)

        if inc.x and inc.y:
            inc *= self.DIAG_MOVE_CORR
        self.pos += inc
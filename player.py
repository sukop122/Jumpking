import pygame as pg
from settings import *
from utility import image_cutter, load_animation

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, sheet):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_y = 0
        self.state = "idle"
        self.index = 0
        self.animation_speed = 0.15

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.animations = {
            "idle": load_animation(sheet, 0, 4, 15, 21, 1)
            
        }

    def update(self):
        gravity = 0.5
        
        self.vel_y += gravity
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)

        self.state = "idle"

        if self.index >= len(self.animations["idle"]):
            self.index = 0

    def drew(self, screen):
        frame = self.animations["idle"][(self.index)]
        screen.blit(frame, (self.x, self.y))

    def jump(self, power):
        self.vel_y = -power
        self.index = 0
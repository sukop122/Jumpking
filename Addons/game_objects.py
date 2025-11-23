import pygame as pg
import json

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)

    def draw(self, screen):
        pg.draw.rect(screen, (100, 60, 20), self.rect)
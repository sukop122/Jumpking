import pygame as pg
import sys, json, os
import random
from settings import *
from player import Player

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.init()

screen = pg.display((screen_width, screen_height))

clock = pg.time.Clock()
running = True

sheet = pg.image.load("assets/dataset/brackey/sprites/knight.png").convert_alpha()

player = Player(400, (screen_height - 50))

while running:
    screen.fill((30, 30, 30))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:


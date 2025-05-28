import pygame as pg
import sys, json, os
import random
from settings import *
from player import Player
from game_objects import Platform


os.chdir(os.path.dirname(os.path.abspath(__file__)))



pg.init()

screen = pg.display.set_mode((screen_width, screen_height))

clock = pg.time.Clock()
running = True

sheet = pg.image.load("assets/dataset/brackey/sprites/knight.png").convert_alpha()

player = Player(400, (screen_height - 50), sheet)

while running:
    screen.fill((30, 30, 30))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    player.update(keys)
    player.draw(screen)

    pg.display.update()
    clock.tick(60)

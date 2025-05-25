import pygame as pg
import sys, json, os
import random
from settings import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.init()

screen = pg.display((screen_width, screen_height))

clock = pg.time.Clock()
running = True


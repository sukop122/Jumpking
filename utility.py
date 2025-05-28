import pygame as pg, json
from game_objects import Platform

def image_cutter(sheet, frame_x, frame_y, width, height, scale):
    img = pg.Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame_x * width),(frame_y * height), width, height))
    img = pg.transform.scale(img,(width*scale, height*scale))
    img.set_colorkey((0,0,0))
    return img

def load_animation(sheet, row, frame_count, width, height, scale):
    frames = []
    for i in range(frame_count):
        frame = image_cutter(sheet, i, row, width, height, scale)
        frames.append(frame)
    return frames

def load_platforms(path):
    with open(path) as file:
        data = json.load(file)


    platforms = []

    for entity in data["entities"]["Platform"]:
        x = entity["x"]
        y = entity["y"]
        w = entity["width"]
        h = entity["height"]
        platforms.append(Platform(x, y, w, h))

    return platforms

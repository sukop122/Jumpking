import pygame as pg

def image_cutter(sheet, frame_x, frame_y, width, height, scale):
    img = pg.Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame_x * width),(frame_y * height), width, height))
    img = pg.transform.scale(img,(width*scale, height*scale))
    img.set_colorkey((0,0,0))
    return img

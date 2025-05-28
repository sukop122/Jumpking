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
        self.vel_x = 0
        self.jump_direction = 0
        self.on_ground = False
        self.charging = False
        self.charge_power = 0
        self.max_charge = 18
        self.in_air = False
        self.speed = 2.5

        self.state = "idle"
        self.index = 0
        self.animation_speed = 0.15

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.animations = {
            "idle": load_animation(sheet, 0, 4, 15, 21, 3),
            "charge": load_animation(sheet, 0, 4, 15, 21, 3),
            "jump": load_animation(sheet, 0, 4, 15, 21, 3),
            "fall": load_animation(sheet, 0, 4, 15, 21, 3)
        } 

    def update(self, keys):
        
        if not self.in_air:
            if keys[pg.K_a]:
                self.x -= self.speed
            if keys[pg.K_d]:
                self.x += self.speed

        if self.on_ground:
            if keys[pg.K_SPACE]:
                self.charging = True
                self.charge_power += 0.5
                if self.charge_power > self.max_charge:
                    self.charge_power = self.max_charge
                self.state = "charge"
            elif self.charging:
                self.jump(self.charge_power)
                self.charging = False
                self.charge_power = 0
            else:
                self.state = "idle"
        
        gravity = 0.5
        
        self.vel_y += gravity
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)

        if self.y + self.height >= screen_height - 50:
            self.y = screen_height - 50 - self.height
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        

        if self.state in self.animations:
            self.index += self.animation_speed
            if self.index >= len(self.animations[self.state]):
                self.index = 0

        if self.y + self.height >= screen_height - 50:
            self.y = screen_height - 50 - self.height
            self.vel_y = 0 

    def draw_charge_bar(self, screen):
        if self.charging:
            bar_width = 40
            bar_height = 6
            charge_ratio = self.charge_power / self.max_charge
            filled_width = int(bar_width * charge_ratio)

            # pozice nad hlavou
            bar_x = self.x + self.width // 2 - bar_width // 2
            bar_y = self.y - 15

            
            bg_rect = pg.Rect(bar_x, bar_y, bar_width, bar_height)
            pg.draw.rect(screen, (50, 50, 50), bg_rect)

            # vyplněná část
            fill_rect = pg.Rect(bar_x, bar_y, filled_width, bar_height)
            pg.draw.rect(screen, (200, 0, 0), fill_rect)


    def draw(self, screen):
        frame = self.animations["idle"][int(self.index)]
        screen.blit(frame, (self.x, self.y))
        self.draw_charge_bar(screen)

    def jump(self, power):
        self.vel_y = -power
        self.index = 0
        self.state = "jump"
import pygame as pg
from Addons.settings import *
from Addons.utility import image_cutter, load_animation

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
        self.on_ground = True
        self.charging = False
        self.charge_power = 0
        self.max_charge = 18
        self.in_air = False
        self.speed = 2.5

        self.state = "idle"
        self.index = 0
        self.animation_speed = 0.1
        self.facing_right = True
        self.collision = False

        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.animations = {
            "idle": image_cutter(sheet, 0, 0, 32, 32, 3),
            "charge": image_cutter(sheet, 1, 0, 32, 32, 3),
            "jump": image_cutter(sheet, 2, 0, 32, 32, 3),
            "bump": image_cutter(sheet, 3, 0, 32, 32, 3),
            "fall": image_cutter(sheet, 4, 0, 32, 32, 3),
            "run": load_animation(sheet, row=1, frame_count=3, width=32, height=32, scale=3)
            
        } 

    def update(self, keys):
        

     #Movement Left and Right on ground

        if not self.charging and self.on_ground:
            if keys[pg.K_a]:
                self.vel_x = -self.speed
                self.facing_right = False
                self.jump_direction = -1
                self.state = "run"
                print(">> MOVE LEFT | state:", self.state)
                
            elif keys[pg.K_d]:
                self.vel_x = self.speed
                self.facing_right = True
                self.jump_direction = 1
                self.state = "run"
                print(">> MOVE RIGHT | state:", self.state)
            else:
                self.vel_x = 0
                self.state = "idle"
                

        

    #Jumping and Charging
     
        if self.on_ground:
            if keys[pg.K_SPACE]:
                self.charging = True
                self.charge_power += 0.5
            
                if self.charging == True:    
                    if keys[pg.K_a]:
                        self.facing_right = False
                        self.jump_direction = -1
                    elif keys[pg.K_d]:
                        self.facing_right = True
                        self.jump_direction = 1
                    elif keys[pg.K_w]:
                        self.jump_direction = 0
                
                if self.charge_power > self.max_charge:
                    self.charge_power = self.max_charge
                self.state = "charge"

            elif self.charging:
                self.jump(self.charge_power)
                self.charging = False
                self.charge_power = 0
            


        #Lock horizontal movement when charging or airborne
        if self.charging:
            self.vel_x = 0

        
    #Gravity
        gravity = 0.5
        self.vel_y += gravity

    #Aplication of velocities
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)
    #Collision with screen borders
        if self.in_air:
            if self.x <= -self.width:
                self.x = 0
                self.collision = True
                if self.collision == True:
                    self.facing_right = True
                    self.state = "bump"
                    
                    self.vel_x *= -0.6
                    if self.y == screen_height - 50 - self.height:
                        self.collision = False
            


            elif self.x + self.width  >= screen_width - 50:
                self.x = screen_width - self.width - 50
                self.collision = True
                if self.collision == True:
                    self.facing_right = False
                    self.state = "bump"
                    self.vel_x *= -0.6
                    if self.y == screen_height - 50 - self.height:
                        self.collision = False
                      
    
    #Ground level
        if self.y + self.height >= screen_height - 50: 
            self.y = screen_height - 50 - self.height
            self.vel_y = 0
            self.on_ground = True
            self.in_air = False
        else:
            self.on_ground = False
            self.in_air = True

        if self.vel_y > 0 and self.in_air and not self.collision:
            self.state = "fall"


        #Animation state changes - running
        if self.state == "run":
            print(self.index)
            self.index += self.animation_speed
            if self.index >= len(self.animations["run"]):
                self.index = 0
                

    #Jump function        
    def jump(self, power):
            side_force_multiplier = 0.5
            self.vel_y = -power
            self.vel_x = self.jump_direction * (power * side_force_multiplier)
            self.index = 0
            self.state = "jump"
            self.in_air = True
            self.on_ground = False

    def draw_charge_bar(self, screen):
        if self.charging:
            bar_width = 40
            bar_height = 6
            charge_ratio = self.charge_power / self.max_charge
            filled_width = int(bar_width * charge_ratio)

            #position above player
            bar_x = self.x + self.width // 2 - bar_width // 2
            bar_y = self.y - 15

            
            bg_rect = pg.Rect(bar_x, bar_y, bar_width, bar_height)
            pg.draw.rect(screen, (50, 50, 50), bg_rect)

            # vyplněná část
            fill_rect = pg.Rect(bar_x, bar_y, filled_width, bar_height)
            pg.draw.rect(screen, (200, 0, 0), fill_rect)


    def draw(self, screen):
        self.draw_charge_bar(screen)

        current_anim = self.animations[self.state]

        if isinstance(current_anim, list):
            frame = current_anim[int(self.index)]
        else:
            frame = current_anim  # single frame

        if self.facing_right:
            screen.blit(frame, (self.x, self.y))
        else:
            screen.blit(pg.transform.flip(frame, True, False), (self.x, self.y))



    def draw_coords (self, screen):
        font = pg.font.Font("assets/dataset/brackey/fonts/Jersey20-Regular.ttf", 24)
        text_X = font.render(f"X: {self.x}", False, "#FFFFFF")
        text_Y = font.render(f"Y: {self.y}", False, "#FFFFFF")
        screen.blit(text_X, (screen_width-100, 30))
        screen.blit(text_Y, (screen_width-100, 50))
    
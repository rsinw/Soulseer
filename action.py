import pygame 
from animation import *


class Action:

    def __init__(self, unit):
        self.unit = unit
        
       
        self.anim = self.attack_anim = Animation("resalt/Sprites/Attack1.png", 4)
        self.anim.repeat = False 
        self.image = pygame.image.load("resalt/ability_sprites/slash1.png")        # Create 100x100 surface 

        self.complete = False 

        self.duration = 1 * unit.haste
        self.real_duration = 0 
        self.working_duration = 0

        self.init_duration()

        self.working_cd = 0
        self.cd = 5 * 60 

    

    def update(self):
        self.anim.update()
        self.unit.switch_anim(self.anim)
        if self.anim.complete():
            self.complete = True 
    
    def reset(self):
        self.complete = False 
        self.anim.reset()

    def get_speed(self):
        return self.anim.num_frames * self.anim.frame_duration
    
    def init_duration(self):
        frames = self.duration * 60 
        frame_duration = frames // self.anim.num_frames 
        if frame_duration <= 0:
            frame_duration = 1 

        self.anim.frame_duration = frame_duration

        self.real_duration = frame_duration * self.anim.num_frames


class actionPlayerSlash(Action):
    pass

    
class Hitbox:
    def __init__(self, x, y, width, height):
        self.rect = None

        self.image = None

        self.units_hit = set()

        self.damage = 10
        self.draw_hitbox = False

        self.unit = None
        self.width = width
        self.height = height
    
    # element marker for enc 

        self.remove = False


    def on_hit(self, unit):

        unit.take_damage(self.damage)
        print(f"Hit unit {unit} for {self.damage} damage")
        print("Unit hit")

        if self.unit.rect.centerx < unit.rect.centerx:
            unit.knockback_dx += 5
            print("knocked back")
        else:
            unit.knockback_dx -= 5
            print("knocked back")
        
        self.unit.heal(10)

        pass

    def update(self):

        if self.wait > 0:
            self.wait -= 1
            self.draw_hitbox = False
            return
        
        if self.wait == 0:
            self.rect = pygame.Rect(0, 0, self.width, self.height)
            if self.unit.facing_right:

                self.rect.bottomleft = self.unit.rect.bottomright

            else:
                self.rect.bottomright = self.unit.rect.bottomleft


            self.image = pygame.Surface((self.rect.width, self.rect.height))
            self.image.fill((255, 0, 0))
            self.wait = -1

            
        
        self.draw_hitbox = True


        
        for unit in self.enc.units:
            if unit.side == self.unit.side:
                continue
            if self.rect.colliderect(unit.rect) and unit not in self.units_hit:
                self.on_hit(unit)
                self.units_hit.add(unit)

        self.duration -= 1

        if self.duration <= 0:
            self.remove = True

    def draw(self, surface):
        if self.draw_hitbox:
            # surface.blit(self.image, self.rect)
            pass


'''
class SingleHitAttackHitbox(Hitbox):
    def __init__(self, x, y, width, height):
        self.damage = 0
        self.wait = 0 
        self.units_hit = set()

        self.frames = 0
        self.frame_duration = 10
        self.attack_frame = 0
        self.wait = self.frame_duration * self.attack_frame

        self.remove = False
        self.draw_hitbox = False
        
        # You can add player-specific hitbox logic her

class PlayerAttack1Action(Action):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # You can add player-specific hitbox logic here

class SkeletonAttackAction(Action):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        # You can add skeleton-specific hitbox logic here

        self.damage = 5

        self.wait = 70
    
'''
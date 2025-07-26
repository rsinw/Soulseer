# unit.py

# Element with its own autonomous logic 

import pygame 
import uuid
from animation import Animation
from action import *


class Unit:
    def __init__(self):

        self.scale = 2
        self.hp = 100
        self.max_hp = 100

        self.rect = pygame.Rect(100, 100, 40*self.scale, 50*self.scale)
    
        self.hitbox_image = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox_image.fill((0, 255, 0))

        self.target_location = None 

        self.speed = 2

        self.haste = 1

        # movement 
        self.dx = 0
        self.dy = 0

        self.knockback_dx = 0

        # states 

        self.voluntary_movement = False
  
        self.action = None 

        # visual stuff

        self.offsetx = -50*self.scale
        self.offsety = -40*self.scale

        self.facing_right = True

        self.anims = []

        self.idle_anim = Animation("resalt/Sprites/Idle.png", 10)
        self.move_anim = Animation("resalt/Sprites/Run.png", 6)

        self.hit_anim = Animation("resalt/Sprites/Get Hit.png", 3)
        self.death_anim = Animation("resalt/Sprites/Death.png", 9)
        self.death_anim.repeat = False

        self.anims = [
            self.idle_anim,
            self.move_anim,
            self.death_anim
        ]

        self.action0 = Action(self)
        self.action1 = Action(self)
        self.action2 = Action(self)
        self.action3 = Action(self)

        self.actions = [
            self.action0,
            self.action1,
            self.action2,
            self.action3,
        ]

        self.current_anim = self.idle_anim
        self.image = self.current_anim.image

        self.target_unit = None

   

        # encounter markers 

        self.side = None 
        self.remove_timer = 0
        self.remove = False
        self.uuid = uuid.uuid4()
        self.type_name = "Knight"


        #Healthbar 

        self.healthbar_color = (0, 255, 0)

        self.healthbar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
        self.healthbar_top = pygame.Surface((self.rect.width, 5))
        self.healthbar_top.fill(self.healthbar_color)

        self.healthbar_bot = pygame.Surface((self.rect.width, 5))
        self.healthbar_bot.fill((255, 0, 0))
    
    def cancel_action(self):
        if self.action:
            self.action.reset()
            self.action.working_cd = 0
            self.action = None 

    def set_action(self, action):
        self.action = action
        self.action.reset()

    def update(self):
        # Remove all attack actions belonging to this unit if staggered
        voluntary_dx = 0  # Track voluntary movement in x

        if self.action:
            if self.action.complete:
                self.action.reset()
                self.action = None 
        
        for action in self.actions:
            if action.working_cd > 0:
                action.working_cd -= 1 
                

        if self.is_dead():
            self.remove_timer += 1 
            if self.remove_timer > 3000:
                self.remove == True 
            
            self.cancel_action()
            self.switch_anim(self.death_anim)
        
        elif self.target_unit or self.target_location:
            if self.target_unit:
                # Simulate the attack hitbox position
                hitbox_width = 50 * self.scale
                hitbox_height = 100 * self.scale
                hitbox_rect = pygame.Rect(0, 0, hitbox_width, hitbox_height)
                if self.facing_right:
                    hitbox_rect.bottomleft = self.rect.bottomright
                else:
                    hitbox_rect.bottomright = self.rect.bottomleft

                # Check if the hitbox would hit the target
                if not hitbox_rect.colliderect(self.target_unit.rect):
                    # Move towards the target if not in range
                    if self.facing_right:
                        self.set_target_location(self.target_unit.rect.bottomright[0] + 25, self.target_unit.rect.bottomright[1])
                    else:
                        self.set_target_location(self.target_unit.rect.bottomleft[0] - 25, self.target_unit.rect.bottomleft[1])
                else:
                    self.attack(self.facing_right)

            if self.target_location:
                current = pygame.Vector2(self.rect.midbottom)
                target = pygame.Vector2(self.target_location)
                direction = target - current
                distance = direction.length()
                if distance <= self.speed:
                    voluntary_dx = target.x - current.x
                    self.dx += voluntary_dx
                    self.dy += target.y - current.y
                    self.target_location = None
                else:
                    direction.normalize_ip()
                    move_vector = direction * self.speed
                    voluntary_dx = move_vector.x
                    print(move_vector)
                    self.dx += move_vector.x
                    self.dy += move_vector.y

            self.cancel_action()
            self.switch_anim(self.move_anim)
  
        
        elif self.action:
            self.action.update()
        

        else:
            self.switch_anim(self.idle_anim)


        # For skeleton, spawn hitbox on the 7th frame of attac

        # Always process knockback and dx/dy
        if self.knockback_dx > 0:
            self.dx += self.knockback_dx
            self.knockback_dx -= 1
        if self.knockback_dx < 0:
            self.dx += self.knockback_dx
            self.knockback_dx += 1
            
        if voluntary_dx > 0:
            self.facing_right = True
        elif voluntary_dx < 0:
            self.facing_right = False

        
        
        self.current_anim.update()
        image = self.current_anim.image
        if not self.facing_right:
            self.image = pygame.transform.scale(pygame.transform.flip(image, True, False), (image.get_width() * self.scale, image.get_height() * self.scale))
        else:
            self.image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))

        self.move()

    def switch_anim(self, new_anim):
        if self.current_anim == new_anim:
            return 
        else:
            self.current_anim = new_anim
    def move(self):

        current = pygame.Vector2(self.rect.midbottom)
        new_pos = current + pygame.Vector2(self.dx, self.dy)
        
        if new_pos.y < self.enc.y_bound or new_pos.y > self.enc.game.screen.get_height():
            self.dy = 0

        new_pos = current + pygame.Vector2(self.dx, self.dy)

        self.rect.midbottom = (new_pos.x, new_pos.y)
        self.dx = 0
        self.dy = 0

 
    def set_target_unit(self, unit):
        self.target_unit = unit


    def set_target_location(self, x, y):
        if y < self.enc.y_bound:
            y = self.enc.y_bound
        self.target_location = (x, y)



    def is_alive(self):
        return self.hp > 0
    
    def is_dead(self):
        return self.hp <= 0 
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        
        self.staggered = True
        # Cancel all actions when hit
        self.attacking = False
        self.target_location = None
        # Remove all attack actions belonging to this unit
        from action import Action
        for element in list(self.enc.elements):
            if isinstance(element, Action) and getattr(element, 'unit', None) is self:
                element.remove = True
        # Optionally reset attack animation if in progress
        if self.current_anim == 2:
            self.anims[self.current_anim].reset()
        print(f"Unit took {damage} damage")
    
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"Unit healed {amount} hp")
    
    
    def control(self):

        x, y = pygame.mouse.get_pos()

        action_keys = [pygame.K_q,
                       pygame.K_w,
                       pygame.K_e,
                       pygame.K_r]

        for event in self.enc.game.events:
            if pygame.mouse.get_pressed()[0]:
                enemy_selected = False 
                for unit in self.enc.return_enemy_group():
                    if unit.rect.collidepoint(x, y):
                        self.target_unit = unit
        
                if not enemy_selected:
                    self.set_target_location(x, y)

                    self.target_unit = None
       

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_q:
                    if self.actions[0].working_cd == 0:
                        self.action = self.actions[0]

                    print("Action 0 pressed")
            
                for index, key in enumerate(action_keys):
                    if event.key == key:
                        if self.actions[index].working_cd == 0:
                            self.actions[index].working_cd = self.actions[index].cd
                            self.action = self.actions[index]
                            

    
    def draw(self, surface):

        # draw hitbox
        # surface.blit(self.hitbox_image, self.rect)

        temp_rect = self.rect.copy()
        temp_rect.x += self.offsetx
        temp_rect.y += self.offsety

        # draw unit
        surface.blit(self.image, temp_rect)

         
        #overlay 
        mask = pygame.mask.from_surface(self.image)

        # Get the outline as a list of points
        outline = mask.outline()

        if not outline:
            return  # No visible pixels

        # Adjust position to where the image is drawn on screen
        temp_rect = self.rect.copy()
        temp_rect.x += self.offsetx
        temp_rect.y += self.offsety

        # Offset the outline points to screen position
        offset_outline = [(x + temp_rect.x, y + temp_rect.y) for x, y in outline]

        # Draw the green outline
        pygame.draw.lines(surface, (0, 255, 0), True, offset_outline, 1)

        # Only draw healthbar if not dead
        if self.is_dead():
            return

        self.healthbar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
        self.healthbar_rect.midbottom = self.rect.midtop

        ratio = self.hp / self.max_hp

        self.healthbar_top = pygame.Surface((int(self.healthbar_rect.width*ratio), self.healthbar_rect.height))
        self.healthbar_top.fill(self.healthbar_color)

        self.healthbar_bot = pygame.Surface((self.healthbar_rect.width, self.healthbar_rect.height))
        self.healthbar_bot.fill((255, 0, 0))

        surface.blit(self.healthbar_bot, self.healthbar_rect)
        surface.blit(self.healthbar_top, self.healthbar_rect)


class Skeleton(Unit):
    def __init__(self):
        super().__init__()
        self.hp = 50
        self.max_hp = 50

        self.speed = 1
        # Override animations with Skeleton-specific ones
        self.idle_anim = Animation("resalt/monster_sprites/Skeleton/Idle.png", 4, frame_size=150)
        self.move_anim = Animation("resalt/monster_sprites/Skeleton/Walk.png", 4, frame_size=150)  # 'run' for Unit is 'walk' for Skeleton
        self.attack_anim = Animation("resalt/monster_sprites/Skeleton/Attack.png", 8, frame_size=150)
        self.attack_anim.repeat = False
        self.hit_anim = Animation("resalt/monster_sprites/Skeleton/Take Hit.png", 4, frame_size=150)
        self.death_anim = Animation("resalt/monster_sprites/Skeleton/Death.png", 4, frame_size=150)
        self.death_anim.repeat = False

        self.anims = [
            self.idle_anim,
            self.move_anim,
            self.attack_anim,
            self.death_anim
        ]
        # Enemy AI: Skeleton uses the same AI logic as Unit (targeting, attacking, etc.)


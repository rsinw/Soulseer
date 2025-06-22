# unit.py

import pygame 
from animation import Animation
from action import Hitbox


class Unit:
    def __init__(self):

        self.scale = 2
        self.hp = 100
        self.max_hp = 100

        self.rect = pygame.Rect(100, 100, 40*self.scale, 50*self.scale)

    
        self.hitbox_image = pygame.Surface((self.rect.width, self.rect.height))
        self.hitbox_image.fill((0, 255, 0))

        self.target_location = None 
        self.is_moving = False  

        self.speed = 2

        self.attack_setcd = 60
        self.attack_cd = 0

        self.healthbar_color = (0, 255, 0)

        self.healthbar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
        self.healthbar_top = pygame.Surface((self.rect.width, 5))
        self.healthbar_top.fill(self.healthbar_color)

        self.healthbar_bot = pygame.Surface((self.rect.width, 5))
        self.healthbar_bot.fill((255, 0, 0))
        


        # movement 
        self.dx = 0
        self.dy = 0

        self.knockback_dx = 0


        # visual stuff

        self.offsetx = -50*self.scale
        self.offsety = -40*self.scale

        self.facing_right = True

        self.anims = []

        self.idle_anim = Animation("resalt/Sprites/Idle.png", 10)
        self.run_anim = Animation("resalt/Sprites/Run.png", 6)
        self.attack_anim = Animation("resalt/Sprites/Attack1.png", 4)
        self.attack_anim.repeat = False

        self.hit_anim = Animation("resalt/Sprites/Get Hit.png", 3)
        self.death_anim = Animation("resalt/Sprites/Death.png", 9)
        self.death_anim.repeat = False

        self.anims.append(self.idle_anim)
        self.anims.append(self.run_anim)
        self.anims.append(self.attack_anim)
        self.anims.append(self.hit_anim)
        self.anims.append(self.death_anim)

        

        self.current_anim = 0
        self.image = self.anims[self.current_anim].image

        self.attacking = False
        self.staggered = False


        self.target_unit = None

    def update(self):


        # animations 

        self.determine_image()

        image = self.anims[self.current_anim].image
        if not self.facing_right:
            
            self.image = pygame.transform.scale(pygame.transform.flip(image, True, False), (image.get_width() * self.scale, image.get_height() * self.scale))

        else:
            self.image = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale))


        self.anims[self.current_anim].update()


        if self.is_dead():
            return
        
        if self.attack_cd > 0:
            self.attack_cd -= 1

        if self.target_unit and self.knockback_dx == 0:
            
            right_side = True
            test_rect = pygame.Rect(self.rect.x, self.rect.y, 50, 100)
            if self.rect.x > self.target_unit.rect.x:
                right_side = True
            else:
                right_side = False

            if right_side:
                test_rect.midright = self.rect.midleft
            else:
                test_rect.midleft = self.rect.midright
            
            if not test_rect.colliderect(self.target_unit.rect):
                if right_side:
                    self.set_target_location(self.target_unit.rect.bottomright[0] + 25, self.target_unit.rect.bottomright[1])

                else:
                    self.set_target_location(self.target_unit.rect.bottomleft[0] - 25, self.target_unit.rect.bottomleft[1])
                
            else:
                self.attack(not right_side)
                
 
        if self.is_moving and self.target_location:
            current = pygame.Vector2(self.rect.midbottom)
            target = pygame.Vector2(self.target_location)
            direction = target - current
            distance = direction.length()
            if distance <= self.speed:
                self.dx += target.x - current.x
                self.dy += target.y - current.y
                self.is_moving = False
                self.target_location = None
                print("Arrived at target location")
            else:
                direction.normalize_ip()
                move_vector = direction * self.speed
                print(move_vector)
                self.dx += move_vector.x
                self.dy += move_vector.y
        
        if self.knockback_dx > 0:
            self.dx += self.knockback_dx
            self.knockback_dx -= 1
        if self.knockback_dx < 0:
            self.dx += self.knockback_dx
            self.knockback_dx += 1
        
        self.move()

    def move(self):

        current = pygame.Vector2(self.rect.midbottom)
        new_pos = current + pygame.Vector2(self.dx, self.dy)
        
        if new_pos.x < 0 or new_pos.x > self.enc.x_bound:
            self.dx = 0
        if new_pos.y < self.enc.y_bound or new_pos.y > self.enc.game.screen.get_height():
            self.dy = 0

        new_pos = current + pygame.Vector2(self.dx, self.dy)

        self.rect.midbottom = (new_pos.x, new_pos.y)
        self.dx = 0
        self.dy = 0

    
    def determine_image(self):
        if self.is_dead():
            self.current_anim = 4
            image = self.anims[self.current_anim].image
    
            return

        if self.current_anim == 2 and self.anims[self.current_anim].complete():
            self.attacking = False
            self.anims[self.current_anim].reset()

        if self.attacking:
            self.current_anim = 2
            return
        

        if self.current_anim == 3 and self.anims[self.current_anim].complete():
            self.staggered = False
            self.anims[self.current_anim].reset()

        if self.staggered:
            self.current_anim = 3
            return


        self.current_anim = 0

        if self.is_moving:
            self.current_anim = 1

    def set_target_unit(self, unit):
        self.target_unit = unit
        if self.target_unit:
            if self.rect.x < self.target_unit.rect.x:
                self.facing_right = True
            else:
                self.facing_right = False


    def set_target_location(self, x, y):

        if y < self.enc.y_bound:
            y = self.enc.y_bound

        self.target_location = (x, y)
        self.is_moving = True
        print("Setting target location: ", self.target_location)

        if self.target_location:
            if self.rect.x < self.target_location[0]:
                self.facing_right = True
            else:
                self.facing_right = False


    def is_dead(self):
        return self.hp <= 0
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        
        self.staggered = True
        print(f"Unit took {damage} damage")

    def attack(self, right_side=True):
        if self.attack_cd > 0:
            return
        hitbox = Hitbox(self.rect.x, self.rect.y, 50*self.scale, 100*self.scale)

        hitbox.unit = self
        self.enc.add_element(hitbox)

        self.attack_cd = self.attack_setcd
        self.attacking = True
    
    def control(self):

        x, y = pygame.mouse.get_pos()

        for event in self.enc.game.events:
            if pygame.mouse.get_pressed()[0]:
                for unit in self.enc.units[1]:
                    if unit.rect.collidepoint(x, y):
                        self.target_unit = unit
                        print("targeting unit")
        
                    else:
                        self.set_target_location(x, y)
                        self.target_unit = None
                        print("mouse clicked")

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_a:
                    if x < self.rect.x:
                        self.attack(0)
                    else:
                        self.attack(1)

                    print("attacking")
    
    def draw(self, surface):

        # draw hitbox
        # surface.blit(self.hitbox_image, self.rect)

        temp_rect = self.rect.copy()
        temp_rect.x += self.offsetx
        temp_rect.y += self.offsety



        # draw unit
        surface.blit(self.image, temp_rect)

        self.healthbar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
        self.healthbar_rect.midbottom = self.rect.midtop

        ratio = self.hp / self.max_hp

        self.healthbar_top = pygame.Surface((int(self.healthbar_rect.width*ratio), self.healthbar_rect.height))
        self.healthbar_top.fill(self.healthbar_color)

        self.healthbar_bot = pygame.Surface((self.healthbar_rect.width, self.healthbar_rect.height))
        self.healthbar_bot.fill((255, 0, 0))

        surface.blit(self.healthbar_bot, self.healthbar_rect)
        surface.blit(self.healthbar_top, self.healthbar_rect)


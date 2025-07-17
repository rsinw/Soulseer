# unit.py

import pygame 
from animation import Animation
from action import Hitbox
from action import PlayerAttack1Hitbox, SkeletonAttackHitbox


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

        # Always process knockback and dx/dy
        if self.knockback_dx > 0:
            self.dx += self.knockback_dx
            self.knockback_dx -= 1
        if self.knockback_dx < 0:
            self.dx += self.knockback_dx
            self.knockback_dx += 1

        # Block voluntary actions while staggered (stunned)
        if self.staggered:
            self.move()
            return

        # For skeleton, spawn hitbox on the 7th frame of attack
        if isinstance(self, Skeleton) and getattr(self, 'skeleton_hitbox_pending', False):
            if self.current_anim == 2 and self.attack_anim.current_frame == 6 and not getattr(self, 'skeleton_hitbox_spawned', False):
                hitbox = SkeletonAttackHitbox(self.rect.x, self.rect.y, 50*self.scale, 100*self.scale)
                hitbox.unit = self
                self.enc.add_element(hitbox)
                self.skeleton_hitbox_spawned = True
            # Reset flags when attack animation is done or changes
            if self.current_anim != 2 or self.attack_anim.complete():
                self.skeleton_hitbox_pending = False
                self.skeleton_hitbox_spawned = False

        if self.attack_cd > 0:
            self.attack_cd -= 1

        # Remove: Always face the target if there is one
        # Facing will be set based on voluntary movement below

        if self.target_unit and self.knockback_dx == 0:
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

        voluntary_dx = 0  # Track voluntary movement in x

        if self.is_moving and self.target_location:
            current = pygame.Vector2(self.rect.midbottom)
            target = pygame.Vector2(self.target_location)
            direction = target - current
            distance = direction.length()
            if distance <= self.speed:
                voluntary_dx = target.x - current.x
                self.dx += voluntary_dx
                self.dy += target.y - current.y
                self.is_moving = False
                self.target_location = None
                print("Arrived at target location")
            else:
                direction.normalize_ip()
                move_vector = direction * self.speed
                voluntary_dx = move_vector.x
                print(move_vector)
                self.dx += move_vector.x
                self.dy += move_vector.y
        
        # Determine facing based on voluntary_dx (voluntary movement in x)
        if voluntary_dx > 0:
            self.facing_right = True
        elif voluntary_dx < 0:
            self.facing_right = False

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
        # Remove facing logic here; facing is now set by movement


    def is_dead(self):
        return self.hp <= 0
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        
        self.staggered = True
        # Cancel all actions when hit
        self.attacking = False
        self.is_moving = False
        self.target_location = None
        # Optionally reset attack animation if in progress
        if self.current_anim == 2:
            self.anims[self.current_anim].reset()
        print(f"Unit took {damage} damage")

    def attack(self, right_side=True):
        if self.attack_cd > 0:
            return
        # Use different hitbox classes for player and skeleton
        if isinstance(self, Skeleton):
            # For skeleton, set a flag to spawn hitbox on the 7th frame
            self.skeleton_hitbox_pending = True
            self.skeleton_hitbox_spawned = False
        else:
            hitbox = PlayerAttack1Hitbox(self.rect.x, self.rect.y, 50*self.scale, 100*self.scale)
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


class Skeleton(Unit):
    def __init__(self):
        super().__init__()
        # Override animations with Skeleton-specific ones
        self.idle_anim = Animation("resalt/monster_sprites/Skeleton/Idle.png", 4, frame_size=150)
        self.run_anim = Animation("resalt/monster_sprites/Skeleton/Walk.png", 4, frame_size=150)  # 'run' for Unit is 'walk' for Skeleton
        self.attack_anim = Animation("resalt/monster_sprites/Skeleton/Attack.png", 8, frame_size=150)
        self.attack_anim.repeat = False
        self.hit_anim = Animation("resalt/monster_sprites/Skeleton/Take Hit.png", 4, frame_size=150)
        self.death_anim = Animation("resalt/monster_sprites/Skeleton/Death.png", 4, frame_size=150)
        self.death_anim.repeat = False

        self.anims = [
            self.idle_anim,
            self.run_anim,
            self.attack_anim,
            self.hit_anim,
            self.death_anim
        ]
        self.current_anim = 0
        self.image = self.anims[self.current_anim].image
        # Enemy AI: Skeleton uses the same AI logic as Unit (targeting, attacking, etc.)


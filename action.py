import pygame 

class Action:
    def __init__(self, x, y, width, height):
        self.rect = None

        self.image = None

        self.units_hit = set()

        self.damage = 10

        self.duration = 10
        self.remove = False
        
        self.wait = 20

        self.draw_hitbox = False

        self.unit = None
        self.width = width
        self.height = height
    

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
        
        for group in self.enc.units:
            for element in group:
                if element.side == self.unit.side:
                    continue
                if self.rect.colliderect(element.rect) and element not in self.units_hit:
                    self.on_hit(element)
                    self.units_hit.add(element)

        self.duration -= 1

        if self.duration <= 0:
            self.remove = True

    def draw(self, surface):
        if self.draw_hitbox:
            # surface.blit(self.image, self.rect)
            pass

class SingleHitAttackAction(Action):
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
    

# encounter.py

import pygame
from window import Window, Button
from animation import Animation
from unit import Unit
from unit import Skeleton

import random


class Encounter(Window):
    def __init__(self):
        super().__init__()


        self.y_bound = 400
        self.x_bound = 1200

        self.timer = 0

        self.units = [[], [], []]
        self.selected_unit = None

        self.add_unit(Unit(), 0)  # Add player unit back
  

        self.selected_unit = self.elements[0]

        self.selected_unit.speed = 3
        # self.selected_unit.hp = 1000
        # self.selected_unit.max_hp = 1000

        for i in range(3):
            self.add_unit(Skeleton(), 1)  # Keep Skeleton as the enemy

        self.bg_image = pygame.transform.scale(pygame.image.load("resalt/mansion2.png"), (1200, 800))

        self.selected_unit.rect.midbottom = (100, 600)

        self.over = False
        self.over_timer = 300
        self.side_win = None
        self.over_text = None

        self.enemy_respawn_timer = 0
        self.dead_unit_timers = {}  # unit: frames_dead


    def add_element(self, element):
        self.elements.append(element)
        element.enc = self
        element.remove = False

    def add_unit(self, unit, side=0):
        self.add_element(unit)
        self.units[side].append(unit)
        unit.side = side

        screen_height = self.game.screen.get_height() if hasattr(self, 'game') and hasattr(self.game, 'screen') else 800
        min_y = self.y_bound
        max_y = screen_height
        spawn_y = random.randint(min_y, max_y)

        if side == 0:
            # Spawn player in the middle of the screen
            unit.rect.midbottom = (self.x_bound // 2, max_y)
        else:
            # Randomly choose left or right offscreen
            spawn_side = random.choice(['left', 'right'])
            if spawn_side == 'left':
                spawn_x = -unit.rect.width // 2
            else:
                spawn_x = self.x_bound + unit.rect.width // 2
            unit.rect.midbottom = (spawn_x, spawn_y)
            # Set enemy healthbar color
            unit.healthbar_color = (255, 255, 0)
            # Set enemy target to a random living player unit
            living_players = [u for u in self.units[0] if not u.is_dead()]
            if living_players:
                unit.set_target_unit(random.choice(living_players))

    def update(self):
        
        super().update()

        if self.over and self.over_timer > 0:
            self.over_timer -= 1
            if self.over_timer <= 0:
                self.game.main_menu()
        if self.over:
            return

        temp_elements = []

        if self.selected_unit:
            self.selected_unit.control()

        # Remove dead units after 3 seconds (180 frames)
        for element in self.elements:
            if hasattr(element, 'is_dead') and element.is_dead():
                if element not in self.dead_unit_timers:
                    self.dead_unit_timers[element] = 1
                else:
                    self.dead_unit_timers[element] += 1
                if self.dead_unit_timers[element] > 180:
                    element.remove = True
            else:
                if element in self.dead_unit_timers:
                    del self.dead_unit_timers[element]

        for element in self.elements:
            if element.remove == False:
                temp_elements.append(element)

        self.elements = temp_elements

        side0_alive = False
        side1_alive = False

        for unit in self.units[0]:
            if unit.is_dead() == False:
                side0_alive = True
        for unit in self.units[1]:
            if unit.is_dead() == False:
                side1_alive = True

        # Remove dead units from self.units lists as well
        for side in [0, 1]:
            self.units[side] = [u for u in self.units[side] if not (hasattr(u, 'is_dead') and u.is_dead() and self.dead_unit_timers.get(u, 0) > 180)]

        # Enemy respawn logic
        living_enemies = [u for u in self.units[1] if not u.is_dead()]
        if len(living_enemies) < 3:
            self.enemy_respawn_timer += 1
            if self.enemy_respawn_timer > 3 * 60:  # 10 seconds at 60fps
                from unit import Skeleton
                self.add_unit(Skeleton(), 1)
                self.enemy_respawn_timer = 0
        else:
            self.enemy_respawn_timer = 0
        
        
        if side1_alive == False:
            self.over = True

            my_font = pygame.font.SysFont('Comic Sans MS', 60)
            self.over_text = my_font.render('Player Wins', False, (255, 255, 255))

        elif side0_alive == False:
            self.over = True

            my_font = pygame.font.SysFont('Comic Sans MS', 60)
            self.over_text= my_font.render('Enemies Win', False, (255, 255, 255))
      
      
               


    def draw(self):
        
        self.game.screen.blit(self.bg_image, (0,0))
        super().draw()

        if self.over:
            self.game.screen.blit(self.over_text, (400,200))
       
            
        
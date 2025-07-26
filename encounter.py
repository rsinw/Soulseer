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

        self.elements = []

        self.timer = 0

        self.units = []


        self.selected_unit = None

        self.over = False
        self.over_timer = 300
        self.side_win = None
        self.over_text = None

        self.enemy_respawn_timer = 0
        

        # Changeable test initialization +++++++++++++++++++++++++++++++

        self.bg_image = pygame.transform.scale(pygame.image.load("resalt/mansion2.png"), (1200, 800))

        self.add_unit(Unit(), 0)  # Add player unit

        print(self.return_player_group())
  
        self.selected_unit = self.return_player_group()[0]

        self.selected_unit.speed = 3
        # self.selected_unit.hp = 1000
        # self.selected_unit.max_hp = 1000

        '''

        for i in range(3):
            self.add_unit(Skeleton(), 1)  # Keep Skeleton as the enemy

        '''


    def add_element(self, element):
        self.elements.append(element)
        element.enc = self
        element.remove = False

    def add_unit(self, unit, side=0):
        
        unit.side = side
        self.add_element(unit)
        self.units.append(unit)

        # REFACTORING RIGHT NOW
        if unit.side == 1:
            phys_side = random.randint(0,1)
            if phys_side == 1:
                unit.rect.midbottom = (random.randint(self.x_bound, self.x_bound + 200), random.randint(self.y_bound, 2 * self.y_bound))
            else:
                unit.rect.midbottom = (random.randint(-200, 0), random.randint(self.y_bound, 2 * self.y_bound))
        else:
            unit.rect.midbottom = (self.y_bound // 2, self.x_bound // 2)

    def update(self):
        
        super().update()

        self.remove_marked_elements()

        if self.over and self.over_timer > 0:
            self.over_timer -= 1
            if self.over_timer <= 0:
                self.game.main_menu()
        if self.over:
            return

        if self.selected_unit:
            self.selected_unit.control()


        # Enemy respawn logic

        '''
        if self.is_side_alive(self.return_player_group()) == False:
            self.over = True

            my_font = pygame.font.SysFont('Comic Sans MS', 60)
            self.over_text = my_font.render('Player Wins', False, (255, 255, 255))

        elif self.is_side_alive(self.return_enemy_group()) == False:
            self.over = True

            my_font = pygame.font.SysFont('Comic Sans MS', 60)
            self.over_text= my_font.render('Enemies Win', False, (255, 255, 255))
        '''
      
      
               

# helper 
    def get_elements_by_y_order(self):
        # Returns elements sorted from highest to lowest midbottom.y
        return sorted(self.elements, key=lambda e: getattr(e, 'rect', None) and getattr(e.rect, 'midbottom', (0,0))[1] or 0)
    
    def remove_marked_elements(self):
        temp_list = []
        for element in self.elements:
            if not element.remove:
                temp_list.append(element)
        
        self.elements = temp_list 

    def return_player_group(self):
        temp_list = [] 
        for unit in self.units:
            if unit.side == 0:
                temp_list.append(unit)
        
        return temp_list 

    def return_enemy_group(self):
        temp_list = [] 
        for unit in self.units:
            if unit.side == 1:
                temp_list.append(unit)

        return temp_list
    
    def return_group(self, side):
        if side == 0:
            return self.return_player_group()
        elif side == 1:
            return self.return_enemy_group()
        return self.return_enemy_group()
    
    def is_side_alive(self, group):
        for unit in group:
            if unit.is_alive():
                return True 
        return False

    def draw(self):
        
        self.game.screen.blit(self.bg_image, (0,0))
        # Draw elements in y-order
        for element in self.get_elements_by_y_order():
            element.draw(self.game.screen)
        if self.over:
            self.game.screen.blit(self.over_text, (400,200))
       
            
        
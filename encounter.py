# encounter.py

import pygame
from window import Window, Button
from animation import Animation
from unit import Unit 


class Encounter(Window):
    def __init__(self):
        super().__init__()


        self.y_bound = 400
        self.x_bound = 1200

        self.units = [[], [], []]
        self.selected_unit = None

        self.add_unit(Unit(), 0)
        self.add_unit(Unit(), 1)

        self.elements[1].set_target_unit(self.elements[0])

        self.selected_unit = self.elements[0]

        self.selected_unit.speed = 3
        # self.selected_unit.hp = 1000
        # self.selected_unit.max_hp = 1000

        self.bg_image = pygame.transform.scale(pygame.image.load("resalt/mansion2.png"), (1200, 800))

        self.selected_unit.rect.midbottom = (100, 600)

        self.over = False
        self.over_timer = 300
        self.side_win = None
        self.over_text = None

        self.units[1][0].healthbar_color = (255, 255, 0)


    def add_element(self, element):
        self.elements.append(element)
        element.enc = self
        element.remove = False

    def add_unit(self, unit, side=0):
        self.add_element(unit)
        self.units[side].append(unit)
        unit.side = side

        if side == 0:
            unit.rect.midbottom = (100, 600)
        else:
            unit.rect.midbottom = (self.x_bound - 100, 600)

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
       
            
        
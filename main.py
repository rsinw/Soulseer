# main_menu.py

import pygame 
from main_menu import MainMenu
from encounter import Encounter


class Game:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60   
        self.background_color = (0, 0, 0)

        self.windows = []

        self.events = pygame.event.get()

    def add_window(self, window):
        self.windows.append(window)
        window.game = self 


    # windows

    def start_encounter(self):
        self.windows = []
        self.add_window(Encounter())
    
    def main_menu(self):
        self.windows = []
        self.add_window(MainMenu())

    # update -> draw
    def update(self):
        for window in self.windows:
            window.update()
        
    def draw(self):
        self.screen.fill(self.background_color)
        self.screen.blit
        for window in self.windows:
            window.draw()
        
pygame.init()

game = Game()

game.main_menu()

run = True

while run:
    game.clock.tick(game.fps)

    game.events = pygame.event.get()
    
    for event in game.events:
        if event.type == pygame.QUIT:
            run = False

    game.update()
    game.draw()

    pygame.display.update()


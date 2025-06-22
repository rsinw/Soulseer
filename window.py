# window.py 
import pygame


class Window:
    def __init__(self):
        self.elements = []
        pass

    def update(self):
        for element in self.elements:
            element.update()
        
    def draw(self):
        for element in self.elements:
            element.draw(self.game.screen)


class Button:
    def __init__(self, text, x, y, width, height):

        self.text = text

        self.rect = pygame.Rect(x, y, width, height)

        self.bg_color = (0, 0, 0)
        self.text_color = (255, 255, 255)

        self.font = pygame.font.Font(None, 32)
        self.text_render = self.font.render(text, True, self.text_color)

        self.hovered = False
        self.clicked = False
        pass


    def update(self):
        self.hovered = False
        self.clicked = False

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
        

        if self.hovered:
            self.bg_color = (255, 255, 255)
            self.text_color = (0, 0, 0)
        else:
            self.bg_color = (0, 0, 0)
            self.text_color = (255, 255, 255)
        
        if self.clicked:
            print("Button clicked")        

    def draw(self, surface):
        img = pygame.Surface((self.rect.width, self.rect.height))
        img.fill(self.bg_color)
        self.text_render = self.font.render(self.text, True, self.text_color)
        surface.blit(img, self.rect)
        surface.blit(self.text_render, (self.rect.x + self.rect.width // 2 - self.text_render.get_width() // 2, self.rect.y + self.rect.height // 2 - self.text_render.get_height() // 2))


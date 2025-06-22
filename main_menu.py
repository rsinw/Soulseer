# main_menu.py

from window import Window, Button



class MainMenu(Window):
    def __init__(self):
        super().__init__()

        self.button = Button("Start", 100, 100, 200, 50)
        self.button.rect.center = (600, 400)
        self.elements.append(self.button)

    def update(self):
        super().update()

        if self.button.clicked:
            self.game.start_encounter()

    def draw(self):
        super().draw()
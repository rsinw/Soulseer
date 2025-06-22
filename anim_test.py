import pygame

rect = pygame.Rect(100, 100, 100, 100)

class Animation:
    def __init__(self, spritesheet, num_frames):
        self.frames = []
        self.num_frames = num_frames
        self.current_frame = 0
        self.frame_duration = 10
        self.frame_timer = 0

        self.repeat = True

        spritesheet = pygame.image.load(spritesheet)

        for i in range(num_frames):
            frame = pygame.Surface.subsurface(spritesheet, ((i*135, 0), (135, 135)))
            self.frames.append(frame)

        self.image = self.frames[self.current_frame]
        pass

    def update(self):
        self.frame_timer += 1

        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= self.num_frames:
                if self.repeat:
                    self.current_frame = 0
                else:
                    self.current_frame = self.num_frames - 1


        self.image = self.frames[self.current_frame]
    
    def reset(self):
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[self.current_frame]



pygame.init()


clock = pygame.time.Clock()

run = True

screen = pygame.display.set_mode((800, 600))

rect = pygame.Rect(100, 100, 100, 100)

run_anim = Animation("res/Sprites/Run.png", 8)
attack_anim = Animation("res/Sprites/Attack.png", 6)
dash_anim = Animation("res/Sprites/Dash.png", 4)
death_anim = Animation("res/Sprites/Death.png", 9)

hit_anim = Animation("res/Sprites/Take Hit.png", 4)
a3 = Animation("resalt/Sprites/Attack3.png", 5)
a2 = Animation("resalt/Sprites/Attack2.png", 4)

death_anim.repeat = False

while True:
    clock.tick(60)

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    screen.blit(a3.image, rect)

    run_anim.update()
    attack_anim.update()
    dash_anim.update()
    hit_anim.update()
    death_anim.update()

    a3.update()
    a2.update()
    
    pygame.display.update()



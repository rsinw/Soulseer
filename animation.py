import pygame 

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
    
    def complete(self):
        return self.current_frame == self.num_frames - 1
    
    def reset(self):
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.frames[self.current_frame]

import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.6, -self.rect.height * 0.8))

class Water(Generic):
    def __init__(self, pos, frames, groups, z):
        #animation setup
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos = pos, 
                         surface = self.frames[self.frame_index],
                         groups = groups,
                         z = LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
            self.animate(dt)

class Wildflower(Generic):
    def __init__(self, pos, surface, groups):
        super().__init__(pos, surface, groups)
        self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Tree(Generic):
    def __init__(self, pos, surface, groups, name):
        super().__init__(pos, surface, groups)

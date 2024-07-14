import pygame
from settings import *
from random import randint, choice
from timer import Timer

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

        #tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surface = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        #apples
        self.apple_surface = pygame.image.load('../graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        self.health -= 1

        if len(self.apple_sprites.sprites()):
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surface
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate((-10,-self.rect.height * 0.95))
            self.hitbox.bottom -= 25
            self.alive = False

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(pos = (x, y), 
                        surface = self.apple_surface, 
                        groups = [self.apple_sprites, self.groups()[0]],
                        z = LAYERS['fruit']) #self.groups()[0] points to all_sprites group
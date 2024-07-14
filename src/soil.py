import pygame
from settings import *
from pytmx.util_pygame import load_pygame

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']

class SoilLayer:
    def __init__(self, all_sprites):
        #sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        #graphics
        self.soil_surface = pygame.image.load('../graphics/soil/o.png')

        self.create_soil_grid()
        self.create_hit_rects()

        #requirements
        #if the area is farmable
        #if the soil has been watered
        #if the soil has a plant

    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        '''
        One long list representing the entire map;
        Inside that list, one list for each row;
        And finally one list for each tile inside the 'row_lists'

        The for loop adds a F for each Farmable tile imported from map.tmx
        '''
        self.grid = [[[] for col in range (h_tiles)] for row in range (v_tiles)]
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)
    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(pos = (index_col*TILE_SIZE, index_row*TILE_SIZE), 
                             surface = self.soil_surface, 
                             groups = [self.all_sprites, self.soil_sprites])
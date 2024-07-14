import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        #imports
        overlay_path = '../graphics/overlay/'
        self.tools_surfaces = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surfaces = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):
        tool_surfaces = self.tools_surfaces[self.player.selected_tool]
        tool_rect = tool_surfaces.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surfaces, tool_rect)

        seed_surfaces = self.seeds_surfaces[self.player.selected_seed]
        seed_rect = seed_surfaces.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surfaces, seed_rect)
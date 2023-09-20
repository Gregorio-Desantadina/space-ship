import pygame
from config import *

class Ship(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()
        self.image = pygame.image.load(skin)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
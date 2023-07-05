import pygame
# from player import quitEvent

blobImg = pygame.transform.scale(pygame.image.load("sources/ennemies/blob.png"), (100, 100))

class Ennemy:
    def __init__(self, surface):
        self.img = blobImg
        self.rect = self.img.get_rect()

        self.surface: pygame.Surface = surface

        # place the ennemy
        self.rect.y = 40
        self.rect.x = 50

    def update(self):
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.img, self.rect)
import pygame
import enemy

# 250 x 50
originalImage = pygame.image.load("boss_spirtesheet.png")
originalImage = pygame.transform.scale_by(originalImage, 2)

class Boss(enemy.Enemy):
    def __init__(self, x, y):
        # This is the Enemy constructor since we inherited it
        super(). __init__(x, y)
        self.image = pygame.Surface((originalImage.get_height(), originalImage.get_height()), pygame.SRCALPHA)
        self.image.blit(originalImage, (0,0))
        self.rect = pygame.Rect((x,y), self.image.get_size())

        self.strength = 2
        self.maxHealth = 20
        self.health = self.maxHealth

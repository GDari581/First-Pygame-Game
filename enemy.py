import pygame
import random

enemyScale = 2

try:
    originalImage = pygame.image.load("enemy_spritesheet.png")
except:
    originalImage = pygame.Surface((16,16))
    originalImage.fill("red")

originalImage = pygame.transform.scale_by(originalImage, enemyScale)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface( (enemyScale*16, enemyScale*16), pygame.SRCALPHA )
        self.image.blit(originalImage, (0, 0), pygame.Rect(0, 0, enemyScale*16, enemyScale*16))

        self.rect = pygame.Rect( (x, y), self.image.get_size() ) # This represents the location and hitbox

        self.maxHealth = 4
        self.health = self.maxHealth
        self.speed = random.random()*2 + 1.5 # 0.5 <= self.speed < 3.5
        self.strength = 1
    
    def getDamage(self):
        return self.strength
    
    def damage(self, damageAmount):
        self.health -= damageAmount
        if self.health <= 0:
            self.kill()

    def update(self, player):
        # enemy update needs player, since it's targeting player
        enemyToPlayer = pygame.math.Vector2( player.rect.center ) - self.rect.center
        if enemyToPlayer.magnitude() > 0:
            enemyToPlayer.scale_to_length(self.speed)

        self.rect.x += enemyToPlayer.x
        self.rect.y += enemyToPlayer.y

        # if(self.rect.colliderect( player.rect )):
        #     self.kill()
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        healthBarRect = pygame.Rect(0, 0, self.rect.width, self.rect.width//6)
        healthBarRect.midbottom = self.rect.midtop
        pygame.draw.rect(screen, "gray", healthBarRect, 0, 3)
        healthBarRect.width = (self.health/self.maxHealth)*self.rect.width
        pygame.draw.rect(screen, "red", healthBarRect, 0, 3)
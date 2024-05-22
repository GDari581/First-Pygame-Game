import pygame


try:
    originalImage = pygame.image.load("weapon_sprite.png")
except:
    originalImage = pygame.Surface((20, 20))
    originalImage.fill("cyan)")

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y , velx, vely, damage = 1, durability = 1):
        super().__init__()

        # Swoard is 6 X 17

        # Make 20X20 surface
        self.image = pygame.Surface ( (20, 20), pygame.SRCALPHA) 
        self.rect = pygame.Rect( (x, y), self.image.get_size() )

        self.velocity = pygame.math.Vector2( (velx, vely) )
        assetRotation =  -pygame.math.Vector2((0,-1)).angle_to(self.velocity)
        caanvasRect = pygame.Rect((0,0), self.rect.size)
        projectileAssetSurface = pygame.transform.rotate( pygame.image.load("weapon_sprite.png"), assetRotation)
        projectileAssetRect = projectileAssetSurface.get_rect(center = caanvasRect.center)

        self.image.blit(projectileAssetSurface, projectileAssetRect)

        # self.image.fill("cyan")

        self.durability = durability
        self.exemptEnemies = pygame.sprite.Group()
        self.damage = damage
        self.despwanTimer = 2.5

    def getDamage(self):
        self.durability -= 1
        if self.durability <= 0:
            self.kill()
        return self.damage

    def update(self):
        self.despwanTimer -= 1/60
        if (self.despwanTimer < 0):
            self.kill()
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
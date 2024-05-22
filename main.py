# Example file showing a basic pygame "game loop"
import pygame
import random

#     file         class
from player import Player
from enemy import Enemy
from boss import Boss
from projectile import Projectile
from settings import *

username = input("What's your name?: ")

# pygame setup
pygame.init()
pygame.font.init()

button_font = pygame.font.SysFont(None, 102)
ui_font = pygame.font.Font("freesansbold.ttf", 32)
stat_font = pygame.font.SysFont(None, 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# "start", "play", "loss"
currentScene = "start"

waveNumber = 0

def waveToEnemyCount(waveNumber):
    return round (1/13 * waveNumber**2 + 5)

p1 = Player(200, 100, pygame.Color("#15247F"))
# This spawns 5 enemies for our level
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Start
startButton = pygame.Rect(0,0,400,175)
startButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 200)
startText = button_font.render("Start", True, "black")
startTextRect = startText.get_rect(center = startButton.center)

# Retry
retryButton = pygame.Rect(0,0,400,175)
retryButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 200)
retryText = button_font.render("Retry", True, "black")
retryTextRect = retryText.get_rect(center = retryButton.center)


# Exit
exitButton = pygame.Rect(0,0,400,175)
exitButton.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200)
exitText = button_font.render("Exit", True, "black")
exitTextRect = exitText.get_rect(center = exitButton.center)

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# topleft corners of tiles (0, 160), (32, 160), (64, 160), (96, 160), (128, 160)
# tiles are 32x32
floorTileSet = pygame.image.load("TilesetFloor.png")
floorTileSet = pygame.transform.scale_by(floorTileSet, 2)
for r in range(0, SCREEN_HEIGHT, 32):
    for c in range(0, SCREEN_WIDTH, 32):
        background.blit(floorTileSet, (c, r), pygame.Rect(random.randint(0,4)*32 + 352, 384, 32, 32))
        # background.blit(floorTileSet, (c, r), pygame.Rect(352, 384, 32, 32))

def spawmEnemies(numberOfEnemies):
    while len(enemies) < numberOfEnemies:
        randX = random.randint(-1000, SCREEN_WIDTH+ 1000)
        randY = random.randint(-1000, SCREEN_HEIGHT + 1000)

        # calculate the distance between random point and player
        distanceToPlayer = (pygame.math.Vector2(p1.rect.center) - (randX, randY)).magnitude()

        # If enemy spawn is too close, don''t spawn there
        if distanceToPlayer < SAFE_ENEMY_RADIUS:
            continue

        if 0 < randX < SCREEN_WIDTH and 0 < randY < SCREEN_HEIGHT:
            continue

        bossChance = random.randint(0, 100)
        if bossChance < waveNumber:
            enemies.add(Boss(randX,randY))
        else:
            enemies.add(Enemy(randX, randY))

def drawUI(screen):
    # playerHealthText = ui_font.render("Health: " + str(p1.health), True, "black")
    # screen.blit(playerHealthText, (20,20))

    waveNumberText = ui_font.render("Wave Number: " + str(waveNumber), True, "black")
    screen.blit(waveNumberText, (20,20))

    enemyCountText = ui_font.render("Enemy count: " + str(len(enemies)), True, "black")
    screen.blit(enemyCountText, (20,50))

    PlayerLevelText = ui_font.render("Player level: " + str(p1.level), True, "black")
    screen.blit(PlayerLevelText, (20,110))

    PlayerXpText = ui_font.render("player xp: " + str(p1.xp), True, "black")
    screen.blit(PlayerXpText, (20, 140))
        
    for i, stateName in enumerate(p1.statLevels):
        statLevel = p1.statLevels[stateName]

        statSurface = stat_font.render(stateName + ": " + str(statLevel), True, "black")
        screen.blit(statSurface, (20, 174 + 20*i))


    # Player health bar
    playerHealthBarWidth = 400 * (p1.health / p1.maxHealth)
    pygame.draw.rect(screen, "gray", pygame.Rect(20, SCREEN_HEIGHT - (40+20), 400, 40), 0, 50)
    pygame.draw.rect(screen, "red", pygame.Rect(20, SCREEN_HEIGHT - (40+20), playerHealthBarWidth, 40), 0, 50)
    pygame.draw.rect(screen, "black", pygame.Rect(20, SCREEN_HEIGHT - (40+20), 400, 40), 3, 50)

    playerStaminaBarWidth = 400 * (p1.stamina / p1.maxStamina)

    staminaColor = "green"
    if p1.lowStamina:
        staminaColor = (225, 172, 0)

    pygame.draw.rect(screen, "gray", pygame.Rect(SCREEN_WIDTH -20 - 400, SCREEN_HEIGHT - (40+20), 400, 40), 0, 50)
    pygame.draw.rect(screen, staminaColor, pygame.Rect(SCREEN_WIDTH -20 - 400, SCREEN_HEIGHT - (40+20), playerStaminaBarWidth, 40), 0, 50)
    pygame.draw.rect(screen, "black", pygame.Rect(SCREEN_WIDTH -20 - 400, SCREEN_HEIGHT - (40+20), 400, 40), 3, 50)
    
def gameUpdate():
    global waveNumber, currentScene
    # Part of Game Loop
    if len(enemies) == 0:
        waveNumber+= 1
        spawmEnemies(waveToEnemyCount(waveNumber))

    currentEnemies = len(enemies)

    p1.update()
    enemies.update(p1)
    projectiles.update()

    # For every projectile, check every enemy for collision
    for enemy in enemies:
        # check all projectiles
        for projectile in projectiles:
            if projectile.rect.colliderect( enemy.rect ):
                if not enemy in projectile.exemptEnemies:
                    enemy.damage( projectile.getDamage() )
                    projectile.exemptEnemies.add(enemy)

        # ... check player collision
        if p1.rect.colliderect( enemy.rect ):
            p1.takeDamage( enemy.getDamage() )

        enemiesEliminated = currentEnemies - len(enemies)

        for i in range(enemiesEliminated):
            # add random amount of xp to player
            xpAmount = max(random.randint(-2, 3), 0)
            p1.xp += xpAmount

    if p1.health <= 0:
        # update the leaderboard
        with open ("leaderboard.txt", "a") as textFile:
            textFile.write(f"{username} {waveNumber}\n")
        currentScene = "lost"

    #This will update the lost screen
    pass

def resetGame():
    global p1, waveNumber
    p1 = Player(200, 100, pygame.Color("#15247F"))
    waveNumber = 0
    enemies.empty()
    projectiles.empty()


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if currentScene == "play":
                if event.button == 1 and p1.speed < p1.baseSpeed*1.5:
                    # Spawn Projectile
                    playerToMouse = pygame.math.Vector2( event.pos ) - p1.rect.center
                    if playerToMouse.magnitude() > 0:
                        playerToMouse.scale_to_length( 10 )
                    projectiles.add( Projectile(p1.rect.centerx, p1.rect.centery, playerToMouse.x, playerToMouse.y, p1.damage, p1.piercing) )
            elif currentScene == "start":
                if event.button == 1 and startButton.collidepoint(pygame.mouse.get_pos()):
                    currentScene = "play"
                elif event.button == 1 and exitButton.collidepoint( pygame.mouse.get_pos() ):
                    running = False
            elif currentScene == "lost":
                if event.button == 1 and retryButton.collidepoint( pygame.mouse.get_pos() ):
                    currentScene = "play"
                    resetGame()
                elif event.button == 1 and exitButton.collidepoint( pygame.mouse.get_pos() ):
                    running = False
    
    if currentScene == "play":
        gameUpdate()
    
        


    # fill the screen with a color to wipe away anything from last frame
    # screen.fill(BACKGROUND_COLOR)
    screen.blit(background, (0, 0))


    if currentScene == "play":
        drawUI(screen)
        p1.draw(screen)
        for e in enemies:
            e.draw(screen)
        projectiles.draw(screen)
    elif currentScene == "start":
        pygame.draw.rect(screen, "cyan", startButton, 0, 50)
        screen.blit(startText, startTextRect)
        pygame.draw.rect(screen, "black", startButton, 5, 50)

        pygame.draw.rect(screen, "red", exitButton, 0, 50)
        screen.blit(exitText, exitTextRect)

        pygame.draw.rect(screen, "black", exitButton, 5, 50)

    elif currentScene == "lost":
        pygame.draw.rect(screen, "cyan", retryButton, 0, 50)
        screen.blit(retryText, retryTextRect)
        pygame.draw.rect(screen, "black", retryButton, 5, 50)

        
        pygame.draw.rect(screen, "red", exitButton, 0, 50)
        screen.blit(exitText, exitTextRect)
        pygame.draw.rect(screen, "black", exitButton, 5, 50)

 # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FRAME_RATE)  # limits FPS to 60


pygame.quit()
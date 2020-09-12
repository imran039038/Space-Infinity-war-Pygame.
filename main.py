import math
import pygame
import random
from pygame import mixer

# screen
pygame.init()
screen = pygame.display.set_mode((626, 626))
pygame.display.set_caption("Corona Defender".upper())
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
scorevalue = 0
# background
background = pygame.image.load("backgroun.png")
explosion = (pygame.transform.scale(pygame.image.load("explosion.png"), (64, 64)))
# player
playerimg = pygame.image.load("plane.png")
playerX = 294
playerY = 540
playerchange = 0
playerchangeY = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemychange = []
num = 4

for i in range(num):
    enemyimg.append(pygame.image.load("virus.png"))
    enemyimg.append(pygame.image.load("virus1.png"))
    enemyimg.append(pygame.image.load("virus2.png"))
    enemyimg.append(pygame.image.load("virus3.png"))
    enemyX.append(random.randint(0, 560))
    enemyY.append(random.randint(50, 300))
    enemychange.append(0.6)

# Bullet
bulletimg = pygame.image.load("soap.png")
bulletX = 310
bulletY = 540
bulletchangeX = 0
bulletchangeY = -2
bulletstate = "ready"

stoneimg = []
stoneX = []
stoneY = []
stonespeed = []
stonenum = 5
if scorevalue >= 200:
    stonenum = 10

for u in range(stonenum):
    stoneimg.append(pygame.transform.scale(pygame.image.load("ston2.png"), (40, 40)))
    stoneX.append(random.randint(-800, 0))
    stoneY.append(random.randint(-500, 0))
    stonespeed.append(1.2)

# score

font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10
texty = 10

gameover_text = pygame.font.Font("freesansbold.ttf", 64)

Level = 1
levelfont = pygame.font.Font("freesansbold.ttf", 32)

tip = pygame.font.Font("freesansbold.ttf", 16)


def tips():
    tiptxt = tip.render("Tip:Power Activate.", True, (255, 255, 0))
    screen.blit(tiptxt, (130, 35))


def levelpoint():
    global Level
    if scorevalue >= 1000:
        Level = 2

    if scorevalue >= 2000:
        Level = 3

    leveltxt = levelfont.render("Level:" + str(Level), True, (255, 255, 255))
    screen.blit(leveltxt, (500, 10))


def gameover():
    game = gameover_text.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game, (120, 300))


def showscore(x, y):
    score = font.render("Score:" + str(scorevalue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))


def bullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg, (x + 17, y))


def Collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def collision_stone(playerX, playerY, stoneX, stoneY):
    distance_of_stone = math.sqrt(math.pow(playerX - stoneX, 2) + (math.pow(playerY - stoneY, 2)))
    if distance_of_stone < 35:
        return True
    else:
        return False


def speed():
    for u in range(stonenum):
        if Level >= 1:
            stoneY[u] += stonespeed[u]
            stoneX[u] += stonespeed[u]
            screen.blit(stoneimg[u], (stoneX[u], stoneY[u]))
            if stoneY[u] and stoneX[u] > 3000:
                stoneX[u] = (random.randint(-800, 0))
                stoneY[u] = (random.randint(-500, 0))


bg2 = mixer.Sound("bg level3.wav")
bg1 = mixer.Sound("bg level2.wav")
if scorevalue == 200:
    pygame.mixer.pause(bg1)
    bg2.play(-1)
else:

    bg1.play(-1)

# main game loop
# clock=pygame.time.Clock()
runing = True
while runing:
    # clock.tick(200)
    # RGB
    screen.fill((10, 50, 100))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False

        # keys
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                playerchange = 1
            if event.key == pygame.K_LEFT:
                playerchange = -1
            if event.key == pygame.K_UP:
                playerchangeY += -0.6
            if event.key == pygame.K_DOWN:
                playerchangeY += 0.6
            if event.key == pygame.K_SPACE:
                if bulletstate is "ready":
                    sounds = mixer.Sound("fire.wav")
                    sounds.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                playerchange = 1
            if event.key == pygame.K_LEFT:
                playerchange = -1
            if event.key == pygame.K_UP:
                playerchangeY = 0
            if event.key == pygame.K_DOWN:
                playerchangeY = 0

    playerX += playerchange

    if Level == 3:
        tips()

        if playerX <= -64:
            playerX = 615
        elif playerX >= 615:
            playerX = -64
    else:

        if playerX <= 0:
            playerX = 0
        elif playerX >= 562:
            playerX = 562
    playerY += playerchangeY
    if playerY <= 0:
        playerY = 0
    elif playerY >= 562:
        playerY = 562

    # enney part
    for i in range(num):

        # game over

        if enemyY[i] >= 500:
            for j in range(num):
                enemyY[j] = 2000
                playerchange = 0
                pygame.mixer.pause()
            gameover()
            break

        if enemyX[i] >= 562:

            if scorevalue >= 1000:
                enemychange[i] = -1
                enemyY[i] += 20
            if scorevalue >= 2000:

                enemychange[i] = -1.2
                enemyY[i] += 20
            else:
                enemychange[i] = -0.6
                enemyY[i] += 20

        elif enemyX[i] <= 0:

            if scorevalue >= 1000:
                enemychange[i] = 1
                enemyY[i] += 20
            if scorevalue >= 2000:

                enemychange[i] = 1.2
                enemyY[i] += 20
            else:
                enemychange[i] = 0.6
                enemyY[i] += 20
        enemyX[i] += enemychange[i]

        iscollision = Collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if iscollision:
            sounds = mixer.Sound("enemy.wav")
            sounds.play()
            bulletY = 480
            bulletstate = "ready"

            enemyX[i] = (random.randint(0, 550))
            enemyY[i] = (random.randint(50, 300))

            scorevalue += 100

        enemy(enemyX[i], enemyY[i], i)

    # bullet part
    if bulletY <= 0:
        bulletY = 540
        bulletstate = "ready"
    if bulletstate is "fire":
        bulletY += bulletchangeY
        bullet(bulletX, bulletY)
    levelpoint()

    player(playerX, playerY)
    speed()
    for u in range(stonenum):
        stone = collision_stone(playerX, playerY, stoneX[u], stoneY[u])
        if stone:
            sounds = mixer.Sound("explosion.wav")
            sounds.play()
            enemyY[i] += 2
            screen.blit(explosion, (playerX + 10, playerY + 5))

    showscore(textx, texty)

    pygame.display.update()

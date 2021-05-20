#importing pygame
import random
import pygame
import time
import math
from pygame import mixer
#initialising pygame
pygame.init()

#setting caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#loading the screen
screen = pygame.display.set_mode((800,600))
back = pygame.image.load("background.png")

#Background sound
mixer.music.load("background.wav")
mixer.music.play(~1)

#upload player image
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 520
playerX_change = 0
def player(x,y):
    screen.blit(playerImg,(x,y))

#upload the enemy
num_of_enemies = 5
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(15)
    enemyY_change.append(25)
def enemy(x,y,i):
    screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))

#upload the bullet
#Ready = cannot see bullet on screen
#fired = bullet is being fired
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 570
bulletX_change = 0
bulletY_change = 35
bullet_state = "ready"
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg,(x + 16,y + 10))

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(198,89,255))
    screen.blit(score,(x,y))

#Condition for collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    return False

running = True
while running:
  #  screen.fill((255,158,9))
    screen.blit(back,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #check if a key is pressed
        if event.type == pygame.KEYDOWN:
            #check which key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
            if event.key == pygame.K_UP and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX,bulletY)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
 #           if event.key == pygame.KEYUP:
  #              if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
   #                 playerX_change = 0.1

        if event.type == pygame.KEYUP:
            #check which key is pressed
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

#enemy movement
    for i in range(num_of_enemies):
        if enemyX[i] > 750 or enemyX[i] < 0:
            if enemyX[i] > 750:
                enemyX[i] = 740
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]



#    enemyX -= enemyX_change
#collision
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 570
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,150)
#player movement
    playerX += playerX_change
    if playerX >= 800:
        playerX = 775
        playerX -= playerX_change
    if playerX < 0:
        playerX -= playerX_change

#bullet movement
    if bulletY <= 0:
        bulletY = 570
        bullet_state = "ready"

    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

#collision
    end = False
    for i in range(num_of_enemies):
        if enemyY[i] > 480:
            end = True
            break
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 150
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,150)

#updating screen

    player(playerX,playerY)
    show_score(textX,textY)
    if end:
        over = pygame.font.Font("freesansbold.ttf",72)
        for j in range(num_of_enemies):
            enemyX[j] = 2000
            enemyY[j] = 2000
        playerX = 2000
        playerY = 2000
        textX = 2000
        textY = 2000
        game_over = over.render("Game Over",True,(255,255,255))
        screen.blit(game_over,(10,20))
        final = pygame.font.Font("freesansbold.ttf",48)
        fin_score = final.render("Final Score : " + str(score_value),True,(255,255,255))
        screen.blit(fin_score,(10,100))


    for i in range(num_of_enemies):
        enemy(enemyX,enemyY,i)
    pygame.display.update()


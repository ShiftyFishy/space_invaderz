
import pygame
import random
import math
import os 
from pygame import mixer
import time
import tkinter as tk


# imgs


game_over_bg = pygame.image.load('assets/bg2.png')
game_over_alien = pygame.image.load('assets/alien2.png')
game_over_img1 = pygame.image.load('assets/game_over_txt.png')
game_over_img2 = pygame.image.load('assets/game_over_txt2.png')

# initialize pygame

pygame.font.init()
pygame.init()
mixer.init()

  
# create the game screen
screen_width = 800
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
game_over_bg = pygame.image.load('assets/bg2.png')

# caption of game
pygame.display.set_caption("Space Invaderz")
   
# Set the score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.SysFont("comicsans", 50)


# game over
game_over_font = pygame.font.SysFont("comicsans", 64)
screen_center =  (screen_width/5,screen_height/5)
  
def show_score(x, y):
    score = font.render("Points: " + str(score_val),True, ("pink"))
    screen.blit(score, (x , y ))



def game_over():
    
    screen.blit(game_over_img1, (70, 100))
   

#####################


#####################

# player
playerImage = pygame.image.load('assets/pixel_ship_yellow.png')
player_X = 350
player_Y = 500
player_Xchange = 0
player_Ychange = 0
  
# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 16
         
invader_file_image = pygame.image.load('assets/alien.png')

for num in range(no_of_invaders):

    number = 1
    invaderImage.append(invader_file_image)
    invader_X.append(random.randint(64, 800))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(number)
    invader_Ychange.append(50)
    
# Bullet: rest - not moving,  fire - moving
bulletImage = pygame.image.load('assets/pixel_laser_yellow.png')
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 8
bullet_state = "rest"
  

# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
    if distance <= 40:
        return True
    else:
        return False

  
def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))
  
def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))
  
def bullet(x, y):
    global bullet_state
    screen.blit(bulletImage, (x+18, y))
    bullet_state = "fire"
  
def timer_over():
    screen.blit(game_over_bg(0,0))



# game loop

surface = pygame.display.set_mode((screen_width, screen_height))
displayImage = pygame.transform.scale(pygame.image.load('assets/bg.png'),(screen_width,screen_height))


running = 0

while running == False or running == 0: 


    surface.blit(displayImage, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = running + 1
    




while running or running == 1:
    surface.blit(displayImage, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player_Xchange = -6
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player_Xchange = 6
            if event.key == pygame.K_UP or event.key == ord('w'):
                player_Ychange = -6
            
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                    player_Ychange = 6
            
            if event.key == pygame.K_SPACE:
            
                
                # Fixing the change of direction of bullet
                if bullet_state is "rest":
                    bullet_X = player_X + 4
                    bullet_Y = player_Y - 8
                    bullet(bullet_X, bullet_Y)
                    '''bullet_sound = mixer.Sound('data/bullet.wav')
                    bullet_sound.play()'''
        if event.type == pygame.KEYUP:
            player_Xchange = 0
            player_Ychange = 0
  
    # change in the player position
    player_X += player_Xchange
    player_Y += player_Ychange

    for i in range(no_of_invaders):
        invader_X[i] += invader_Xchange[i]
  
    # bulletz
    if bullet_Y <= 0:
        bullet_Y = 100
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet(bullet_X, bullet_Y)
        bullet_Y -= bullet_Ychange
  
    # movement of the invader (gameover at 400)
    for i in range(no_of_invaders):

        game_over_collision = isCollision(player_X, invader_X[i], player_Y, invader_Y[i])

        if game_over_collision:
            surface.blit(displayImage, (0,0))
            surface.blit(game_over_img1, (70,100))
            for j in range(no_of_invaders):
                 invader_Y[j] = 2000
            game_over()
            break
  
        if invader_X[i] >= 735 or invader_X[i] <= 0:
            invader_Xchange[i] *= -1
    
            invader_Y[i] += invader_Ychange[i]
        # collision
        collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
        
        if collision:
            score_val += 1
            bullet_Y = 100
            bullet_state = "rest"
            invader_X[i] = random.randint(64, 736)
            invader_Y[i] = random.randint(30, 200)
            invader_Xchange[i] *= -1
            
  
        invader(invader_X[i], invader_Y[i], i)
  
  
    # spaceship dont go off da screen
    if player_X <= 16:
        player_X = 16;
    elif player_X >= 675:
        player_X = 675
    
    if player_Y <= 450:
        player_Y = 450
    
    elif player_Y >= 500:
        player_Y = 500
    
    player(player_X, player_Y)
    show_score(scoreX, scoreY)

   

    pygame.display.update()
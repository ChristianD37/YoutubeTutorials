import pygame
from player import Player
from camera import *

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
house = pygame.image.load('house_full.png').convert()

################################# LOAD PLAYER AND CAMERA###################################
cat = Player()
camera = Camera(cat)
follow = Follow(camera,cat)
border = Border(camera,cat)
auto = Auto(camera,cat)
camera.setmethod(follow)
################################# GAME LOOP ##########################
while running:
    clock.tick(60)
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY, cat.FACING_LEFT = True, True
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY, cat.FACING_LEFT = True, False
            elif event.key == pygame.K_1:
                camera.setmethod(follow)
            elif event.key == pygame.K_2:
                camera.setmethod(auto)
            elif event.key == pygame.K_3:
                camera.setmethod(border)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                cat.LEFT_KEY = False
            elif event.key == pygame.K_RIGHT:
                cat.RIGHT_KEY = False

    ################################# UPDATE/ Animate SPRITE #################################
    cat.update()
    camera.scroll()
    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.blit(house, (0 - camera.offset.x, 0 - camera.offset.y))
    canvas.blit(cat.current_image,(cat.rect.x - camera.offset.x, cat.rect.y - camera.offset.y))
    window.blit(canvas, (0,0))
    pygame.display.update()










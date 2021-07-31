import pygame
from util import load_save, reset_keys
from controls import Controls_Handler


################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W * 2,DISPLAY_H * 2)))
running = True

actions = {"Left": False, "Right": False, "Up": False, "Down": False, "Start": False, "Action1": False}

################################ LOAD THE CURRENT SAVE FILE #################################
save = load_save()
control_handler = Controls_Handler(save)
################################# GAME LOOP ##########################
while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == control_handler.controls['Left']:
                actions['Left'] = True
            if event.key == control_handler.controls['Right']:
                actions['Right'] = True
            if event.key == control_handler.controls['Up']:
                actions['Up'] = True
            if event.key == control_handler.controls['Down']:
                actions['Down'] = True
            if event.key == control_handler.controls['Start']:
                actions['Start'] = True
            if event.key == control_handler.controls['Action1']:
                actions['Action1'] = True

        if event.type == pygame.KEYUP:
            if event.key == control_handler.controls['Left']:
                actions['Left'] = False
            if event.key == control_handler.controls['Right']:
                actions['Right'] = False
            if event.key == control_handler.controls['Up']:
                actions['Up'] = False
            if event.key == control_handler.controls['Down']:
                actions['Down'] = False
            if event.key == control_handler.controls['Start']:
                actions['Start'] = False
            if event.key == control_handler.controls['Action1']:
                actions['Action1'] = False

    ################################# UPDATE THE GAME #################################
    control_handler.update(actions)
    ################################# RENDER WINDOW AND DISPLAY #################################
    canvas.fill((135, 206, 235))
    control_handler.render(canvas)
    window.blit(pygame.transform.scale(canvas, (DISPLAY_W * 2,DISPLAY_H * 2) ), (0,0))
    pygame.display.update()
    reset_keys(actions)
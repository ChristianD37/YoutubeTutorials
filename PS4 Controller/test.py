import pygame
import json, os

################################# LOAD UP A BASIC WINDOW #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 960, 570
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
player = pygame.Rect(DISPLAY_W/2, DISPLAY_H/2, 60,60)
LEFT, RIGHT, UP, DOWN = False, False, False, False
clock = pygame.time.Clock()
color = 0
###########################################################################################

#Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

with open(os.path.join("ps4_keys.json"), 'r+') as file:
    button_keys = json.load(file)
# 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

# START OF GAME LOOP
while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            pass

        # HANDLES BUTTON PRESSES
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['left_arrow']:
                LEFT = True
            if event.button == button_keys['right_arrow']:
                RIGHT = True
            if event.button == button_keys['down_arrow']:
                DOWN = True
            if event.button == button_keys['up_arrow']:
                UP = True
        # HANDLES BUTTON RELEASES
        if event.type == pygame.JOYBUTTONUP:
            if event.button == button_keys['left_arrow']:
                LEFT = False
            if event.button == button_keys['right_arrow']:
                RIGHT = False
            if event.button == button_keys['down_arrow']:
                DOWN = False
            if event.button == button_keys['up_arrow']:
                UP = False

        #HANDLES ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
            # print(analog_keys)
            # Horizontal Analog
            if abs(analog_keys[0]) > .4:
                if analog_keys[0] < -.7:
                    LEFT = True
                else:
                    LEFT = False
                if analog_keys[0] > .7:
                    RIGHT = True
                else:
                    RIGHT = False
            # Vertical Analog
            if abs(analog_keys[1]) > .4:
                if analog_keys[1] < -.7:
                    UP = True
                else:
                    UP = False
                if analog_keys[1] > .7:
                    DOWN = True
                else:
                    DOWN = False
                # Triggers
            if analog_keys[4] > 0:  # Left trigger
                color += 2
            if analog_keys[5] > 0:  # Right Trigger
                color -= 2






    # Handle Player movement
    if LEFT:
        player.x -=5 #*(-1 * analog_keys[0])
    if RIGHT:
        player.x += 5 #* analog_keys[0]
    if UP:
        player.y -= 5
    if DOWN:
        player.y += 5

    if color < 0:
        color = 0
    elif color > 255:
        color = 255


    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((255,255,255))
    pygame.draw.rect(canvas, (0,0 + color,255), player)
    window.blit(canvas, (0,0))
    clock.tick(60)
    pygame.display.update()




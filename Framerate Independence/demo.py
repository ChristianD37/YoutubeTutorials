import pygame, time

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri',40)
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60
WHITE = (255,255,255)
################################# LOAD VARIABLES AND OBJECTS###################################
rect_pos = 0
timer = 0
velocity = 300
prev_time = time.time()
dt = 0
record = 0
passed, start = False, False
FPS = 60
#TARGET_FPS = 60
################################# GAME LOOP ##########################
while running:
    # Limit framerate
    clock.tick(FPS)
    # Compute delta time
    now = time.time()
    dt = now - prev_time
    prev_time = now

    # Update the timer and move the rectangle
    if start:
        timer += dt
        rect_pos += velocity *dt
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True

    if rect_pos > DISPLAY_W and not passed:
        record = timer
        passed = True
    ################################# UPDATE/ Animate SPRITE #################################
    countdown = font.render("Time: " +str(round(timer,5)), False, (255,255,255))

    fps_text = font.render("FPS: " +str(round(clock.get_fps(),2)), False, (255,255,255))
    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((0, 0, 0)) # Fills the entire screen with light blue
    canvas.blit(countdown, (0,0))
    canvas.blit(fps_text, (0, 50))
    pygame.draw.rect(canvas,WHITE,(rect_pos,DISPLAY_H/2 + 30,40,40))
    if record:
        record_text = font.render("Time: " +str(round(record,5)), False, (255,255,255))
        canvas.blit(record_text, (DISPLAY_W/4, DISPLAY_H/2))
    window.blit(canvas, (0,0))
    pygame.display.update()









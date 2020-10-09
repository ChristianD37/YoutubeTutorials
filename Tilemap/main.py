from tiles import *
from spritesheet import Spritesheet


################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()

################################# LOAD PLAYER AND SPRITESHEET###################################
spritesheet = Spritesheet('spritesheet.png')
player_img = spritesheet.parse_sprite('chick.png')
player_rect = player_img.get_rect()

#################################### LOAD THE LEVEL #######################################
map = TileMap('test_level.csv', spritesheet )
player_rect.x, player_rect.y = map.start_x, map.start_y

################################# GAME LOOP ##########################
while running:
    clock.tick(60)
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
        #     if event.key == pygame.K_LEFT:
        #         player.LEFT_KEY, player.FACING_LEFT = True, True
        #     elif event.key == pygame.K_RIGHT:
        #         player.RIGHT_KEY, player.FACING_LEFT = True, False
        #
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT:
        #         player.LEFT_KEY = False
        #     elif event.key == pygame.K_RIGHT:
        #         player.RIGHT_KEY = False

    ################################# UPDATE/ Animate SPRITE #################################

    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((0, 180, 240)) # Fills the entire screen with light blue
    map.draw_map(canvas)
    canvas.blit(player_img, player_rect)
    window.blit(canvas, (0,0))
    pygame.display.update()










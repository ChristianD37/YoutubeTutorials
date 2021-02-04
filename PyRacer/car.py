import pygame,os

class Car():
    def __init__(self, game):
        self.game = game
        self.position, self.distance = 0, 0
        self.position_int = self.game.DISPLAY_W / 2 + int(self.game.SCREEN_WIDTH * self.position / 2) - 14
        self.speed = 0
        self.curvature = 0
        self.image = pygame.image.load(os.path.join(self.game.img_dir,"car.png")).convert()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()

    def clamp_speed(self):
        self.speed = max(0, self.speed)
        self.speed = min(self.speed,1)

    def update(self):
        # Update the Car's movement
        if self.game.actions['accel']:
            self.speed += .5 * self.game.dt
        else:
            self.speed -= .25 * self.game.dt

        if self.game.actions['brake']:
            self.speed -=.75 * self.game.dt

        if self.game.actions['left']:
             self.curvature -= .3 * self.game.dt
        if self.game.actions['right']:
            self.curvature += .3 * self.game.dt

        if abs(self.curvature - self.game.map.track_curvature) >= .55:
            self.speed -= 5 * self.game.dt

        self.clamp_speed()
        self.distance += 70 * self.speed * self.game.dt

    def draw(self):
        self.position = self.curvature - self.game.map.track_curvature
        self.position_int = self.game.DISPLAY_W / 2 + int(self.game.DISPLAY_W * self.position / 2)
        self.rect.center = (self.position_int, 220)
        self.game.display.blit(self.image, self.rect)
        pygame.draw.rect(self.game.display, (0,0,0), (self.position_int, 220, 4, 4) )
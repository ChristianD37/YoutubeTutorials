import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect()
        self.rect.midbottom = (570, 244)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = 'idle'
        self.current_image = self.idle_frames_left[0]
        self.left_border, self.right_border = 250, 1150
        self.ground_y = 224
        self.box = pygame.Rect(self.rect.x, self.rect.y, self.rect.w * 2, self.rect.h)
        self.box.center = self.rect.center
        self.passed = False

    def draw(self, display):
        display.blit(self.current_image, self.rect)

    def update(self):
        self.velocity = 0
        if self.LEFT_KEY:
            self.velocity = -2
        elif self.RIGHT_KEY:
            self.velocity = 2
        self.rect.x += self.velocity
        if self.velocity == 0 and self.passed:
            self.passed = False
            self.box.center = self.rect.center
        if self.rect.x > 1150 - self.rect.w:
            self.rect.x = 1150 - self.rect.w
        elif self.rect.x < 250:
            self.rect.x = 250
        self.set_state()
        self.animate()
        if self.rect.left > self.box.left and self.rect.right < self.box.right :
            pass
        else:
            self.passed = True
            if self.rect.left > self.box.left :
                self.box.left += self.velocity
            elif self.rect.right < self.box.right :
                self.box.left += self.velocity


    def set_state(self):
        self.state = ' idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'

    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == ' idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.current_image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.current_image = self.walking_frames_right[self.current_frame]



    def load_frames(self):
        my_spritesheet = Spritesheet('poppy_sheet.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [my_spritesheet.parse_sprite("poppy_idle1.png"),
                                 my_spritesheet.parse_sprite("poppy_idle2.png")]
        self.walking_frames_left = [my_spritesheet.parse_sprite("poppywalk1.png"), my_spritesheet.parse_sprite("poppywalk2.png"),
                           my_spritesheet.parse_sprite("poppywalk3.png"), my_spritesheet.parse_sprite("poppywalk4.png"),
                           my_spritesheet.parse_sprite("poppywalk5.png"), my_spritesheet.parse_sprite("poppywalk6.png"),
                           my_spritesheet.parse_sprite("poppywalk7.png"), my_spritesheet.parse_sprite("poppywalk8.png")]
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append( pygame.transform.flip(frame,True, False) )
        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(pygame.transform.flip(frame, True, False))













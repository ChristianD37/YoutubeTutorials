import pygame, time, os
from map import Map

class Game():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # Prevents delay in jumping sound
        pygame.init()
        # Intitialize display surface and screen
        self.DISPLAY_W, self.DISPLAY_H = 480, 270 # Dimensions of the 'canvas'. Use this for game logic May be upscaled later
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 480 * 2 , 270 * 2  # Dimensions of the screen that canvas will be drawn onto
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.screen.set_alpha(None)
        pygame.display.set_caption("PyRacer")
        # Initialize clock, controls, and other variables
        self.running, self.playing = True, False
        self.load_assets()
        self.prev_time = time.time()
        self.fps_list = []
        self.actions = {'left' : False, 'right' : False, 'accel' : False, 'brake' : False, 'start' : False}
        self.best_time = 1000000000000

        # Resets any logic that needs to be reset after every game loop
        # May include player, enemies, level, objects, etc
    def reset(self):
        self.map = Map(self)
        self.go_text = 0
        self.lap_time = 0
        self.countdown = 3
        self.countdownUpdate = time.time()
        self.counting_down = True
        self.complete = False
        self.finished_countdown = 0
        self.light_sound.play()



    # Main Game Loop. Starts by resetting the game, and then loops until playing is set to false
    def game_loop(self):
        self.reset()
        pygame.mixer.music.play(-1)
        while self.playing:
            self.get_dt()
            self.get_events()
            if self.countdown > 0:  self.count_down()
            else:   self.update()
            self.render()
        pygame.mixer.music.stop()

    def get_events(self):
        # Gets all events from the user, stores them in the 'actions' dictionary
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_a:
                    self.actions['left'] = True
                if event.key == pygame.K_d:
                    self.actions['right'] = True
                if event.key == pygame.K_w:
                    self.actions['accel'] = True
                if event.key == pygame.K_s:
                    self.actions['brake'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions['left'] = False
                if event.key == pygame.K_d:
                    self.actions['right'] = False
                if event.key == pygame.K_w:
                    self.actions['accel'] = False
                if event.key == pygame.K_s:
                    self.actions['brake'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False
                
    # Update any of the game sprites
    def update(self):
        self.timer()
        self.map.update()
        if self.complete: self.complete_timer()

    # Draw all sprites and images onto the screen
    def render(self):
        self.map.render()
        self.draw_startup()
        self.draw_to_screen()
    # Helper function to draw our 'canvas' to the screen
    def draw_to_screen(self):
        self.screen.blit(pygame.transform.scale(self.display,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
        pygame.display.update()

    # Displays Main Menu
    def main_menu(self):
        display_menu = True
        while display_menu:
            self.get_events()
            # If start is pressed, play the game
            display_menu = self.running
            if self.actions['start']: 
                display_menu = False
                self.playing = True
            self.display.fill((209,29,39))
            self.draw_lg_text("PyRacer!", ((255, 250, 239)), self.DISPLAY_W *.5, self.DISPLAY_H * .4)
            self.draw_text("Press Start to Play", ((255, 250, 239)), self.DISPLAY_W *.22, self.DISPLAY_H * .5)
            self.draw_to_screen()

    def draw_startup(self):
        if self.countdown >0:
            self.display.blit(self.light_images[self.countdown-1],(self.DISPLAY_W * .5 - 32, 50))
        elif self.go_text < .75:
            self.go_sound.play()
            self.go_text += self.dt
            self.display.blit(self.go_img,(self.DISPLAY_W * .5 - 32, 50))

    # Computes FPS, delta time, and caps the frame rate if specified in the FPS() class 
    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
        self.get_fps()

    def get_fps(self):
        fps = 0
        if self.dt: fps = 1/self.dt
        if len(self.fps_list) == 50:
            self.fps_list.pop(0)
        self.fps_list.append(fps)
        avg_fps = sum(self.fps_list) / len(self.fps_list)
        pygame.display.set_caption('PyRacer - FPS:' + str(round(avg_fps,2)))

        # Resets all the keys to False. Useful for Menus
    def reset_keys(self):
        for key in self.actions:
            self.actions[key] = False

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = x, y
        self.display.blit(text_surface, text_rect)

    def draw_lg_text(self, text, color, x, y):
        text_surface = self.lg_font.render(text, True, color)
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)


    def timer(self):
        self.lap_time += self.dt

    def complete_timer(self):
        self.finished_countdown += self.dt
        if self.finished_countdown > 3:
            self.playing = False

    def count_down(self):
        now = time.time()
        if now - self.countdownUpdate > 1:
            self.countdownUpdate = now
            self.countdown -=1
            self.light_sound.play()
        if self.countdown > 0:
            self.counting_down = False

    def load_assets(self):
        self.load_directories()
        self.load_images()
        self.load_sounds()

    def load_directories(self):
        self.dir = os.path.join(os.path.dirname(os.path.abspath("game.py")))  # Gets the directory name of the game.py file
        self.img_dir = os.path.join(self.dir,"Assets", "images")
        self.sound_dir = os.path.join(self.dir,"Assets","sounds")
        

    def load_images(self):
        # Load all the images
        self.light_images = [
            pygame.image.load(os.path.join(self.img_dir, "streetlight3.png")).convert(),
            pygame.image.load(os.path.join(self.img_dir, "streetlight2.png")).convert(),
            pygame.image.load(os.path.join(self.img_dir, "streetlight1.png")).convert()
        ]
        self.go_img = pygame.image.load(os.path.join(self.img_dir, "GO.png")).convert()
        for image in self.light_images:
            image.set_colorkey((0,0,0))
        self.go_img.set_colorkey((0,0,0))
        # Load all the fonts
        self.font = pygame.font.Font(os.path.join(self.img_dir, "PressStart2P-vaV7.ttf"), 14)
        self.lg_font = pygame.font.Font(os.path.join(self.img_dir, "PressStart2P-vaV7.ttf"), 28)

    def load_sounds(self):
        self.theme = pygame.mixer.music.load( os.path.join(self.sound_dir,"racing_song.ogg") )
        self.light_sound = pygame.mixer.Sound(os.path.join(self.sound_dir,"light.wav"))
        self.go_sound = pygame.mixer.Sound(os.path.join(self.sound_dir, "go.wav"))
        self.light_sound.set_volume(.3)
        self.go_sound.set_volume(.2)
    


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.main_menu()
        g.game_loop()
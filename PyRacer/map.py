import pygame, math,os
from car import Car

class Map():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = int(self.game.DISPLAY_W /2), int(self.game.DISPLAY_H /2)
        self.car = Car(self.game)
        self.curvature = 0
        self.track_curvature = 0
        self.track_length = 0
        self.load_track()
        self.lap, self.counted = 0,True
        self.lap_times = []
        self.background_img = pygame.image.load(os.path.join(self.game.img_dir, "background.png")).convert()

    def render(self):
        #self.update()
        self.draw_map()

    def update(self):
        # Update the car
        self.car.update()
        self.update_track()
        if self.lap > 2:
            self.lap = 2
            self.game.complete = True
            self.game.best_time = min(self.game.best_time, sum(self.lap_times))

    def update_track(self):
        track_section, offset = 0, 0

        if self.car.distance >= self.track_length:
            self.car.distance -= self.track_length

        # optimise Curvature Calculations
        while track_section < len(self.track) and offset <= self.car.distance:
            offset += self.track[track_section][1]
            track_section += 1
        target_curvature = self.track[track_section - 1][0]

        track_curve_diff = (target_curvature - self.curvature) * self.game.dt * self.car.speed
        self.curvature += track_curve_diff

        self.track_curvature += self.curvature * self.game.dt * self.car.speed

        if track_section == 1 and not self.counted:
            self.store_times()
            self.counted = True
            self.lap += 1

        if track_section > 1:
            self.counted = False

    def draw_map(self):

        self.game.display.blit(self.background_img, (0, 0))

        x,y = 0,0
        # Draw the Entire map
        while y < self.mid_h:
            x = 0
            while x < self.game.DISPLAY_W:
                # Calculate perspective (farther tiles are closer to 1)
                perspective = float(y / self.mid_w)

                midpoint = .5 + self.curvature * math.pow(1 - perspective,3)
                road_w = .2 + perspective * .9
                clip_width = road_w * .16

                road_w *= .5

                LeftGrass = int( (midpoint - road_w - clip_width) * self.game.DISPLAY_W )
                LeftClip = int((midpoint - road_w) * self.game.DISPLAY_W)
                RightClip = int((midpoint + road_w) * self.game.DISPLAY_W)
                RightGrass = int((midpoint + road_w + clip_width) * self.game.DISPLAY_W)

                nRow = self.mid_h + y

                #grass_color = (0,255,100)
                grass_color = (	194, 178, 128)
                grass_val = math.sin(20 * math.pow(1 - perspective, 3) + self.car.distance * .1)
                if grass_val > 0: grass_color = 	(	198, 163, 80)

                clip_color = (255,0,0)
                clip_val = math.sin(80 * math.pow(1 - perspective, 2) + self.car.distance * .5 )
                if clip_val > 0: clip_color = (255,255,255)
                # Draw the appropriate tile
                if x >= 0 and x < LeftGrass:
                    pygame.draw.rect(self.game.display, grass_color, (x,nRow,8,8))
                if x >= LeftGrass and x < LeftClip:
                    pygame.draw.rect(self.game.display, clip_color, (x, nRow, 8, 8))
                if x >= LeftClip and x < RightClip:
                    pygame.draw.rect(self.game.display, (89,89,89), (x, nRow, 8, 8))
                if x >= RightClip and x < RightGrass:
                    pygame.draw.rect(self.game.display, clip_color, (x, nRow, 8, 8))
                if x >= RightGrass and x < self.game.DISPLAY_W:
                    pygame.draw.rect(self.game.display, grass_color, (x,nRow,8,8))
                x += 8
            y += 8

        # Draw the player's car
        self.car.draw()
        self.draw_stats()

    def draw_stats(self):
        speed_color = (255,255,255)
        if self.car.speed > .9:
            speed_color = (255,0,0)
        self.game.draw_text('Speed (Km): ' + str(round(self.car.speed * 100,2)) , speed_color, 10,10)
        self.game.draw_text('Time: ' + str(round(self.game.lap_time, 2)), (255, 255, 255), 10, 30)
        self.game.draw_text('Lap: ' + str(self.lap) + "/2", (255, 255, 255), 10, 50)
        # Draw lap times
        i = 0
        for lap in self.lap_times:
            self.game.draw_text('Lap ' + str(i+ 1) +': ' + str(round(lap,2)), (255, 255, 255) ,
                                self.game.DISPLAY_W - 200, 10 + (20 * i))
            i += 1

        # If the track is complete, draw text that displays the players times
        if self.game.complete: 
            self.game.draw_lg_text('FINISHED', (0, 0, 255), self.mid_w - 10,self.mid_h)
            self.game.draw_text('Best Time:' + str(round(self.game.best_time,2)), (0, 0, 255), self.mid_w*.5,self.mid_h + 40)

    def load_track(self):
        self.track = [
            (0,10), # Start/ Finish Line
            (0,200),
            (.5,200),
            (0,200),
            (.6, 200),
            (-.5,200),
            (.4,200),
            (-.6,200),
            (0,100)
        ]
        # Comput the total track length
        for lane in self.track:
            self.track_length += lane[1]

    def store_times(self):
        self.lap_times.append(self.game.lap_time)
        self.game.lap_time = 0
        self.game.go_sound.play()
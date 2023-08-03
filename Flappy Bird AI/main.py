import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD1_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\bird1.png"
BIRD2_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\bird2.png"
BIRD3_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\bird3.png"
PIPE_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\pipe.png"
BASE_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\base.png"
BG_file_path = "C:\\Coding2\\Machine-Learning-Projects(public)\\Flappy Bird AI\\imgs\\bg.png"

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(BIRD1_file_path)), 
             pygame.transform.scale2x(pygame.image.load(BIRD2_file_path)), 
             pygame.transform.scale2x(pygame.image.load(BIRD3_file_path))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(PIPE_file_path))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(BASE_file_path))
BG_IMG = pygame.transform.scale2x(pygame.image.load(BG_file_path))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16 : d = 16
        if d < 0 : d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG 
        
        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height() #lefttop corner of the top pipe
        self.bottom = self.height + self.GAP #lefttop corner of the bottom pipe
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self): pass




def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()

main()

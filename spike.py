import pygame
import random
import os
import time

pygame.init()

WIN_WIDTH = 272 #multiple of bird width
WIN_HEIGHT = 512

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

bird_imgs = {"right": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","birdright.png")).convert_alpha()),
             "left": pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","birdleft.png")).convert_alpha())}
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipeleft.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (WIN_WIDTH, WIN_HEIGHT))

wall_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","wallleft.png")).convert_alpha())

bird_imgs = {"right": pygame.image.load(os.path.join("imgs","birdright.png")).convert_alpha(),
             "left": pygame.image.load(os.path.join("imgs","birdleft.png")).convert_alpha()}
pipe_img = pygame.image.load(os.path.join("imgs","pipeleft.png")).convert_alpha()
bg_img =pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha()

wall_img = pygame.image.load(os.path.join("imgs","wallleft.png")).convert_alpha()



class Bird:
    """
    Bird class representing the flappy bird
    """
    IMGS = bird_imgs
    xvel = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.facing = 1
        self.vel = 0
        self.xvel = self.xvel
        self.height = self.y
        self.img = self.IMGS["right"]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        
        self.tick_count+=1
        
        d = self.vel * self.tick_count + 1.5*self.tick_count**2
        
        if d >= 10:
            d = 10
        if d < 0:
            d =- 10
        
        self.y = self.y + d
        
        if self.facing == 1:
            self.img = self.IMGS["right"]
            self.x += self.xvel
        elif self.facing == -1:
            self.img = self.IMGS["left"]
            self.x -= self.xvel
        

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
        
    def hitwall(self, walls):
        #print(self.x)
        if self.x <= walls.leftx + wall_img.get_width() or (self.x + self.img.get_width()) >= walls.rightx:
            #print("bump")
            self.facing *= -1

        
        


class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.gap = 50
        self.left = pipe_img
        self.right = pygame.transform.flip(pipe_img, True, True)
        self.passed = False

    
        
        


class Walls:
    
    def __init__(self):
        self.right = pygame.transform.flip(wall_img, True, True)
        self.left = wall_img
        
        birdveloffset = abs(self.left.get_width()- Bird.xvel)
        self.leftx = birdveloffset
        self.rightx = WIN_WIDTH - (self.right.get_width() + birdveloffset)
    def draw(self, win):
        win.blit(self.left, (self.leftx, 0))
        win.blit(self.right, (self.rightx, 0))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.left), pygame.mask.from_surface(self.right)
        



def draw_window(win, bird, walls):
    win.blit(bg_img, (0,0))
    bird.draw(win)
    walls.draw(win)
    pygame.display.update()
        
def main():
    clock = pygame.time.Clock()
    bird = Bird(200, 200)
    walls = Walls()
    run = True
    while run:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    bird.jump()
        bird.move()
        bird.hitwall(walls)
        draw_window(win, bird, walls)
        #pygame.display.update()
    pygame.quit()
            
main()
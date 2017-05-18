import pygame
from pygame.locals import *
import sys
from sys import exit
import random
import time
import os

size = (800, 600)
black = (0, 0, 0)
white = (255, 255, 255)
red =(255,0,0)
green =(0,255,0)
blue =(0,0,255)

title = "Hello, Pygame!"
screen = pygame.display.set_mode(size, 0, 32)
letters=["a","b","c","d","e","f","g","h","i","j","k","l"\
        ,"m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
imgs=["ball1.png","ball2.png","ball3.png","ball4.png","ball5.png","ball6.png"]
clock=pygame.time.Clock()

class ball:
    def __init__(self):
        font = pygame.font.SysFont('Comic Sans MS', 60)
        self.letter=random.choice(letters)
        self.text = font.render(self.letter, True, black)
        img="img/{}".format(random.choice(imgs))
        self.img= pygame.image.load(img)
        self.x=random.randint(0,size[0]-self.img.get_rect().size[0])
        self.y=random.randint(size[0],size[0]+100)
    def draw(self):
        #w,h=self.img.size
        screen.blit(self.img, (self.x, self.y))
        screen.blit(self.text, (self.x+(self.img.get_rect().size[0]-self.text.get_width())/2,\
                             self.y+self.img.get_rect().size[1]/5))
def run():
    bg = pygame.image.load("img/bg.jpg")
    top = pygame.image.load("img/top.png")
    pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12) 
    boom_sound = pygame.mixer.Sound("sound/boom.wav")
    shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
    pygame.mixer.music.load("sound/bgm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    pygame.init()
    pygame.display.set_caption(title)

    grade=0
    heart=3
    font = pygame.font.SysFont('Comic Sans MS', 50)
    balls=list([ball() for count in xrange(5)])
    print balls
    addball=0

    #x = (size[0]-text.get_width()) / 2
    #y = (size[1]-text.get_height()) / 2
    dx=50
    dy=50
    while True and heart>0:
        message= "Grade:{}".format(grade)
        text = font.render(message, True, red)
        heartimg=pygame.image.load("img/{}heart.png".format(heart))
        #message2= "Heart:{}".format(heart)
        #text2 = font.render(message2, True, red)
        for event in pygame.event.get():
            #print event
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                same=0
                for balloon in balls:
                    if balloon.letter==pygame.key.name(event.key):
                        shoot_sound.play()
                        grade+=1
                        addball+=1
                        balloon.__init__()
                        #del balls[balls.index(balloon)] 
                        #balls.append(ball())
                        same +=1
                if same==0:
                    heart-=1
                    boom_sound.play()

        #screen.fill(white)
        screen.blit(bg, (0,0))
        screen.blit(top, (0,0))
        screen.blit(text, (0, size[1]-text.get_height()))
        screen.blit(heartimg, (size[0]-heartimg.get_rect().size[0], size[1]-heartimg.get_rect().size[1]))
        #screen.blit(text2, (size[0]-text2.get_width(), size[1]-text2.get_height()))
        for balloon in balls:
            if balloon.y <= 10:
                heart-=1
                boom_sound.play()
                balloon.__init__()
            else:
                balloon.draw()
                balloon.y-=10
        if addball>10:
            balls.append(ball())
            addball=0
        clock.tick(10)
        pygame.display.update()
    pygame.mixer.music.stop()
    screen.blit(text, ((size[0]-text.get_width())/2, (size[1]-text.get_height())/2))
    pygame.display.update()
    os.system("pause")


 
if __name__ == "__main__":
    run()
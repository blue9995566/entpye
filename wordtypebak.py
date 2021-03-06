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
blue =(128,128,255)
pygame.init()
title = "Hello, Pygame!"
screen = pygame.display.set_mode(size, 0, 32)
text_file = open("words.txt", "r")
allwords=text_file.readline().rstrip('\n').split(',')
clock=pygame.time.Clock()
grade=0
message= "Grade:{}".format(grade)
font = pygame.font.SysFont('Comic Sans MS', 40)
imgs=["ball1.png","ball2.png","ball3.png","ball4.png","ball5.png","ball6.png"]
text = font.render(message, True, red)
wpm=0

positions=[]
def newposition():
    a=(random.randint(-2,-1)*200,random.randint(0,9)*60)
    while a in positions:
        a=(random.randint(-2,-1)*200,random.randint(0,9)*60)
    positions.append(a)
    return a

class a_word:
    def __init__(self):
        font = pygame.font.SysFont('Comic Sans MS', 30)
        self.word=random.choice(allwords)
        self.text = font.render(self.word, True, white)
        self.initpos=newposition()
        self.x=self.initpos[0]
        self.y=self.initpos[1]
        print text.get_width()
        print text.get_height()
    def draw(self):
        screen.blit(self.text, (self.x,self.y))
def run():
    bg = pygame.image.load("img/bg.jpg")
    pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12) 
    boom_sound = pygame.mixer.Sound("sound/boom.wav")
    shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
    pygame.mixer.music.load("sound/bgm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    pygame.display.set_caption(title)

    global grade
    global wpm
    grade=0
    heart=3
    words=list([a_word() for count in xrange(5)])
    print words
    FPS=50
    word_input= ""
    start=time.time()
    while True and heart>0:
        global message
        global text
        global positions
        input_text= font.render(word_input, True, blue)
        message= "Grade:{}".format(grade)
        text = font.render(message, True, red)
        heartimg=pygame.image.load("img/{}heart.png".format(heart))
        for event in pygame.event.get():
            #print event
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                same=0
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_BACKSPACE:
                    word_input = word_input[:-1]
                elif event.key == K_RETURN:
                    for word in words:
                        if word.word==word_input:
                            shoot_sound.play()
                            grade+=1
                            del words[words.index(word)]
                            same +=1
                    if same==0:
                        boom_sound.play()
                    word_input=""
                else:
                    word_input+=pygame.key.name(event.key)
                

        #screen.fill(white)
        screen.blit(bg, (0,0))
        screen.blit(input_text, (0, size[1]-text.get_height()))
        #screen.blit(text, (0, size[1]-text.get_height()))
        screen.blit(heartimg, (size[0]-heartimg.get_rect().size[0], size[1]-heartimg.get_rect().size[1]))
        for word in words:
            if word.x >= size[0]:
                heart-=1
                if heart==0:
                    break
                boom_sound.play()
                del words[words.index(word)]
            else:
                word.draw()
                word.x+=2
        if len(words)==0:
            positions=[]
            words=list([a_word() for count in xrange(5)])
        clock.tick(FPS)
        pygame.display.update()
    end = time.time()
    wpm=int(round(grade/(end-start)*60))
    heartimg=pygame.image.load("img/{}heart.png".format(heart))
    screen.blit(heartimg, (size[0]-heartimg.get_rect().size[0], size[1]-heartimg.get_rect().size[1]))
    pygame.display.update()
    gameover()
    

def gameover():
    while True:
        pygame.mixer.music.stop()
        message= "wpm:{}".format(wpm)
        text = font.render(message, True, red)
        screen.blit(text, ((size[0]-text.get_width())/2, (size[1]-text.get_height())/2))
        gameover_message="gameover press C to try again!"
        gameover_text = font.render(gameover_message, True, green)
        screen.blit(gameover_text, ((size[0]-gameover_text.get_width())/2, (size[1]-gameover_text.get_height())/2+50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_c:
                    run()

if __name__ == "__main__":
    run()
    
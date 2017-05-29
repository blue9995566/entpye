# coding=utf-8
import Tkinter as tk   # python
from Tkinter import *
import tkMessageBox
import MySQLdb

import platform
import os

import pygame
from pygame.locals import *
import sys
from sys import exit
import random
import time
import os

TITLE_FONT = ("Helvetica", 18, "bold")
HOST="140.120.57.34"
#HOST="localhost"

size = (800, 600)
black = (0, 0, 0)
white = (255, 255, 255)
red =(255,0,0)
green =(0,255,0)
blue =(0,0,255)
title = "Hello, Pygame!"
letters=["a","b","c","d","e","f","g","h","i","j","k","l"\
        ,"m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
imgs=["ball1.png","ball2.png","ball3.png","ball4.png","ball5.png","ball6.png"]


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, RegistPage, Menu,gamepage,letterpage,person,person_letter,topten,topten_letter):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        #self.show_frame("letterpage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
        #label.grid(row=0,columnspan=4)
        label.place(x=400, y=200, anchor=CENTER)

        account_label = tk.Label(self, text="Account:", font=TITLE_FONT)
        #account_label.grid(row=1,column=0,columnspan=2)
        account_label.place(x=300, y=250, anchor=CENTER)

        self.nameEntry = Entry(self)
        self.nameEntry.grid(row=1,column=3)
        self.nameEntry.place(x=450, y=250, anchor=CENTER)

        pwd_label = tk.Label(self, text="Password:", font=TITLE_FONT)
        pwd_label.grid(row=2,column=0,columnspan=2)
        pwd_label.place(x=300, y=300, anchor=CENTER)

        self.passEntry = Entry(self, show='*')
        self.passEntry.grid(row=2,column=3)
        self.passEntry.place(x=450, y=300, anchor=CENTER)

        button1 = tk.Button(self, text="regist",
                            command=lambda: controller.show_frame("RegistPage"))
        button1.place(x=300, y=350, anchor=CENTER)
        #button1.grid(row=3,column=0,columnspan=2)
        button2 = tk.Button(self, text="Login",command=self.login)
        button2.place(x=450, y=350, anchor=CENTER)
        #button2.grid(row=3,column=3)
    def login(self):
        if self.nameEntry.get()!='' and self.passEntry.get()!='':
            DBlogin(self.nameEntry.get(),self.passEntry.get())
            if login_id!=0:
                self.controller.show_frame("Menu")
        else:
            tkMessageBox.showinfo( "Fail to regist", "Please check the form!")

def DBlogin(name,pwd):
    try:
        db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
        login_sql="SELECT * from user where account= \'%s\' and password = \'%s\'" %(name,pwd)
        cursor = db.cursor()
        cursor.execute(login_sql)
        results = cursor.fetchall()
        if len(results)==0:
            tkMessageBox.showinfo( "Fail to login", "Wrong account or password!")
        else:
            global login_id
            login_id=results[0][0]
            print login_id
            login_user=results[0][1]
            hello_user="Hello,",login_user
            app.frames['Menu'].id_var.set(hello_user)
            #tkMessageBox.showinfo( "Successfully", "Login successfully!")
        # 關閉連線
        db.close()

    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        tkMessageBox.showinfo( "Fail to connect", "Please check connection!")

#個人紀錄(type:1為字母，2為單字)
def person_record(uid,tpyee,listbox):
    try:
        db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
        record_sql="SELECT * from record where uid= \'%d\' and type = \'%d\' ORDER BY `time` DESC" %(uid,tpyee)
        cursor = db.cursor()
        cursor.execute(record_sql)
        results = cursor.fetchall()
        listbox.delete(0,END)
        for record in results:
            listbox.insert(END,"{}---{}".format(record[3],record[4]))
            #app.frames['PageTwo'].id_var.set(hello_user)
            #tkMessageBox.showinfo( "Successfully", "Login successfully!")
        # 關閉連線
        db.close()

    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        tkMessageBox.showinfo( "Fail to connect", "Please check connection!")
#排行榜(type:1為字母，2為單字)
def top_record(tpyee,listbox):
    try:
        db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
        record_sql="SELECT `user`.`account`, `record`.`grade` from `record` INNER JOIN `user` on `user`.`id`=`record`.`uid` and type = \'%d\' ORDER BY `record`.`grade` DESC limit 0,10" %(tpyee)
        cursor = db.cursor()
        cursor.execute(record_sql)
        results = cursor.fetchall()
        listbox.delete(0,END)
        x=1
        for record in results:
            listbox.insert(END,"第{}名:{}---{}".format(x,record[0],record[1]))
            x+=1
            #app.frames['PageTwo'].id_var.set(hello_user)
            #tkMessageBox.showinfo( "Successfully", "Login successfully!")
        # 關閉連線
        db.close()

    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        tkMessageBox.showinfo( "Fail to connect", "Please check connection!")


def DBinsert(name,pwd):
    try:
        db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
        check_sql="SELECT * from user where account= \'%s\'" %(name)
        cursor = db.cursor()
        cursor.execute(check_sql)
        results = cursor.fetchall()
        if len(results)!=0:
            tkMessageBox.showinfo( "Fail to regist", "This account has been registed!")
        else:
            insert_sql = "INSERT INTO user (id, account, password) VALUES (NULL, \'%s\', \'%s\');"% (name,pwd)
            #sql = "INSERT INTO user (id, account, password) VALUES (NULL, '123','456')"
            # 執行SQL statement
            cursor = db.cursor()
            cursor.execute(insert_sql)
            db.commit()
            tkMessageBox.showinfo( "Successfully", "Regist successfully!")
        # 關閉連線
        db.close()

    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        tkMessageBox.showinfo( "Fail to connect", "Please check connection!")

def record_insert(uid,grade,typee):
    try:
        db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
        insert_sql = "INSERT INTO record (id, uid,type, grade, `time`) VALUES (NULL, \'%d\', \'%d\', \'%d\',CURRENT_DATE);"% (uid,typee,grade)
        # 執行SQL statement
        cursor = db.cursor()
        cursor.execute(insert_sql)
        db.commit()
        # 關閉連線
        db.close()

    except MySQLdb.Error as e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        tkMessageBox.showinfo( "Fail to connect", "Please check connection!")



class RegistPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is register page", font=TITLE_FONT)
        label.place(x=400, y=200, anchor=CENTER)
        
        account_label = tk.Label(self, text="Account:", font=TITLE_FONT)
        account_label.place(x=300, y=250, anchor=CENTER)

        self.nameEntry = Entry(self)
        self.nameEntry.place(x=450, y=250, anchor=CENTER)


        pwd_label = tk.Label(self, text="Password:", font=TITLE_FONT)
        pwd_label.place(x=300, y=300, anchor=CENTER)

        self.passEntry = Entry(self, show='*')
        self.passEntry.place(x=450, y=300, anchor=CENTER)

        B = tk.Button(self, text ="regist", command = self.helloCallBack,fg="blue")
        B.place(x=300, y=350, anchor=CENTER)

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(x=450, y=350, anchor=CENTER)

    def helloCallBack(self):
        if self.nameEntry.get()!='' and self.passEntry.get()!='':
            DBinsert(self.nameEntry.get(),self.passEntry.get())
        else:
            tkMessageBox.showinfo( "Fail to regist", "Please check the form!")



class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id_var=StringVar()
        #self.id_var.set("dfgzxgffdgh")
        #textvariable=id_var
        label = tk.Label(self, textvariable=self.id_var, font=TITLE_FONT)
        #label.grid(row=0,columnspan=4)
        label.place(x=400, y=200, anchor=CENTER)

        button = tk.Button(self, text="開始",command=lambda:controller.show_frame("gamepage"))
        #button.grid(row=1,columnspan=4)
        button.place(x=400, y=250, anchor=CENTER)

        button = tk.Button(self, text="個人紀錄",command=lambda:controller.show_frame("person"))
        #button.grid(row=1,columnspan=4)
        button.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="排行榜",command=lambda:controller.show_frame("topten"))
        #button.grid(row=1,columnspan=4)
        button.place(x=400, y=350, anchor=CENTER)

        button = tk.Button(self, text="登出",command=self.logout)
        #button.grid(row=2,columnspan=4)
        button.place(x=500, y=350, anchor=CENTER)
    def logout(self):
        global login_id
        login_id=0
        self.controller.show_frame("StartPage")

class gamepage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="選擇模式", font=TITLE_FONT)
        #label.grid(row=1,columnspan=4)
        label.place(x=400, y=250, anchor=CENTER)
        button = tk.Button(self, text="字母",command=self.next)
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="單字",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=350, anchor=CENTER)


        button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=500, y=400, anchor=CENTER)
    def next(self):
        self.controller.show_frame("letterpage")
        app.frames['letterpage'].run()


class person(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="選擇模式", font=TITLE_FONT)
        #label.grid(row=1,columnspan=4)
        label.place(x=400, y=250, anchor=CENTER)
        button = tk.Button(self, text="字母",command=self.show_preson)
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="單字",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=350, anchor=CENTER)

        button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=500, y=400, anchor=CENTER)
    def show_preson(self):
        person_record(login_id,1,app.frames['person_letter'].L)
        self.controller.show_frame("person_letter")

class person_letter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="字母，個人紀錄", font=TITLE_FONT)
        #label.grid(row=1,columnspan=4)
        label.place(x=400, y=100, anchor=CENTER)

        self.L=Listbox(self,width=50, height=20)
        self.L.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("person"))
        #button.grid(row=2,columnspan=4)
        button.place(x=600, y=500, anchor=CENTER)


class topten(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="排行榜，選擇模式", font=TITLE_FONT)
        #label.grid(row=1,columnspan=4)
        label.place(x=400, y=250, anchor=CENTER)
        button = tk.Button(self, text="字母",command=self.topten_letter)
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="單字",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=400, y=350, anchor=CENTER)

        button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("Menu"))
        #button.grid(row=2,columnspan=4)
        button.place(x=500, y=400, anchor=CENTER)
    def topten_letter(self):
        top_record(1,app.frames['topten_letter'].L)
        self.controller.show_frame("topten_letter")

class topten_letter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="排行榜-字母", font=TITLE_FONT)
        #label.grid(row=1,columnspan=4)
        label.place(x=400, y=100, anchor=CENTER)

        self.L=Listbox(self,width=50, height=20)
        self.L.place(x=400, y=300, anchor=CENTER)

        button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("topten"))
        #button.grid(row=2,columnspan=4)
        button.place(x=600, y=500, anchor=CENTER)


class letterpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 
        #button = tk.Button(self, text="上一頁",command=lambda:controller.show_frame("gamepage"))
        #button.grid(row=2,columnspan=4)
        #button.place(x=600, y=500, anchor=CENTER)
    def run(self):
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        if sys.platform == "windows":
            os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygame=pygame
        self.pygame.init()
        self.display=self.pygame.display
        self.screen = self.pygame.display.set_mode((800, 600))
        self.clock=self.pygame.time.Clock()
        self.bg = self.pygame.image.load("img/bg.jpg")
        self.top = self.pygame.image.load("img/top.png")
        self.pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 2**12) 
        self.boom_sound = pygame.mixer.Sound("sound/boom.wav")
        self.shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
        self.music=self.pygame.mixer.music
        self.music.load("sound/bgm.mp3")
        self.music.set_volume(0.3)
        my_event = self.pygame.event.Event(MOUSEBUTTONDOWN, button=1,pos=(500,500))
        self.pygame.event.post(my_event)
        grade=0
        message= "Grade:{}".format(grade)
        self.font = pygame.font.SysFont('Comic Sans MS', 50)
        self.text = self.font.render(message, True, red)
        self.music.play(-1)

        grade=0
        heart=3
        balls=list([ball() for count in xrange(5)])
        print balls
        addball=0
        FPS=10

        while True and heart>0:
            my_event = self.pygame.event.Event(MOUSEBUTTONDOWN, button=1,pos=(500,500))
            self.pygame.event.post(my_event)
            message= "Grade:{}".format(grade)
            self.text = self.font.render(message, True, red)
            heartimg=pygame.image.load("img/{}heart.png".format(heart))
            #message2= "Heart:{}".format(heart)
            #text2 = font.render(message2, True, red)
            for event in self.pygame.event.get():
                print event
                if event.type == QUIT:
                    self.pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pygame.quit()
                        exit()
                    same=0
                    for balloon in balls:
                        if balloon.letter==self.pygame.key.name(event.key):
                            self.shoot_sound.play()
                            grade+=1
                            addball+=1
                            balloon.__init__()
                            #del balls[balls.index(balloon)] 
                            #balls.append(ball())
                            same +=1
                    if same==0:
                        heart-=1
                        self.boom_sound.play()

            #screen.fill(white)
            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.top, (0,0))
            self.screen.blit(self.text, (0, size[1]-self.text.get_height()))
            self.screen.blit(heartimg, (size[0]-heartimg.get_rect().size[0], size[1]-heartimg.get_rect().size[1]))
            #screen.blit(text2, (size[0]-text2.get_width(), size[1]-text2.get_height()))
            for balloon in balls:
                if balloon.y <= 10:
                    heart-=1
                    if heart==0:
                        break
                    self.boom_sound.play()
                    balloon.__init__()
                else:
                    balloon.draw(self)
                    balloon.y-=10
            if addball>20:
                balls.append(ball())
                FPS+=5
                addball=0

            self.clock.tick(FPS)
            self.display.update()
        heartimg=pygame.image.load("img/{}heart.png".format(heart))
        self.screen.blit(heartimg, (size[0]-heartimg.get_rect().size[0], size[1]-heartimg.get_rect().size[1]))
        self.display.update()
        record_insert(login_id,grade,1)
        self.gameover()
    def gameover(self):
        while True:
            self.music.stop()
            self.screen.blit(self.text, ((size[0]-self.text.get_width())/2, (size[1]-self.text.get_height())/2))
            gameover_message="gameover press C to try again!"
            gameover_text = self.font.render(gameover_message, True, white)
            self.screen.blit(gameover_text, ((size[0]-gameover_text.get_width())/2, (size[1]-gameover_text.get_height())/2+50))
            self.display.update()
            for event in self.pygame.event.get():
                #print event
                if event.type == QUIT:
                    self.pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    if event.key == K_c:
                        self.run()
                    if event.key == K_q:
                        self.pygame.quit()
                        self.controller.show_frame("gamepage")


class ball:
    def __init__(self):
        font = pygame.font.SysFont('Comic Sans MS', 60)
        self.letter=random.choice(letters)
        self.text = font.render(self.letter, True, black)
        img="img/{}".format(random.choice(imgs))
        self.img= pygame.image.load(img)
        self.x=random.randint(0,size[0]-self.img.get_rect().size[0])
        self.y=random.randint(size[1],size[1]+150)
    def draw(self,frame):
        #w,h=self.img.size
        frame.screen.blit(self.img, (self.x, self.y))
        frame.screen.blit(self.text, (self.x+(self.img.get_rect().size[0]-self.text.get_width())/2,\
                             self.y+self.img.get_rect().size[1]/5))



login_id=0

if __name__ == "__main__":
    app = SampleApp()
    app.title("Entype")
    app.resizable(0,0)
    app.geometry("800x600")
    app.mainloop()
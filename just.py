import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from keras.models import load_model
import pygame, sys
from pygame.locals import *
from gtts import gTTS
import os
from pygame import mixer
mixer.init()
language = 'en'
r = tk.Tk()
r.geometry('500x600')
li3 = []

def add():
    str = "".join(li3)
    myobj = gTTS(text=str, lang=language, slow=False)
    myobj.save(str+".mp3")
    pygame.mixer.music.load(str+".mp3")
    mixer.music.play()
    
def remove():
    files = os.listdir(r"C:\Users\91883\OneDrive\Documents\GitHub\APLHA_NUM")
    for f in files:
        if not os.path.isdir(f) and ".mp3" in f:
            os.remove(f)
  
def display1():
    win_size_x = 1000
    win_size_y = 500
    BOUNDARY = 4
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    IMAGESAVE = False
    model = load_model('model_hand.h5')
# Dictionary for getting characters from index values...
    word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}

#initialize our pygame
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((win_size_x, win_size_y), pygame.RESIZABLE)
    FONT = pygame.font.Font("freesansbold.ttf", 24)
    FONT1 = pygame.font.Font("freesansbold.ttf", 24)


    pygame.display.set_caption("                   Welcome to computeried recognition of handwriting")

    image = pygame.image.load('th.jfif')
    img_count = 1
    iswriting = False
    PRIDICT = True
    num_x_cord = []
    num_y_cord = []

    text = FONT1.render('*      PROJECT EXHIBITION 2    *', True, green, blue)
    text1 = FONT1.render('* Project has successfully run  *', True, green, blue)
    text2 = FONT1.render('* * * * * * * * * * * * * * * * * * * * * * * *', True, green, blue)
 
# create a rectangular object for the
# text surface object
 
# set the center of the rectangular objec
    while True:
        DISPLAYSURF.blit(text2, (500,10))
        DISPLAYSURF.blit(text, (500,30))
        DISPLAYSURF.blit(text1, (500,50))
        DISPLAYSURF.blit(text2, (500,75))

        DISPLAYSURF.blit(image, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                mixer.quit()
                remove()
                pygame.quit()
            if event.type == KEYDOWN:
                    if event.key == K_a:
                        add()
                        li3.clear()
                    if event.key == K_SPACE:
                        li3.append(" ")
            if event.type == MOUSEMOTION and iswriting:
                x_cord, y_cord = event.pos
                pygame.draw.circle(DISPLAYSURF, WHITE, (x_cord, y_cord), 4, 0)
                num_x_cord.append(x_cord)
                num_y_cord.append(y_cord)
            if event.type == MOUSEBUTTONDOWN:
                iswriting = True
        
            if event.type == MOUSEBUTTONUP:
                iswriting = False
                num_x_cord = sorted(num_x_cord)
                num_y_cord = sorted(num_y_cord)

                rect_min_x, rect_max_x = max(num_x_cord[0]-BOUNDARY, 0), min(win_size_x, num_x_cord[-1]+BOUNDARY)
                rect_min_y, rect_max_y = max(num_y_cord[0]-BOUNDARY, 0), min(num_y_cord[-1]+BOUNDARY, win_size_y)

                num_x_cord = []
                num_y_cord = []

                img_array = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

                if IMAGESAVE:
                    cv2.imwrite("image.png")
                    img_count +=1
            
                if PRIDICT:
                    try:
                        img = cv2.resize(img_array, (28,28))
                        img = np.pad(img, (10,10), 'constant', constant_values=0)
                        img = cv2.resize(img, (28,28))/255
                    except:
                        print("error denied")

                    lable = str(word_dict[np.argmax(model.predict(img.reshape(1,28,28,1)))])
                    myobj = gTTS(text=lable, lang=language, slow=False)
                    li3.append(lable)
                    textSurface = FONT.render(lable, True, RED, WHITE)
                    textRecobj = textSurface.get_rect()
                    textRecobj.right, textRecobj.bottom = rect_min_x, rect_max_y

                    DISPLAYSURF.blit(textSurface, textRecobj)
            
                if event.type == KEYDOWN:
                    if event.unicode == "n":
                        DISPLAYSURF.fill(BLACK)
            pygame.display.update()
    
def display():

    win_size_x = 1000
    win_size_y = 500

    BOUNDARY = 4
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED = (255,0,0)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    IMAGESAVE = False
    MODEL = load_model('bestmodel.h5')
    LABLES = {0:"Zero", 1:"One", 2:"Two", 3:"Three", 4:"Four", 
              5:"five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine"}

#initialize our pygame
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((win_size_x, win_size_y), pygame.RESIZABLE)
    FONT = pygame.font.Font("freesansbold.ttf", 18)
    FONT1 = pygame.font.Font("freesansbold.ttf", 24)

    pygame.display.set_caption("                   Welcome to computeried recognition of handwriting")

    image = pygame.image.load('th.jfif')
    img_count = 1
    iswriting = False
    PRIDICT = True
    num_x_cord = []
    num_y_cord = []

    text = FONT1.render('*      PROJECT EXHIBITION 2    *', True, green, blue)
    text1 = FONT1.render('* Project has successfully run  *', True, green, blue)
    text2 = FONT1.render('* * * * * * * * * * * * * * * * * * * * * * * *', True, green, blue)
 
# create a rectangular object for the
# text surface object
 
# set the center of the rectangular objec
    while True:
        DISPLAYSURF.blit(text2, (500,10))
        DISPLAYSURF.blit(text, (500,30))
        DISPLAYSURF.blit(text1, (500,50))
        DISPLAYSURF.blit(text2, (500,75))

        DISPLAYSURF.blit(image, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                mixer.quit()
                remove()
                pygame.quit()
            if event.type == MOUSEMOTION and iswriting:
                x_cord, y_cord = event.pos
                pygame.draw.circle(DISPLAYSURF, WHITE, (x_cord, y_cord), 4, 0)
                num_x_cord.append(x_cord)
                num_y_cord.append(y_cord)
            if event.type == MOUSEBUTTONDOWN:
                iswriting = True
        
            if event.type == MOUSEBUTTONUP:
                iswriting = False
                num_x_cord = sorted(num_x_cord)
                num_y_cord = sorted(num_y_cord)

                rect_min_x, rect_max_x = max(num_x_cord[0]-BOUNDARY, 0), min(win_size_x, num_x_cord[-1]+BOUNDARY)
                rect_min_y, rect_max_y = max(num_y_cord[0]-BOUNDARY, 0), min(num_y_cord[-1]+BOUNDARY, win_size_y)

                num_x_cord = []
                num_y_cord = []

                img_array = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)

                if IMAGESAVE:
                    cv2.imwrite("image.png")
                    img_count +=1
            
                if PRIDICT:
                    try:
                        img = cv2.resize(img_array, (28,28))
                        img = np.pad(img, (10,10), 'constant', constant_values=0)
                        img = cv2.resize(img, (28,28))/255
                    except:
                        print("error denied")

                    lable = str(LABLES[np.argmax(MODEL.predict(img.reshape(1,28,28,1)))])
                    textSurface = FONT.render(lable, True, RED, WHITE)
                    myobj = gTTS(text=lable, lang=language, slow=False)
                    myobj.save(lable+".mp3")
                    pygame.mixer.music.load(lable+".mp3")
                    mixer.music.play()
                    textRecobj = textSurface.get_rect()
                    textRecobj.right, textRecobj.bottom = rect_min_x, rect_max_y

                    DISPLAYSURF.blit(textSurface, textRecobj)

                if event.type == KEYDOWN:
                    if event.unicode == "n":
                        DISPLAYSURF.fill(BLACK)

            pygame.display.update()
btn = Button(r, text ='char recognition', command = display1).pack()
btn = Button(r, text ='digit recognition', command = display).pack()
r.mainloop()
from random import randint
import cv2
import numpy as np
import math
cap=cv2.VideoCapture(0)

cv2.startWindowThread()
cv2.namedWindow('result',cv2.WINDOW_NORMAL)
cv2.namedWindow('comp',cv2.WINDOW_NORMAL)
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.namedWindow('human_score',cv2.WINDOW_NORMAL)
cv2.namedWindow('computer_score',cv2.WINDOW_NORMAL)



vs=cv2.imread('vs.jpg')
win=cv2.imread('win.jpg')
lose=cv2.imread('loose.png')
tie=cv2.imread('tie.png')
rock=cv2.imread('rock.jpg')
paper=cv2.imread('paper.jpg')
scissors=cv2.imread('scissors.png')
zero=cv2.imread('zero.jpg')
one=cv2.imread('1.jpg')
two=cv2.imread('2.jpg')
victory=cv2.imread('victory.jpg')
over=cv2.imread('over.png')
gameload=1
gamestart=1
scoring=0
com=0
human=0







def results(p,c):
    if p is "Rock":
        if c is "Rock":
            cv2.imshow('comp',rock)
            cv2.imshow('result',tie)
        elif c is "Paper":
            cv2.imshow('comp',paper)
            cv2.imshow('result',lose)
            currentscorecom()
        elif c is "Scissors":
            cv2.imshow('comp',scissors)
            cv2.imshow('result',win)
            currentscorehuman()
    elif p is "Paper":
         if c is "Rock":
            cv2.imshow('comp',rock)
            cv2.imshow('result',win)
            currentscorehuman()
         elif c is "Paper":
            cv2.imshow('comp',paper)
            cv2.imshow('result',tie)
         elif c is "Scissors":
            cv2.imshow('comp',scissors)
            cv2.imshow('result',lose)
            currentscorecom()
    elif p is "Scissors":
        if c is "Rock":
            cv2.imshow('comp',rock)
            cv2.imshow('result',lose)
            currentscorecom()
        elif c is "Paper":
            cv2.imshow('comp',paper)
            cv2.imshow('result',win)
            currentscorehuman()
        elif c is "Scissors":
            cv2.imshow('comp',scissors)
            cv2.imshow('result',tie)








def currentscorecom():
    global com
    global gamestart
    com=com+1
    if com is 1:
        cv2.imshow('computer_score',one)
    elif com is 2:
         cv2.imshow('computer_score',two)
    elif com > 2:
         cv2.imshow('computer_score',over)
         cv2.imshow('human_score',over)
         gamestart=2
    return com






def currentscorehuman():
    global human
    global gamestart
    human=human+1
    if human is 1:
        cv2.imshow('human_score',one)
    elif human is 2:
         cv2.imshow('human_score',two)
    elif human > 2:
         cv2.imshow('computer_score',victory)
         cv2.imshow('human_score',victory)
         gamestart=2
    return human




while(gameload==1):
    while(gamestart==1):
        t=["Rock","Paper","Scissors"]
        computer=t[randint(0,2)]
        if(scoring == 0):
          cv2.imshow('computer_score',zero)
          cv2.imshow('human_score',zero)
          scoring=1
        cv2.imshow('result',vs)


        _,feed=cap.read()
        cv2.rectangle(feed,(50,100),(300,400),(0,255,0),0)
        image=feed[100:400,50:300]
        #image=cv2.imread('C:\Users\Admin\Desktop\hand.jpg')
        img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(img,(35,35),0)
        ret,thresh = cv2.threshold(blur,0,255,1+cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh,1,1)
        max_area=0
        pos=0
        for i in contours:
            area=cv2.contourArea(i)
            if area>max_area:
                max_area=area
                pos=i
        peri=cv2.arcLength(pos,True)
        approx=cv2.approxPolyDP(pos,0.02*peri,True)
        hull=cv2.convexHull(pos)
        #print len(hull)
        #cv2.polylines(image,[approx],True,(0,255,255))
        #cv2.drawContours(image,[approx],-1,(255,100,50),2)
        cv2.drawContours(image,[hull],-1,(0,0,255),2)
        hull = cv2.convexHull(pos,returnPoints = False)
        defects = cv2.convexityDefects(pos,hull)
        num=0
        l=defects.shape[0]
        for i in range(1,defects.shape[0]):
            s,e,f,d = defects[i,0]
            far = tuple(pos[f][0])
            if d>10000:
                num+=1
                cv2.circle(image,far,3,[0,0,255],-1)
        num+=1;
        if num==2:
            s='Scissors'
            results(s,computer)
            print (s)
            cv2.waitKey(0)

        elif num==5:
            s='PAPER'
            results(s,computer)
            print (s)
            cv2.waitKey(0)
        else:
            s='ROCK'
            results(s,computer)
            print (s)
            cv2.waitKey(0)
        feed[100:400,50:300]=image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(feed,s,(100,450), font, 2,(255,10,10),2,cv2.LINE_AA)

        #cv2.imshow('image',thresh)
        k=cv2.waitKey(10)

    cv2.destroyAllWindows()

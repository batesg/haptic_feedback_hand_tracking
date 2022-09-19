#from asyncore import read
#from re import X
#from tkinter import WORD, Y
import serial 
#import csv
#from io import StringIO
#import numpy as np
#import pandas as pd
import time

from module import findnameoflandmark, findpostion, speak

import cv2
import mediapipe as mp

cap = cv2.VideoCapture(1) #change to 1 for exsternal camera, 0 for on mac camera
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

global iteration
global ser
global message 
global split 
global counter
counter = 0
split = ["X", "0", "Y", "0"]

ser = serial.Serial(
        port='/dev/cu.usbmodem11302',\ # mbed serial, change to correct port
        baudrate=9600)#,\
        #parity=serial.PARITY_NONE,\
        #stopbits=serial.STOPBITS_ONE,\
        #bytesize=serial.EIGHTBITS,\
            #timeout=0)

ser2 = serial.Serial(
        port='/dev/cu.usbmodem11201',\ # arduino serial, change to port
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
# need to add check to make sure in right format, crashes if reads trip in position of motor position. re run and normaly works 2nd time
def read_CV():
    global x_val
    global y_val
    global trip_mot1
    global trip_mot2

    word = ""
    iteration = 0
    while True:
        for line in ser.read():
            if (chr(line) == "#"):
                word = word 
                print("the msg: ", word)

                split = word.split(",")
                trip_mot1 = split[0]
                trip_mot2 = split[1]
                x_val = int(split[3])
                y_val = int(split[5])
                print("mot 1 trip: ", trip_mot1)
                print("mot 2 trip: ", trip_mot2)
                print("split X: ", x_val)       
                print("split Y: ", y_val)                                      

                word = ''
                iteration = 1

            else:
                word = word + chr(line)
            if (iteration == 1):
                return
    ser.close()

def move_hand():
    print("starting ")
    global x_reverse
    global y_reverse
    global x_max
    global y_max

    ser.write("B".encode()) # anti clockwise x axis
    #ser.write("Y".encode()) # anti clockwise y axis

    x_reverse = 0
    y_reverse = 0
    x_homed = 0
    y_homed =0
    while True:
        time.sleep(0.1)
        read_CV()
        
        print(trip_mot1, x_val , y_val)
        if (trip_mot1 == 'R'):      # change to when button pressed
            ser.write("AD".encode())    # reverse and clear numbers
            print("rev")
            #x_reverse =1
        
        #if (trip_mot2 == 'R'):      # change to when button pressed
        #    ser.write("XK".encode())     # reverse and clear numbers
        #    y_reverse =1

        if (trip_mot1 == 'L'):      # change to when button pressed
            ser.write("C".encode())    # stop
            x_max = x_val
            print("x homed at: ", x_val)
            x_homed = 1
        
        #if (trip_mot2 == 'L'):      # change to when button pressed
        #    ser.write("Z".encode())     # stop
        #    print("y homed at: ", y_val)
        #    y_max = y_val
        #    y_homed = 1

        if (#(y_homed == 1) and 
        (x_homed == 1)):
            return

def hand_tracking():
    print("hand tracking begin")
    # type control+c to kill
    global cx
    global cy
    global cz

    global x_screen
    global y_screen

    thumb_servo = 90
    index_servo = 90
    middle_servo = 90

    # Use CV2 Functionality to create a Video stream and add some values + variables
    tip = [8, 12, 16, 20]
    tipname = [8, 12, 16, 20]
    fingers = []
    finger = []
    x_screen = 640
    y_screen = 360

    while True:
        # data to send to close the fingers 
        sending_data = str(thumb_servo) + "," + str(index_servo) + "," + str(middle_servo) + ",,,"
        serial_print(sending_data)
        read_CV()
        #ret, frame = cap.read()
        success, image = cap.read()

        image = cv2.resize(image, (x_screen, y_screen))
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)

        a = findpostion(image)
        b = findnameoflandmark(image)

        # checking whether a hand is detected
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    #print("ID: ", id,lm)
                    h, w, c = image.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    
                    #print("pos: ", cx, cy, cz)
                    if id ==9:
                        cz = float(lm.z)
                        cv2.circle(image, (cx,cy), 10, (255,0,255), cv2.FILLED)
                        print("pos: ", cx, cy, cz)
            if len(b and a) != 0:
                finger = []
                if a[0][1:] > a[4][1:]: # struggles to read the thumb pose, can change to be tip is right of base point, would give better response imo.
                    finger.append(1)
                    print (b[4])
                    thumb_servo = 130

                else:
                    finger.append(0)
                    thumb_servo = 90

                fingers = []
                for id in range(0, 3):
                    if a[tip[id]][2:] > a[tip[id]-2][2:]:
                        print(b[tipname[id]])
                        fingers.append(1)
                        if (id == 0):
                            index_servo = 140
                        if (id == 1):
                            middle_servo = 140
                        #if (id == 2):
                            #thumb_servo = 150
                            
                    else:
                        fingers.append(0)
                        if (id == 0):
                            index_servo = 90
                        if (id == 1):
                            middle_servo = 90
                        #if (id == 2):
                            #thumb_servo = 90

                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
                follow_hand()

            cv2.putText(image,str(cx), (10,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 3)
            cv2.putText(image,str(cy), (110,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 3)
            cv2.putText(image,str(cz), (210,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 3)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
        else:
            ser.write("C".encode())

        cv2.imshow("Output", image)
        cv2.waitKey(1)

def follow_hand():
    global x_scaler
    global y_scaler
    global x_val_scaled
    global y_val_scaled

    y_max = y_screen
    y_val = cy
    y_val_scaled = (y_max/ y_screen)
    x_scaler = (x_max / x_screen)
    

    read_CV()

    x_val_scaled = cx * x_scaler
    print("x scaled: ", x_val_scaled)
    print("x values: ", x_val)
    #y_val_scaled = cy * y_scaler
    #print("y scaled: ", y_val_scaled)

    if not ((x_max >= x_screen) or (x_max <= 0)):
        if (x_val >= (x_val_scaled + 6)):
            ser.write("B".encode())
            print("left")

        if (x_val <= (x_val_scaled - 6)):
            ser.write("A".encode())
            print("right")
        
        if (x_val <= (x_val_scaled + 6) and x_val >= (x_val_scaled - 6)):
            ser.write("C".encode())  
            print("stop")
    
    #if not ((y_max >= y_screen) or (y_max <= 0)):
        #if (y_val >= (y_val_scaled + 4)):
            #ser.write("X".encode())

        #if (y_val <= (y_val_scaled -4)):
        #    ser.write("Y".encode())
        
        #else:
        #    ser.write("Z".encode())
    #if(cy >= 190):
    #    ser.write("X".encode())
    #if(cy <= 170):
    #    ser.write("Y".encode())
    #if ((cy <= 190) and (cy >= 170)):
    #        ser.write("Z".encode())

    return 
def serial_print(sending_data):
    print("finger pos data")
    global counter
    print(sending_data)
    print(counter)
    if (counter >= 3): # slow down data sending rate
        ser2.write(sending_data.encode())
        print("finger pos data sent")
        counter = 0
    else:
        counter = counter +1
    #time.sleep(0.2)
    return



if __name__ == '__main__':
    #read_CV() 
    answer = input("ready to start: [Y/n]")
    print(answer)
    if(answer == 'Y'):
        move_hand()
        hand_tracking()

#####################################################################
# author: Stephen Hall, Johnnie Ellis
# date: Due 10/25/2023
# description: A camera feed that uses the opencv and deepface databases to track facial expressions and activate LEDs corresponding with the emotions.
#####################################################################
#Angry Disgust Fear Happy Sad Surprise Neutral
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from deepface import DeepFace
import RPi.GPIO as GPIO


GPIO.setmode (GPIO.BCM)

# Left to Right pin number setup
LEDpin1= 6
LEDpin2 = 13
LEDpin3 = 19
LEDpin4 = 21
LEDpin5 = 24 and 25 

GPIO.setup (LEDpin1, GPIO.OUT)
GPIO.setup (LEDpin2, GPIO.OUT)
GPIO.setup (LEDpin3, GPIO.OUT)
GPIO.setup (LEDpin4, GPIO.OUT)
GPIO.setup (LEDpin5, GPIO.OUT)


def expression_tracking():
    #initializes a facial detection algorithm that comes with opencv
    fc = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0) #We are setting the capture to 0 because that is the default camera
    #When this system is put on a pi kit we will change this camera to be whatever it needs

    while cap.isOpened():
        _,frame = cap.read()

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #set the frame to grayscale for easier tracking
        face=fc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5) #quality control for face detection

        for x,y,w,h in face:
            img=cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1) #draw rectangle around face
            try:
                result = DeepFace.analyze(frame, actions=['emotion'])
                print(result[0]["dominant_emotion"])
                light_option = (result[0]["dominant_emotion"])
            except:
                print("No face found.")

            if light_option == "Sad":       #If an emotion matches condition it lights the corresponding LED
                GPIO.output(LEDpin1, True)    #and shuts off the other ones
                GPIO.output(LEDpin2, False)
                GPIO.output(LEDpin3, False)
                GPIO.output(LEDpin4, False)
                GPIO.output(LEDpin5, False)
            elif light_option == "Disgust" or "Angry":
                GPIO.output(LEDpin1, False)
                GPIO.output(LEDpin2, True)
                GPIO.output(LEDpin3, False)
                GPIO.output(LEDpin4, False)
                GPIO.output(LEDpin5, False)
            elif light_option == "Happy":
                GPIO.output(LEDpin1, False)
                GPIO.output(LEDpin2, False)
                GPIO.output(LEDpin3, True)
                GPIO.output(LEDpin4, False)
                GPIO.output(LEDpin5, False)
            elif light_option == "Fear" or "Surprise":
                GPIO.output(LEDpin1, False)
                GPIO.output(LEDpin2, False)
                GPIO.output(LEDpin3, False)
                GPIO.output(LEDpin4, True)
                GPIO.output(LEDpin5, False)
            elif light_option == "Neutral":
                GPIO.output(LEDpin1, False)
                GPIO.output(LEDpin2, False)
                GPIO.output(LEDpin3, False)
                GPIO.output(LEDpin4, False)
                GPIO.output(LEDpin5, True)
 

        cv2.imshow("video", frame) #set up gui camera frame
        key=cv2.waitKey(1)
        if key==ord("q"): #turn the program off when q is pressed
            break
    cap.release()
    GPIO.cleanup()

expression_tracking()
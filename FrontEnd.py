#####################################################################
# author: Stephen Hall, Johnnie Ellis
# date: Due 10/25/2023
# description: A GUI displaying a camera feed using the opencv library 
#####################################################################
import cv2
import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Webcam Feed")

# Creates the label for the camera to be in
label = tk.Label(window)
label.pack()

cap = cv2.VideoCapture(0) #We are setting the capture to 0 because that is the default camera
#When this system is put on a pi kit we will change this camera to be whatever it needs


def show_frame(): #This whole function displays the video feed in the GUI

    ret, frame = cap.read() #gets the next frame from the camera
    if ret: #if an image is received...
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #converts the frame into a cv2 image
        img = Image.fromarray(cv2image) #converts cv2 image into a generic image
        imgtk = ImageTk.PhotoImage(image=img) #converts generic image into a tk image
        label.imgtk = imgtk #sets the image of the UI label to a tk image
        label.configure(image=imgtk) #have the label show the updated image
        window.after(10, show_frame) #call show_frame() again in 10 milliseconds

show_frame()
window.mainloop() #when out of prototype, turn this part into a separate file ig

#The command to run in the console is: python .\FrontEnd.py
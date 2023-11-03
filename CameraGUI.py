#####################################################################
# author: Stephen Hall, Johnnie Ellis
# date: Due 10/25/2023
# description: A camera feed that uses the opencv and deepface databases to track facial expressions and activate LEDs corresponding with the emotions.
#####################################################################
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from deepface import DeepFace

# initializes a facial detection algorithm that comes with OpenCV
fc = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)  # Set the capture to 0 because that is the default camera

# Create a Tkinter window
root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())  # Press 'Esc' to quit

# Create a label for the video frame
video_label = tk.Label(root, width=900, height=720)  # Adjust the width and height as needed
video_label.pack(side=tk.LEFT)

# Create a label for the print statements
print_label = tk.Label(root, text="", anchor="w", justify="left", font=("Arial", 20), padx=250, pady=20)  
print_label.pack(side=tk.RIGHT, fill=tk.Y)

while cap.isOpened():
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Set the frame to grayscale for easier tracking
    face = fc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)  # Quality control for face detection

    for x, y, w, h in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)  # Draw a rectangle around the face
        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            emotion = result[0]["dominant_emotion"]
            print(emotion)
            print_label.config(text=f"Emotion: {emotion}")  # Update the print label with the emotion
        except:
            print_label.config(text="No face found.")

    # Display the video frame in the GUI
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB for displaying in Tkinter
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.config(image=imgtk)

    # Update the GUI
    root.update()

    key = cv2.waitKey(1)
    if key == ord("q"):  # Turn the program off when 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()
root.destroy()
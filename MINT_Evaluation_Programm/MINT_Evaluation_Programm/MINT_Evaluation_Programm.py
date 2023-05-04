#!/usr/bin/env python
from types import NoneType
from fer import FER
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

def main():
    App(tk.Tk(), "MINT Test Session")


class Face:
    def __init__(self):        
        # create a FER object
        self._detector = FER()

    def detector(self):
        return self._detector


class App:
    def __init__(self, window, window_title):

        # Initialize main window
        self.window = window
        self.window.title(window_title)
        self.window.attributes("-fullscreen",True)
        self.window.configure(bg="#98FB98") 
        self.window.rowconfigure(0, weight=1)

        # initialize detector for faces and emotions + width of textbox
        self._rect_width = 400
        self._face = Face()
        
        # Initialize Videostreams
        self.cap = cv2.VideoCapture(0)

        # Create a gradient background
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.create_gradient_background(width, height)

        # Create Buttons
        self.create_button()

        # Create a frame to hold the camera video stream canvas, but it is invisible at the beginning
        self.bottom_frame = tk.Frame(self.window, bg="#ffffff", height=height//2, width=width)
        self.camera_canvas = tk.Canvas(self.bottom_frame, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)+self.rect_width(), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),bg="#ffffff")

        self.delay = 15 # millisecondsd
        self.update()

        self.window.mainloop()
        
    def update(self):
        self.videostream_to_tk_display(self.cap, self.camera_canvas)
        self.window.after(self.delay, self.update)

    def start_demo(self):
        self.start_button.grid_forget()
        self.bottom_frame.grid(column=0, row=0, rowspan=2)
        self.camera_canvas.pack()

    def videostream_to_tk_display(self, stream, canvas, emotion_classification = True):
        ret, frame = stream.read()

        if ret:
            if emotion_classification:
                frame = self.classify_emotion(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

    def classify_emotion(self, frame):
         # get the height and width of the original image
        height, width, channels = frame.shape
        # create a new image with the same height and a larger width
        new_width = width + self.rect_width()
        new_frame = np.zeros((height, new_width, channels), dtype=np.uint8)
        
        # copy the original image onto the left side of the new image
        new_frame[:, :width, :] = frame

        # draw the black rectangle on the right side of the new image
        new_frame[:, width:, :] = (0, 0, 0)
        # detect faces in the frame
        faces = self.face().detector().detect_emotions(new_frame)
        dominant_emotion = self.face().detector().top_emotion(new_frame)
        if type(dominant_emotion[0]) != NoneType:
            dominant_emotion = "Dominant emotion:  " + dominant_emotion[0]
        i = 0
        # loop through the faces
        for face in faces:
            
            if len(faces)==0:
                break
            x, y, w, h = face["box"]

            # draw a rectangle around the face
            cv2.rectangle(new_frame, (x, y), (x + w, y + h), (137, 180, 62), 2)

            # get the emotions from the face
            emotions = face["emotions"]

            for j, (emotion, score) in enumerate(emotions.items()):
                text = f"{emotion}: {score:.2f}"
                cv2.putText(new_frame, text, (width+10, i + (j + 1) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(new_frame, dominant_emotion, (width+10, i+(j + 2) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            i = i + (j + 2) * 20
        return new_frame

    # Create Widges

    def create_button(self):
        self.start_button = tk.Button(self.window, command=self.start_demo, bg="black", fg="white", text="Start Demo", highlightcolor="darkgrey", padx=20, pady=20)
        self.start_button.grid(column=0, row=0, rowspan=2)

    def create_gradient_background(self, width, height):
        gradient = tk.Canvas(self.window, width=width, height=height)
        gradient.grid(column=0, row=0, rowspan=2)
        for i in range(height):
            # Calculate the color values for each row of pixels
            r = int(255 - (i / height) * 255)
            g = int(255 - (i / height) * 255)
            b = int(255 - (i / height) * 255)
            color = f"#{r:02x}{g:02x}{b:02x}"
            gradient.create_rectangle(0, i, width, i+1, fill=color, outline="")
            
    # Getter and Setter
    
    def rect_width(self):
        return self._rect_width

    def face(self):
        return self._face






if __name__ == "__main__":
    main()

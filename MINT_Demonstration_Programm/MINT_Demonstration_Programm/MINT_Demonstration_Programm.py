#!/usr/bin/env python
from types import NoneType
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

def main():
    App(tk.Tk(), "MINT Test Session")



class App:
    def __init__(self, window, window_title):

        # Initialize main window
        self.window = window
        self.window.title(window_title)
        self.window.attributes("-fullscreen",True)
        self.window.configure(bg="#98FB98") 
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # initialize some flags and attributes
        self.flag_intro = True
        self.flag_start_demo = False

        self.load_content()

        self.delay = 5 # milliseconds
        self.update()

        self.window.mainloop()
        
    def load_content(self):
        # Initialize Videostreams
        self.introvideo = cv2.VideoCapture("./Intro_Video.mp4")


        # Create a gradient background
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.create_gradient_background(self.width, self.height)

        # Create Buttons
        self.create_start_button()

                 
        # Create a frame to hold the MINT video stream canvas, but it is invisible at the beginning
        self.demo_frame = tk.Frame(self.window, height=self.height//2, width=self.width//2)
        self.MINT_canvas = tk.Canvas(self.demo_frame, width=self.introvideo.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.introvideo.get(cv2.CAP_PROP_FRAME_HEIGHT),bg="#ffffff")
        self.button_frame = tk.Frame(self.window, height=self.height//12, width=self.width)

    def update(self):
        if self.flag_start_demo:
            if self.flag_intro:
                self.videostream_to_tk_display(self.introvideo, self.MINT_canvas)
            else:
                self.videostream_to_tk_display(self.evaluation_video, self.MINT_canvas)
        self.window.after(self.delay, self.update)

    def start_demo(self):
        self.start_button.grid_forget()
        self.flag_start_demo = True

        self.demo_frame.grid(column=0, row=0, rowspan=2, columnspan=2)
        self.MINT_canvas.pack(padx=75, pady=75)
        self.create_gender_button()
        self.button_frame.grid(row=1, column=0, columnspan=2)

    def start_evaluation(self, choice):
        self.male_button.pack_forget()
        self.female_button.pack_forget()
        self.create_cancel_button()
        if choice == "male":
            self.evaluation_video = cv2.VideoCapture("./Male.mp4")
        else:
            self.evaluation_video = cv2.VideoCapture("./Female.mp4")
        self.flag_intro= False

    def start_mainpage(self):
        self.flag_start_demo = False
        self.flag_intro = True
        self.cancel_button.grid_remove()
        self.demo_frame.grid_forget()
        self.load_content()

    def videostream_to_tk_display(self, stream, canvas, emotion_classification = False):
        ret, frame = stream.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width-200, self.height-200))
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

    
    # Create Widges
    
    def create_start_button(self):
        self.start_button = tk.Button(self.window, command=self.start_demo, bg="black", fg="white", text="Start Demo", highlightcolor="darkgrey", padx=20, pady=20)
        self.start_button.grid(column=0, row=0, rowspan=2)

    def create_cancel_button(self):
        self.cancel_button = tk.Button(self.window, command=self.start_mainpage, bg="black", fg="white", text="Cancel Demo", highlightcolor="darkgrey", padx=20, pady=20)
        self.cancel_button.grid(column=0, row=1)

    def create_gender_button(self):
        
        self.male_button = tk.Button(self.button_frame, command=lambda:self.start_evaluation("male"), bg="black", fg="white", text="Male AI", highlightcolor="darkgrey", padx=20, pady=20)
        self.male_button.pack(side="left")
        
        self.female_button = tk.Button(self.button_frame, command=lambda:self.start_evaluation("female"), bg="black", fg="white", text="Female AI", highlightcolor="darkgrey", padx=20, pady=20)
        self.female_button.pack(side="left")

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







if __name__ == "__main__":
    main()

"""
Logic for questions.
"""
import os.path

import random
import tkinter as tk

from PIL import Image, ImageTk, ImageFilter

VIDEO_FORMATS = ["mp4", "mov"]
AUDIO_FORMATS = ["mp3", "wav"]

class Question:
    """
    Class that describes questions.
    """
    def __init__(self, conf):
        self.played = False
        self.delay = 0
        self.question = conf[0]
        self.solution = conf[1]
        self.answers = conf[1:5]
        random.shuffle(self.answers)
        self.points = int(conf[5])
        if os.path.isfile(conf[6]):
            self.solution_file = conf[6]
            if not "mp3" in self.solution_file:
                self.images = []
        else:
            if conf[6]:
                print(f"Invalid path: {conf[6]}")
            self.solution_file = None

    def check_answer(self, a_nr):
        """
        Check if the answer was correct.
        """
        if self.answers[a_nr] == self.solution:
            return True
        return False

    def get_answer(self, parent):
        """
        Return the answer to the question.
        """
        if not self.solution_file:
            return
        if self.solution_file.split(".")[-1] in AUDIO_FORMATS:
            parent.player.play_audio(self.solution_file)
            return

        self.show_answer(parent)
        return

    def show_answer(self, parent):
        """
        Show the image to the result.
        """
        width = 1280
        height = 720
        canvas = tk.Canvas(width=width*parent.scale,
                           height=height*parent.scale, bg='black')
        canvas.place(x=int(parent.offset[0]+parent.scale*(1920-width)/2),
                     y=int(parent.offset[1]+parent.scale*200))
        width = int(1280*parent.scale)
        height = int(720*parent.scale)

        if self.solution_file.split(".")[-1] in VIDEO_FORMATS:
            parent.player.play_video(self.solution_file, canvas)
        else:
            try:
                img = Image.open(self.solution_file)
            except FileNotFoundError:
                self.delay = 2000

            im_width, im_height = img.size

            if im_width > width:
                scale = width/im_width
                img = img.resize((int(im_width*scale), int(im_height*scale)), Image.ANTIALIAS)
                im_width, im_height = img.size

            if im_height > height:
                scale = height/im_height
                img = img.resize((int(im_width*scale), int(im_height*scale)), Image.ANTIALIAS)

            blurred = ImageTk.PhotoImage(img.resize((width, height), Image.ANTIALIAS).filter(
                ImageFilter.GaussianBlur(radius=10)))
            self.images.append(blurred)
            canvas.create_image(0, 0, image=self.images[0], anchor=tk.NW)

            image = ImageTk.PhotoImage(img)
            self.images.append(image)

            canvas.create_image(int((width-image.width())/2), int((height-image.height())/2),
                                image=self.images[1], anchor=tk.NW)
            self.delay = 7000

        parent.window.after(2000, self.disable_canvas, parent, canvas)

    def disable_canvas(self, parent, canvas):
        """
        Disable canvas after video is played.
        """
        delay = max(self.delay, parent.player.delay)
        parent.window.after(delay, canvas.place_forget)

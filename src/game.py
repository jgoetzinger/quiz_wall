"""
Logic for game.
"""
import os
import sys
import csv
import tkinter as tk
from functools import partial

from PIL import Image, ImageTk

from src.player import Player
from src.scores import PointHandler
from src.questionboard import QuestionBoard
from src.question import Question
from src.questionscreen import QuestionScreen

__version__ = "1.0.0"

FONT = "comfortaa"

RESOLUTIONS = [(640, 360), (960, 540), (1280, 720), (1600, 900), (1920, 1080),
               (2048, 1152), (2560, 1440), (3200, 1800), (3840, 2160), (4096, 2304),
               (5120, 2880), (7680, 4320), (15360, 8640)]

class Framework:
    """
    Class that handles game layout.
    """
    def __init__(self):
        self.quiz = None
        self.scale = 1
        self.offset = (0, 0)
        geo = self.select_quiz()
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.bind("<Escape>", self.full_screeen)
        self.window.bind("<F11>", self.full_screeen)
        self.player = Player(self.window)

        self.game = Game(self)
        self.full_screeen_on = True
        self.setup_game(geo)

    def select_quiz(self):
        """
        Select the quiz and get screen resolution.
        """
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", partial(self.quit, root))
        root.update_idletasks()
        width, height = [int(f) for f in root.winfo_geometry().split("+")[0].split("x")]

        res = tk.Entry(root)
        res.insert(0, f"{width}x{height}")
        self.change_res(res, False)

        quizzes = [
            f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f)) \
            and f.split(".")[-1] == "csv"]

        img = Image.open("gameplay/hintergrund.jpg")
        img = ImageTk.PhotoImage(img.resize((int(1920*self.scale), int(1080*self.scale)),
                                            Image.ANTIALIAS))
        background_label = tk.Label(root, image=img, bg="black")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        root.iconphoto(False, tk.PhotoImage(file="gameplay/icon.png"))

        res = tk.Entry(root)
        res.insert(0, f"{width}x{height}")
        x_pos = int(1800*self.scale)
        y_pos = int(1000*self.scale)
        res.place(x=x_pos, y=y_pos, width=int(100*self.scale), height=int(50*self.scale))
        action = partial(self.change_res, res)
        button = tk.Button(root, text="Change resolution", command=action)
        x_pos = int(1580*self.scale)
        y_pos = int(1000*self.scale)
        button.place(x=x_pos, y=y_pos, width=int(200*self.scale), height=int(50*self.scale))

        x_pos = int((width-1920*self.scale)/2 + 710*self.scale)
        y_pos = int((height-1080*self.scale)/2 +100*self.scale)
        title = tk.Text(root, highlightthickness=0, borderwidth=0)
        title.place(x=x_pos, y=y_pos, width=int(500*self.scale), height=int(80*self.scale))
        title.tag_configure("center", justify='center')
        title.insert(tk.END, "Select Quiz:")
        title.tag_add("center", "1.0", "end")
        title.config(font=self.get_font(), wrap=tk.WORD, fg="black")
        title.config(state="disabled")

        x_pos = int(0*self.scale)
        y_pos = int(1040*self.scale)
        version = tk.Text(root, highlightthickness=0, borderwidth=0)
        version.place(x=x_pos, y=y_pos, width=int(100*self.scale), height=int(40*self.scale))
        version.tag_configure("center", justify='center')
        version.insert(tk.END, "v" + __version__)
        version.tag_add("center", "1.0", "end")
        version.config(font=self.get_font(20), wrap=tk.WORD, fg="black")
        version.config(state="disabled")
        for i, quiz in enumerate(quizzes):
            action = partial(self.quit, root, None, quiz)
            button = tk.Button(root, text=quiz.split(".")[0], command=action)
            x_pos = int((width-1920*self.scale)/2 + 710*self.scale)
            y_pos = int((height-1080*self.scale)/2 + (200+i*100)*self.scale)
            button.place(x=x_pos, y=y_pos, width=int(500*self.scale), height=int(80*self.scale))

        root.mainloop()
        return f"{int(1920*self.scale)}x{int(1080*self.scale)}"

    def change_res(self, entry, change_color=True):
        """
        Change the resolution from user input.
        """
        text = entry.get()
        if "x" in text:
            width, height = [int(f) for f in text.split("x")]
            self.scale = get_resolution(width, height)
            self.offset = (int((width-1920*self.scale)/2), int((height-1080*self.scale)/2))
            if change_color:
                entry.config({"background": "#44ff00"})
        else:
            entry.config({"background": "#ff0000"})

    def quit(self, root=None, event=None, quiz=None):
        """
        Destroy window.
        """
        if event:
            sys.exit("No quiz choosen.")
        if quiz:
            self.quiz = quiz

        root.destroy()

    def get_font(self, size=40):
        """
        Get the scaled font.
        """
        return (FONT, int(size*self.scale))

    def full_screeen(self, _):
        """
        Toggle full screen mode.
        """
        self.full_screeen_on = not self.full_screeen_on
        self.window.attributes("-fullscreen", self.full_screeen_on)

    def setup_game(self, geo):
        """
        Initialize the game and setup some basic tkinter stuff.
        """
        self.window.title(self.quiz.split(".")[0])
        self.window.geometry(geo)
        img = Image.open("gameplay/hintergrund2.png")
        img = ImageTk.PhotoImage(img.resize((int(1920*self.scale), int(1080*self.scale)),
                                            Image.ANTIALIAS))
        background_label = tk.Label(self.window, image=img, bg="black")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        photo = tk.PhotoImage(file="gameplay/icon.png")
        self.window.iconphoto(False, photo)

        self.point_handler = PointHandler(self)
        self.question_board = QuestionBoard(self, self.game.questions)
        self.question_screen = QuestionScreen(self)

        self.title = tk.Text(self.window, highlightthickness=0, borderwidth=0)
        self.title.place(x=self.offset[0]+int(418*self.scale), y=self.offset[1]+int(40*self.scale),
                         width=int(1140*self.scale), height=int(80*self.scale))
        self.title.tag_configure("center", justify='center')
        self.title.insert(tk.END, self.quiz.split(".")[0])
        self.title.tag_add("center", "1.0", "end")
        self.title.config(font=self.get_font(), wrap=tk.WORD, fg="blue")
        self.title.config(state="disabled")

        self.window.mainloop()


class Game:
    """
    Class that contains game logic.
    """
    def __init__(self, framework):
        self.players = {"blue": 0,
                        "red": 0}
        self.team_blues_turn = True
        self.current_question = None
        self.framework = framework
        self.questions = create_questions(self.framework.quiz)

    def ask_question(self, num, points, i):
        """
        Setup a question to ask.
        """
        self.current_question = num
        question = self.questions[points][i]
        if question.played:
            return

        self.framework.question_board.hide_buttons()
        if self.team_blues_turn:
            active_team = "blue"
        else:
            active_team = "red"
        self.framework.question_screen.set_elements(question, active_team)
        self.framework.question_screen.enable_elements()

    def question_answered(self, player, answ_question):
        """
        Logic to handle what happens when a question was answerded.
        """
        self.team_blues_turn = not self.team_blues_turn

        if self.team_blues_turn:
            self.framework.title.config(fg="blue")

        else:
            self.framework.title.config(fg="red")

        self.players[player] += answ_question.points
        self.framework.point_handler.set_points()
        self.framework.question_board.set_button_color(player)
        self.framework.question_screen.disable_elements()
        self.framework.question_board.show_buttons()
        finished = True
        for points in self.questions:
            for question in self.questions[points]:
                if not question.played:
                    finished = False
            if not finished:
                break

        if finished:
            self.show_winner()

    def show_winner(self):
        """
        Show who won the game.
        """
        self.framework.question_board.add_winner_button()


def create_questions(config):
    """
    Create the questions from csv file.
    """
    questions = {}

    with open(config, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            question = Question(row)
            if question.points not in questions.keys():
                questions[question.points] = []
            questions[question.points].append(question)

    return questions

def get_resolution(screen_w, screen_h):
    """
    Returns the optimal resolution to use and scale compared to Full HD.
    """
    scale = None

    if 1.75 < round(screen_w/screen_h, 2) < 1.8:
        scale = min([screen_w/1920, screen_h/1080])
    else:
        for (width, height) in RESOLUTIONS:
            if width > screen_w or height > screen_h:
                break
            scale = min([width/1920, height/1080])

        if not scale:
            sys.exit(f"Sorry min resolution is {RESOLUTIONS[0]}.")
    return scale

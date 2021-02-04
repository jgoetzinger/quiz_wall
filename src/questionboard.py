"""
Functionality that shows all available questions.
"""

import tkinter as tk
from functools import partial


class QuestionBoard:
    """
    Question board to show which question to ask.
    """
    def __init__(self, parent, questions):
        self.parent = parent
        self.game = parent.game
        self.framework = parent
        self.questions = questions
        self.buttons, self.positions = self.create_question_buttons()
        self.winner_buttons = []

    def create_question_buttons(self):
        """
        Create the question buttons.
        """
        buttons = {}
        positions = {}
        y_start = 580 - len(self.questions)*170/2
        for j, points in enumerate(self.questions):
            for i in range(len(self.questions[points])):
                num = f"{chr(ord('a') + j).upper()}{i+1}"
                text = num + "\n" + str(points)
                action = partial(self.game.ask_question, num, points, i)
                button = tk.Button(self.framework.window, text=text, command=action,
                                   bg="#ffffff", font=self.parent.get_font(25))
                start = (1980 - 180*len(self.questions[points]))/2
                x_pos = self.parent.offset[0] + int((start+i*180)*self.parent.scale)
                y_pos = self.parent.offset[1] + int((y_start+j*160)*self.parent.scale)
                button.place(x=x_pos, y=y_pos,
                             width=int(130*self.parent.scale), height=int(130*self.parent.scale))
                buttons[num] = button
                positions[num] = (x_pos, y_pos)
        return buttons, positions

    def show_buttons(self):
        """
        Show buttons.
        """
        for button in self.buttons:
            (x_pos, y_pos) = self.positions[button]
            self.buttons[button].place(x=x_pos, y=y_pos, width=int(130*self.parent.scale),
                                       height=int(130*self.parent.scale))

    def hide_buttons(self):
        """
        Hide buttons.
        """
        for button in self.buttons:
            self.buttons[button].place_forget()

    def set_button_color(self, color):
        """
        Set the color of a won button.
        """
        self.buttons[self.game.current_question].config(bg=color, activebackground=color)

    def add_winner_button(self):
        """
        Add a button for the winner to celebrate victory.
        """
        button_r = tk.Button(self.framework.window, text="Celebrate!", command=self.winner_called,
                             bg="#f5d60f", activebackground="#f5d60f", font=self.parent.get_font(25)
                             )
        button_b = tk.Button(self.framework.window, text="Celebrate!", command=self.winner_called,
                             bg="#f5d60f", activebackground="#f5d60f", font=self.parent.get_font(25)
                             )
        if self.game.players["red"] >= self.game.players["blue"]:
            button_r.place(x=self.parent.offset[0]+1580*self.parent.scale,
                           y=self.parent.offset[1]+20*self.parent.scale,
                           width=300*self.parent.scale, height=120*self.parent.scale)
            self.winner_buttons.append(button_r)
        if self.game.players["red"] <= self.game.players["blue"]:
            button_b.place(x=self.parent.offset[0]+100*self.parent.scale,
                           y=self.parent.offset[1]+20*self.parent.scale,
                           width=300*self.parent.scale, height=120*self.parent.scale)
            self.winner_buttons.append(button_b)

    def winner_called(self):
        """
        Winner has been called.
        """
        for button in self.buttons:
            self.buttons[button].config(bg="#ffffff", activebackground="#ffffff")

        for i, button in enumerate(self.buttons):
            self.framework.window.after(1000*(i+1), self.set_button, button, i)
        self.parent.player.play_audio("gameplay/winner.mp3")

    def set_button(self, button, i):
        """
        Set desired button to color.
        """
        if self.game.players["red"] > self.game.players["blue"]:
            winner = "red"
        elif self.game.players["red"] < self.game.players["blue"]:
            winner = "blue"
        else: # we have a draw
            if i % 2:
                winner = "blue"
            else:
                winner = "red"
        self.buttons[button].config(bg=winner, activebackground=winner)
        self.framework.title.config(fg=winner)

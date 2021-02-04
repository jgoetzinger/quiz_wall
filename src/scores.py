"""
Functionality that handles the scores at the bottom of the game.
"""

import tkinter as tk


class PointHandler:
    """
    Class that handles point logic.
    """
    def __init__(self, parent):
        self.parent = parent
        self.point_canvas = tk.Canvas(parent.window, width=int(1355*self.parent.scale),
                                      height=int(82*self.parent.scale), bg="#ffffff")
        self.points = self.create_points()
        self.score = self.create_score()

    def create_points(self):
        """
        Create points at the bottom of the screen.
        """
        points = {}
        num_points = 0
        for question_points in self.parent.game.questions:
            for _ in self.parent.game.questions[question_points]:
                num_points += question_points

        num_bars = int(num_points/50)
        width = (1355 - num_bars*3)/num_bars
        for point_bar in range(num_bars):
            x_start = int(((point_bar+1)*3+point_bar*width)*self.parent.scale)
            x_end = int(((point_bar)*3+(point_bar+1)*width)*self.parent.scale)

            rect = self.point_canvas.create_rectangle(x_start, int(self.parent.scale*5),
                                                      x_end, int(self.parent.scale*77),
                                                      outline="#5a5a5a", fill="#ffffff")

            points[point_bar] = rect
        self.point_canvas.place(x=self.parent.offset[0]+int(self.parent.scale*283),
                                y=self.parent.offset[1]+int(self.parent.scale*959))

        return points

    def create_score(self):
        """
        Create text widgets with score.
        """
        blue = tk.Text(self.parent.window, height=1, width=4, font=self.parent.get_font(25),
                       bg="blue", borderwidth=0, highlightthickness=0)
        blue.place(x=self.parent.offset[0]+int(190*self.parent.scale),
                   y=self.parent.offset[1]+int(980*self.parent.scale))
        blue.insert(tk.END, "0")
        blue.config(state="disabled")
        red = tk.Text(self.parent.window, height=1, width=4, font=self.parent.get_font(25),
                      bg="red", borderwidth=0, highlightthickness=0)
        red.place(x=self.parent.offset[0]+int(1650*self.parent.scale),
                  y=self.parent.offset[1]+int(980*self.parent.scale))
        red.insert(tk.END, "0")
        red.config(state="disabled")
        return {"blue": blue, "red": red}

    def set_points(self):
        """
        Change the colors according to the current score.
        """
        blue = int(self.parent.game.players["blue"]/50)
        red = int(self.parent.game.players["red"]/50)
        for i in range(blue):
            self.fill_rect(i, "blue")

        num_points = len(self.points)
        for i in range(red):
            self.fill_rect(num_points-1-i, "red")

        for team in ["blue", "red"]:
            self.score[team].config(state="normal")
            self.score[team].delete("1.0", tk.END)
            self.score[team].insert(tk.END, self.parent.game.players[team])
            self.score[team].config(state="disabled")

    def fill_rect(self, rect, color):
        """
        Fill a rectengle with the desired color.
        """
        self.point_canvas.itemconfig(self.points[rect], fill=color)

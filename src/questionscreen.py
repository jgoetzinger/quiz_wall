"""
Class that handels functionallity to ask a question.
Therefore it shows a question, checks it and shows the solution
if it is answered correctly.
"""

import tkinter as tk
from functools import partial

class QuestionScreen:
    """
    Handle the screen that is used to ask a question.
    """
    def __init__(self, parent):
        self.parent = parent
        self.elements, self.positions = self.create_elements()
        self.disable_elements()
        self.question_info = {
            "question": None,
            "answer_logged_in": -1,
            "wrong_answers": [],
            "active_team": "blue"
        }

    def create_elements(self):
        """
        Create elements to ask a question.
        """
        elements = {}
        positions = {}

        question = tk.Text(self.parent.window, height=3, width=31)
        x_pos = self.parent.offset[0] + int(460*self.parent.scale)
        y_pos = self.parent.offset[1] + int(300*self.parent.scale)
        question.place(x=x_pos, y=y_pos)
        question.insert(tk.END, "Frage: Warum ist hier kein text?")
        question.config(font=self.parent.get_font(), wrap=tk.WORD)

        elements["question"] = question
        positions["question"] = (x_pos, y_pos, int(1000*self.parent.scale),
                                 int(180*self.parent.scale))
        for answer in [0, 1, 2, 3]:
            action = partial(self.login_answer, answer)
            button = tk.Button(self.parent.window, text=str(f"Antwort {answer+1}"), command=action,
                               bg="#ffffff", font=self.parent.get_font(25),
                               wraplength=int(500*self.parent.scale))
            x_pos = self.parent.offset[0] + int((460+(answer%2)*510)*self.parent.scale)
            y_pos = self.parent.offset[1] + int((500+int(answer/2)*200)*self.parent.scale)
            button.place(x=x_pos, y=y_pos, height=100, width=100)
            elements[answer] = button
            positions[answer] = (x_pos, y_pos, int(490*self.parent.scale),
                                 int(180*self.parent.scale))

        return elements, positions


    def enable_elements(self):
        """
        Enable all elements.
        """
        for element in self.elements:
            x_pos, y_pos, width, height = self.positions[element]
            self.elements[element].place(x=x_pos, y=y_pos, height=height, width=width)

    def disable_elements(self):
        """
        Disable all elements.
        """
        for element in self.elements:
            self.elements[element].place_forget()

    def set_elements(self, question, active_team):
        """
        Set the elements of the questions.
        """
        self.question_info["active_team"] = active_team
        self.question_info["question"] = question
        self.elements["question"].config(state="normal", fg=active_team)
        self.elements["question"].delete("1.0", tk.END)
        self.elements["question"].insert(tk.END, question.question)
        self.elements["question"].config(state="disabled")
        for i in range(4):
            self.elements[i].configure(text=question.answers[i],
                                       bg="#ffffff", activebackground="#ffffff")

        self.question_info["answer_logged_in"] = -1


    def login_answer(self, button_nr):
        """
        Mark answer yellow and wait for comfirmation.
        """
        if self.question_info["question"].played:
            return
        if self.question_info["answer_logged_in"] != button_nr: # we log in the answer
            self.question_info["answer_logged_in"] = button_nr
            for button in range(4):
                if button in self.question_info["wrong_answers"]:
                    continue
                if button == button_nr:
                    self.elements[button].configure(bg="#f5c242", activebackground="#f5c242")
                else:
                    self.elements[button].configure(bg="#ffffff", activebackground="#ffffff")
        else: # logged in answer has been choosen
            if self.question_info["question"].check_answer(self.question_info["answer_logged_in"]):
                self.question_info["question"].played = True
                self.elements[button_nr].configure(bg="#44ff00", activebackground="#44ff00")
                self.question_info["answer_logged_in"] = -1
                self.question_info["wrong_answers"] = []
                self.parent.player.play_audio("gameplay/right.mp3", False)
                self.parent.window.after(1500, self.question_info["question"].get_answer,
                                         self.parent)
                self.parent.window.after(3000, self.get_solution)

            else:
                self.parent.player.play_audio("gameplay/sadTone.mp3", False)

                if self.question_info["active_team"] == "blue":
                    self.question_info["active_team"] = "red"
                else:
                    self.question_info["active_team"] = "blue"
                self.elements[button_nr].configure(bg="#b52d00", activebackground="#b52d00")
                self.elements["question"].config(state="normal",
                                                 fg=self.question_info["active_team"])
                self.elements["question"].delete("1.0", tk.END)
                self.elements["question"].insert(tk.END, self.question_info["question"].question)
                self.elements["question"].config(state="disabled")
                self.parent.title.config(fg=self.question_info["active_team"])
                self.question_info["wrong_answers"].append(button_nr)
                self.question_info["answer_logged_in"] = -1

    def get_solution(self):
        """
        Return to the main window after delay.
        """
        delay = max([self.question_info["question"].delay, self.parent.player.delay])
        self.parent.window.after(delay+3000, self.parent.game.question_answered,
                                 self.question_info["active_team"], self.question_info["question"])

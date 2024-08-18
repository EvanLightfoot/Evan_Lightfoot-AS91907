# Date: 17/06/2024
# Version: 1
from tkinter import *
class Game:
    def __innit__(self, points=0, time=0, game=1, guess=None):
        self.points = points
        self.time = time
        self.game = game
        self.guess = guess

def __innit__(self, points=0, time=0, game=1, guess=None):
    self.points = points
    self.time = time
    self.game = game
    self.guess = guess

def get_guess(self):
    self.guess = guess.get()
    answer = answer.get()
    if self.guess == answer:
        self.points + 1
        self.game + 1
        correct = Label(root, text="Correct!", fg='lime', font=("Calibri", "15", "bold")).grid(column=3, row=4)
        return self.points, self.game
    else:
        correct.destroy()
        incorrect = Label(root, text="Incorrect!", fg='red', font=("Calibri", "15", "bold")).grid(column=3, row=4)
        time.sleep(3)
        incorrect.destroy()
    def get_guess(self):
        self.guess = guess.get()
        answer = answer.get()
        if self.guess == answer:
            self.points + 1
            self.game + 1
            correct = Label(root, text="Correct!", fg='lime', font=("Calibri", "15", "bold")).grid(column=3, row=4)
            return self.points, self.game
        else:
            correct.destroy()
            incorrect = Label(root, text="Incorrect!", fg='red', font=("Calibri", "15", "bold")).grid(column=3, row=4)
            time.sleep(3)
            incorrect.destroy()

def quit(root):
    root.destroy()

# G.U.I
root = Tk()
root.resizable(False, False)
root.state('zoomed')
root.title("Howick College GeoGuesser V1.0")
root.geometry("800x410")
root.configure(background='cyan')
guess = StringVar()
guess_text_box = Entry(root, textvariable=guess, width=30).place(x=70, y=375)
guess_text_box = Entry(root, textvariable=guess, width=34, font=("Calibiri", "11")).place(x=770, y=917)
guess_text_box_label = Label(root, text="Location:", fg="black", bg="cyan",
                                font=("Calibri", "15", "bold")).place(x=0, y=370)
                                font=("Calibri", "15", "bold")).place(x=750, y=910)
submit_btn = Button(root, text="Guess", borderwidth="5", width="13", bg='lime', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:get_guess()).place(x=270, y=360)
info_btn = Button(root, text="Quit", borderwidth="5", width="13", bg='lime', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:get_guess()).place(x=430, y=360)
imgframe = Frame(root, width=500, height=300, bg='white').place(anchor='center', relx=0.5, rely=0.5)
                         font=("Calibri", "15", "bold"),command=lambda:get_guess()).place(x=1050, y=900)
reset_btn = Button(root, text="Reset", borderwidth="5", width="13", bg='lime', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:get_guess()).place(x=600, y=900)
quit_btn = Button(root, text="Quit", borderwidth="5", width="13", bg='lime', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:quit(root)).place(x=450, y=900)

how_to_play_frame = Frame(root, bg='lime', width=430, height=725, highlightbackground="black", highlightthickness=5).place(x=1480, y=168)
how_to_play_title = Label(root, bg='lime', text="How to play?", font=("Calibri", "18", "bold")).place(x=1490, y=175)
title = Label(root, text="Howick College GeoGuesser", bg='cyan', fg='darkblue',
                         font=("Calibri", "30", "bold"),).place(x=170, y=0)
                         font=("Calibri", "30", "bold", "underline"),).place(x=740, y=100)
location = PhotoImage(file="location.png")
location_label = Label(root, height=293, width=444, image=location).place(x=152, y=57)
location_label = Label(root, height=700, width=1000, image=location, bg='white', highlightbackground="black",
highlightthickness=5).place(anchor='center', x=960, y=530)
root.mainloop()
# Written By: Evan Lightfoot
# Date: 17/06/2024
# Version: 1
global count
count = 0

from tkinter import *
class Game:
    def __innit__(self, points=0, game=1, guess=None):
    def __init__(self, points=0, rnd=0, guess=None):
        self.points = points
        self.game = game
        self.rnd = rnd
        self.guess = guess

    def get_guess(self, root):
        global count
        self.guess = guess.get()
        with open("answer_sheet.txt", 'r') as answers:
            data = answers.readlines()
            for line in data:
                if self.guess in current_line:
                    self.points += 1
                    self.game += 1
                    count += 1
            try:
                incorrect.destroy()
                correct = Label(root, text="Correct!", fg='lime', font=("Calibri", "15", "bold")).place(x=770, y=900)
            except NameError:
                correct = Label(root, text="Correct!", fg='lime', font=("Calibri", "15", "bold")).place(x=770, y=900)
            return self.points, self.game, count
        else:
            try:
                correct.destroy()
                incorrect = Label(root, text="Incorrect!", fg='red', font=("Calibri", "15", "bold")).place(x=770, y=900)
            except NameError:
                incorrect = Label(root, text="Incorrect!", fg='red', font=("Calibri", "15", "bold")).place(x=770, y=900)
            answers.close()
            line = data[count].strip()
            if self.guess in line:
                self.points += 1
                self.rnd += 1
                count += 1
                points_val = IntVar(value=self.points)
                rnd_val = IntVar(value=self.rnd) 
                try:
                    incorrect.destroy()
                    correct = Label(root, text="Correct!", bg="#FFFDD0", fg='green', font=("Calibri", "15", "bold")).place(x=888, y=887)
                    points_label = Label(root, textvariable=points_val, fg='black', bg='#FFFDD0', font=("Calibri", "15", "bold")).place(x=20, y=200)
                    rnd_label = Label(root, textvariable=rnd_val, fg='black', bg='#FFFDD0', font=("Calibri", "15", "bold")).place(x=220, y=257)
                    return self.points, self.rnd, count
                except NameError:
                    correct = Label(root, text="Correct!", bg="#FFFDD0", fg='green', font=("Calibri", "15", "bold")).place(x=888, y=887)
                    points_label = Label(root, textvariable=points_val, fg='black', bg='#FFFDD0', font=("Calibri", "15", "bold")).place(x=20, y=200)
                    rnd_label = Label(root, textvariable=rnd_val, fg='black', bg='#FFFDD0', font=("Calibri", "15", "bold")).place(x=220, y=257)
                    return self.points, self.rnd, count
            else:
                try:
                    correct.destroy()
                    incorrect = Label(root, text="Incorrect!", bg="#FFFDD0", fg='darkred', font=("Calibri", "15", "bold")).place(x=888, y=887)
                except NameError:
                    incorrect = Label(root, text="Incorrect!", bg="#FFFDD0", fg='darkred', font=("Calibri", "15", "bold")).place(x=888, y=887)
            answers.close()                    
instance = Game()

# Quits the game (closes the window)
@@ -63,8 +70,9 @@ def quit(root):
how_to_play_text_l3 = Label(root, bg='white', text="- Gather as many points as possible by guessing correctly!", font=("Calibri", "11", "bold")).place(x=1490, y=285)
how_to_play_text_l4 = Label(root, bg='white', text="- Get your best time! by guessing faster and faster as you play!", font=("Calibri", "11", "bold")).place(x=1490, y=320)              
title = Label(root, text="Howick College GeoGuesser", bg='#FFFDD0', fg='darkblue', font=("Calibri", "30", "bold", "underline")).place(x=740, y=100)
points_text = Label(root, bg='#FFFDD0', text="Points:", fg='darkblue', font=("Calibri", "20", "bold")).place(x=20, y=200)
best_time_text = Label(root, bg='#FFFDD0', text='Best Time:', fg='darkblue', font=("Calibri", "20", "bold")).place(x=20, y=250)
points_text = Label(root, bg='#FFFDD0', text="Points:", fg='black', font=("Calibri", "20", "bold")).place(x=20, y=200)
rnd_text = Label(root, bg='#FFFDD0', text="Round Number:", fg='black', font=("Calibri", "20", "bold")).place(x=20, y=250)
rnd_text2 = Label(root, bg='#FFFDD0', text="/10", fg='black', font=("Calibri", "16", "bold")).place(x=400, y=257)
location_img = PhotoImage(file="location.png")
crest_img = PhotoImage(file="crest.png") # Imports the Howick College Crest
crest_label = Label(root, height=175, width=200, image=crest_img, bg='white').place(x=1700, y=700)
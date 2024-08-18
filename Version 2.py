# Written By: Evan Lightfoot
# Date: 26/07/2024
# Version: 2
import random
import random as r
import re
from tkinter import *
class Game:
def __init__(self, points=0, rnd=0, guess=None, correct=None, incorrect=None):
    def get_guess(self, root):
        global count
        global amount
        global additive
        global loc
        self.guess = guess.get().replace(" ", "")
        validated_guess = re.sub('[^A-Za-z0-9]+', '', self.guess)
        self.guess = validated_guess
        if self.guess == "":
            pass
        else:
            with open("Assets\answer_sheet.txt", 'r') as answers:
            with open("Assets/answer_sheet.txt", 'r') as answers:
                data = answers.readlines()
                line = data[count].strip().lower()
                line = data[loc_num].strip().lower()
                words = line.split()
                for word in words:
                    if word in self.guess():
                    if word in self.guess:
                        self.points += additive
                        self.rnd += 1
                        count += 1
def reset(self, root):
        return self.points, self.rnd, count

instance = Game()
loc = []
count = 0
additive = 3
# Quits the game (closes the window)
def quit(root):
    root.destroy()

def get_loc(root):
    global loc
    try:
        loc.destroy()
        loc_label.destroy()
    except NameError:
        pass
    loc_generate = r.randint(1, 31)
    loc_set = f"Loc{loc_generate}"
    loc_img = PhotoImage(file=f"Assets\{loc_set}.png")
    loc_label = Label(root, height=700, width=1000, image=location_img, bg='white', highlightbackground="black", highlightthickness=5)
    loc_generate = r.randint(1, 30)
    loc.append(loc_generate)    
    loc_num = loc[0]
    loc_set = f"Loc{loc_num}"
    loc_img = PhotoImage(file=f"Assets/{loc_set}.png")
    loc_label = Label(root, height=700, width=1000, image=loc_img, bg='white', highlightbackground="black", highlightthickness=5)
    loc_label.image = loc_img
    loc_label.place(anchor='center', x=960, y=530)
    loc.pop(0)

# G.U.I
root = Tk() # Initialises the window.
@@ -130,10 +138,12 @@ def get_loc(root):
how_to_play_text_l2.place(x=1490, y=250)
how_to_play_text_l3 = Label(root, bg='white', fg="green", text="- Gather as many points as possible by guessing correctly!", font=("Calibri", "11", "bold"))
how_to_play_text_l3.place(x=1490, y=285)
how_to_play_text_l4 = Label(root, bg='white', fg="green", text="- There are 10 rounds, so there are 10 points to get!", font=("Calibri", "11", "bold"))
how_to_play_text_l4 = Label(root, bg='white', fg="green", text="- There are 10 rounds, but there are 30 points to get!", font=("Calibri", "11", "bold"))
how_to_play_text_l4.place(x=1490, y=320)
how_to_play_text_l5 = Label(root, bg='white', fg="green", text="- Good luck and have fun!", font=("Calibri", "11", "bold"))
how_to_play_text_l5.place(x=1490, y=355)  
how_to_play_text_l5 = Label(root, bg='white', fg="green", text="- +3 points if you guess a location first try, +2 on second try!", font=("Calibri", "11", "bold"))
how_to_play_text_l5.place(x=1490, y=355)
how_to_play_text_l6 = Label(root, bg='white', fg="green", text="- Any more guesses give +1, so good luck and have fun!", font=("Calibri", "11", "bold"))
how_to_play_text_l6.place(x=1490, y=390)  
title = Label(root, text="Howick College GeoGuesser", bg='#00FFFF', fg='darkblue', font=("Calibri", "30", "bold", "underline"))
title.place(x=740, y=120)
game_stats_frame = Frame(root, bg='white', width=300, height=150, highlightbackground="black", highlightthickness=5)
def get_loc(root):
crest_img = PhotoImage(file="Assets\crest.png") # Imports the Howick College Crest
crest_label = Label(root, height=175, width=200, image=crest_img, bg='white')
crest_label.place(x=1700, y=700)
get_loc(root)
root.mainloop() # Keeps the window open.
# Written By: Evan Lightfoot
# Date: 17/06/2024
# Version: 1
import time
count = 0

from tkinter import *
class Game:
    def __init__(self, points=0, rnd=0, guess=None):
    def __init__(self, points=0, rnd=0, guess=None, correct=None, incorrect=None):
        self.points = points
        self.rnd = rnd
        self.guess = guess

        self.correct = correct
        self.incorrect = incorrect

    def get_guess(self, root):
        global count
        self.guess = guess.get()
        with open("answer_sheet.txt", 'r') as answers:
            data = answers.readlines()
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
        if self.guess == "":
            pass
        else:
            with open("answer_sheet.txt", 'r') as answers:
                data = answers.readlines()
                line = data[count].strip()
                if self.guess in line:
                    self.points += 1
                    self.rnd += 1
                    count += 1
                    points_val = IntVar(value=self.points)
                    rnd_val = IntVar(value=self.rnd) 
                    try:
                        self.incorrect.destroy()
                    except AttributeError:
                        pass
                    self.correct = Label(root, text="Correct!", bg="#FFFDD0", fg='green', font=("Calibri", "15", "bold"))
                    self.correct.place(x=888, y=887)
                    points_label = Label(root, textvariable=points_val, fg='black', bg='#FFFDD0', font=("Calibri", "16", "bold"))
                    points_label.place(x=110, y=205)
                    rnd_label = Label(root, textvariable=rnd_val, fg='black', bg='#FFFDD0', font=("Calibri", "16", "bold"))
                    rnd_label.place(x=110, y=255)
                    return self.points, self.rnd, count
            else:
                try:
                    correct.destroy()
                    incorrect = Label(root, text="Incorrect!", bg="#FFFDD0", fg='darkred', font=("Calibri", "15", "bold")).place(x=888, y=887)
                except NameError:
                    incorrect = Label(root, text="Incorrect!", bg="#FFFDD0", fg='darkred', font=("Calibri", "15", "bold")).place(x=888, y=887)
            answers.close()                    
                else:
                    try:
                        self.correct.destroy()
                    except AttributeError:
                        pass
                    self.incorrect = Label(root, text="Incorrect!", bg="#FFFDD0", fg='darkred', font=("Calibri", "15", "bold"))
                    self.incorrect.place(x=888, y=887)
            answers.close()    
instance = Game()

# Quits the game (closes the window)
@@ -54,27 +61,40 @@ def quit(root):
root.title("Howick College GeoGuesser V1.0")
root.configure(background='#FFFDD0') # Cream coloured background.
guess = StringVar()
guess_text_box = Entry(root, textvariable=guess, width=30, highlightbackground="black", highlightthickness="1", font=("Calibiri", "11")).place(x=830, y=917)
guess_text_box_label = Label(root, text="Location:", fg="black", bg="#FFFDD0",
                                font=("Calibri", "15", "bold")).place(x=748, y=910)
guess_btn = Button(root, text="Guess", borderwidth="2", width="13", bg='lime', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:instance.get_guess(root)).place(x=1100, y=900) # Guess button, calls the guess function.
reset_btn = Button(root, text="Reset", borderwidth="2", width="13", bg='red', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:reset(self, root)).place(x=600, y=900) # Reset button, calls the reset function.
quit_btn = Button(root, text="Quit", borderwidth="2", width="13", bg='red', fg='black',
                         font=("Calibri", "15", "bold"),command=lambda:quit(root)).place(x=450, y=900) # Quit button, calls the quit function.
how_to_play_frame = Frame(root, bg='white', width=430, height=714, highlightbackground="black", highlightthickness=5).place(x=1480, y=173) # Creates a frame (coloured box) for tidyness.
how_to_play_title = Label(root, fg="darkblue", bg='white', text="How to play?", font=("Calibri", "20", "bold", "underline")).place(x=1490, y=178)
how_to_play_text_l1 = Label(root, bg='white', text="- Type your guess in the text box 'location' undeneath the image.", font=("Calibri", "11", "bold")).place(x=1490, y=215)
how_to_play_text_l2 = Label(root, bg='white', text="- Ensure that you use correct grammer and clear guesses.", font=("Calibri", "11", "bold")).place(x=1490, y=250)
how_to_play_text_l3 = Label(root, bg='white', text="- Gather as many points as possible by guessing correctly!", font=("Calibri", "11", "bold")).place(x=1490, y=285)
how_to_play_text_l4 = Label(root, bg='white', text="- Get your best time! by guessing faster and faster as you play!", font=("Calibri", "11", "bold")).place(x=1490, y=320)              
title = Label(root, text="Howick College GeoGuesser", bg='#FFFDD0', fg='darkblue', font=("Calibri", "30", "bold", "underline")).place(x=740, y=100)
points_text = Label(root, bg='#FFFDD0', text="Points:", fg='black', font=("Calibri", "20", "bold")).place(x=20, y=200)
rnd_text = Label(root, bg='#FFFDD0', text="Round Number:", fg='black', font=("Calibri", "20", "bold")).place(x=20, y=250)
rnd_text2 = Label(root, bg='#FFFDD0', text="/10", fg='black', font=("Calibri", "16", "bold")).place(x=400, y=257)
guess_text_box = Entry(root, textvariable=guess, width=30, highlightbackground="black", highlightthickness="1", font=("Calibiri", "11"))
guess_text_box.place(x=830, y=917)
guess_text_box_label = Label(root, text="Location:", fg="black", bg="#FFFDD0", font=("Calibri", "15", "bold"))
guess_text_box_label.place(x=748, y=910)
guess_btn = Button(root, text="Guess", borderwidth="2", width="13", bg='lime', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.get_guess(root)) # Guess button, calls the guess function.
guess_btn.place(x=1100, y=900)
quit_btn = Button(root, text="Quit", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:quit(root)) # Quit button, calls the quit function.
quit_btn.place(x=590, y=900)
how_to_play_frame = Frame(root, bg='white', width=430, height=714, highlightbackground="black", highlightthickness=5) # Creates a frame (coloured box) for tidyness.
how_to_play_frame.place(x=1480, y=173)
how_to_play_title = Label(root, fg="darkblue", bg='white', text="How to play?", font=("Calibri", "20", "bold", "underline"))
how_to_play_title.place(x=1490, y=178)
how_to_play_text_l1 = Label(root, bg='white', fg="green", text="- Type your guess in the text box 'location' undeneath the image.", font=("Calibri", "11", "bold"))
how_to_play_text_l1.place(x=1490, y=215)
how_to_play_text_l2 = Label(root, bg='white', fg="green", text="- Ensure that you use correct grammer and clear guesses.", font=("Calibri", "11", "bold"))
how_to_play_text_l2.place(x=1490, y=250)
how_to_play_text_l3 = Label(root, bg='white', fg="green", text="- Gather as many points as possible by guessing correctly!", font=("Calibri", "11", "bold"))
how_to_play_text_l3.place(x=1490, y=285)
how_to_play_text_l4 = Label(root, bg='white', fg="green", text="- There are 10 rounds, so there are 10 points to get!", font=("Calibri", "11", "bold"))
how_to_play_text_l4.place(x=1490, y=320)
how_to_play_text_l5 = Label(root, bg='white', fg="green", text="- Good luck and have fun!", font=("Calibri", "11", "bold"))
how_to_play_text_l5.place(x=1490, y=355)  
title = Label(root, text="Howick College GeoGuesser", bg='#FFFDD0', fg='darkblue', font=("Calibri", "30", "bold", "underline"))
title.place(x=740, y=100)
points_text = Label(root, bg='#FFFDD0', text="Points:", fg='black', font=("Calibri", "20", "bold"))
points_text.place(x=20, y=200)
rnd_text = Label(root, bg='#FFFDD0', text="Round:", fg='black', font=("Calibri", "20", "bold"))
rnd_text.place(x=20, y=250)
rnd_text2 = Label(root, bg='#FFFDD0', text="/10", fg='black', font=("Calibri", "16", "bold"))
rnd_text2.place(x=124, y=255)
location_img = PhotoImage(file="location.png")
location_label = Label(root, height=700, width=1000, image=location_img, bg='white', highlightbackground="black", highlightthickness=5)
location_label.place(anchor='center', x=960, y=530)
crest_img = PhotoImage(file="crest.png") # Imports the Howick College Crest
crest_label = Label(root, height=175, width=200, image=crest_img, bg='white').place(x=1700, y=700)
location_label = Label(root, height=700, width=1000, image=location_img, bg='white', highlightbackground="black", highlightthickness=5).place(anchor='center', x=960, y=530)
crest_label = Label(root, height=175, width=200, image=crest_img, bg='white')
crest_label.place(x=1700, y=700)
root.mainloop() # Keeps the window open.
# AS91907 - Howick College GeoGuesser
# Written By: Evan Lightfoot
# Date: 26/07/2024
# Version: 2
import random as r
import re
from tkinter import *
'''Default values that are passed in'''
additive = 3
class Game:
    def __init__(self, points=0, rnd=1, guess=None, correct=None, incorrect=None, loc_num=None, additive=3): # Sets self values.
        '''Sets the self values'''
        self.points = points # Amount of points the user has.
        self.rnd = rnd # The current round (rnd) number since there are 10 rounds.
        self.guess = guess # The users guess.
        '''Allows the labels to be updated within the instance as this is more reliable than updating them in the GUI.'''
        self.correct = correct
        self.incorrect = incorrect
        self.loc_num = loc_num # Loc Num
        self.additive = additive
        
    def get_guess(self, root): # Gets the guess from the Entry Box
        self.guess = guess.get().replace(' ', '') # Removes all spaces from the guess so it can be validated easily.
        validated_guess = re.sub('[^A-Za-z0-9]+', '', self.guess) # Removes all non-alphanumeric characters from the guess as answers are only alphanumeric.
        self.guess = validated_guess # Updates self.guess
        if self.guess == "": # If the user didn't enter anything but submitted, ignore it.
            pass
        else:
            return self.guess, self.get_answer() # Validate the guess.
            
    def get_answer(self): # Gets the answer for the current location image.
        with open("Assets/answer_sheet.txt", 'r') as answers:
            data = answers.readlines()
            line = data[self.loc_num -1].strip().lower() # Finds the line which the answer is located in.
            words = line.split() # Splits the line up into words (answers).
            return words, self.update_game_state(words) # Returns the acceptable answers and calls the method which updates the game state.
        answers.close()
        
    def update_game_state(self, words): # Updates the game statistics e.g. points, rnd number, textvariables, labels on correct guess.
        for word in words: # For every word in the acceptable answers line within the answer_sheet.txt file, if the guess contains any accepted answer it is correct, e.g. receptionist is correct because reception is an acceptable answer. 
            if word in self.guess:
                '''Updates game stats'''
                self.points += self.additive
                self.rnd += 1
                points_val = IntVar(value=self.points)
                rnd_val = IntVar(value=self.rnd) 
                try:
                    self.incorrect.destroy() # Destroys the old incorrect label, otherwise it would keep generating a new one if guesses are correct two or more times which would overlay the correct label.
                except AttributeError:
                    pass
                try:
                    self.correct.destroy() # Destroys the old correct label, otherwise it would keep generating a new one if guesses are correct two or more times which would overlay the incorrect label.
                except AttributeError:
                    pass
                self.correct = Label(root, text="Correct!", bg="#00FFFF", fg='green', font=("Calibri", "15", "bold"))
                self.correct.place(x=888, y=887)
                points_label = Label(root, textvariable=points_val, fg='black', bg='white', font=("Calibri", "16", "bold"))
                points_label.place(x=110, y=205)
                rnd_label = Label(root, textvariable=rnd_val, fg='black', bg='white', font=("Calibri", "16", "bold"))
                rnd_label.place(x=110, y=258)
                return self.points, self.rnd, self.get_loc(root) # Gets the location for the next rnd since the current one was correctly guessed, also returns all updated values.
            else:
                try:
                    self.correct.destroy()
                except AttributeError:
                    pass
                try:
                    self.incorrect.destroy()
                except AttributeError:
                    pass
                if self.additive > 1: # Additive reductions cap at 1 otherwise the user would get no points.
                    self.additive -= 1
                self.incorrect = Label(root, text="Incorrect!", bg="#00FFFF", fg='darkred', font=("Calibri", "15", "bold"))
                self.incorrect.place(x=888, y=887)
                return self.additive # Returns new additive value.
        
    def reset(self, root): # Allows user to reset their game.
        self.additive = 3 # Resets the additive value to default.
        '''Sets game stats to 0'''
        self.points = 0
        self.rnd = 0
        '''Destroys any existing labels'''
        try:
            self.correct.destroy()
        except AttributeError:
            pass
        try:
            self.incorrect.destroy()
        except AttributeError:
            pass
        '''Resets the IntVar (text that appears on the GUI)'''
        points_val = IntVar(value=self.points)
        rnd_val = IntVar(value=self.rnd)
        points_label = Label(root, textvariable=points_val, fg='black', bg='white', font=("Calibri", "16", "bold"))
        points_label.place(x=110, y=205)
        rnd_label = Label(root, textvariable=rnd_val, fg='black', bg='white', font=("Calibri", "16", "bold"))
        rnd_label.place(x=110, y=255)
        return self.points, self.rnd, self.additive # Returns the new variable values.
        
    def get_loc(self, root): # Gets a random location image.png and displays it.
        self.additive = 3
        '''If there is an existing location image displayed, delete it.'''
        try:
            loc_label.destroy()
        except NameError:
            pass
        loc_generate = r.randint(1, 30) # Generates a random location img since image names are labeled from one to thirty i.e Loc1
        self.loc_num = loc_generate
        loc_set = f"Loc{self.loc_num}" # Sets the name of the random loc img.
        loc_img = PhotoImage(file=f"Assets/{loc_set}.png") # Opens the generated loc img from the assets folder.
        loc_label = Label(root, height=700, width=1000, image=loc_img, bg='black', highlightbackground="white", highlightthickness=5)
        loc_label.image = loc_img
        loc_label.place(anchor='center', x=960, y=530) # Ensures the image is placed in the Frame correctly.
        return self.loc_num, self.additive # Returns the name of the generated loc image so the answer for it can be located in the answer sheet in get_answer().
    
    def skip(self): # Allows the user to skip if they don't know the area of a location.
        self.additive = 3
        return additive, instance.get_loc(root)    
        
instance = Game() # Creates the object.
# Quits the game (closes the window)
def quit(root): # Closes the program.
    root.destroy()
    
# G.U.I
root = Tk() # Initialises the window.
root.resizable(False, False) # Locks the window size to prevent re-sizing.
root.state('zoomed') # Makes the window fullscreen.
root.title("Howick College GeoGuesser V2.0")
root.configure(background='#00FFFF') # Cream coloured background.
guess = StringVar() # Initialises the EntryBox as a string variable so I can get their guesses.
guess_text_box = Entry(root, textvariable=guess, width=30, highlightbackground="black", highlightthickness="1", font=("Calibiri", "11")) # Textbox where the user enters their guess.
guess_text_box.place(x=830, y=917)
guess_text_box_label = Label(root, text="Location:", fg="black", bg='#00FFFF', font=("Calibri", "15", "bold"))
guess_text_box_label.place(x=748, y=910)
guess_btn = Button(root, text="Guess", borderwidth="2", width="13", bg='#01F9C6', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.get_guess(root)) # Guess button, calls the guess function.
guess_btn.place(x=1100, y=900)
quit_btn = Button(root, text="Quit", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:quit(root)) # Quit button, calls the quit function.
quit_btn.place(x=594, y=900)
reset_btn = Button(root, text="Reset", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.reset(root)) # Reset button, calls the reset function.
reset_btn.place(x=454, y=900)
skip_btn = Button(root, text="Skip", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.skip()) # Skip button, calls the get_loc function.
skip_btn.place(x=1240, y=900)
how_to_play_frame = Frame(root, bg='white', width=430, height=714, highlightbackground="black", highlightthickness=5) # Creates a frame to hold the text for tidyness.
how_to_play_frame.place(x=1480, y=173)
how_to_play_title = Label(root, fg="darkblue", bg='white', text="How to play?", font=("Calibri", "20", "bold", "underline"))
how_to_play_title.place(x=1490, y=178)
'''Text is split into separate lines to ensure they are placed correctly and do not break.'''
how_to_play_text_l1 = Label(root, bg='white', fg="green", text="- Type your guess in the text box 'location' undeneath the image.", font=("Calibri", "11", "bold"))
how_to_play_text_l1.place(x=1490, y=215)
how_to_play_text_l2 = Label(root, bg='white', fg="green", text="- Ensure that you use correct grammer and clear guesses.", font=("Calibri", "11", "bold"))
how_to_play_text_l2.place(x=1490, y=250)
how_to_play_text_l3 = Label(root, bg='white', fg="green", text="- Gather as many points as possible by guessing correctly!", font=("Calibri", "11", "bold"))
how_to_play_text_l3.place(x=1490, y=285)
how_to_play_text_l4 = Label(root, bg='white', fg="green", text="- There are 10 rounds, but there are 30 points to get!", font=("Calibri", "11", "bold"))
how_to_play_text_l4.place(x=1490, y=320)
how_to_play_text_l5 = Label(root, bg='white', fg="green", text="- +3 points if you guess a location first try, +2 on second try!", font=("Calibri", "11", "bold"))
how_to_play_text_l5.place(x=1490, y=355)
how_to_play_text_l6 = Label(root, bg='white', fg="green", text="- Any more guesses give +1, so good luck and have fun!", font=("Calibri", "11", "bold"))
how_to_play_text_l6.place(x=1490, y=390)  
title = Label(root, text="Howick College GeoGuesser", bg='#00FFFF', fg='darkblue', font=("Calibri", "30", "bold", "underline"))
title.place(x=740, y=120)
game_stats_frame = Frame(root, bg='white', width=300, height=150, highlightbackground="black", highlightthickness=5) # Frame for the game stats (points, rnd number) to ensure tidyness.
game_stats_frame.place(x=2, y=174)
points_text = Label(root, bg='white', text="Points:", fg='black', font=("Calibri", "20", "bold"))
points_text.place(x=20, y=200)
rnd_text = Label(root, bg='white', text="Round:", fg='black', font=("Calibri", "20", "bold"))
rnd_text.place(x=20, y=250)
rnd_text2 = Label(root, bg='white', text="/10", fg='black', font=("Calibri", "16", "bold"))
rnd_text2.place(x=124, y=258)
crest_img = PhotoImage(file="Assets\crest.png") # Opens the Howick College Crest png from the Assets folder.
crest_label = Label(root, height=175, width=200, image=crest_img, bg='white')
crest_label.place(x=1700, y=700)
instance.get_loc(root) # Initialises get_loc when the program starts.
root.mainloop() # Keeps the GUI open.
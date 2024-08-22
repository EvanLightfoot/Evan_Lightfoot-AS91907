# AS91907 - Howick College GeoGuesser
# Written By: Evan Lightfoot
# Date: 26/07/2024
# Version: 2
# Added a Skip and Replay feature as well as changed the background colour and improved validation.

import random as r
import re
from tkinter import *
class Game:
    def __init__(self, points=0, rnd=1, guess=None, loc_num=None, additive=3, correct=None, incorrect=None): # Sets self values.
        '''Sets the self values'''
        self.points = points # Amount of points the user has.
        self.rnd = rnd # The current round (rnd) number since there are 10 rounds.
        self.guess = guess # The users guess.
        '''Allows the labels to be updated within the instance as this is more reliable than updating them in the GUI.'''
        self.correct = correct
        self.incorrect = incorrect
        self.points_label = None
        self.rnd_label = None
        self.loc_num = loc_num # The image name and therefore the line the answers to the image are located.
        self.additive = additive # 3 points on first guess if correct, 2 points on second guess, 1 point all others.

    def get_guess(self, root): # Gets the guess from the Entry Box       
        self.guess = guess.get().replace(' ', '') # Removes all spaces from the guess so it can be validated easily.
        validated_guess = re.sub('[^A-Za-z0-9]+', '', self.guess) # Removes all non-alphanumeric characters from the guess as answers are only alphanumeric.
        self.guess = validated_guess # Updates self.guess
        if self.guess == "": # If the user didn't enter anything but submitted their guess, ignore it.
            pass
        else:
            return self.guess, self.get_answer() # Validate the guess.

    def get_answer(self): # Gets the answer for the current location image.
        with open("Assets/answer_sheet.txt", 'r') as answers:
            data = answers.readlines()
            line = data[self.loc_num -1].strip().lower() # Finds the line which the answer is located in.
            words = line.split() # Splits the line up into words (answers).
            return words, self.update_game_state(words) # Returns the acceptable answers and calls the method which updates the game state.

    def update_game_state(self, words): # Updates the game statistics e.g. points, rnd number, textvariables, labels on correct guess.
        for word in words: # For every word in the acceptable answers line within the answer_sheet.txt file, if the guess contains any accepted answer it is correct, e.g. receptionist is correct because reception is an acceptable answer.
            if self.guess.lower() in [answer.lower() for answer in words if self.guess.lower() in answer.lower()]:
                '''Updates game stats'''
                self.points += self.additive
                self.rnd += 1
                try:
                    self.incorrect.destroy() # Destroys the old incorrect label, otherwise it would keep generating a new one if guesses are correct two or more times which would overlay the correct label.
                except AttributeError:
                    pass
                try:
                    self.correct.destroy() # Destroys the old correct label, otherwise it would keep generating a new one if guesses are correct two or more times which would overlay the incorrect label.
                except AttributeError:
                    pass
                points_val = IntVar(value=self.points)
                self.correct = Label(root, text="Correct!", bg="#00FFFF", fg='green', font=("Calibri", "20", "bold"))
                self.correct.place(relx=0.5, rely=0.12, anchor=CENTER)
                points_val.set(self.points)
                self.points_label.config(textvariable=points_val)                
                if self.rnd == 11:
                    rnd_val = IntVar(value=self.rnd-1)
                    return self.game_end(root)
                rnd_val = IntVar(value=self.rnd)                             
                rnd_val.set(self.rnd)
                self.rnd_label.config(textvariable=rnd_val)
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
                self.incorrect = Label(root, text="Incorrect!", bg="#00FFFF", fg='darkred', font=("Calibri", "20", "bold"))
                self.incorrect.place(relx=0.5, rely=0.12, anchor=CENTER)
                return self.additive # Returns new additive value.

    def replay(self, root): # Allows user to reset their game.
        guess_btn.config(state='normal')
        self.additive = 3 # Resets the additive value to default.
        '''Sets game stats to 0'''
        self.points = 0
        self.rnd = 1
        self.time = 0
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
        self.time_label.config(textvariable=IntVar(value=0), bg='white', fg='black', font=("Calibri", "18", "bold"))
        self.points_label.config(textvariable=IntVar(value=0), fg='black', bg='white', font=("Calibri", "18", "bold"))
        self.rnd_label.config(textvariable=IntVar(value=1), fg='black', bg='white', font=("Calibri", "18", "bold"))
        return self.points, self.rnd, self.additive, self.time, self.continue_timer # Returns the new variable values.

    def get_loc(self, root):  # Gets a random location image.png and displays it.
        self.additive = 3
        '''If there is an existing location image displayed, delete it.'''
        try:
            self.loc_label.destroy()
        except AttributeError:
            pass
        loc_generate = r.randint(1, 30)  # Generates a random location img since image names are labeled from one to thirty i.e Loc1
        self.loc_num = loc_generate
        self.loc_set = f"Loc{loc_generate}"  # Create the filename for the location image
        self.loc_img = PhotoImage(file=f"Assets/{self.loc_set}.png")  # Opens the generated loc img from the assets folder.
        self.img_frame = Frame(root, bg='black', highlightbackground="white", highlightthickness=1)
        self.img_frame.place(relx=0.5, rely=0.4744, anchor=CENTER, relwidth=0.478, relheight=0.63)
        self.loc_label = Label(self.img_frame, image=self.loc_img, bg='white')
        self.loc_label.image = self.loc_img
        self.loc_label.place(relx=0.498, rely=0.497, anchor=CENTER, relwidth=1, relheight=0.998)  # Adjusts the image size to fit in frame
        return self.loc_num, self.additive  # Returns the name of the generated loc image so the answer for it can be located in the answer sheet in get_answer().
    
    def skip(self): # Allows the user to skip if they don't know the area of a location.
        if self.continue_timer == False:
            pass
        else:
            self.additive = 3
            return self.additive, self.get_loc(root)

    def update_time(self, root):  
        if self.continue_timer:
            self.time += 1
            time_val = StringVar()
            time_val.set(str(self.time) + "s")  
            self.time_label.config(textvariable=time_val, bg='white', fg='black', font=("Calibri", 18, "bold"))            
            root.after(1000, lambda: self.update_time(root))
        else:   
            self.process_time()
                
    def game_end(self, root):
        self.continue_timer = False
        guess_btn.config(state='disabled')
        return self.continue_timer
              
instance = Game() # Creates the object.
# Quits the game (closes the window)
def quit(root): # Closes the program.
    root.destroy()

# G.U.I
root = Tk() # Initialises the window.
root.resizable(False, False) # Locks the window size to prevent re-sizing.
root.state('zoomed') # Makes the window fullscreen.
root.title("Howick College GeoGuesser V2.0")
root.configure(background='#00FFFF') # Aqua coloured background.
guess = StringVar() # Initialises the EntryBox as a string variable so I can get their guesses.
guess_text_box = Entry(root, textvariable=guess, width=35, highlightbackground="black", highlightthickness="1", font=("Calibiri", "11"))
guess_text_box.place(relx=0.5, rely=0.9, anchor=CENTER)
guess_text_box_label = Label(root, text="Location:", fg="black", bg='#00FFFF', font=("Calibri", "20", "bold"))
guess_text_box_label.place(relx=0.347, rely=0.898, anchor=CENTER)
guess_btn = Button(root, text="Guess", borderwidth="2", width="13", bg='lime', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.get_guess(root))
guess_btn.place(relx=0.689, rely=0.83, anchor=CENTER)
quit_btn = Button(root, text="Quit", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:quit(root))
quit_btn.place(relx=0.311, rely=0.83, anchor=CENTER)
replay_btn = Button(root, text="Replay", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.replay(root))
replay_btn.place(relx=0.41, rely=0.83, anchor=CENTER)
skip_btn = Button(root, text="Skip", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.skip())
skip_btn.place(relx=0.5, rely=0.83, anchor=CENTER)
how_to_play_frame = Frame(root, bg='white', width=340, height=469, highlightbackground="black", highlightthickness=5)
how_to_play_frame.place(relx=0.875, rely=0.474, anchor=CENTER)
how_to_play_title = Label(root, fg="darkblue", bg='white', text="How to play?", font=("Calibri", "20", "bold", "underline"))
how_to_play_title.place(relx=0.87, rely=0.194, anchor=CENTER)
how_to_play_text = Label(root, bg='white', fg="black", text="\n- Type your guess in the 'location' box\n\n- Ensure that you use correct grammar and clear guesses.\n\n- Gather as many points as possible by guessing correctly!\n\n- Use the buttons below to skip, quit, reset and guess.\n\n- There are 10 rounds, but there are 30 points to get! \n\n +3 points if you guess a location first try, +2 on second try! \n\n- Any more guesses give +1, so good luck and have fun! \n\n- Also there is a timer, try and guess as fast as possible!")
how_to_play_text.place(relx=0.872, rely=0.38, anchor=CENTER)
how_to_play_text.config(state='disabled')
title_banner = Frame(root, bg="#03055B", height=50)
title_banner.pack(fill="x")
title = Label(root, text="Howick College GeoGuesser 2024", bg='#03055B', fg='white', font=("Calibri", "30", "bold"))
title.place(relx=0.5, rely=0.03, anchor=CENTER)
game_stats_frame = Frame(root, bg='white', width=250, height=150, highlightbackground="black", highlightthickness=5)
game_stats_frame.place(relx=0.16, rely=0.26, anchor=CENTER)
points_text = Label(root, text="Points:", bg='white', fg='black', font=("Calibri", "18", "bold"))
points_text.place(relx=0.102, rely=0.203, anchor=CENTER)
out_of_divider1 = Label(root, text="/", bg='white', fg='black', font=("Calibri", "18", "bold"))
out_of_divider1.place(relx=0.16, rely=0.203, anchor=CENTER)
out_of_30 = Label(root, text="30", bg='white', fg='black', font=("Calibri", "18", "bold"))
out_of_30.place(relx=0.18, rely=0.203, anchor=CENTER)
instance.points_label = Label(root, textvariable=IntVar(value=0), bg='white', fg='black', font=("Calibri", "18", "bold"))
instance.points_label.place(relx=0.14, rely=0.203, anchor=CENTER)
rnd_text = Label(root, text="Round:", bg='white', fg='black', font=("Calibri", "18", "bold"))
rnd_text.place(relx=0.102, rely=0.25, anchor=CENTER)
instance.rnd_label = Label(root, textvariable=IntVar(value=1), bg='white', fg='black', font=("Calibri", "18", "bold"))
instance.rnd_label.place(relx=0.14, rely=0.25, anchor=CENTER)
out_of_divider2 = Label(root, text="/", bg='white', fg='black', font=("Calibri", "18", "bold"))
out_of_divider2.place(relx=0.16, rely=0.25, anchor=CENTER)
round_10_label = Label(root, text="10", bg='white', fg='black', font=("Calibri", "18", "bold"))
round_10_label.place(relx=0.18, rely=0.25, anchor=CENTER)
'''crest img'''
crest_img = PhotoImage(file=f"Assets/crest.png")  # Opens the generated loc img from the assets folder.
crest_label = Label(how_to_play_frame, image=crest_img, bg='white')
crest_label.place(relx=0.872, rely=0.78, anchor='ne')
'''grab first location'''
instance.get_loc(root) # Calls the get_loc method to display a location image.
root.mainloop() # Starts the GUI event loop.
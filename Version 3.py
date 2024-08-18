# AS91907 - Howick College GeoGuesser
# Written By: Evan Lightfoot
# Date: 5/08/2024
# Version: 3
import random as r
import re
from tkinter import *
class Game:
    def __init__(self, loc_num=None, points=0, additive=3, rnd=1, guess=None, time=0, correct=None, incorrect=None, feedback_msg=None, win=None): # Defines and sets the attribute states.
        '''Instance variables'''
        self.loc_num = loc_num # The image name and therefore the line the answers to that image are located.
        self.points = points # Amount of points the user has.
        self.points_label = None # Displays the amount of points on screen.
        self.additive = additive # 3 points on first guess if correct, 2 points on second guess, 1 point all others.
        self.rnd = rnd # The current round (rnd) number since there are 10 rounds.
        self.rnd_label = None
        self.guess = guess # The users guess.
        self.time = time # The users elapsed game time.
        self.time_label = None
        self.correct = correct # Correct label so it can be destroyed/recreated within the instance on correct guess.
        self.incorrect = incorrect
        self.feedback_msg = None
        self.continue_timer = True # Will end the game if set to false.
        self.win = win

    def get_guess(self, root):
        '''Gets the guess (text) from the guess_text_box entry box'''
        if self.continue_timer == False:
            pass
        else:
            self.guess = guess.get().replace(' ', '') # Removes all spaces from the guess so it can be validated easily.
            if self.guess == "": # If the user didn't enter anything but submitted their guess
                try:
                    self.feedback_msg.destroy() # Destroys the old label (if there is one), otherwise do nothing.
                except AttributeError:
                    pass
                self.feedback_msg = Label(root, text="Type in the guess box below!", bg="#00FFFF", fg='darkred', font=("Calibri", "20", "bold"))
                self.feedback_msg.place(relx=0.5, rely=0.12, anchor=CENTER)
            elif len(self.guess) > 13: # If the users guess is more than 15 letters.
                try:
                    self.feedback_msg.destroy()
                except AttributeError:
                    pass
                self.feedback_msg = Label(root, text="Your guess is too long, most answers are around 5 to 13 letters.", bg="#00FFFF", fg='darkred', font=("Calibri", "20", "bold"))
                self.feedback_msg.place(relx=0.5, rely=0.12, anchor=CENTER)
                guess_text_box.delete(0, END) # Clears the guess box so its ready for the user to guess again.
            else:
                try:
                    self.feedback_msg.destroy()
                except AttributeError:
                    pass
                validated_guess = re.sub('[^A-Za-z0-9]+', '', self.guess) # Removes all non-alphanumeric characters from the guess as answers are only alphanumeric.
                self.guess = validated_guess # Updates self.guess.
                guess_text_box.delete(0, END)
                return self.guess, self.get_answer()

    def get_answer(self):
        '''Fetches the answer for the current image'''
        with open("Assets/answer_sheet.txt", 'r') as answers: # Answers are stored in this txt file for organisation and maintenance.
            data = answers.readlines() # Reads the txt file.
            line = data[self.loc_num -1].lower() # Finds the line which the answer is located in (-1 because the txt file is read from line 0 not line 1.
            answers = line.split() # Splits the line up into words (possible answers)
            return answers, self.update_game_state(answers) # Returns the acceptable answers so the self.guess can be processed.

    def update_game_state(self, answers):
        '''Updates the game statistics: Points, Round number, IntVar's (points/time/rnd labels) and handles the correct/incorrect label.'''
        for answer in [answer for answer in answers if answer.lower() in self.guess.lower()]: # Check every possible answer to see if the answer lies within self.guess.         
            if self.rnd == 1:
                self.update_time(root)              
            self.points += self.additive # Add the additive value +3+ on first guess if its correct, +2 on second guess, +1 on all others.
            self.rnd += 1 # Update the round number.
            try:
                self.incorrect.destroy() # Destroys the old incorrect label (if there is one)
            except AttributeError: # If there isn't an incorrect label, do nothing.
                pass
            try:
                self.correct.destroy() # Destroys the old correct label (if there is one)
            except AttributeError:
                pass
            points_val = IntVar(value=self.points) # Sets the points value thats displayed on screen.
            self.correct = Label(root, text="Correct!", bg="#00FFFF", fg='green', font=("Calibri", "20", "bold"))
            self.correct.place(relx=0.5, rely=0.12, anchor=CENTER)
            points_val.set(self.points)
            self.points_label.config(textvariable=points_val)                
            if self.rnd == 11: # There are only 10 rounds in the game, so round 11 means the game is done.
                rnd_val = IntVar(value=self.rnd-1) # Round 11 is actually round 10.
                return self.game_end(root) # Ends the game.
            rnd_val = IntVar(value=self.rnd)                         
            rnd_val.set(self.rnd)
            self.rnd_label.config(textvariable=rnd_val)
            return self.points, self.rnd, self.get_loc(root)
        else: # If the user guessed incorrect.
            try:
                self.correct.destroy()
            except AttributeError:
                pass
            try:
                self.incorrect.destroy()
            except AttributeError:
                pass
            if self.additive > 1: # Additive reductions cap at 1, otherwise the user would get no points or negative points.
                self.additive -= 1
            self.incorrect = Label(root, text="Incorrect!", bg="#00FFFF", fg='darkred', font=("Calibri", "20", "bold"))
            self.incorrect.place(relx=0.5, rely=0.12, anchor=CENTER)
            return self.additive # So points can continue to be reduced if the user keeps guessing wrong on the same round.

    def replay(self, root):
        '''Allows the user to reset the game or play again'''
        if self.continue_timer:
            pass
        else:
            self.continue_timer = True # Stops the timer so the user can start guessing on their own time and restart it.
        try:
            self.game_win.destroy() # If the user wanted to play again and won last game.
        except AttributeError:
            pass
        self.additive = 3 # Default values are set, effectively resetting the game.
        self.points = 0
        self.rnd = 1
        self.time = 0
        try:
            self.correct.destroy() # Clears any correct labels that may be present.
        except AttributeError:
            pass
        try:
            self.incorrect.destroy()
        except AttributeError:
            pass
        self.time_label.config(textvariable=IntVar(value=0), bg='white', fg='black', font=("Calibri", "18", "bold")) # Resets the displayed values on screen to default.
        self.points_label.config(textvariable=IntVar(value=0), fg='black', bg='white', font=("Calibri", "18", "bold"))
        self.rnd_label.config(textvariable=IntVar(value=1), fg='black', bg='white', font=("Calibri", "18", "bold"))
        return self.points, self.rnd, self.additive, self.time, self.continue_timer

    def get_loc(self, root):
        '''Generates a random location image.png and displays it.'''
        self.additive = 3 # Sets the additive value to default
        try:
            self.loc_label.destroy() # Deletes the old image if there is one.
        except AttributeError:
            pass
        loc_generate = r.randint(1, 30)  # Generates a random location img since image names are labeled from one to thirty i.e Loc1.
        self.loc_num = loc_generate # Sets the loc_num so it can be used for getting the answers (number is the same as the line the answers are on -1)
        self.loc_set = f"Loc{loc_generate}"  # Open the location image with that filename.
        self.loc_img = PhotoImage(file=f"Assets/{self.loc_set}.png") # Opens the generated loc img from the assets folder.
        self.img_frame = Frame(root, bg='black', highlightbackground="white", highlightthickness=1)
        self.img_frame.place(relx=0.5, rely=0.4744, anchor=CENTER, relwidth=0.478, relheight=0.63)
        self.loc_label = Label(self.img_frame, image=self.loc_img, bg='white')
        self.loc_label.image = self.loc_img # Keeps a reference image for the image so its not garbage collected by tkinter.
        self.loc_label.place(relx=0.498, rely=0.497, anchor=CENTER, relwidth=1, relheight=0.998)  # Adjusts the image size to fit in the frame.
        return self.loc_num, self.additive

    def skip(self):
        '''Allows the user to skip an image if they don't know it or do not want to guess it'''
        if self.continue_timer == False: # So the user can't skip if the games over.
            pass
        else:
            self.additive = 3
            return self.additive, self.get_loc(root)

    def update_time(self, root):
        '''Updates the users elapsed time independantly from other methods'''
        if self.continue_timer: # While the game is active.
            self.time += 1 # Add 1 second.
            time_val = StringVar()
            time_val.set(str(self.time) + "s") # Updates the displayed time label on screen.
            self.time_label.config(textvariable=time_val, bg='white', fg='black', font=("Calibri", 18, "bold"))
            root.after(1000, lambda: self.update_time(root)) # After each second, recall the method so the time can be updated again.
        else:
            self.process_time() # If the game has ended, process the time.

    def game_end(self, root):
        '''Ends the game'''
        try:
            self.game_win.destroy() # Incase the user has played before.
        except AttributeError:
            pass
        self.game_win = Label(root, text="You Win! Click 'Replay' to play again!", bg="#00FFFF", fg='green', font=("Calibri", "20", "bold"))
        self.game_win.place(relx=0.5, rely=0.12, anchor=CENTER)
        self.continue_timer = False # Stops the timer.
        return self.continue_timer

    def process_time(self):
        '''Processes the elapsed time which determines if the user is eligible for a leaderboard placement'''
        leaderboard_position = 0 # Their current position is 0.
        with open("Assets/leaderboard.txt", 'r') as leaderboard: # Opens the leaderboard txt file where the top five fastest times are recorded.
            lb_data = [line.strip() for line in leaderboard]
            for i, time in enumerate(lb_data): # Checks all times in the leaderboard file.
                if self.time < int(time): # If the time is less than a leaderboard time.
                    lb_data.insert(i, str(self.time)) # Inserts the time.
                    lb_data = lb_data[:5] # Takes the top 5 positions.
                    leaderboard.close()
                    break
                else:
                    leaderboard_position += 1
            with open("Assets/leaderboard.txt", 'w') as leaderboard:
                leaderboard.write('\n'.join(lb_data)) # Writes the positions to the txt file so they can be stored and updated in the txt variables within the lb widget.
                leaderboard.close()
                return self.leaderboard(root)

    def leaderboard(self, root):
        '''Leaderboard'''
        leaderboard_frame = Frame(root, bg='white', width=250, height=300, highlightbackground="black", highlightthickness=5)
        leaderboard_frame.place(relx=0.16, rely=0.587, anchor=CENTER)
        leaderboard_title = Label(root, text="Leaderboard", bg='white', fg='darkblue', font=("Calibri", "20", "bold", "underline"))
        leaderboard_title.place(relx=0.105, rely=0.4)
        leaderboard_pos1_time = StringVar()
        leaderboard_pos2_time = StringVar()
        leaderboard_pos3_time = StringVar()
        leaderboard_pos4_time = StringVar()
        leaderboard_pos5_time = StringVar()
        with open("Assets/leaderboard.txt", 'r') as leaderboard: # Opens the leaderboard txt file where the fastest times are recorded.
            lb_data = [line.strip() for line in leaderboard.readlines()]
            leaderboard_pos1_time.set(str("1st:  " + lb_data[0]) + "s") # Sets the time for position 1 since its the first line in the leaderboard txt file.
            leaderboard_pos2_time.set(str("2nd:  " + lb_data[1]) + "s")
            leaderboard_pos3_time.set(str("3rd:  " + lb_data[2]) + "s")
            leaderboard_pos4_time.set(str("4th:  " + lb_data[3]) + "s")
            leaderboard_pos5_time.set(str("5th:  " + lb_data[4]) + "s")
        leaderboard_pos1_label = Label(root, textvariable=leaderboard_pos1_time, bg='white', fg='black', font=("Calibri", "14", "bold"))
        leaderboard_pos1_label.place(relx=0.09, rely=0.5)
        leaderboard_pos2_label = Label(root, textvariable=leaderboard_pos2_time, bg='white', fg='black', font=("Calibri", "14", "bold"))
        leaderboard_pos2_label.place(relx=0.09, rely=0.55)
        leaderboard_pos3_label = Label(root, textvariable=leaderboard_pos3_time, bg='white', fg='black', font=("Calibri", "15", "bold"))
        leaderboard_pos3_label.place(relx=0.09, rely=0.6)
        leaderboard_pos4_label = Label(root, textvariable=leaderboard_pos4_time, bg='white', fg='black', font=("Calibri", "15", "bold"))
        leaderboard_pos4_label.place(relx=0.09, rely=0.65)
        leaderboard_pos5_label = Label(root, textvariable=leaderboard_pos5_time, bg='white', fg='black', font=("Calibri", "15", "bold"))
        leaderboard_pos5_label.place(relx=0.09, rely=0.7)
        leaderboard.close()

instance = Game() # Creates the object.
def quit(root):
    '''Quits the game: closes the GUI'''
    root.destroy()

# G.U.I
root = Tk() # Initialises the window.
root.resizable(False, False) # Locks the window size to prevent re-sizing.
root.state('zoomed') # Makes the window fullscreen.
root.title("Howick College GeoGuesser V3.0")
root.configure(background='#00FFFF') # Aqua coloured background.
title_banner = Frame(root, bg="#03055B", height=50)
title_banner.pack(fill="x")
title = Label(root, text="Howick College GeoGuesser 2024", bg='#03055B', fg='white', font=("Calibri", "30", "bold"))
title.place(relx=0.5, rely=0.03, anchor=CENTER)

'''Get Guess Widgets'''
guess = StringVar() # Initialises the EntryBox as a string variable so I can get their guesses.
guess_text_box = Entry(root, textvariable=guess, width=35, highlightbackground="black", highlightthickness="1", font=("Calibiri", "11"))
guess_text_box.place(relx=0.5, rely=0.9, anchor=CENTER)
guess_text_box_label = Label(root, text="Location:", fg="black", bg='#00FFFF', font=("Calibri", "20", "bold"))
guess_text_box_label.place(relx=0.347, rely=0.898, anchor=CENTER)

'''Buttons'''
guess_btn = Button(root, text="Guess", borderwidth="2", width="13", bg='lime', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.get_guess(root))
guess_btn.place(relx=0.689, rely=0.83, anchor=CENTER)
quit_btn = Button(root, text="Quit", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:quit(root))
quit_btn.place(relx=0.311, rely=0.83, anchor=CENTER)
replay_btn = Button(root, text="Replay", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.replay(root))
replay_btn.place(relx=0.41, rely=0.83, anchor=CENTER)
skip_btn = Button(root, text="Skip", borderwidth="2", width="13", bg='red', fg='black', font=("Calibri", "15", "bold"),command=lambda:instance.skip())
skip_btn.place(relx=0.5, rely=0.83, anchor=CENTER)

'''How to play Frame'''
how_to_play_frame = Frame(root, bg='white', width=340, height=469, highlightbackground="black", highlightthickness=5)
how_to_play_frame.place(relx=0.875, rely=0.474, anchor=CENTER)
how_to_play_title = Label(root, fg="darkblue", bg='white', text="How to play?", font=("Calibri", "20", "bold", "underline"))
how_to_play_title.place(relx=0.87, rely=0.194, anchor=CENTER)
how_to_play_text = Label(root, bg='white', fg="black", text="\n- Type your guess in the 'location' box\n\n- Ensure that you use correct grammar and clear guesses.\n\n- Gather as many points as possible by guessing correctly!\n\n- Use the buttons below to skip, quit, reset and guess.\n\n- There are 10 rounds, but there are 30 points to get! \n\n +3 points if you guess a location first try, +2 on second try! \n\n- Any more guesses give +1, so good luck and have fun! \n\n- Also there is a timer, try and guess as fast as possible!")
how_to_play_text.place(relx=0.872, rely=0.38, anchor=CENTER)
how_to_play_text.config(state='disabled')

'''Game Stats Frame'''
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
time_text = Label(root, text="Time:", bg='white', fg='black', font=("Calibri", "18", "bold"))
time_text.place(relx=0.098, rely=0.3, anchor=CENTER)
instance.time_label = Label(root, textvariable=IntVar(value=0), bg='white', fg='black', font=("Calibri", "18", "bold"))
instance.time_label.place(relx=0.14, rely=0.3, anchor=CENTER)
'''Start Game'''
instance.leaderboard(root)
instance.get_loc(root) # Calls the get_loc method to display a location image.
root.mainloop() # Starts the GUI event loop.
# AS91907 - Howick College GeoGuesser
# Written By: Evan Lightfoot
# Date: 5/08/2024
# Version: 3
import random as r
import re
from tkinter import *
class Game:
    # Constants
    max_characters = 13 # Caps the guess length for user experience so they stick to short, rapid fire guesses.
    max_rounds = 11 # There are 10 rounds, but the game starts at round 1 which is actually round 0 but is shown as round 11.
    time_increment = 1000 # 1000ms == 1s
    num_of_images = 30 # There are 30 images that the program will cycle through.
    max_points = 30 # There are a maximum of 30 points available.
    additive_penalty = 1 # Minus one point if the user guesses incorrectly (caps at one point)
    max_time = 1000 # Stops the game after 15 minutes as the user is likely not playing anymore. The game is expected to take 3 minutes or less and stopping will save resources.
    
    # Instance Variables
    def __init__(self, loc_num=None, points=0, additive=3, rnd=1, guess=None, time=0, output_msg=None): # Defines and sets the attribute states.
        '''Defines the instance variables which are frequently calculated, updated or returned as derived values'''
        self.loc_num = loc_num # The image name and therefore the line the answers to that image are located.
        self.guess = guess # The users guess.
        self.additive = additive # 3 points on first guess if correct, 2 points on second guess, 1 point all others.
        self.points = points # Amount of points the user has.
        self.rnd = rnd # The current round (rnd) number since there are 10 rounds.
        self.time = time # The users elapsed game time.
        self.output_msg = None # This is dynamically updated according to the intended output message.
        self.continue_timer = True # Will end the game if set to false.

    def start_game(self, root):
        if self.rnd == self.max_rounds:
            pass
        elif self.time == 0:
            self.update_time(root)
        self.get_guess(root)
        
    def get_guess(self, root):
        '''Fetches the guess from the guess_text_box entry box and validates it by removing
        numbers, special characters, punctuation and spaces as no answers include these attributes.'''
        self.guess = guess.get().replace(' ', '') # Removes all spaces from the guess.
        if self.guess == '': # If the user didn't enter anything but submitted their guess, do not proceed.
            self.clear_labels(root)
            output_text = Label(output_msg_frame, text='Type in the guess box below!', bg='aqua', fg='darkred', font=('Calibri', '20', 'bold'))
            self.output_msg = output_text # Sets the output message, this is more robust than creating a new label each time.
            self.output_msg.pack()
        elif len(self.guess) > self.max_characters: # If the users guess is more than 13 letters.
            self.clear_labels(root)
            output_text = Label(output_msg_frame, text='Your guess is too long, most answers are around 5 to 13 letters.', bg='aqua', fg='darkred', font=('Calibri', '20', 'bold'))
            self.output_msg = output_text
            self.output_msg.pack()
            guess_text_box.delete(0, END) # Clears the guess box of any text so the user may guess again.
        else:
            self.clear_labels(root)
            validated_guess = re.sub('[^A-Za-z0-9]+', '', self.guess) # Removes all non-alphanumeric characters from the guess as answers are only alphanumeric.
            self.guess = validated_guess # Updates the self.guess so it can be processed in update_game_state()
            guess_text_box.delete(0, END)
            return self.guess, self.get_answer()

    def get_answer(self):
        '''Fetches the answer for the current image from the answer_sheet text file.'''
        with open('Assets/answer_sheet.txt', 'r') as answers:
            data = answers.readlines() # Reads the text file.
            line = data[self.loc_num -1].lower() # Finds the line which the answer is located in (the '-1' is because the text file is read from line 0 instead of line 1)
            answers = line.split() # Splits the line up into words, i.e. All of the possible answers.
            return answers, self.update_game_state(answers) # Returns all of the potential answers so the guess can be marked as correct/incorrect in update_game_state()

    def update_game_state(self, answers):
        '''Updates the game statistics: Points and round number on correct guess and outputs whether the user was correct or not.'''
        for answer in [answer for answer in answers if answer.lower() in self.guess.lower()]: # For every answer in the file, check if the answer lies within the guess.           
            self.points += self.additive # Adds the additive value '+3' on first guess if its correct, +2 on second guess and +1 on all others to the total points.
            self.rnd += 1 # Updates the round number.
            self.clear_labels(root)
            output_text = Label(output_msg_frame, text='Correct!', bg='aqua', fg='green', font=('Calibri', '20', 'bold'))
            self.output_msg = output_text
            self.output_msg.pack()
            points_val = IntVar(value=self.points)  
            points_val.set(self.points) # Sets the displayed points value.
            self.points_label.config(textvariable=points_val)                
            if self.rnd == self.max_rounds: # Game is over since its round 10.
                rnd_val = IntVar(value=self.rnd-1) # Round 11 is actually round 10 since 'round 0' is round 1.
                return self.game_end(root) # Ends the game.
            rnd_val = IntVar(value=self.rnd)                         
            rnd_val.set(self.rnd)
            self.rnd_label.config(textvariable=rnd_val)
            return self.points, self.rnd, self.get_loc(root)
        else: # If the user guessed incorrectly.
            self.clear_labels(root)
            if self.additive > 1: # Additive reductions cap at 1, otherwise the user would get no points or negative points.
                self.additive -= self.additive_penalty
            output_text = Label(output_msg_frame, text='Incorrect!', bg='aqua', fg='darkred', font=('Calibri', '20', 'bold'))
            self.output_msg = output_text
            self.output_msg.pack()
            return self.additive # So points can continue to be reduced if the user keeps guessing wrong on the same round.

    def replay(self, root):
        self.continue_timer = False
        '''Allows the user to replay the game by resetting all variables to their default values.'''
        self.clear_labels(root)
        self.additive = 3
        self.points = 0
        self.rnd = 1
        self.time = 0
        self.clear_labels(root) # Clears any existing labels.
        self.time_label.config(textvariable=IntVar(value=0), bg='white', fg='black', font=('Calibri', '18', 'bold')) # Resets the displayed values on screen to default.
        self.points_label.config(textvariable=IntVar(value=0), fg='black', bg='white', font=('Calibri', '18', 'bold'))
        self.rnd_label.config(textvariable=IntVar(value=1), fg='black', bg='white', font=('Calibri', '18', 'bold'))
        return self.points, self.rnd, self.additive, self.time, self.continue_timer

    def get_loc(self, root):
        '''Fetches a random image from the assets folder and displays it.'''
        self.additive = 3 # Sets the additive value to default
        try:
            self.loc_label.destroy() # Deletes the existing image if there is one.
        except AttributeError:
            pass
        loc_generate = r.randint(1, self.num_of_images)  # Generates a random img value since image names are labeled from one to thirty (num_of_images) e.g. Loc12.
        self.loc_num = loc_generate # Sets the value to loc_num so it can be used for getting the answers (number is the same as the line the answers are on -1)
        loc_set = f'Loc{loc_generate}'  # Creates the filename.
        self.loc_img = PhotoImage(file=f'Assets/{loc_set}.png') # Opens the file from the assets folder.
        self.loc_label = Label(img_frame, image=self.loc_img, bg='white')
        self.loc_label.image = self.loc_img # Keeps a reference image for the image so it is not garbage collected by tkinter.
        self.loc_label.pack()  # Adjusts the image size to fit within the frame.
        return self.loc_num, self.additive

    def skip(self):
        '''Allows the user to skip if they don't know where an image is or do not want to guess it'''
        if self.continue_timer == False: # Disables skipping if the game is over.
            pass
        else:
            self.additive = 3
            return self.additive, self.get_loc(root)

    def update_time(self, root):
        '''Updates the users elapsed time independantly from other methods'''
        if self.time == self.max_time:
            root.destroy()
        else:
            if self.continue_timer: # While the game is active.
                self.time += (self.time_increment / self.time_increment) # Adds the time increment to the elapsed time.
                time_val = StringVar()
                time_val.set(str(self.time) + 's') # Updates the displayed time on screen.
                self.time_label.config(textvariable=time_val, bg='white', fg='black', font=('Calibri', '18', 'bold'))
                root.after(self.time_increment, lambda: self.update_time(root)) # Recall the method again so the time can be updated continuously each second.
            else:  # If the game has ended, process the time.
                if self.rnd == self.max_rounds:
                    self.process_time()
                else:
                    self.continue_timer = True
 
    def game_end(self, root):
        '''Ends the game by disabling the buttons and stopping the timer'''
        self.clear_labels(root)
        output_text = Label(output_msg_frame, text='You Win! Click Replay to play again!', bg='aqua', fg='green', font=('Calibri', '20', 'bold'))
        self.output_msg = output_text
        self.output_msg.pack()
        self.continue_timer = False # Stops the timer since it will only recall if continue_timer == True.
        return self.continue_timer

    def process_time(self):
        '''Processes the elapsed time which determines if the user is eligible for a leaderboard placement'''
        with open('Assets/leaderboard.txt', 'r') as leaderboard: # Opens the leaderboard txt file where the top five fastest times are recorded.
            lb_data = [time.strip() for time in leaderboard] # Reads the times in the file.
            split_lb_data = [time for time in lb_data]
            for i, time in enumerate(split_lb_data):
                if self.time < float(time):
                    lb_data.insert(i, str(self.time)) # Take hold of the old times position.
                    lb_data.pop(5)
                    break
        with open('Assets/leaderboard.txt', 'w') as leaderboard:
            leaderboard.write('\n'.join(lb_data)) # Writes the new time to the txt file so it can be displayed and stored for the future.
            leaderboard.close()
            return self.get_leaderboard(root)

    def get_leaderboard(self, root):
        '''Leaderboard widgets'''
        with open('Assets/leaderboard.txt', 'r') as leaderboard: # Opens the leaderboard txt file where the fastest times are recorded.
            lb_data = [line.strip() for line in leaderboard.readlines()]
            leaderboard_pos1_time.set(str('1st:   ' + lb_data[0]) + 's') # Sets the time for positions from the text file.
            leaderboard_pos2_time.set(str('2nd:  ' + lb_data[1]) + 's')
            leaderboard_pos3_time.set(str('3rd:  ' + lb_data[2]) + 's')
            leaderboard_pos4_time.set(str('4th:  ' + lb_data[3]) + 's')
            leaderboard_pos5_time.set(str('5th:  ' + lb_data[4]) + 's')
        leaderboard_pos1_label.configure(textvariable=leaderboard_pos1_time, bg='white', fg='black', font=('Calibri', '18', 'bold'))
        leaderboard_pos2_label.configure(textvariable=leaderboard_pos2_time, bg='white', fg='black', font=('Calibri', '18', 'bold'))
        leaderboard_pos3_label.configure(textvariable=leaderboard_pos3_time, bg='white', fg='black', font=('Calibri', '18', 'bold'))
        leaderboard_pos4_label.configure(textvariable=leaderboard_pos4_time, bg='white', fg='black', font=('Calibri', '18', 'bold'))
        leaderboard_pos5_label.configure(textvariable=leaderboard_pos5_time, bg='white', fg='black', font=('Calibri', '18', 'bold'))
        leaderboard.close()
    
    def clear_labels(self, root):
        try:
            self.output_msg.destroy() # Deletes the old label if there is one as it is no longer needed.
        except AttributeError: # If there is no label, do not do anything.
            pass
        
instance = Game() # Creates the object.
def quit(root):
    '''Quits the game: closes the GUI'''
    root.destroy()

'''G.U.I'''
# Main Configuration
root = Tk() # Opens the window (GUI)
root.resizable(False, False) # Locks the window size to prevent re-sizing which could make the program unplayable.
root.state('zoomed') # Makes the window fullscreen so everything can be displayed on the GUI.
root.title('Howick College GeoGuesser V3.0') # Program title.
root.configure(background='aqua') # Aqua coloured background.
title_banner = Frame(root, bg='#03055B', height=10)
title_banner.pack(fill='x')
title = Label(title_banner, text='Howick College GeoGuesser 2024', bg='#03055B', fg='#d3b846', font=('Calibri', '30', 'bold'))
title.pack(pady=5)
output_msg_frame = Frame(root, bg='aqua')
output_msg_frame.pack(anchor='n')
space_placeholder = Label(output_msg_frame, text='\n\n', bg='aqua')
space_placeholder.pack(side='right')
main_frame = Frame(root, bg='aqua')
main_frame.pack(pady=(0, 0))

# Leaderboard Set Up
leaderboard_frame = Frame(main_frame, bg='white', width=250, height=300, highlightbackground='black', highlightthickness=2)
leaderboard_frame.pack(side='left', anchor='nw', pady=5, padx=1)
leaderboard_pos1_time = StringVar()
leaderboard_pos2_time = StringVar()
leaderboard_pos3_time = StringVar()
leaderboard_pos4_time = StringVar()
leaderboard_pos5_time = StringVar()
leaderboard_title = Label(leaderboard_frame, text='Leaderboard', bg='white', fg='darkblue', font=('Calibri', '20', 'bold', 'underline'))
leaderboard_title.pack()
leaderboard_pos1_label = Label(leaderboard_frame)
leaderboard_pos1_label.pack(side='top', anchor='nw')
leaderboard_pos2_label = Label(leaderboard_frame)
leaderboard_pos2_label.pack(side='top', anchor='nw')
leaderboard_pos3_label = Label(leaderboard_frame)
leaderboard_pos3_label.pack(side='top', anchor='nw')
leaderboard_pos4_label = Label(leaderboard_frame)
leaderboard_pos4_label.pack(side='top', anchor='nw') 
leaderboard_pos5_label = Label(leaderboard_frame)
leaderboard_pos5_label.pack(side='top', anchor='nw')   

# Guess Widgets
guess = StringVar() # Initialises the entry box as a string variable so I can get the users guess.
guess_text_box = Entry(root, textvariable=guess, width=35, highlightbackground='black', highlightthickness='1', font=('Calibiri', '15'))
guess_text_box.pack(side='bottom', pady=(0, 20))
guess_text_box_label = Label(root, text='Guess:', fg='black', bg='aqua', font=('Calibri', '20', 'bold'))
guess_text_box_label.pack(side='bottom', padx=5)

# Buttons
button_frame = Frame(main_frame, bg='aqua')
button_frame.pack(side='bottom', anchor='s', ipadx=72, pady=(0, 20))
quit_btn = Button(button_frame, text='Quit', borderwidth='2', width='13', bg='red', fg='black', font=('Calibri', '15', 'bold'),command=lambda:quit(root))
quit_btn.pack(side='left')
replay_btn = Button(button_frame, text='Replay', borderwidth='2', width='13', bg='red', fg='black', font=('Calibri', '15', 'bold'),command=lambda:instance.replay(root))
replay_btn.pack(side='left')
skip_btn = Button(button_frame, text='Skip', borderwidth='2', width='13', bg='red', fg='black', font=('Calibri', '15', 'bold'),command=lambda:instance.skip())
skip_btn.pack(side='left')
submit_btn = Button(button_frame, text='Submit', borderwidth='2', width='13', bg='lime', fg='black', font=('Calibri', '15', 'bold'),command=lambda:instance.start_game(root))
submit_btn.pack(side='left', padx=(78, 0))

# How to play Frame
how_to_play_frame = Frame(main_frame, bg='white', width=340, height=500, highlightbackground='black', highlightthickness=2)
how_to_play_frame.pack(side='right', anchor='ne', pady=5)
how_to_play_title = Label(how_to_play_frame, fg='darkblue', bg='white', text='How to play?', font=('Calibri', '20', 'bold', 'underline'))
how_to_play_title.pack()
how_to_play_text = Label(how_to_play_frame, bg='white', fg='black', text='\n- Type your guess in the Guess box\n\n- Ensure that you use correct grammar.\n\n- Use the buttons below to skip, quit, replay and guess.\n\n- There are 10 rounds, but there are 30 points to get! \n\n +3 points if you guess on your first try, +2 on second try! \n\n- Correct guesses after two tries give +1 point \n\n- Gather as many points as you can by guessing correctly!\n\n- Also there is a timer, try and guess as fast as possible!\n\n-Good luck and have fun!')
how_to_play_text.pack()
crest_img = PhotoImage(file='Assets/crest.png')
crest_img_label = Label(how_to_play_frame, image=crest_img, bg='white')
crest_img_label.pack(side='right')

# Game Stats Frame
game_stats_frame = Frame(main_frame, bg='white', width=170, height=176.3, highlightbackground='black', highlightthickness=2)
game_stats_frame.pack(side='left', anchor='nw', pady=5, ipady=20.5) # Packs the frame to the top left of the main_frame
game_stats_frame.pack_propagate(False) # Prevents the game_stats_frame from resizing at round 10 to accomodate space for the extra digit as this disalignes all the widgets.
game_stats_header = Label(game_stats_frame, text='Game Stats', bg='white', fg='darkblue', font=('Calibri', '20', 'bold', 'underline'))
game_stats_header.pack(side='top', anchor='w')

# Rnd Widgets
rnd_frame = Frame(game_stats_frame, bg='white')
rnd_frame.pack(side='top', fill='x', anchor='nw')
rnd_header = Label(rnd_frame, text='Round:', bg='white', fg='black', font=('Calibri', '18', 'bold'))
rnd_header.pack(side='left', anchor='nw')
instance.rnd_label = Label(rnd_frame, textvariable=IntVar(value=1), bg='white', fg='black', font=('Calibri', '18', 'bold'))
instance.rnd_label.pack(side='left')
rnd_separator = Label(rnd_frame, text='/', bg='white', fg='black', font=('Calibri', '18', 'bold'))
rnd_separator.pack(side='left')
total_rnd = instance.max_rounds - 1
total_rnd_var = IntVar()
total_rnd_var.set(total_rnd)
total_rnd_text = Label(rnd_frame, textvariable=total_rnd_var, bg='white', fg='black', font=('Calibri', '18', 'bold'))
total_rnd_text.pack(side='left')

# Points Widgets
points_frame = Frame(game_stats_frame, bg='white')
points_frame.pack(side='top', fill='x', anchor='nw')
points_header = Label(points_frame, text='Points:', bg='white', fg='black', font=('Calibri', '18', 'bold'))
points_header.pack(side='left')
instance.points_label = Label(points_frame, textvariable=IntVar(value=0), bg='white', fg='black', font=('Calibri', '18', 'bold'))
instance.points_label.pack(side='left')
points_separator = Label(points_frame, text='/', bg='white', fg='black', font=('Calibri', '18', 'bold'))
points_separator.pack(side='left')
total_points_var = IntVar()
total_points_var.set(instance.max_points)
total_points = Label(points_frame, textvariable=total_points_var, bg='white', fg='black', font=('Calibri', '18', 'bold'))
total_points.pack(side='left')

# Time Widgets
time_frame = Frame(game_stats_frame, bg='white')
time_frame.pack(side='top', fill='x', anchor='nw')
time_header = Label(time_frame, text='Time:', bg='white', fg='black', font=('Calibri', '18', 'bold'))
time_header.pack(side='left')
instance.time_label = Label(time_frame, textvariable=IntVar(value=0), bg='white', fg='black', font=('Calibri', '18', 'bold')) # The starting time is 0s.
instance.time_label.pack(side='left')

# On game start
instance.get_leaderboard(root)
img_frame = Frame(main_frame, bg='black', highlightbackground='black', highlightthickness=2)
img_frame.pack(side='top', anchor='center', padx=2, pady=(5, 0))
instance.get_loc(root) # Calls the get_loc method to display a location image.
root.mainloop() # Starts the GUI event loop.    
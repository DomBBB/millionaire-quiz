import html # comment
import tkinter as tk
import tkinter.font as font

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PIL import ImageTk

from wwm_gamelogic import Quiz

import wwm_ui


###############################################################################
# This code acts as bridge between the user and the game logic. This means that
# it creates a user interface with tkinter in which the user can play the game
# and it handles all necessary calls to the Quiz interface of wwm_gamelogic.
# It also uses the helper functions from wwm_ui to set the properties and
# define the layout of the tkinter window.
###############################################################################
class QuizApp(tk.Tk):
    """
    This class creates the tkinter window and uses the imported functions to
    show a proper user interface through which the user can play the game. It
    therefore also contains all logic needed to show questions and control the
    code flow according to the inputs (which buttons were pressed) from the
    user.
    """
    def __init__(self):
        """
        This method initializes a new tkinter window, sets its properties,
        retrieves all images for the jokers and switches to the starting page.
        """
        # Initializes the tkinter window.
        tk.Tk.__init__(self)
        # Sets the tkinter window properties.
        wwm_ui.setup_window_properties(self)

        # Retrieves the images for the jokers.
        files = wwm_ui.store_images()
        # The images need to be stored as global variables because pythons
        # garbage collecting creates a bug when trying to display an image
        # in a tkinter window. See: https://stackoverflow.com/questions/
        # 16424091/why-does-tkinter-image-not-show-up-if-created-in-a-function
        for key, value in files.items():
            # A unique name is used so it does not overwrite another variable
            # that were already used in the code.
            globals()["initialized__file__" + key] = ImageTk.PhotoImage(value)

        # Uses the change_page function to switch to the "start" page.
        self.change_page("start")

    def change_page(self, page):
        """
        This method handles switching to other pages. It deletes all existing
        widgets (frames, labels, buttons, ...) in order to display the page it
        switches to properly.
        """
        # Destroys all existing widgets (frames, labels, buttons, ...).
        for widget in self.winfo_children():
            widget.destroy()
        # Dictionary to track what function corresponds to the parameter
        # "page".
        pages = {
                "start": self.startPage,
                "game": self.gamePage,
                "result": self.resultPage
        }
        # Executes the function that belongs to the given parameter "page".
        # This therefore executes either startPage(), gamePage() or
        # resultPage() that can all be found below.
        pages[page]()

    def startPage(self):
        """
        This method starts a new game and displays a starting page with some
        information about the game.
        """
        # Initializes a new Quiz object to start a new game and queries for its
        # status.
        self.quiz = Quiz()
        status = self.quiz.status()

        # Creates the tkinter layout for the starting page.
        main_top_1, main_top_2, main_top_3, main_bottom, sidebar_jokers,\
            sidebar_winnings = wwm_ui.page_layout(self, "start")

        #######################################################################
        # MAIN TOP:
        # Displays information about the game rules.
        #######################################################################
        # Defines the text that should be displayed.
        display_text = "Who wants to be a millionaire?"
        # Displays the defined test.
        tk.Label(
            main_top_1,
            text=display_text, wraplength=600,
            font=font.Font(family="Helvetica", size=20)
        ).grid(row=0, column=0)
        display_text = "".join([
            "Each question you answer correctly lets you ",
            "take home more money. But beware, if you give an incorrect ",
            "answer you might lose everything.\n\n If you struggle with a ",
            "question you can always surrender and take home the money you ",
            "already won. You can also use one of three jokers that might "
            "help you with your answer. Or you can risk falling back on the ",
            "security levels from question 5 or 10."])
        tk.Label(
            main_top_2,
            text=display_text, wraplength=600,
            font=font.Font(family="Helvetica", size=16)
        ).grid(row=0, column=0)
        display_text = "Good Luck!"
        tk.Label(
            main_top_3,
            text=display_text, wraplength=600,
            font=font.Font(family="Helvetica", size=20)
        ).grid(row=0, column=0)

        #######################################################################
        # MAIN BOTTOM:
        # Displays the button to start a new game.
        #######################################################################
        tk.Button(
            main_bottom, text="Start New Game", width=40,
            font=font.Font(family="Helvetica", size=20),
            command=lambda: self.change_page("game")
        ).grid(row=0, column=0)

        #######################################################################
        # SIDEBAR JOKERS:
        # Displays the joker pictures.
        #######################################################################
        # Sets the default names for each not crossed picture.
        files = ["initialized__file__5050",
                 "initialized__file__audience",
                 "initialized__file__phone"]
        # If the joker has already been used the crossed picture of this joker
        # is used.
        if "50:50 Joker" not in status["jokers"]:
            files[0] += "_crossed"
        if "Audience Joker" not in status["jokers"]:
            files[1] += "_crossed"
        if "Phone Joker" not in status["jokers"]:
            files[2] += "_crossed"
        # Due to the garbage collecting bug (explained in the init method) the
        # correct image is retrieved from the global variables and displayed.
        for index, file in enumerate(files):
            img = globals()[file]
            if index == 0:
                tk.Label(sidebar_jokers, image=img).grid(row=1, column=0)
            elif index == 1:
                tk.Label(sidebar_jokers, image=img).grid(row=0, columnspan=2)
            else:
                tk.Label(sidebar_jokers, image=img).grid(row=1, column=1)

        #######################################################################
        # SIDEBAR WINNINGS:
        # Displays all possible winnings.
        #######################################################################
        # Retrieves all winnings and stores them in a new list.
        winnings = status["winnings"][:]
        # Ensures that the winnings are always centered and big enough to
        # make borders around each label look good.
        modified_winnings = []
        for win in winnings:
            modified_winnings.append(" " * ((30 - len(win))//2) + win +
                                     " " * ((30 - len(win))//2))
        # Placeholder label to position the winnings labels properly.
        tk.Label(
            sidebar_winnings, text=" "*30, borderwidth=2,
            font=font.Font(family="Helvetica", size=14)
        ).grid(row=0, column=0)
        # Displays each winning amount.
        for index, winning in enumerate(modified_winnings):
            tk.Label(
                sidebar_winnings, text=winning, borderwidth=2,
                font=font.Font(family="Helvetica", size=14)
            ).grid(row=index+1, column=0)

    def gamePage(self):
        """
        This method displays a new question and the possible answers and
        contains all ui logic for a question so that the player can interact
        with the game.
        """
        # Queries the Quiz object for its status.
        status = self.quiz.status()
        state = status["state"]

        # Checks the current state of the game and either changes to the result
        # page (if path) or executes the game logic (else path).
        if state != "playing":
            self.change_page("result")
        else:
            ###################################################################
            # STATIC PART OF THE CODE (does not change during one question)
            ###################################################################

            # Creates the tkinter layout for the game page.
            main_top, sidebar_jokers, sidebar_winnings, main_top_1, \
                main_graph_l, main_graph_2, main_top_3, main_top_4, \
                main_bottom_1, main_bottom_2 = wwm_ui.page_layout(self, "game")

            ###################################################################
            # MAIN TOP - STATIC:
            # Retrieves a new question and displays it.
            ###################################################################
            # Retrieve a new question.
            questionobj, question, answers, tips = self.quiz.ask_question()
            # Display the question without html escape characters.
            tk.Label(
                main_top_1, text=html.unescape(question), wraplength=600,
                font=font.Font(family="Helvetica", size=18)
            ).grid(row=0, column=0)

            ###################################################################
            # MAIN BOTTOM - STATIC:
            # Displays all buttons that are used to play the game (give an
            # answer / use a joker / surrender). The answer and joker buttons
            # can be modified dynamically later on to disable them.
            ###################################################################
            # Displays the surrender button so a player can surrender and take
            # the payout from the last question he answered correctly.
            tk.Button(
                main_bottom_2, width=25, height=2, wraplength=190,
                text=f"Surrender and take: {status['current_payout']}",
                font=font.Font(family="Helvetica", size=12),
                # The variable control_var makes the code wait with
                # execution (after creating and displaying all labels)
                # until it is set by clicking e.g. this button. setattr()
                # then sets a new instance attribute to store the
                # answer in.
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, "__surrender"))]
            ).grid(row=0, column=0)

            # Stores all joker buttons so they can be modified in the dynamic
            # part of the code.
            buttons_jokers = []
            # Displays the joker buttons so that a player can use a joker.
            buttons_jokers.append(tk.Button(
                main_bottom_1, width=15, height=1,
                text="50:50 Joker",
                font=font.Font(family="Helvetica", size=12),
                # The variable control_var makes the code wait with
                # execution (after creating and displaying all labels)
                # until it is set by clicking e.g. this button. setattr()
                # then sets a new instance attribute to store the
                # answer in.
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, "__joker_50:50"))]))
            buttons_jokers.append(tk.Button(
                main_bottom_1, width=15, height=1,
                text="Audience Joker",
                font=font.Font(family="Helvetica", size=12),
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, "__joker_audience"))]))
            buttons_jokers.append(tk.Button(
                main_bottom_1, width=15, height=1,
                text="Phone Joker",
                font=font.Font(family="Helvetica", size=12),
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, "__joker_phone"))]))
            # Positions the buttons.
            for index, button in enumerate(buttons_jokers):
                if index == 0:
                    button.grid(row=1, column=0)
                elif index == 1:
                    button.grid(row=0, columnspan=2)
                else:
                    button.grid(row=1, column=1)

            # Stores all answer buttons so they can be modified in the dynamic
            # part of the code.
            buttons_answers = []
            # Displays the answer buttons without html escape characters so
            # that a player can select his answers.
            buttons_answers.append(tk.Button(
                main_top_3, width=25, height=3,
                text="A: " + html.unescape(answers[0]), wraplength=200,
                font=font.Font(family="Helvetica", size=12),
                # The variable control_var makes the code wait with
                # execution (after creating and displaying all labels)
                # until it is set by clicking e.g. this button. setattr()
                # then sets a new instance attribute to store the
                # answer in.
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, answers[0]))]))
            buttons_answers.append(tk.Button(
                main_top_4, width=25, height=3,
                text="B: " + html.unescape(answers[1]), wraplength=200,
                font=font.Font(family="Helvetica", size=12),
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, answers[1]))]))
            buttons_answers.append(tk.Button(
                main_top_3, width=25, height=3,
                text="C: " + html.unescape(answers[2]), wraplength=200,
                font=font.Font(family="Helvetica", size=12),
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, answers[2]))]))
            buttons_answers.append(tk.Button(
                main_top_4, width=25, height=3,
                text="D: " + html.unescape(answers[3]), wraplength=200,
                font=font.Font(family="Helvetica", size=12),
                command=lambda: [
                    control_var.set(True),
                    setattr(
                        self, "evaluation",
                        self.quiz.evaluate_answer(
                            questionobj, answers[3]))]))
            # Positions the buttons.
            for index, button in enumerate(buttons_answers):
                if index in (0, 1):
                    r = 0
                else:
                    r = 1
                button.grid(row=r, column=0)

            ###################################################################
            # SIDEBAR WINNINGS - STATIC:
            # Displays all possible winnings.
            ###################################################################
            # Retrieves all winnings and stores them in a new list.
            winnings = status["winnings"][:]
            # Ensures that the winnings are always centered and big enough to
            # make borders around each label look good.
            modified_winnings = []
            for win in winnings:
                modified_winnings.append(" " * ((30 - len(win))//2) + win +
                                         " " * ((30 - len(win))//2))
            # Placeholder label to position the winnings labels properly.
            tk.Label(
                sidebar_winnings, text=" "*30, borderwidth=2,
                font=font.Font(family="Helvetica", size=14)
            ).grid(row=0, column=0)
            # Displays each winning amount.
            for index, winning in enumerate(modified_winnings):
                label = tk.Label(
                    sidebar_winnings, text=winning, borderwidth=2,
                    font=font.Font(family="Helvetica", size=14))
                label.grid(row=index+1, column=0)
                # Queries the current round
                c_round = status["round"]
                # Accentuates for which winning the player was playing.
                if c_round-1 == index:
                    label["relief"] = "ridge"
                # Accentuates the safety nets in the winnings that the player
                # reached.
                if c_round > 10 and index == 9:
                    label["fg"] = "green"
                elif c_round > 5 and c_round <= 10 and index == 4:
                    label["fg"] = "green"

            ###################################################################
            # DYNAMIC PART OF THE CODE (changes during one question)
            ###################################################################

            # Stores all tips from the jokers so that multiple jokers can be
            # used for one question.
            previous_tips = []

            # This loop makes the player stay on the same game page until an
            # answer (answer / joker / surrender) was given for this question.
            while True:
                # Queries the Quiz object for its status.
                status = self.quiz.status()

                ###############################################################
                # MAIN BOTTOM - DYNAMIC:
                # If a joker that was created in the "MAIN BOTTOM - STATIC"
                # part has already been used in this game, its button gets
                # disabled meaning it can not be clicked anymore.
                ###############################################################
                for button in buttons_jokers:
                    if button["text"] not in status["jokers"]:
                        button["state"] = "disabled"

                ###############################################################
                # SIDEBAR JOKERS - DYNAMIC:
                # Displays either the normal or the crossed out image for the
                # joker depending on whether the joker has already been used
                # in this game or not.
                ###############################################################
                # Tracks all joker images to be able to delete and reinitialize
                # them after a joker has been used for this question. This is
                # necessary because tkinter can not overwrite the images which
                # would result in unintended displaying issues.
                joker_labels = []
                # Sets the default names for each not crossed picture.
                files = ["initialized__file__5050",
                         "initialized__file__audience",
                         "initialized__file__phone"]
                # If the joker has already been used the crossed picture of
                # this joker is used.
                if "50:50 Joker" not in status["jokers"]:
                    files[0] += "_crossed"
                if "Audience Joker" not in status["jokers"]:
                    files[1] += "_crossed"
                if "Phone Joker" not in status["jokers"]:
                    files[2] += "_crossed"
                #  Due to the garbage collecting bug (explained in the init
                # method) the correct image is retrieved from the global
                # variables and displayed.
                for index, file in enumerate(files):
                    img = globals()[file]
                    if index == 0:
                        label = tk.Label(sidebar_jokers, image=img)
                        label.grid(row=1, column=0)
                    elif index == 1:
                        label = tk.Label(sidebar_jokers, image=img)
                        label.grid(row=0, columnspan=2)
                    else:
                        label = tk.Label(sidebar_jokers, image=img)
                        label.grid(row=1, column=1)
                    joker_labels.append(label)

                ###############################################################
                # ANSWER PARSING
                ###############################################################
                # Tracks the fifty-fifty joker because this joker only disables
                # buttons and does not update the other possibly shown tips.
                fifty_fifty = False

                # This code is executed when the fifty-fifty joker is chosen.
                if tips == "fifty-fifty":
                    # Setting the tracking variable to True ensures that
                    # (possible) previous tips are not updated.
                    fifty_fifty = True
                    # Deletes all already existing answer buttons. This is
                    # necessary because tkinter can not overwrite the labels
                    # which would result in unintended displaying issues.
                    for button in buttons_answers:
                        button.destroy()
                    # Then the buttons are displayed again. This is done
                    # because the fifty-fifty joker changes the answer values
                    # and therefore the new values need to be fetched from the
                    # new quiz status. To make positioning easier they are
                    # stored in a new list.
                    buttons_answers = []
                    # Displays the answer buttons without html escape
                    # characters so that a player can select his answers.
                    buttons_answers.append(tk.Button(
                        main_top_3, width=25, height=3, wraplength=200,
                        text="A: " + html.unescape(answers[0]),
                        font=font.Font(family="Helvetica", size=12),
                        # The variable control_var makes the code wait with
                        # execution (after creating and displaying all labels)
                        # until it is set by clicking e.g. this button.
                        # setattr() then sets a new instance attribute to store
                        # the answer in.
                        command=lambda: [
                            control_var.set(True),
                            setattr(
                                self, "evaluation",
                                self.quiz.evaluate_answer(
                                    questionobj, answers[0]))]))
                    buttons_answers.append(tk.Button(
                        main_top_4, width=25, height=3, wraplength=200,
                        text="B: " + html.unescape(answers[1]),
                        font=font.Font(family="Helvetica", size=12),
                        command=lambda: [
                            control_var.set(True),
                            setattr(
                                self, "evaluation",
                                self.quiz.evaluate_answer(
                                    questionobj, answers[1]))]))
                    buttons_answers.append(tk.Button(
                        main_top_3, width=25, height=3, wraplength=200,
                        text="C: " + html.unescape(answers[2]),
                        font=font.Font(family="Helvetica", size=12),
                        command=lambda: [
                            control_var.set(True),
                            setattr(
                                self, "evaluation",
                                self.quiz.evaluate_answer(
                                    questionobj, answers[2]))]))
                    buttons_answers.append(tk.Button(
                        main_top_4, width=25, height=3, wraplength=200,
                        text="D: " + html.unescape(answers[3]),
                        font=font.Font(family="Helvetica", size=12),
                        command=lambda: [
                            control_var.set(True),
                            setattr(
                                self, "evaluation",
                                self.quiz.evaluate_answer(
                                    questionobj, answers[3]))]))
                    # Positions the buttons and disables them if the
                    # fifty-fifty joker deletes the answer corresponding to
                    # this button.
                    for index, button in enumerate(buttons_answers):
                        if index in (0, 1):
                            r = 0
                        else:
                            r = 1
                        button.grid(row=r, column=0)
                        if "DELETED" in button["text"]:
                            button["state"] = "disabled"
                            button["text"] = button["text"][:3] +\
                                button["text"][10:]

                # This code is executed when the audience or phone joker has
                # already been used in this round and the respective other one
                # is also used. This ensures that previous tips are moved to
                # another position to display the new tip from the joker if
                # the newly used joker is not the fifty-fifty one.
                if len(previous_tips) > 0 and not fifty_fifty:
                    # Depending on the previously used joker there is either
                    # canvas1 or label_tips that needs to be deleted. This is
                    # necessary because tkinter can not overwrite already
                    # used space which would result in unintended displaying
                    # issues.
                    try:
                        canvas1.get_tk_widget().destroy()
                    except NameError:
                        label_tips.destroy()
                    # If the previous tip was an audience joker it was stored
                    # as a list and therefore this code is executed.
                    if isinstance(previous_tips[0], list):
                        # Creates a new plot and sets its properties.
                        fig, axes = plt.subplots(
                            nrows=1, ncols=1, figsize=(3, 3), dpi=100)
                        plt.title('Audience Vote')
                        plt.subplots_adjust(bottom=0.2, top=0.8)
                        # Retrieves the data to be plotted.
                        answer = [x[0] for x in previous_tips[0]]
                        percentage = [x[1] for x in previous_tips[0]]
                        # Plots the data.
                        axes.bar(answer, percentage, align='center')
                        # Displays only the character instead of the whole
                        # answer on the plot.
                        axes.set_xticks(axes.get_xticks())
                        if len(axes.get_xticks()) == 4:
                            xticklabels = ["A", "B", "C", "D"]
                        else:
                            xticklabels = []
                            for a in answer:
                                if a in answers[0]:
                                    xticklabels.append("A")
                                elif a in answers[1]:
                                    xticklabels.append("B")
                                elif a in answers[2]:
                                    xticklabels.append("C")
                                else:
                                    xticklabels.append("D")
                        axes.set_xticklabels(xticklabels)
                        # Displays and positions the plot in the tkinter frame.
                        canvas2 = FigureCanvasTkAgg(fig, master=main_graph_2)
                        canvas2.draw()
                        main_top["highlightcolor"] = "white"
                        canvas2.get_tk_widget().pack()
                    # If the previous tip was a phone joker it was not
                    # stored as a list and therefore this code is executed.
                    else:
                        # Displays and positions the joker's tip.
                        label_previous_tips = tk.Label(
                            main_graph_2, wraplength=250,
                            text="I think it is: " + html.unescape(
                                previous_tips[0]) + "!",
                            font=font.Font(family="Helvetica", size=13))
                        label_previous_tips .grid(row=0, column=0)

                # This code is executed when the audience or phone joker is
                # used.
                if tips and not fifty_fifty:
                    # If the tip comes from an audience joker it is a list
                    # and therefore this code is executed.
                    if isinstance(tips, list):
                        # Creates a new plot and sets its properties.
                        fig, axes = plt.subplots(
                            nrows=1, ncols=1, figsize=(3, 3), dpi=100)
                        plt.title('Audience Vote')
                        plt.subplots_adjust(bottom=0.2, top=0.8)
                        # Retrieves the data to be plotted.
                        answer = [x[0] for x in tips]
                        percentage = [x[1] for x in tips]
                        # Plots the data.
                        axes.bar(answer, percentage, align='center')
                        # Displays only the character instead of the whole
                        # answer on the plot.
                        axes.set_xticks(axes.get_xticks())
                        if len(axes.get_xticks()) == 4:
                            xticklabels = ["A", "B", "C", "D"]
                        else:
                            xticklabels = []
                            for a in answer:
                                if a in answers[0]:
                                    xticklabels.append("A")
                                elif a in answers[1]:
                                    xticklabels.append("B")
                                elif a in answers[2]:
                                    xticklabels.append("C")
                                else:
                                    xticklabels.append("D")
                        axes.set_xticklabels(xticklabels)
                        # Displays and positions the plot in the tkinter frame.
                        canvas1 = FigureCanvasTkAgg(fig, master=main_graph_l)
                        canvas1.draw()
                        main_top["highlightcolor"] = "white"
                        canvas1.get_tk_widget().pack()
                    # If the tip comes from a phone joker it is not a list and
                    # therefore this code is executed.
                    else:
                        # Displays and positions the joker's tip.
                        label_tips = tk.Label(
                            main_graph_l, wraplength=250,
                            text="I think it is: " + html.unescape(tips) + "!",
                            font=font.Font(family="Helvetica", size=13))
                        label_tips.grid(row=0, column=0)
                    # Stores the tip to be able to retrieve it when another
                    # joker's tip get also displayed.
                    previous_tips.append(tips)

                ###############################################################
                # ANSWER EVALUATION
                ###############################################################
                # These two lines create a control variable that stops the code
                # flow until the control variable is updated. Each button is
                # coded to update this variable when the button is pressed.
                control_var = tk.BooleanVar()
                self.wait_variable(control_var)
                # If the player's answer returns None the loop breaks:
                # Surrendering or answering the question correct/wrong
                # returns None.
                if self.evaluation is None:
                    # The instance attribute is deleted so it can be filled
                    # with the next evaluation.
                    del self.evaluation
                    break
                # If the player's answer returns something the variables are
                # updated and the while loop continues with its next iteration:
                # Using a joker returns something.
                else:
                    questionobj, question, answers, tips = self.evaluation
                    # The instance attribute is deleted so it can be filled
                    # with the next evaluation.
                    del self.evaluation
                    # Deletes all joker images to be able to update the shown
                    # image after using a joker. This is necessary because
                    #  tkinter can not overwrite the images which would result
                    # in unintended displaying issues.
                    for label in joker_labels:
                        label.destroy()

            self.change_page("game")

    def resultPage(self):
        """
        This method displays the result page and shows there the game round as
        well as the state of the game and the amount of money the player gets.
        """
        # Queries the Quiz object for its status.
        status = self.quiz.status()

        # Creates the tkinter layout for the result page.
        main_top_1, main_top_2, main_bottom, sidebar_jokers, sidebar_winnings = \
            wwm_ui.page_layout(self, "result")

        #######################################################################
        # MAIN TOP:
        # Displays the game round, the state of the game and the amount of
        # money the player gets.
        #######################################################################
        # Retrieves the curent game state.
        state = status["state"]
        # According to the state (whether the player won lost or surrendered)
        # and the round different messages and winnings amounts are defined.
        if state == "surrendered":
            print_state = f"You surrendered in Round {status['round']}!"
            print_amount = \
                f"You will therefore take home: {status['current_payout']}"
        elif state == "lost":
            print_state = f"You lost in Round {status['round']}!"
            print_amount = \
                f"You will therefore take home: {status['secured_payout']}"
        else:
            print_state = "You answered all 15 questions correct!"
            print_amount = \
                f"You will therefore take home: {status['current_payout']}"
        # Displays the labels showing those messages and winnings amount.
        tk.Label(main_top_1, text=print_state,
                 font=font.Font(family="Helvetica", size=20)
                 ).grid(row=0, column=0)
        tk.Label(main_top_2, text=print_amount,
                 font=font.Font(family="Helvetica", size=20)
                 ).grid(row=0, column=0)

        #######################################################################
        # MAIN BOTTOM:
        # Displays the button to go back to the starting page.
        #######################################################################
        tk.Button(main_bottom, text="Back To Start", width=40,
                  font=font.Font(family="Helvetica", size=20),
                  command=lambda: self.change_page("start")
                  ).grid()

        #######################################################################
        # SIDEBAR JOKERS:
        # Displays the joker pictures.
        #######################################################################
        # Sets the default names for each not crossed picture.
        files = ["initialized__file__5050",
                 "initialized__file__audience",
                 "initialized__file__phone"]
        # If the joker has already been used the crossed picture of this joker
        # is used.
        if "50:50 Joker" not in status["jokers"]:
            files[0] += "_crossed"
        if "Audience Joker" not in status["jokers"]:
            files[1] += "_crossed"
        if "Phone Joker" not in status["jokers"]:
            files[2] += "_crossed"
        # Due to the garbage collecting bug (explained in the init method) the
        # correct image is retrieved from the global variables and displayed.
        for index, file in enumerate(files):
            img = globals()[file]
            if index == 0:
                tk.Label(sidebar_jokers, image=img).grid(row=1, column=0)
            elif index == 1:
                tk.Label(sidebar_jokers, image=img).grid(row=0, columnspan=2)
            else:
                tk.Label(sidebar_jokers, image=img).grid(row=1, column=1)

        #######################################################################
        # SIDEBAR WINNINGS:
        # Displays all possible winnings.
        #######################################################################
        # Retrieves all winnings and stores them in a new list.
        winnings = status["winnings"][:]
        # Ensures that the winnings are always centered and big enough to
        # make borders around each label look good.
        modified_winnings = []
        for win in winnings:
            modified_winnings.append(" " * ((30 - len(win))//2) + win +
                                     " " * ((30 - len(win))//2))
        # Placeholder label to position the winnings labels properly.
        tk.Label(sidebar_winnings, text=" "*30, borderwidth=2,
                 font=font.Font(family="Helvetica", size=14)
                 ).grid(row=0, column=0)
        # Displays each winning amount.
        for index, winning in enumerate(modified_winnings):
            label = tk.Label(sidebar_winnings, text=winning, borderwidth=2,
                             font=font.Font(family="Helvetica", size=14))
            label.grid(row=index+1, column=0)
            # Queries the current round
            c_round = status["round"]
            # Accentuates for which winning the player was playing.
            if c_round-1 == index:
                label["relief"] = "ridge"
            # Accentuates the safety nets in the winnings that the player
            # reached.
            if c_round > 10 and index == 9:
                label["fg"] = "green"
            elif c_round > 5 and c_round <= 10 and index == 4:
                label["fg"] = "green"


# This calls the following functions when the file gets executed by the python
# interpreter. It then creates a new QuizApp object and uses the mainloop
# method which is needed to display a tkinter window.
if __name__ == '__main__':
    app = QuizApp()
    app.mainloop()

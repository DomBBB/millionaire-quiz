import ctypes
import os
import tkinter as tk

from PIL import Image


###############################################################################
# This code is a helper for the user interface: It sets up the window
# properties, handles the joker images and creates the layout for each page.
###############################################################################
def setup_window_properties(self):
    """
    This function gets passed the tkinter window and it then sets all
    properties for this window.
    """
    # Disables DPI scaling to prevent a bug when using matplotlib within a
    # tkinter window on windows 8/10.
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(0)
    # Other OS do not have this functionality and therefore depending on the
    # os and the monitor resolution the graphs might be slightly distorted.
    except AttributeError:
        pass
    # Sets the window title.
    self.title("Who wants to be a millionaire?")
    # Defines the window size.
    window_width = 900
    window_height = 600
    # Gets the screen dimensions.
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    # Calculates the center point.
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    # Sets the position of the window to the center of the screen.
    self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    # Blocks window resizing to prevent scaling issues.
    self.resizable(False, False)
    # Adds an icon to the window. Uses os.path.join() to make the program
    # operating system independent. This icon was downloaded from:
    # https://freebiesupply.com/logos/who-wants-to-be-a-millionaire-logo/
    self.iconbitmap(os.path.join("assets", "wwtbam.ico"))


def store_images():
    """
    This function converts and resizes all images needed to display the jokers
    in their appropriate size in a dictionary and returns the whole dictionary.
    """
    # Opens each image, converts it into a compatible mode and resizes it so
    # that it fits the window.
    files = {"5050":
             Image.open(os.path.join("assets", "5050.gif"))
             .convert(mode="RGBA").resize((70, 38)),
             "audience":
             Image.open(os.path.join("assets", "audience.gif"))
             .convert(mode="RGBA").resize((70, 38)),
             "phone":
             Image.open(os.path.join("assets", "phone.gif"))
             .convert(mode="RGBA").resize((70, 38)),
             "5050_crossed":
             Image.open(os.path.join("assets", "5050_crossed.gif"))
             .convert(mode="RGBA").resize((70, 38)),
             "audience_crossed":
             Image.open(os.path.join("assets", "audience_crossed.gif"))
             .convert(mode="RGBA").resize((70, 38)),
             "phone_crossed":
             Image.open(os.path.join("assets", "phone_crossed.gif"))
             .convert(mode="RGBA").resize((70, 38))}

    # Returns the dictionary.
    return files


def page_layout(self, page_indicator):
    """
    This function gets passed the tkinter window and creates and places the
    different frames that divide the window into several parts. The frames and
    their position depend on the page it should create the layout for
    (page_indicator). In the end it returns the created frames.
    """
    # This creates the main frame with the window being its parent and a
    # borderwidth of 0.
    main = tk.Frame(self,  bd=0)
    # Then the main frame is sized (relative height & relative width) and
    # positioned (relative x & relative y) relative to its parent.
    main.place(relheight=1, relwidth=1, relx=0, rely=0)

    # This creates different smaller frames with the main frame being their
    # parent and borderwidth of 0. It then sizes (relative height & relative
    # width) and positions (relative x & relative y) these frames relative to
    # their parent. Additionally it configures the rows and columns for some
    # frames which influences how items can be placed within these frames.
    main_top = tk.Frame(main, bd=0)
    main_top.place(relheight=5/6, relwidth=7/9, relx=0, rely=0)
    main_bottom = tk.Frame(main, bd=0)
    main_bottom.place(relheight=1/6, relwidth=7/9, relx=0, rely=5/6)
    sidebar_jokers = tk.Frame(main, bd=0)
    sidebar_jokers.place(relheight=1/6, relwidth=2/9, relx=7/9, rely=0)
    for num in range(2):
        sidebar_jokers.grid_rowconfigure(num, weight=1)
        sidebar_jokers.grid_columnconfigure(num, weight=1)
    sidebar_winnings = tk.Frame(main, height=400, width=200, bd=0)
    sidebar_winnings.place(relheight=5/6, relwidth=2/9, relx=7/9, rely=1/6)
    for num in range(16):
        sidebar_winnings.grid_rowconfigure(num, weight=1)
    sidebar_winnings.grid_columnconfigure(0, weight=1)

    # Here the thickness and color of the highlight is set which can be
    # understood as a kind of a border that separates frames.
    for frame in [main_top, main_bottom, sidebar_jokers, sidebar_winnings]:
        frame["highlightbackground"] = "white"
        frame["highlightthickness"] = 1

    # Up until here this was functionality for the generic layout. Here
    # functions for the individual layouts are called and their return is
    # returned.
    if page_indicator == "start":
        return page_start(main_top,
                          main_bottom,
                          sidebar_jokers,
                          sidebar_winnings)
    elif page_indicator == "game":
        return page_game(main_top,
                         main_bottom,
                         sidebar_jokers,
                         sidebar_winnings)
    else:
        return page_result(main_top,
                           main_bottom,
                           sidebar_jokers,
                           sidebar_winnings)


def page_start(main_top, main_bottom, sidebar_jokers, sidebar_winnings):
    """
    This function creates and places the frames for the starting page and
    returns them.
    """
    # Here rows and columns for the bottom frame are configured which
    # influences how items can be placed within this frame.
    main_bottom.grid_rowconfigure(0, weight=1)
    main_bottom.grid_columnconfigure(0, weight=1)

    # This creates different smaller frames with other frames being their
    # parent and borderwidth of 0. It then sizes (relative height & relative
    # width) and positions (relative x & relative y) these frames relative to
    # their parent. Additionally it configures the rows and columns for some
    # frames which influences how items can be placed within these frames.
    main_top_1 = tk.Frame(main_top, bd=0)
    main_top_2 = tk.Frame(main_top, bd=0)
    main_top_3 = tk.Frame(main_top, bd=0)
    for index, f in enumerate((main_top_1, main_top_2, main_top_3)):
        relativeheight = 1/4
        relativey = index*1/4
        if index == 1:
            relativeheight *= 2
        elif index == 2:
            relativey = 3/4
        f.place(relheight=relativeheight, relwidth=1, relx=0, rely=relativey)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

    # All necessary frames are returned.
    return (main_top_1,
            main_top_2,
            main_top_3,
            main_bottom,
            sidebar_jokers,
            sidebar_winnings)


def page_game(main_top, main_bottom, sidebar_jokers, sidebar_winnings):
    """
    This function creates and places the frames for the game page and
    returns them.
    """
    # This creates different smaller frames with other frames being their
    # parent and borderwidth of 0. It then sizes (relative height & relative
    # width) and positions (relative x & relative y) these frames relative to
    # their parent. Additionally it configures the rows and columns for some
    # frames which influences how items can be placed within these frames.
    main_top_1 = tk.Frame(main_top, bd=0)
    main_top_2 = tk.Frame(main_top, bd=0)
    for index, f in enumerate((main_top_1, main_top_2)):
        f.place(relheight=1/3, relwidth=1, relx=0, rely=index*1/3)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)
    main_graph_l = tk.Frame(main_top_2, bd=0)
    main_graph_2 = tk.Frame(main_top_2, bd=0)
    for index, f in enumerate((main_graph_l, main_graph_2)):
        f.place(relheight=1, relwidth=1/2, relx=index*1/2, rely=0)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)
    main_top_3 = tk.Frame(main_top, bd=0)
    main_top_4 = tk.Frame(main_top, bd=0)
    for index, f in enumerate((main_top_3, main_top_4)):
        f.place(relheight=1/3, relwidth=1/2, relx=index*1/2, rely=2/3)
        f.grid_rowconfigure(0, weight=1)
        f.grid_rowconfigure(1, weight=1)
        f.grid_columnconfigure(0, weight=1)
    main_bottom_1 = tk.Frame(main_bottom, bd=0)
    main_bottom_2 = tk.Frame(main_bottom, bd=0)
    for index, f in enumerate((main_bottom_1, main_bottom_2)):
        f.place(relheight=0.8, relwidth=1/2, relx=index*1/2, rely=0.1)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)
        if index == 0:
            f.grid_rowconfigure(1, weight=1)
            f.grid_columnconfigure(1, weight=1)

    # All necessary frames are returned.
    return (main_top,
            sidebar_jokers,
            sidebar_winnings,
            main_top_1,
            main_graph_l,
            main_graph_2,
            main_top_3,
            main_top_4,
            main_bottom_1,
            main_bottom_2)


def page_result(main_top, main_bottom, sidebar_jokers, sidebar_winnings):
    """
    This function creates and places the frames for the result page and
    returns them.
    """
    # This creates different smaller frames with other frames being their
    # parent and borderwidth of 0. It then sizes (relative height & relative
    # width) and positions (relative x & relative y) these frames relative to
    # their parent. Additionally it configures the rows and columns for some
    # frames which influences how items can be placed within these frames.
    main_top_1 = tk.Frame(main_top, bd=0)
    main_top_2 = tk.Frame(main_top, bd=0)
    for index, f in enumerate((main_top_1, main_top_2, main_bottom)):
        if index != 2:
            f.place(relheight=1/4, relwidth=1, relx=0, rely=(index+1)*1/4)
        f.grid_rowconfigure(0, weight=1)
        f.grid_columnconfigure(0, weight=1)

    # All necessary frames are returned.
    return (main_top_1,
            main_top_2,
            main_bottom,
            sidebar_jokers,
            sidebar_winnings)


# This ensures that importing doesn't automatically run this code.
if __name__ == '__main__':
    pass

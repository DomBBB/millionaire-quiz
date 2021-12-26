# Who wants to be a millionaire? <br/>

<p align="center">
    Raffael Pirmin Arnold (18-605-600) <br/>
    Dominik Manuel Buchegger (17-661-658) <br/>
    Katja Alison Zimmermann (18-621-771)
</p>

<p align="center">
    HS21 3,793 | 4,799 <br/>
    Programming - Introduction Level <br/>
    Dr. Mario Silic <br/>
    26th December 2021
</p>


## What can you do with the program?
With this program a user can play the well-known game "Who wants to be a millionaire?". To win the large cash prize a user must answer 15 increasingly difficult multiple-choice questions correctly.

During the game the contestant has access to three jokers (Fifty-Fifty, Phone a Friend and Ask the Audience). The contestant can use each joker only once per game but can use more than one on a single question. If a contestant gets a question wrong but had reached a designated cash value during their game (500 or 16'000), they will leave with that amount as their prize. If they hadn’t reached a security level, they will win nothing. If a contestant feels unsure about an answer and does not wish to play on, they can walk away with the money they have won so far.


### Here you can see some screenshots of the game:
<img src="/images/startingPage.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" /> <img src="/images/gamePage1.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" /> <img src="/images/gamePage2.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" /> <img src="/images/gamePage3.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" /> <img src="/images/gamePage4.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" /> <img src="/images/resultPage.PNG" width="350" height="200" style="margin:0px 5px 5px 0px" />


## How does the program work?
The program accesses the public api of the [open trivia database](https://opentdb.com) ([CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)). It retrieves five questions for each of the three difficulty levels and stores them. During the game for each round a question will be chosen randomly within the respective difficulty level (questions 1 to 5 = easy, questions 6 to 10 = medium and questions 11 to 15 = hard). The program then waits until the user presses a button which can either be surrender, a joker or one of the four possible answers. It then either executes the logic for surrendering respectively for using a joker or it compares the given answer to the correct one. If they match, the next question is selected randomly otherwise. This is repeated until the player answers a question wrong, decides to surrender or answers all questions correct. When one of those cases occurs the current round together with the won amount are shown. Then the user can go back to the starting screen and start a new game with other questions.

The code of the game is split in three files (all in the folder src). wwm_gamelogic.py implements all the logic regarding to questions and playing a round of the game. wwm_ui.py contains helper code to properly create a tkinter window and configure its layout. wwm.py then acts as bridge between the user and the gamelogic and implements functions to display the game to the user and connect the input of the user to the game logic. To do this, wwm.py imports the needed functions and class from the other two modules.


## How can you run the program?
This program is coded for Python3 (3.8.5: it should run on other versions >=3.7 aswell but is untested). To prepare for running the program please download all files from github (you need atleast the files from the **src** folder). If not already present on the system the libraries **matplotlib** and **requests** need to be installed. These packages can be installed manually or if you are using Pip you can navigate to the src folder and install all packages with `pip install -r requirements.txt` or `pip3 install -r requirements.txt`.

Now you are ready to run the program: Navigate to the src folder and run the file **wwm.py** with your python interpreter which will open a new window and let you play the game.


### Good luck!

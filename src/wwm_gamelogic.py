import random

import requests


###############################################################################
# This code handles all functionality related to a question and implements all
# the game logic related to asking questions and evaluating answers. It does
# this with private variables and therefore creates the public interface by
# defining the only functions that should be used from outside these classes.
###############################################################################
class Quiz():
    """
    This class implements the public interface for the game. It contains
    functions to start a new game, retrieve the status of the game, ask a new
    question and evaluate the given answers. Each question is stored as an
    instance of the Question class and has different methods that are also used
    in this class.
    """
    def __init__(self):
        """
        This method initializes a new game. It retrieves 15 questions from
        the opentdb.com api and stores them as Question objects in different
        lists. It also defines private game variables and sets them all on
        their starting values.
        """
        # To increase the question difficulty during the game questions are
        # stored according to their difficulty.
        self.__easy_questions = []
        self.__medium_questions = []
        self.__hard_questions = []
        difficulties = ("easy", "medium", "hard")
        for index in range(3):
            # 5 questions for each difficulty are retrieved from a public api.
            params = {"amount": 5,
                      "difficulty": difficulties[index],
                      "type": "multiple",
                      "category": 9}
            response = requests.get(
                      "https://opentdb.com/api.php",
                      params=params)
            # The api response body is parsed to a dictionary.
            for question in response.json()["results"]:
                # For each question a new Question object is created and stored
                # in the list suited for its difficulty.
                question = Question(
                        question["question"],
                        question["correct_answer"],
                        question["incorrect_answers"])
                if index == 0:
                    self.__easy_questions.append(question)
                elif index == 1:
                    self.__medium_questions.append(question)
                else:
                    self.__hard_questions.append(question)

        # This variable defines the possible winnings.
        self.__winnings = ("50", "100", "200", "300", "500", "1'000", "2'000",
                           "4'000", "8'000", "16'000", "32'000", "64'000",
                           "125'000", "500'000", "1'000'000")
        # This variable defines in which round a winnings safety net is
        # created.
        self.__secure_step = (5, 10)

        # This variable tracks which jokers are still available.
        self.__jokers = ["50:50 Joker", "Audience Joker", "Phone Joker"]
        # This variable tracks whether the player lost, won, surrendered or is
        # still playing.
        self.__state = "playing"
        # This variable tracks in which round of the game a player is.
        self.__round = 1
        # This variable tracks how much the player would get according to the
        # winnings safety net.
        self.__secured_payout = 0
        # This variable tracks how much the player would get according to the
        # game round.
        self.__current_payout = 0

    def status(self):
        """
        This method returns a representation of all private game variables
        because programs importing this class can not directly access these
        variables.
        """
        return {"winnings": self.__winnings,
                "secure_step": self.__secure_step,
                "jokers": self.__jokers,
                "state": self.__state,
                "round": self.__round,
                "secured_payout": self.__secured_payout,
                "current_payout": self.__current_payout}

    def ask_question(self):
        """
        This method randomly selects a question according to the difficulty
        of the current round and returns several values from the Question
        methods.
        """
        if self.__round <= 5:
            # random.randint(lower, upper) includes both boundaries so len()-1
            # is used to find an existing index.
            question_index = random.randint(0, len(self.__easy_questions)-1)
            question_difficulty = "easy"
            question = self.__easy_questions[question_index]
        elif self.__round <= 10:
            question_index = random.randint(0, len(self.__medium_questions)-1)
            question_difficulty = "medium"
            question = self.__medium_questions[question_index]
        else:
            question_index = random.randint(0, len(self.__hard_questions)-1)
            question_difficulty = "hard"
            question = self.__hard_questions[question_index]

        # This returns a tuple to properly identify the question, the question,
        # the possible answers and a place holder variable None.
        return ((question_index, question_difficulty),
                question.get_question(),
                question.get_answers(),
                None)

    def evaluate_answer(self, questionobj, given_input):
        """
        This method checks the player's input for a question identified and
        retrieved through the questionobj tuple. It allows the player to
        surrender or use jokers. Otherwise it compares the player's input to
        the correct answer and changes the game state accordingly.
        """
        # The question with the question index is retrieved from
        # the list with the question difficulty (both in questionobj).
        if questionobj[1] == "easy":
            question = self.__easy_questions[questionobj[0]]
        elif questionobj[1] == "medium":
            question = self.__medium_questions[questionobj[0]]
        else:
            question = self.__hard_questions[questionobj[0]]

        # If the player wants to surrender the state is changed accordingly.
        if given_input == "__surrender":
            self.__state = "surrendered"
        # If the player wants to use a joker, it is removed from the
        # available jokers and the corresponding Question method is called.
        # Then the updated values are returned.
        elif given_input == "__joker_50:50":
            self.__jokers.remove("50:50 Joker")
            question.fifty_fifty()
            return ((questionobj[0], questionobj[1]),
                    question.get_question(),
                    question.get_answers(),
                    "fifty-fifty")
        elif given_input == "__joker_audience":
            self.__jokers.remove("Audience Joker")
            audience_result = question.audience()
            return ((questionobj[0], questionobj[1]),
                    question.get_question(),
                    question.get_answers(),
                    audience_result)
        elif given_input == "__joker_phone":
            self.__jokers.remove("Phone Joker")
            phone_result = question.phone()
            return ((questionobj[0], questionobj[1]),
                    question.get_question(),
                    question.get_answers(),
                    phone_result)
        # If the player doesn't want to surrender nor wants to use a joker, the
        # question is removed from the question list.
        else:
            if questionobj[1] == "easy":
                question = self.__easy_questions.pop(questionobj[0])
            elif questionobj[1] == "medium":
                question = self.__medium_questions.pop(questionobj[0])
            else:
                question = self.__hard_questions.pop(questionobj[0])
            # Then it is checked whether the given answer is correct or false.
            if given_input == question:
                # If it is correct and the player is in the last round he wins
                # the game and the state and current payout are updated.
                if self.__round == 15:
                    self.__state = "won"
                    self.__current_payout = self.__winnings[self.__round - 1]
                # If it is correct but the player is not in the last round the
                # current payout is updated. If he is in a round with a
                # winnings safety net the secured payout is also updated.
                # Finally the variable tracking the round is updated.
                else:
                    if self.__round in self.__secure_step:
                        self.__secured_payout = self.__winnings[self.__round-1]
                    self.__current_payout = self.__winnings[self.__round - 1]
                    self.__round += 1
            # If the answer is false the player loses and the state is updated.
            else:
                self.__state = "lost"


class Question:
    """
    This class implements the question objects and its corresponding methods.
    For each object he question and the possible answers can be queried and one
    can check whether a given answer equals the correct answer. It also defines
    the functionalities to use jokers for a question.
    """
    def __init__(self, question, correct_answer, incorrect_answers):
        """
        This method initializes a new question. It stores the attributes
        privately and creates a new instance attribute  __all_answers by
        merging the correct and the incorrect answers and shuffling.
        """
        self.__question = question
        self.__correct_answer = correct_answer
        # Because of python being pass-by-reference we need to do list
        # comprehension to properly store this list (or use copy.deepcopy()).
        self.__all_answers = [correct_answer] + \
            [answer for answer in incorrect_answers]
        # We shuffle the answers to prevent that the first answer is always the
        # correct one.
        random.shuffle(self.__all_answers)

    def get_question(self):
        """
        This method is a getter for the private variable __question.
        """
        return self.__question

    def get_answers(self):
        """
        This method is a getter for the private variable __all_answers.
        """
        return self.__all_answers

    def __eq__(self, answer):
        """
        This method defines the behavior of calling "object == ". One can
        therefore check with "object == answer" if the given answer is equal
        to the correct answer for this object. This way the correct answer is
        never revealed to functions outside of this class.
        """
        return self.__correct_answer == answer

    def fifty_fifty(self):
        """
        This method implements a "50:50" joker on an object. This means that it
        adds a certain string to two incorrect answers so that the program can
        indicate to the player that those two answers are incorrect.
        """
        # The correct index is searched and assigned to a variable.
        correct_index = self.__all_answers.index(self.__correct_answer)
        # These variables ensure that two different incorrect answers are
        # deleted.
        counter = 0
        previous_random_number = None
        while counter < 2:
            # random.randint(lower, upper) includes both boundaries.
            random_number = random.randint(0, 3)
            # This ensures that an answer only gets a string added (to indicate
            # it should be deleted) if it's not the correct answer and not the
            # same as an already deleted answer.
            if random_number not in (correct_index, previous_random_number):
                val = self.__all_answers[random_number]
                # The added string "DELETED" indicates our program that it
                # should show this answer as false to the player.
                self.__all_answers[random_number] = "DELETED" + val
                previous_random_number = random_number
                counter += 1

    def audience(self):
        """
        This method implements an "audience" joker on an object. This means
        that it returns probabilities whether this answer is correct depending
        on randomness. Usually the answer with the highest percentage is
        correct but not always.
        """
        # The percentages for the false answers are created randomly.
        false_percent = [random.randint(3, 12),
                         random.randint(5, 20),
                         random.randint(20, 33)]
        sum_false_percent = sum(false_percent)
        # This list stores the answers and their percentages.
        audience_answers = []
        # This is the program flow when the 50:50 joker was called for the same
        # Question object (meaning some variables start with "DELETED"). A
        # list comprehension is used to check this in a for loop, if nothing is
        # found this list is empty and the if condition evaluates it to false.
        if [x for x in self.__all_answers if x.startswith("DELETED")]:
            # This code iterates through all answers and adds the
            # corresponding percentage
            for answer in self.__all_answers:
                # The correct answer gets the remaning percentage that was not
                # already distributed for the false answers.
                if answer == self.__correct_answer:
                    audience_answers.append((answer,
                                            100 - sum_false_percent))
                # The incorrect but not deleted answer gets the sum of the
                # false percentages.
                elif not answer.startswith("DELETED"):
                    audience_answers.append((answer,
                                            sum_false_percent))
        # This is the program flow when the 50:50 joker was NOT called for the
        # same Question object.
        else:
            # This code iterates through all answers and adds the
            # corresponding percentage
            for answer in self.__all_answers:
                # The correct answer gets the remaning percentage that was not
                # already distributed for the false answers.
                if answer == self.__correct_answer:
                    audience_answers.append((answer,
                                            100 - sum_false_percent))
                # The incorrect answers gets a randomly selected percentage of
                # the false percentages. random.randint(lower, upper) includes
                # both boundaries and therefore len()-1 is used).
                else:
                    audience_answers.append((answer,
                                            false_percent.pop(
                                                random.randint(
                                                    0,
                                                    len(false_percent)-1))))
        # The list with answers and percentages is returned.
        return audience_answers

    def phone(self):
        """
        This method implements a "phone" joker on an object. This means
        that depending on randomness it returns usually the correct answer but
        not always.
        """
        # random.random() creates a random float between 0 and 1. Therefore
        # with a probability of ~90% the correct answer is returned, otherwise
        # an incorrect answer (that has not already been deleted through the
        # 50:50 joker) is returned.
        if random.random() < 0.9:
            return self.__correct_answer
        else:
            while True:
                rand_index = random.randint(0, 3)
                # This ensures that the randomly selected answer is not the
                # correct one and that it has not already been deleted through
                # the 50:50 joker.
                if (self.__all_answers[rand_index] != self.__correct_answer and
                   not self.__all_answers[rand_index].startswith("DELETED")):
                    return self.__all_answers[rand_index]


# This ensures that importing doesn't automatically run this code.
if __name__ == '__main__':
    pass

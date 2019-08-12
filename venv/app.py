import pickle
from random import shuffle
from venv.clue import Clue

# reloading list of clues created in main
clues = open(r'/home/seamus/PycharmProjects/Bunker/clues.pkl', 'rb')
clue_list = pickle.load(clues)
clues.close()

# Begin Quiz App
print("Welcome to Bunker, the Jeopardy preparation application.")
print("Enter \"stop\" to end program.")
print("There are " + str(len(clue_list)) + " clues to be randomized.")
print("\n")

# Score keeper
total_clues = 0
correct_clues = 0
passed_clues = 0

# shuffle to randomize questions
shuffle(clue_list)
stopped = False

for clue in clue_list:
    print(clue.category)
    print(clue.value)
    print(clue.clue)

    response = input()

    if response.lower() == clue.correct_response.lower():
        print("Correct.")
        total_clues = total_clues + 1
        correct_clues = correct_clues + 1
        print(str(correct_clues) + " clue(s) correct out of " + str(total_clues) + " answered.")
    elif response == "stop":
        stopped = True
        break
    elif response == "":
        print("Pass.")
        passed_clues = passed_clues + 1
        print(str(correct_clues) + " clue(s) correct out of " + str(total_clues) + " answered.")
        print("The correct response is \"" + clue.correct_response + "\"")
    else:
        print("Incorrect.")
        total_clues = total_clues + 1
        print(str(correct_clues) + " clue(s) correct out of " + str(total_clues) + " answered.")
        print("The correct response is \"" + clue.correct_response + "\"")

    print("\n")


if stopped:
    print("Quiz stopped.")
    print("\n")
    print("FINAL SCORE:")
    print(str(correct_clues) + " clue(s) correct out of " + str(total_clues) + " answered.")
    percentage = correct_clues / total_clues * 100
    print("You answered " + str(int(percentage)) + "% of the clues correctly.")
    print("You passed on " + str(passed_clues) + " clues.")
    print("Goodbye.")

else:
    print("You have completed all clues.")
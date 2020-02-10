

#All execution is done here, run this file and no other file to make sucessfull

###################################################

def gamemode(gameType):
    """function gamemode: takes in single integer parameter and returns none

            function selects from the files the gamemode from gameType integer, and executes by statement
            no return
    """
    if gameType == 1:
        import chess_onevone as c_ovo
        print("Playing 1V1...")
        c_ovo.startG()
    elif gameType == 2:
        print("Playing 1vC...")
        import chess_onevcpu as c_ovc
        c_ovc.startG()
    else:
        print("Playing CvC...")
        import  chess_cpuvcpu as c_cvc
        c_cvc.startG()

####################################################

def greetings():
    """ function greetings: no parameters, and no returns

            greets user, takes in inputs to send off and start game, asks if user wants a new round of chess,
            if not exits program else, recusively calss greetings
    """

    while True:
        try:
            print("Chose a game mode from the menu below, type in the number\n"
                  "corresponding to the mode to continue")
            gameType = int(input("(1) 1v1 \n"
                                 "(2) 1vC \n"
                                 "(3) CvC \n"))
        except:
            print("Type in a valid single digit please, then hit enter")
            continue
        else:
            if not (1 <= gameType <= 3):
                print("Type in a digit between 1 and 3.")
                continue
            else:
                break
    gamemode(gameType)
    print("Play Again?")
    while True:
        doNew = input("Y \ N\n>")
        if doNew != "N" and doNew != "Y":
            print("Enter a valid input of [Y] or [N]")
        else:
            break
    if doNew == "Y":
        greetings()
    else:
        print("Thank you for playing chess!")
        print("goodbye!")
    #end of program

####################################################

#beginign of program

print("Lets play some chess!")
greetings()

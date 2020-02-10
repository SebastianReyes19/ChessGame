
#importing gamerules and setGameReady for use of functions and variables in libraries
import chess_gamerules as g_rules
import chess_setGameReady as c_sgr
#global variables all set to none for now
Person = None
CPU = None
endGame = False


def startG():
    """ function startG: no returns and no parameters

            Sets up the game for the user, and asks for teams, prints out winner
    """

    global Person, CPU
    c_sgr.setBoard()
    Person, CPU = c_sgr.pickTeamCPU()
    whoWon = playGame()
    if whoWon == 1:
        print("Checkmate! White wins!")
    else:
        print("Checkmate! Black wins!")


def playGame():
    """ fnction playGame: no parameters, returns 1 integer

            function plays the game of cpu v player, depending on global integers, returns winner if checkmate/
            capture of king is done by team
    """

    global Person, CPU
    endGame = False
    winner = None
    print("Use chess coordination to select your pieces!")
    turn = 1
    while not endGame:
        if turn == 1:
            print("White Turn")
            if Person == 1:
                endGame, winner = g_rules.playTeam(turn)
            else:
                endGame, winner = g_rules.playTeamCPU(turn)
        else:
            print("Black Turn")
            if Person == 0:
                endGame, winner = g_rules.playTeam(turn)
            else:
                endGame, winner = g_rules.playTeamCPU(turn)


        endGame = bool(endGame)
        if turn == 1:
            turn = 0
        else:
            turn = 1
    c_sgr.clearBoard()
    return winner
#the board is ready and game is set

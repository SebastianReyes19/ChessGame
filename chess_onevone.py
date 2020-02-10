
#importing gamerules and setGameReady for use of functions and variables in libraries

import chess_gamerules as g_rules
import chess_setGameReady as c_sgr
#globals set to none
p1Team = None
p2Team = None
endGame = False


def startG():
    """ function startG: no returns and no parameters

                Sets up the game for the user, and asks for teams, prints out winner
        """

    global p1Team, p2Team
    c_sgr.setBoard()
    p1Team, p2Team = c_sgr.pickTeam()
    whoWon = playGame()
    if whoWon == 1:
        print("Checkmate! White wins!")
    else:
        print("Checkmate! Black wins!")


def playGame():
    """ fnction playGame: no parameters, returns 1 integer

                function plays the game of player v player, depending on global integers, returns winner if checkmate/
                capture of king is done by team
        """

    endGame = False
    winner = None
    print("Use chess coordination to select your pieces! ex: a1, c5, h7")
    turn = 1
    while not endGame:
        if turn == 1:
            print("White Turn")
        else:
            print("Black Turn")

        endGame, winner = g_rules.playTeam(turn)

        endGame = bool(endGame)
        if turn == 1:
            turn = 0
        else:
            turn = 1
    c_sgr.clearBoard()
    return winner
#the board is ready and game is set

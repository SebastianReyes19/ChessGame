
import chess_pieces as chp

#########################################################

def setonChessBoard(classItem):
    """ Function places a class item with inposX attribute into place in global nested lists
        Param: Class Item
        No returns
    """
    chp.chessFU[classItem.positionX][classItem.positionY] = classItem.symbol
    chp.chessFE[classItem.positionX][classItem.positionY] = classItem

#########################################################

def setBoard():

#
    """ function setBoard: no parameters and no returns

            function sets up pieces in standard chess starting, done in setting up a game
    """

    for i in range(8):
        whitePawn = chp.Pawn(6, i, 1)
        setonChessBoard(whitePawn)
    whiteRook = chp.Rook(7,0,1)
    setonChessBoard(whiteRook)
    whiteRook = chp.Rook(7,7,1)
    setonChessBoard(whiteRook)
    whiteKnight = chp.Knight(7,1,1)
    setonChessBoard(whiteKnight)
    whiteKnight = chp.Knight(7, 6, 1)
    setonChessBoard(whiteKnight)
    whiteBishop = chp.Bishop(7, 2, 1)
    setonChessBoard(whiteBishop)
    whiteBishop = chp.Bishop(7, 5, 1)
    setonChessBoard(whiteBishop)
    whiteQueen = chp.Queen(7,3,1)
    setonChessBoard(whiteQueen)
    whiteKing = chp.King(7,4,1)
    setonChessBoard(whiteKing)

    for i in range(8):
        blackPawn = chp.Pawn(1, i, 0)
        setonChessBoard(blackPawn)
    blackRook = chp.Rook(0, 0, 0)
    setonChessBoard(blackRook)
    blackRook = chp.Rook(0, 7, 0)
    setonChessBoard(blackRook)
    blackKnight = chp.Knight(0, 1, 0)
    setonChessBoard(blackKnight)
    blackKnight = chp.Knight(0, 6, 0)
    setonChessBoard(blackKnight)
    blackBishop = chp.Bishop(0, 2, 0)
    setonChessBoard(blackBishop)
    blackBishop = chp.Bishop(0, 5, 0)
    setonChessBoard(blackBishop)
    blackQueen = chp.Queen(0, 3, 0)
    setonChessBoard(blackQueen)
    blackKing = chp.King(0, 4, 0)
    setonChessBoard(blackKing)

#########################################################

def pickTeam():
    """ function pickTeam: takes in no parameters, returns size 2 tuple of ints


            picks the colors depending on player 1s initial selection, returns list of tuples of the selected
            1 = white, 0 = black
            :return these depending on position as respective player team colors in tuple
    """

    print("Player 1, pick a color!")
    team1 = None
    team2 = None
    while True:
        try:
            print("Enter a number to select from list")
            print("Remember in chess rules, white goes first, take this into consideration")
            team1 = int(input("(1) White\n"
                              "(2) Black\n"))
        except:
            continue
        else:
            if (team1 == 1) or (team1 == 2):
                break
            else:
                continue
    if team1 == 2:
        print("Player 1, you have chosen the Black pieces")
        print("Therefore, Player 2, you are White, you will be going first.")
        team1 -= 2
        team2 = 1
    else:
        team2 = 0
        print("Player 1, you have chosen the White pieces")
        print("Therefore, Player 2, you are Black, you will be going after player 1")
    return team1,team2

#########################################################

def pickTeamCPU():
    """ function pickTeamCPU: takes in no parameters, returns size 2 int tuple

            in 1vcpu, human player picks a piece color and computer becomes the non taken color
            color: 1 = white, 0 = black, returns the numbers as the value in a 2 len tuple
    """

    print("Player, pick a color! The CPU will be the team you do not pick")
    team1 = None
    team2 = None
    while True:
        try:
            print("Enter a number to select from list")
            print("Remember in chess rules, white goes first, take this into consideration")
            team1 = int(input("(1) White\n"
                              "(2) Black\n"))
        except:
            continue
        else:
            if (team1 == 1) or (team1 == 2):
                break
            else:
                continue
    if team1 == 2:
        print("Player 1, you have chosen the Black pieces")
        print("Therefore, CPU, you are White, you will be going first.")
        team1 -= 2
        team2 = 1
    else:
        team2 = 0
        print("Player, you have chosen the White pieces")
        print("Therefore, CPU, you are Black, you will be going after the player")
    return team1,team2

#########################################################

def displayBoard(chessboard, Team):
    """ function displayBoard: takes in 2d list of strings, and single int named team

            function, dependant on the team displays the chessboard as a team pieces facing user to output box
            :return nothing
    """

    if Team == 1:
        letters = [" ", "a ", "b ", "c ", "d ", "e ", "f ", "g ", "h "]
        print("")
        count = 8
        for i in chessboard:
            print(count, end="\t")
            print("\t".join([j for j in i]))
            count -= 1
        print("\t".join(letters))
        print("")
    else:
        letters = [" ", "h ", "g ", "f ", "e ", "d ", "c ", "b ", "a "]
        print("")
        count = 1
        for i in chessboard:
            print(count, end="\t")
            print("\t".join([j for j in i]))
            count += 1
        print("\t".join(letters))
        print("")

#########################################################

def giveInfo():
    """ function giveInfo: takes in no parameters and no returns

            function prints out information to the user, that is all
    """

    print("Use chess notation as directed on the board to select your piece.\n"
          "Then select the valid location to move your piece, examples include: ...\n"
          "'['enemy piece']','X', or special move associated with the piece.\n"
          "Type command 'undo' to select a new piece if you wish to")

#########################################################

def clearBoard():
    """ function cleaBoard: no returns and no parameters

            clears the board after each game.
    """

    chp.chessFU = [["[]" for j in range(8)] for i in range(8)]  # for user
    chp.chessFE = [[None for k in range(8)] for l in range(8)]  # for back end

#########################################################
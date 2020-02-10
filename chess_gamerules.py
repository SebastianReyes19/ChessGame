#importing chess logic variables and displayboard from user input
import chess_pieces as chp

from chess_setGameReady import displayBoard

##################################################################

def playTeam(team):
    """ playTeam function: takes in int parameter team, returns if move was checkmate or not

            Runs the chess game functions, considered the main system of execution for any player v player or
            player vs cpu function

            ask for valid input of chess movements for the turn, returns if the move made a checkmate or not

    """

    from chess_setGameReady import giveInfo
    teamKing = None

    displayBoard(chp.chessFU, team)
    let, num = None, None
    piece = None
    goTo = None
    possibleM = None

    for i in chp.chessFE:
        for j in i:
            if isinstance(j, chp.King) and j.team == team:
                teamKing = j

    if teamKing.inCheck:
        print("Heads Up! Your king is in check, protect it!")

    while True:
        let, num = getInput(team)
        if let == "quit":
            print("You can only undo if you have already selected a piece.")
            continue
        if let == "help":
            giveInfo()
            continue

        pieceR = chp.chessFE[num][let]

        piece = (num, let)
        possibleM = createMoves(pieceR, num, let)
        displayBoard(possibleM, team)

        # we have selected a valid piece, show user possible moves, and ask if
        # where they want to move or to if they want to pick a new piece

        print("Piece selected in brackets, 'X' are possible moves, enemies in a [] are possible captures")
        print("Spaces with a [ ] and letter inside indicates a special move of the piece.")

        Quitted = False
        while True:
            let, num = getInput(team, True, True)
            if let == "quit":
                Quitted = True
                break
            if let == "help":
                giveInfo()
                continue
            if not isValidMove(possibleM, num, let):
                print("Not a valid move for the piece")
                continue
            else:
                break
        if Quitted:
            displayBoard(chp.chessFU, team)
            continue
        goTo = (num, let)

        break
    kingKill, winner = makeMove(possibleM, piece, goTo)

    kingKill = bool(kingKill)

    if kingKill:
        return 1, winner
    else:

        if e_kingStatus(team):
            if team == 1:
                print("Black King in Check!")
            else:
                print("White King in Check!")

        nextTurn()
        return 0, None
    #ignore

##################################################################

def playTeamCPU(team):

    """ playTeamCPU: takes in single int parameter team

            Function runs the execution of the file, considered the main for player vs cpu and cpu vs cpu

            makes valid chess moves through a minor algorithm, always promotes to Queen in pawn promotions.
            :return if move was a checkmate of the piece and nextmove
    """


    teamKing = None

    displayBoard(chp.chessFU, team)
    let, num = None, None
    piece = None
    goTo = None
    possibleM = None

    for i in chp.chessFE:
        for j in i:
            if isinstance(j, chp.King) and j.team == team:
                teamKing = j

    if teamKing.inCheck:
        print("Heads Up CPU! Your king is in check, protect it!")

    let, num = smartPiece(team)

    pieceR = chp.chessFE[let][num]

    piece = (let, num)
    possibleM = createMoves(pieceR, let, num)
    displayBoard(possibleM, team)

    let, num = smartMoveTo(possibleM)

    goTo = (let, num)

    kingKill, winner = makeMove(possibleM, piece, goTo, True)

    kingKill = bool(kingKill)

    if kingKill:
        return 1, winner
    else:
        if e_kingStatus(team):
            if team == 1:
                print("Black King in Check!")
            else:
                print("White King in Check!")

        nextTurn()
        return 0, None

    #ignore


##################################################################

def getInput(team, blankOk = False, captureOK = False):
    """ getInput function: takes in single int parameter and 2 boolean parameters, or defaults all to false if no input
            Function gains valid input from the user, handles non cpu input,
            blankOk means that a blank space being ok is a valid move
            captureOk prevents the announcement that its not a team piece

    """


    let, num = None, None
    possibleM = None
    while True:
        # letter is the row =, number is the collumn |
        let, num = selectPiece()
        if let == "quit":
            return "quit","quit"
        if let == "help":
            return "help","help"
        if bool(team):
            let = ord(let) - 97
            num = 7 - (int(num) - 1)
        else:
            let = 7 + (97 - ord(let))
            num = (int(num) - 1)
        # input as num, let for proper notation
        if not blankOk:
            try:
                valid = (checkvalidpiece(num, let, team, captureOK) and notLocked(num, let)) or blankOk
            except:
                pass
            else:
                if valid:
                    break
                else:
                    print("Cant move piece, select another")
                    continue
        else:
            return let, num
    return let, num
    #end

##################################################################

def selectPiece():
    coord = None
    while True:
        coord = input("Select a piece via coordinates, type 'help' for help\n")
        if coord == "undo":
            return "quit","quit"
        if coord == "help":
            return "help","help"
        if len(coord)!= 2:
            print("Enter a valid input.")
            continue
        try:
            test = ord(coord[0])
        except:
            print("Enter a valid input.")
            continue
        else:
            if not (97 <= test <= 104):
                print("Enter a valid input. keep a-h lowercase")
                continue
            else:
                pass
        try:
            test = int(coord[1])
        except:
            print("Enter a valid input.")
            continue
        else:
            if not(1 <= (test) <= 8):
                print("Enter a valid input. keep number between 1-8")
                continue
            else:
                break
    return coord[0], coord[1]
    #end

##################################################################

def checkvalidpiece(col, row, team, capture = False):
    """ checkvalidpiece: takes in 3 integer outputs, and a single boolean value, boolean defaults to false if no param
        entered

            checks if the position is on the team of the player, if not returns false, capture allows continue
            if the coordinate selected is a capture move
    """
    #checks if piece is on team
    classObj = chp.chessFE[col][row]
    if classObj == None:
        print("No piece selected")
        return False
    if classObj.team != team and not capture:
        print("not on your team!")
        return False
    else:
        return True

##################################################################

def notLocked(col, row):
    """ function notLocked: takes in 2 integer values

            checks if the selected is not locked, and can move in a direction of n,s,e,w and or ne,nw,sw,se
            :return true if not locked else, false

    """
    classObj = chp.chessFE[col][row]

    if not isinstance(classObj, chp.Knight):
        #check all 8 coords
        #if all are None, return false
        count = 0
        for key, value in classObj.directs.items():
            if value != None:
                if isMoveable(col, row, count):
                    return True
                else:
                    count += 1
                    continue
            else:
                count +=1
        return False
    else:
        #special case, its a knight and can jump over pieces, just check if it can move to a new location
        #if
        for count in range(8):
            if isMoveableK(col, row, count):
                return True
            else:
                count += 1

    #ignore

##################################################################

def isMoveable(col, row, rot):
    """ function isMovable: takes in 3 integer values, returns True or False


            If the item is movable in this direction, returns true, else, returns false, hadles knight exeption
            due to its coordination
    """


    classObj = chp.chessFE[col][row]
    if rot == 0:
            if col - 1 >= 0:
                try:
                    coor = chp.chessFE[col - 1][row]
                    #to go up subtract posX by 1, to go down add by1
                    #to go left subtract 1, to go right add 1
                except:
                    pass
                    #out of range error
                else:
                    if coor == None:
                        return True
                    elif coor.team != classObj.team and not(isinstance(classObj, chp.Pawn)):
                        return True
                    else:
                        return False
            else:
                return False
    if rot == 1:
            if col -1 >= 0:
                try:
                    coor = chp.chessFE[col - 1][row + 1]
                except:
                    pass
                    # out of range error
                else:
                    if coor == None:
                        return True
                    elif coor.team != classObj.team:
                        return True
                    else:
                        return False
            else:
                return False
    if rot == 2:
            try:
                coor = chp.chessFE[col][row+1]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
    if rot == 3:
            try:
                coor = chp.chessFE[col + 1][row + 1]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
    if rot == 4:
            try:
                coor = chp.chessFE[col + 1][row]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
    if rot == 5:
            if row - 1 >= 0:
                try:
                    coor = chp.chessFE[col + 1][row - 1]
                except:
                    pass
                    # out of range error
                else:
                    if coor == None:
                        return True
                    elif coor.team != classObj.team:
                        return True
                    else:
                        return False
            else:
                return False
    if rot == 6:
            if row - 1 >= 0:
                try:
                    coor = chp.chessFE[col][row - 1]
                except:
                    pass
                    # out of range error
                else:
                    if coor == None:
                        return True
                    elif coor.team != classObj.team:
                        return True
                    else:
                        return False
            else:
                return False
    if rot == 7:
            if col - 1>= 0 and row - 1 >=0:
                try:
                    coor = chp.chessFE[col - 1][row - 1]
                except:
                    pass
                    # out of range error
                else:
                    if coor == None:
                        return True
                    elif coor.team != classObj.team:
                        return True
                    else:
                        return False
            else:
                return False

##################################################################

def isMoveableK(col, row, rot):
    """ isMovableK : takes in 3 integer values, returns True or False

            similar to is movable, but is special as the piece tested can only be of type chp.knight
    """


    classObj = chp.chessFE[col][row]
    if rot == 0:
        if col - 2 >= 0:
            try:
                coor = chp.chessFE[col - 2][row+ 1]
                #to go up subtract posX by 1, to go down add by1
                #to go left subtract 1, to go right add 1
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    if rot == 1:
        if col - 1 >= 0:
            try:
                coor = chp.chessFE[col - 1][row + 2]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    if rot == 2:
            try:
                coor = chp.chessFE[col + 1][row + 2]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
    if rot == 3:
            try:
                coor = chp.chessFE[col + 2][row + 1]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
    if rot == 4:
        if row - 1 >= 0:
            try:
                coor = chp.chessFE[col + 2][row - 1]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    if rot == 5:
        if row - 2 >= 0:
            try:
                coor = chp.chessFE[col + 1][row -2 ]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    if rot == 6:
        if col - 1 >= 0 and row -2 >=0:
            try:
                coor = chp.chessFE[col - 1][row - 2]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    if rot == 7:
        if col - 2 >= 0 and row - 1>=0:
            try:
                coor = chp.chessFE[col - 2][row - 1]
            except:
                pass
                #out of range error
            else:
                if coor == None:
                    return True
                elif coor.team != classObj.team:
                    return True
                else:
                    return False
        else:
            return False
    #end

##################################################################

def createMoves(classObj, num, let):
    """ function createMoves: takes in chp class object, and 2 integer values, returns a 2d nested list of strings


            function creates a dummy copy of the chessboard, and makes all possible moves associated with the piece
            then adds them tot he dummy copy and retuns it to the user as all posible moves and special moves
    """

    movesMaker = [i[:] for i in chp.chessFE]
    directions = classObj.directs.copy()
    count = 0
    g_board = [i[:] for i in chp.chessFU]

    g_board[num][let] = "{" + g_board[num][let] + "}"

    #if not an instance of class type Knight do this, else its a knight and a special case is made

    if not isinstance(classObj, chp.Knight):
        for value in directions.keys():
            if directions[value] == None:
                count += 1
                continue
                # skip
            else:
                if count == 0:
                    for i in range(1, directions[value] + 1):
                        if (num - i) < 0:
                            break
                        try:
                            coor = movesMaker[num - i][let]
                        except:
                            #end of range
                            break
                        else:
                            if coor == None:
                                if not (classObj.movements != 0 and i == 2):
                                    g_board[num - i][let] = "X"
                                else:
                                    pass
                                # free space
                            elif coor.team != classObj.team:
                                if not isinstance(classObj, chp.Pawn):
                                    g_board[num - i][let] = "[" + g_board[
                                        num - i][let] + "]"
                                    break
                                    #pawn cant attack head on
                                else:
                                    break
                                    #is pawn
                            elif coor.team == classObj.team:
                                break
                if count == 1:
                    for i in range(1, directions[value] + 1):
                        if num - i < 0:
                            break
                        try:
                            coor = movesMaker[num - i][let + i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num - i][let + i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num - i][let + i] = "[" + g_board[
                                    num - i][
                                    let + i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 2:
                    for i in range(1, directions[value] + 1):
                        try:
                            coor = movesMaker[num][let + i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num][let + i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num][let + i] = "[" + g_board[num][let + i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 3:
                    for i in range(1, directions[value] + 1):
                        try:
                            coor = movesMaker[num + i][let + i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num + i][let + i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num + i][let + i] = "[" + g_board[num + i][ let + i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 4:
                    for i in range(1, directions[value] + 1):
                        try:
                            coor = movesMaker[num + i][let]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num + i][let] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num + i][let] = "[" + g_board[num + i][let] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 5:
                    for i in range(1, directions[value] + 1):
                        if let - i < 0:
                            break
                        try:
                            coor = movesMaker[num + i][let - i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num + i][let - i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num + i][let - i] = "[" + g_board[num + i][ let - i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 6:
                    for i in range(1, directions[value] + 1):
                        if let - i < 0:
                            break
                        try:
                            coor = movesMaker[num][let - i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num][let - i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num][let - i] = "[" + g_board[num][let - i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
                if count == 7:
                    for i in range(1, directions[value] + 1):
                        if let - i < 0 or num - 1 < 0:
                            break
                        try:
                            coor = movesMaker[num - i][let - i]
                        except:
                            break
                        else:
                            if coor == None:
                                g_board[num - i][let - i] = "X"
                                # free space
                            elif coor.team != classObj.team:
                                g_board[num - i][let - i] = "[" + g_board[num - i][let-i] + "]"
                                break
                            elif coor.team == classObj.team:
                                break
            count += 1
        #nothing
    else:
        if num - 2 >= 0:
            try:
                coor = movesMaker[num - 2][let + 1]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num - 2][let + 1] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num - 2][let + 1] = "[" + g_board[
                        num - 2][
                        let + 1] + "]"
                else:
                    pass
        if num - 1 >= 0:
            try:
                coor = movesMaker[num - 1][let + 2]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num - 1][let + 2] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num - 1][let + 2] = "[" + g_board[
                        num - 1][
                        let + 2] + "]"
                else:
                    pass
        #rightdown
        try:
            coor = movesMaker[num + 1][let + 2]
            # to go up subtract posX by 1, to go down add by1
            # to go left subtract 1, to go right add 1
        except:
            pass
            # out of range error
        else:
            if coor == None:
                g_board[num + 1][let + 2] = "X"
                # free space
            elif coor.team != classObj.team:
                g_board[num + 1][let + 2] = "[" + g_board[
                    num + 1][
                    let + 2] + "]"
            else:
                pass
        #downright
        try:
            coor = movesMaker[num + 2][let + 1]
            # to go up subtract posX by 1, to go down add by1
            # to go left subtract 1, to go right add 1
        except:
            pass
            # out of range error
        else:
            if coor == None:
                g_board[num + 2][let + 1] = "X"
                # free space
            elif coor.team != classObj.team:
                g_board[num + 2][let + 1] = "[" + g_board[
                    num + 2][
                    let + 1] + "]"
            else:
                pass
        #downleft
        if let - 1 >= 0:
            try:
                coor = movesMaker[num + 2][let - 1]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num + 2][let - 1] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num + 2][let - 1] = "[" + g_board[
                        num + 2][
                        let - 1] + "]"
                else:
                    pass
        #leftdown
        if let - 2 >= 0:
            try:
                coor = movesMaker[num + 1][let - 2]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num + 1][let - 2] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num + 1][let - 2] = "[" + g_board[
                        num + 1][
                        let - 2] + "]"
                else:
                    pass
        #left up
        if (num - 1 >= 0) and (let - 2 >= 0):
            try:
                coor = movesMaker[num - 1][let - 2]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num - 1][let - 2] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num - 1][let - 2] = "[" + g_board[
                        num - 1][
                        let - 2] + "]"
                else:
                    pass
        #upleft
        if (num - 2 >= 0) and (let - 1 >= 0):
            try:
                coor = movesMaker[num - 2][let - 1]
                # to go up subtract posX by 1, to go down add by1
                # to go left subtract 1, to go right add 1
            except:
                pass
                # out of range error
            else:
                if coor == None:
                    g_board[num - 2][let - 1] = "X"
                    # free space
                elif coor.team != classObj.team:
                    g_board[num - 2][let - 1] = "[" + g_board[
                        num - 2][
                        let - 1] + "]"
                else:
                    pass
        #done

    #special case, pawns attack 1 diagonally and has enpass move special, and promotion special

    if isinstance(classObj, chp.Pawn):
        if num - 1 >= 0:
            try:
                coor = movesMaker[num - 1][let + 1]
            except:
                pass
            else:
                if coor == None:
                    if movesMaker[num][let + 1] == None:
                        pass
                    else:
                        target = movesMaker[num][let + 1]
                        if target.team != classObj.team and isinstance(target, chp.Pawn) and target.movements == 1 and abs(target.positionX - target.inposX) == 2:
                            g_board[num - 1][let + 1] = "[E]"
                elif coor.team != classObj.team:
                    if num - 1 == 0:
                        g_board[num - 1][let + 1] = "[P]"
                    else:
                        g_board[num - 1][let + 1] = "[" + g_board[num - 1][
                        let + 1] + "]"
                else:
                    pass
        if num - 1 >= 0 and let - 1 >= 0:
            coor = movesMaker[num - 1][let - 1]
            if coor == None:
                if movesMaker[num][let - 1] == None:
                    pass
                else:
                    target = movesMaker[num][let - 1]
                    if target.team != classObj.team and isinstance(target,chp.Pawn) and target.movements == 1 and abs(target.positionX - target.inposX) == 2:
                        g_board[num - 1][let - 1] = "[E]"
            elif coor.team != classObj.team:
                if num - 1 == 0 and let - 1 == 0:
                    g_board[num - 1][let - 1] = "[P]"
                else:
                    g_board[num - 1][let - 1] = "[" + g_board[num - 1][
                        let - 1] + "]"
            else:
                pass
        try:
            coor = movesMaker[num - 1][let -1]
        except:
            pass
        if num - 1 == 0:
            target = movesMaker[num - 1][let]
            if target == None:
                g_board[num - 1][let] = "[P]"

    #special case, castle-ing for King

    if isinstance(classObj, chp.King):
        if classObj.movements == 0:
            count = 1
            while (let - count >= 0):
                target = movesMaker[num][let - count]
                if target == None:
                    count += 1
                elif target.team == classObj.team and isinstance(target, chp.Rook) and target.movements == 0:
                    g_board[num][let - 2] = "[C]"
                    break
                else:
                    break
            count = 1
            while True:
                try:
                    target = movesMaker[num][let + count]
                except:
                    # hit end of list
                    break
                else:
                    if target == None:
                        count += 1
                    elif target.team == classObj.team and isinstance(target, chp.Rook) and target.movements == 0:
                        g_board[num][let + 2] = "[C]"
                        break
                    else:
                        break

    #cases finished, end

    return g_board

##################################################################

def isValidMove(nestedList, xpos, ypos):
    """ function isValidMove: takes in 2d nested list of strings, and 2 integer values returns True or False

            function checks if the selected position is valid move for the piece from the given nestedList,
            returns True if it is else, False

    """

    item = nestedList[xpos][ypos]

    if item == "X":#if not x, its not valid
        return True
    elif len(item) == 3:#if not special item (size 3), not valid
        if item[0] == "[":#if first item in size 3 string is bracket, valid
            return True
    else:
        return False
    #done

##################################################################

def makeMove(board, oldloc, newloc, isCPU = False):
    """ function makeMove: takes in 2d nested list of strings and 2 tuples, and a single boolean, boolean defaults to false

            makes the move of the piece, checks all cases including promotion, castle, enpass and captures
            :returns True or False if the move was a kill move of the king (checkmate)
    """

    piece = chp.chessFE[oldloc[0]][oldloc[1]]
    #makes chess move, handles enpass, castle, pawnpromotion, or capture move
    moveKind = board[newloc[0]][newloc[1]]
    ground = chp.chessFE[newloc[0]][newloc[1]]

    if moveKind == "[E]": # enpass move, kill pawn below
        #set new position of piece
        piece.positionX = newloc[0]
        piece.positionY = newloc[1]
        #set old posiion of old holder
        piece.inposX = oldloc[0]
        piece.inposY = oldloc[1]
        #set on board the piece and class piece
        chp.chessFU[newloc[0]][newloc[1]] = piece.symbol
        chp.chessFE[newloc[0]][newloc[1]] = piece
        #set old position to none and blank
        chp.chessFU[oldloc[0]][oldloc[1]] = "[]"
        chp.chessFE[oldloc[0]][oldloc[1]] = None
        #set below 1 new position to none blank, because kill move
        chp.chessFU[newloc[0] + 1][newloc[1]] = "[]"
        chp.chessFE[newloc[0] + 1][newloc[1]] = None

        piece.movements += 1

    elif moveKind == "[P]": # promotion, special function needed
        piece.positionX = newloc[0]
        piece.positionY = newloc[1]

        piece.inposX = oldloc[0]
        piece.inposY = oldloc[1]

        chp.chessFU[newloc[0]][newloc[1]] = piece.symbol
        chp.chessFE[newloc[0]][newloc[1]] = piece

        chp.chessFU[oldloc[0]][oldloc[1]] = "[]"
        chp.chessFE[oldloc[0]][oldloc[1]] = None

        pawnpromotion(newloc[0], newloc[1], piece.team, isCPU)
    elif moveKind == "[C]":
        # castleing, 2 piece move
        castleking(oldloc, newloc)
    else:#move is advancement or capture
        piece.positionX = newloc[0]
        piece.positionY = newloc[1]

        piece.inposX = oldloc[0]
        piece.inposY = oldloc[1]

        chp.chessFU[newloc[0]][newloc[1]] = piece.symbol
        chp.chessFE[newloc[0]][newloc[1]] = piece

        chp.chessFU[oldloc[0]][oldloc[1]] = "[]"
        chp.chessFE[oldloc[0]][oldloc[1]] = None

        piece.movements += 1

    displayBoard(chp.chessFU,piece.team)
    #checks if kill was of king, if so checkmate.
    if isinstance(ground, chp.King):
        return 1, piece.team
    else:
        return 0, None

#

##################################################################

def nextTurn():
    """ function nextTurn: takes no parameters, returns no parameters

            simply reverses the 2d list and list contents
            no returns
     """

    chp.chessFE = [[i for i in reversed(j)] for j in reversed(chp.chessFE)]
    chp.chessFU = [[i for i in reversed(j)] for j in reversed(chp.chessFU)]
    print("------------------------------------------------------------")

##################################################################

def pawnpromotion(num, let, team, isCPU = False):
    """ function pawnPromotion: takes in 3 int parameters, and single boolean value, defaults to False

            turns pawnItem into user input of selected piece, returns nothing
            if isCPU is True, the selection is defaulted to turn the pawn into a queen
    """

    from chess_setGameReady import setonChessBoard
    classObj = chp.chessFE[num][let]

    if isCPU:
        promotion = chp.Queen(num, let, team)
        setonChessBoard(promotion)
        return None

    print("Promotion!, your pawn can now be promoted. Input your selected promotion")
    userProm = None
    while True:
        try:
            userProm = input("'Q' - Queen\n"
                             "'R' - Rook\n"
                             "'K' - Knight\n"
                             "'B' - Bishop\n")
        except:
            print("Incorrect input")
            continue
        else:
            if len(userProm) != 1:
                print("Incorrect input")
                continue
            else:
                if not (userProm in ["Q", "R", "K", "B"]):
                    print("Incorrect Input")
                    continue
                else:
                    break
    if userProm == "Q":
        promotion = chp.Queen(num, let, team)
        setonChessBoard(promotion)
    if userProm == "R":
        promotion = chp.Rook(num, let, team)
        setonChessBoard(promotion)
        promotion.movements += 1
    if userProm == "K":
        promotion = chp.Knight(num, let, team)
        setonChessBoard(promotion)
    if userProm == "B":
        promotion = chp.Bishop(num, let, team)
        setonChessBoard(promotion)
    ###

##################################################################

def castleking(oldloc, newloc):
    """ function castleKing: takes in 2 tuples of size 2, both contentes integer

            function moves both the rook selected and the king, and moves to appropriate positions on the board,
            returns nothing
    """

    king = chp.chessFE[oldloc[0]][oldloc[1]]
    if king.team == 1:
        if oldloc[1] - newloc[1] == 2: #moving to the left white piece, long side
            king.positionX = [newloc[0]]
            king.positionY = [newloc[1]]

            chp.chessFE[newloc[0]][newloc[1]] = king
            chp.chessFU[newloc[0]][newloc[1]] = king.symbol

            chp.chessFE[oldloc[0]][oldloc[1]] = None
            chp.chessFU[oldloc[0]][oldloc[1]] = "[]"

            rook = chp.chessFE[newloc[0]][newloc[1] - 2]

            rook.positionX = [newloc[0]]
            rook.positionY = [newloc[1] + 1]

            chp.chessFE[newloc[0]][newloc[1] + 1] = rook
            chp.chessFU[newloc[0]][newloc[1] + 1] = rook.symbol

            chp.chessFE[newloc[0]][newloc[1] - 2] = None
            chp.chessFU[newloc[0]][newloc[1] - 2] = "[]"

            king.movements += 1
            rook.movements += 1

        else:
            king.positionX = [newloc[0]]
            king.positionY = [newloc[1]]

            chp.chessFE[newloc[0]][newloc[1]] = king
            chp.chessFU[newloc[0]][newloc[1]] = king.symbol

            chp.chessFE[oldloc[0]][oldloc[1]] = None
            chp.chessFU[oldloc[0]][oldloc[1]] = "[]"

            rook = chp.chessFE[newloc[0]][newloc[1] + 1]

            rook.positionX = [newloc[0]]
            rook.positionY = [newloc[1] - 1]

            chp.chessFE[newloc[0]][newloc[1] - 1] = rook
            chp.chessFU[newloc[0]][newloc[1] - 1] = rook.symbol

            chp.chessFE[newloc[0]][newloc[1] + 1] = None
            chp.chessFU[newloc[0]][newloc[1] + 1] = "[]"
            king.movements += 1
            rook.movements += 1
    else:
        if oldloc[1] - newloc[1] == 2: #moving to the left
            king.positionX = [newloc[0]]
            king.positionY = [newloc[1]]

            chp.chessFE[newloc[0]][newloc[1]] = king
            chp.chessFU[newloc[0]][newloc[1]] = king.symbol

            chp.chessFE[oldloc[0]][oldloc[1]] = None
            chp.chessFU[oldloc[0]][oldloc[1]] = "[]"

            rook = chp.chessFE[newloc[0]][newloc[1] - 1]

            rook.positionX = [newloc[0]]
            rook.positionY = [newloc[1] + 1]

            chp.chessFE[newloc[0]][newloc[1] + 1] = rook
            chp.chessFU[newloc[0]][newloc[1] + 1] = rook.symbol

            chp.chessFE[newloc[0]][newloc[1] - 1] = None
            chp.chessFU[newloc[0]][newloc[1] - 1] = "[]"
            king.movements += 1
            rook.movements += 1
        else:
            king.positionX = [newloc[0]]
            king.positionY = [newloc[1]]

            chp.chessFE[newloc[0]][newloc[1]] = king
            chp.chessFU[newloc[0]][newloc[1]] = king.symbol

            chp.chessFE[oldloc[0]][oldloc[1]] = None
            chp.chessFU[oldloc[0]][oldloc[1]] = "[]"

            rook = chp.chessFE[newloc[0]][newloc[1] + 2]

            rook.positionX = [newloc[0]]
            rook.positionY = [newloc[1] - 1]

            chp.chessFE[newloc[0]][newloc[1] - 1] = rook
            chp.chessFU[newloc[0]][newloc[1] - 1] = rook.symbol

            chp.chessFE[newloc[0]][newloc[1] + 2] = None
            chp.chessFU[newloc[0]][newloc[1] + 2] = "[]"

            king.movements += 1
            rook.movements += 1
    #

##################################################################

def e_kingStatus(team):
    """ function e_kingStatus: takes in single integer item, returns True or False

            checks if the enemy king is in check after the move, True if so, else False
    """

    teamPieces = []
    for i in range(0,8):
        for j in range(0,8):
            piece = chp.chessFE[i][j]
            if piece == None:
                pass
            elif piece.team != team:
                pass
            else:
                coord = (i,j)
                teamPieces.append(coord)

    enemyKing = None

    for i in chp.chessFE:
        for j in i:
            if isinstance(j, chp.King) and j.team != team:
                enemyKing = j

    #found enemy king and pieces on team of parameter

    for i in teamPieces:
        j = i[0]
        k = i[1]
        piece = chp.chessFE[j][k]
        board = createMoves(piece, j, k)

        for l in board:
            for m in l:
                if len(m) == 3:
                    if m[1] == enemyKing.symbol:
                        enemyKing.inCheck = True
                        return True


    enemyKing.inCheck = False
    return False

##################################################################

def smartPiece(team):
    """ function smartPiece: takes in single integer item, returns 2 integer as a tuple value

            function pics a 'smart' piece from the board on the team of the cpu, then checks if it can be moved,
             if so returns its position on the board as the return values
    """

    import random
    #yeah its not smart, ai is hard

    boardCopy = [i[:] for i in chp.chessFE]

    cpu_pieces = []
    let, num = None, None

    for i in range(0,8):
        for j in range(0,8):
            piece = boardCopy[i][j]
            if piece != None:
                if piece.team == team:
                    cpu_pieces.append((i, j))

    validP = []
    for i in range(0, len(cpu_pieces)):
        pos = cpu_pieces[i]
        if (notLocked(pos[0], pos[1])):
            validP.append(cpu_pieces[i])

    selected = None

    if (len(validP) - 1) != 0:
        i = random.randint(0, (len(validP) - 1))
        selected = validP[i]
    else:
        selected = validP[0]

    let = selected[0]
    num = selected[1]

    return let, num

##################################################################

def smartMoveTo(boardList):
    """ function smartMoveTo: takes in a 2d nested list of strings, returns size 2 tuple of ints

            function seatches for a valid move, and makes a 'smart' decision to move the piece in the direction that
            is valid from existing functions running the coordinates

            :return coordiantes as a tuple of 2 ints
    """

    import random
    validMoves = []
    for i in range(0,8):
        for j in range(0,8):
            if isValidMove(boardList, i, j):
                validMoves.append((i,j))

    smartmove = None

    if (len(validMoves) - 1) != 0:
        smartmove = random.randint(0, (len(validMoves) - 1))
    else:
        return validMoves[0][0], validMoves[0][1]

    return validMoves[smartmove][0], validMoves[smartmove][1]

##################################################################

#this program holds classes and global variables for the chess functions, import to any that use it.

chessFU = [["[]" for j in range(8)] for i in range(8)] # for user

chessFE = [[None for k in range(8)] for l in range(8)] # for back end

class Pawn:
    directs = {
        "N": 2,
        "NE": None,
        "E": None,
        "SE": None,
        "S": None,
        "SW": None,
        "W": None,
        "NW": None,
    }
    killMoves = {
        "N": None,
        "NE": 1,
        "E": None,
        "SE": None,
        "S": None,
        "SW": None,
        "W": None,
        "NW": 1,
    }
    def __init__(self, x, y, team):
        self.value = 20
        self.positionX = x # x is letter
        self.inposX = x
        self.positionY = y # y is number
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265f"
        else:
            self.symbol = "\u2659"

#############################

class Bishop:
    directs = {
        "N": None,
        "NE": 8,
        "E": None,
        "SE": 8,
        "S": None,
        "SW": 8,
        "W": None,
        "NW": 8,
    }
    killMoves = directs.copy()
    def __init__(self, x, y, team):
        self.value = 50
        self.positionX = x # x is letter
        self.inposX = x
        self.positionY = y # y is number
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265d"
        else:
            self.symbol = "\u2657"

#############################

class Rook:
    directs = {
        "N": 8,
        "NE": None,
        "E": 8,
        "SE": None,
        "S": 8,
        "SW": None,
        "W": 8,
        "NW": None,
    }
    killMoves = directs.copy()
    def __init__(self, x, y, team):
        self.value = 50
        self.positionX = x # x is letter, and row placed |2|
        self.inposX = x
        self.positionY = y # y is number, and collumn places 1. 2 .3
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265c"
        else:
            self.symbol = "\u2656"

#############################

class King:
    directs = {
        "N": 1,
        "NE": 1,
        "E": 1,
        "SE": 1,
        "S": 1,
        "SW": 1,
        "W": 1,
        "NW": 1,
    }
    killMoves = directs.copy()
    dead = False
    def __init__(self, x, y, team):
        self.value = 100
        self.inCheck = False
        self.positionX = x # x is letter
        self.inposX = x
        self.positionY = y # y is number
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265A"
        else:
            self.symbol = "\u2654"

#############################

class Queen:
    directs = {
        "N": 8,
        "NE": 8,
        "E": 8,
        "SE": 8,
        "S": 8,
        "SW": 8,
        "W": 8,
        "NW": 8,
    }
    killMoves = directs.copy()
    def __init__(self, x, y, team):
        self.value = 60
        self.positionX = x # x is letter
        self.inposX = x
        self.positionY = y # y is number
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265b"
        else:
            self.symbol = "\u2655"

#############################

class Knight:
    directs = {
        "NL": (2, -1),
        "NR": (2, 1),
        "EU": (1,2),
        "ED": (-1,2),
        "SL": (-2, -1),
        "SR": (-2, 1),
        "WU": (1, -2),
        "WD": (-1, -2),
    }
    killMoves = directs.copy()
    def __init__(self, x, y, team):
        self.value = 50
        self.positionX = x # x is letter
        self.inposX = x
        self.positionY = y # y is number
        self.inposY = y
        self.team = team
        self.movements = 0
        if team == 1:# 0 == Black, lowercase, 1 == white, uppercase
            self.symbol = "\u265E"
        else:
            self.symbol = "\u2658"

#############################
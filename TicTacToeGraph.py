# LET'S PLAY TIC TAC TOE!
# This program creates a graph that visualizes all possible games of Tic Tac Toe!
# Program By Jonathan Kleehammer
# August 30th, 2019

import matplotlib.pyplot as plt
import networkx as nx
import copy

# The Class, where all the magic happens
# We create our first board with all empty spots
# afterwards we call takeTurn() which recursively tries all possibilities
# creating new children boards from the actions taken
class TicTacToeBoard:
    def __init__(self):
        self.turn = 0 # Turn counter, used for tracking X's or O's turn
        # the board is an array of 9 ints,
        # the board is situated as follows
        # We read the board from top left to right
        # moving down when we get to the end of a row
        # 0 represents an empty spot on the board
        # 1 represents an X
        # 2 represents a O
        self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    @staticmethod
    def printBoard(board):
        for i in range(9):
            if board[i] == 0:
                print("_"),
            elif board[i] == 1:
                print("X"),
            elif board[i] == 2:
                print("O"),
            if i % 3 == 2:
                print("")
        print("")

    #rotate 90 clockwise
    @staticmethod
    def rotateCW(board):
        #rotate 90 clockwise
        alternateBoard =   [board[6], board[3], board[0],
                            board[7], board[4], board[1],
                            board[8], board[5], board[2]]
        return alternateBoard

    #flips board upside down
    @staticmethod
    def flip(board):
        alternateBoard =   [board[6], board[7], board[8],
                            board[3], board[4], board[5],
                            board[0], board[1], board[2]]
        return alternateBoard
    
    @staticmethod
    def boardString(board):
        boardString = ""
        for i in range(9):
            boardString += str(board[i])
        return boardString

    # ensuring that we don't add duplicates to the list of boards
    def alreadyExists(self):
        # all rotations and flips of this board
        alternateBoards = []
        alternateBoards.append(self.board) # index 0, normal board
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[0])) # index1, rotated 90 cw
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[1])) # index2, rotated 180 cw
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[2])) # index3, rotated 270 cw
        alternateBoards.append(TicTacToeBoard.flip(alternateBoards[0])) # index4, flipped board
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[4])) # index5, flipped then rotated 90 cw
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[5])) # index6, flipped then rotated 180 cw
        alternateBoards.append(TicTacToeBoard.rotateCW(alternateBoards[6])) # index7, flipped then rotated 270 cw

        global boardLists
        for b in boardLists[self.turn]:
        #if we get 1 match, return true and end this function
            for a in alternateBoards:
                if b == a:
                    return b #return the existing board for us to draw an edge to

        # if we made it this far we went through all the currently existing boards
        # and no match was found
        # let's add this board t if b[i] != self.board[i]:o the list of boards
        boardLists[self.turn].append(self.board)

        return None #return nothing if there was no matching board

    # after taking a turn we'll check if anyone won
    def checkVictory(self):
        # just doing all the sweeps, less efficient but for a small project it's fine
        # top left ref
        ref = self.board[0]
        if ref != 0:
            if ref == self.board[1]:
                if ref == self.board[2]:
                    return True
            if ref == self.board[3]:
                if ref == self.board[6]:
                    return True
            if ref == self.board[4]:
                if ref == self.board[8]:
                    return True
        
        # middle ref
        ref = self.board[4]
        if ref != 0:
            if ref == self.board[1]:
                if ref == self.board[7]:
                    return True
            if ref == self.board[3]:
                if ref == self.board[5]:
                    return True
        
        # bottom right ref
        ref = self.board[8]
        if ref != 0:
            if ref == self.board[2]:
                if ref == self.board[5]:
                    return True
            if ref == self.board[6]:
                if ref == self.board[7]:
                    return True
        
        # if we make it to the end then nobody won
        return False


    # taking a turn involves creating a child object for each possible turn
    def takeTurn(self):
        if self.turn >= 10:
            return
        
        # creating children
        # first we check which spots on the grid we want to attempt
        # placing a new move onto

        # we only care about checking for indexes that have nothing in them
        emptySpots = []
        for i in range(9):
            if self.board[i] == 0:
                emptySpots.append(i)

        # create a child for each spot
        for e in emptySpots:
            childBoard = TicTacToeBoard() # create new child
            childBoard.turn = self.turn + 1 # copy this turn value into it + 1
            childBoard.board = copy.deepcopy(self.board) # copy the board

            # make our move, on odd turns we play X into empty spots
            # even moves we put down an O
            if childBoard.turn % 2 == 1:
                childBoard.board[e] = 1
            elif childBoard.turn % 2 == 0:
                childBoard.board[e] = 2

            selfString = TicTacToeBoard.boardString(self.board)
            childString = TicTacToeBoard.boardString(childBoard.board)
            existingBoard = childBoard.alreadyExists()

            # global G #referencing our global graph
            if existingBoard:
                existingString = TicTacToeBoard.boardString(existingBoard)
                G.add_edge(selfString, existingString)
            else:
                G.add_edge(selfString, childString)
                if childBoard.checkVictory():
                    return
                else:
                    childBoard.takeTurn()

# keeping track of all the unique boards we've created
# We use this to track how many states each turn has
# and to have a total count of board states
boardLists =[[], [], [], [], [], [], [], [], [], []]
boardCounts = []

G = nx.Graph() # creating graph to store the data

# Executing the code!
# We begin by creating the first board
# The first board, the "Root" will then recursively create children
# until every possible board is generated
rootBoard = TicTacToeBoard()
boardLists[0].append(rootBoard)
rootBoard.takeTurn()

# All boards are now generated
# Getting a count of boards per turn then printing it
for i in range(len(boardLists)):
    boardCounts.append(len(boardLists[i]))
print(boardCounts)

# getting a sum of board counts
sum = 0
for i in range(len(boardCounts)):
    sum += boardCounts[i]
print(sum)

# /////////////////////////////////////////////////////////////////////////////
# Making the visualization, just a bunch of number tweaking until it looked
# good on my 1600x1900 monitor I was using to program this
# /////////////////////////////////////////////////////////////////////////////
sizeMap = [] # size of each node
colorMap = [] # color of each node
edgeMap = [] #color of each edge

for node in G:
    #number of empty spots
    #convert to string then count the number of 0's
    nodeString = str(node)
    emptyCount = 0
    for i in range(len(node)):
        if node[i] == '0':
            emptyCount += 1

    sizeMap.append(((emptyCount + 1) * 15) ** 2)
    
    if emptyCount >= 9:
        colorMap.append('red')
    
    elif emptyCount >= 8:
        colorMap.append('darkorange')

    elif emptyCount >= 7:
        colorMap.append('yellow')

    elif emptyCount >= 6:
        colorMap.append('chartreuse')

    elif emptyCount >= 5:
        colorMap.append('turquoise')
    
    elif emptyCount >= 4:
        colorMap.append('teal')
    
    elif emptyCount >= 3:
        colorMap.append('blue')

    elif emptyCount >= 2:
        colorMap.append('indigo')

    elif emptyCount >= 1:
        colorMap.append('purple')

    elif emptyCount >= 0:
        colorMap.append('black')
    
    else:
        print ("Well, that's weird?")
        colorMap.append('white')

for e in G.edges:
    emptyCount = 0
    for i in range(len(e[0])):
        if e[0][i] == '0':
            emptyCount += 1
    
    if emptyCount >= 9:
        edgeMap.append('red')
    
    elif emptyCount >= 8:
        edgeMap.append('darkorange')

    elif emptyCount >= 7:
        edgeMap.append('yellow')

    elif emptyCount >= 6:
        edgeMap.append('chartreuse')

    elif emptyCount >= 5:
        edgeMap.append('turquoise')
    
    elif emptyCount >= 4:
        edgeMap.append('teal')
    
    elif emptyCount >= 3:
        edgeMap.append('blue')

    elif emptyCount >= 2:
        edgeMap.append('indigo')

    elif emptyCount >= 1:
        edgeMap.append('purple')

    elif emptyCount >= 0:
        edgeMap.append('black')
    
    else:
        print ("Well, that's weird?")
        edgeMap.append('white')

plt.figure(figsize=(24, 18))
nx.draw(G, width=2, edge_color=edgeMap, node_color=colorMap, alpha=0.8, node_size=sizeMap)
plt.show()

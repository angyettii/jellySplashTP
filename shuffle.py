from cmu_graphics import *
from random import randint
import copy
from PIL import Image

#check if there exists a possible match
def solExists(board):
    for row in range(len(board)):
            for col in range(len(board[0])):
                sol = []
                if solExistsHelper(board, row, col, sol) == True and board[row][col] != None:
                     return True
                else:
                     continue
    return False


def solExistsHelper(board, row, col, sol):
    
    if len(sol) >= 3:
        return True
    
    else:
        for nextRow in range(row-1, row+2):
            for nextCol in range(col-1, col+2):
                 if isValid(board, row, col, nextRow, nextCol, sol):
                    sol.append((nextRow, nextCol))
                    solution = solExistsHelper(board, nextRow, nextCol, sol)
                    if solution != False:
                        return True
                    sol.pop()
        return False
                

def isValid(board, row, col, nextRow, nextCol, sol):
    #in dimensions of the board and the same thing as the previous thing
    #not in sol already

    if (((nextRow, nextCol) != (row, col)) and 
        (nextRow>=0) and (nextRow < len(board)) and 
        (nextCol>=0) and (nextCol < len(board[0])) and 
        (board[nextRow][nextCol]==board[row][col])and
        ((nextRow, nextCol) not in sol)):
        return True

def shuffle(app):
    #if no solution exists on the current board, need to shuffle
    #returns board with the same contents, just shuffled and guaranteed 
    #to have at least 1 solution
 
    boardContents = flatten(copy.deepcopy(app.board))
   
    newBoard = [([None] * app.cols) for row in range(app.rows)]
   
    shuffleHelper(app, newBoard, boardContents)
    
    if solExists(newBoard):
        
        app.board = newBoard

    else:
        
        return shuffle(app)
   

def shuffleHelper(app, newBoard, boardContents):
    if findUnshuffled(app, newBoard) == 'shuffled':
        return 
    
    else:
        #gives random value from the board contents
        row, col = findUnshuffled(app, newBoard)
        index = randint(0,len(boardContents) - 1)
        newBoard[row][col] = boardContents[index]
        boardContents.pop(index)
        shuffleHelper(app, newBoard, boardContents)
        

#finds cells that don't have a new value yet, if can't find one, 
# the board is shuffled already
def findUnshuffled(app, newBoard):
    for row in range(app.rows):
        for col in range(app.cols):
            if newBoard[row][col] == None: 
                
                return row, col
    
    return 'shuffled'

#csacademy 7.8 exercise 
def flatten(L):
    
    if L == []:
        return []
    else:
        first = L[0]
        rest = L[1:]
        if isinstance(first, list):
            return flatten(first) + flatten(rest)
        else:
            return [first] + flatten(rest)
        
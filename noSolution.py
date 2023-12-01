from random import randint
import copy

def solExists(board):
    for row in range(len(board)):
            for col in range(len(board[0])):
                sol = []
                if solExistsHelper(board, row, col, sol) == True:
                     return True
                else:
                     continue
    return False


def solExistsHelper(board, row, col, sol):
    #check if there exists a possible match
    if len(sol) >= 3:
        return True
    
    else:
        for nextRow in range(row-1, row+2):
            for nextCol in range(col-1, col+2):
                 if isValid(board, row, col, nextRow, nextCol, sol):
                    sol.append(nextRow, nextCol)
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

def shuffle(board):
    #if no solution exists on the current board, need to shuffle
    #returns board with the same contents, just shuffled and guaranteed 
    #to have at least 1 solution
    if solExists(board) == False:
        boardContents = flatten(copy.deepcopy(board))

        newBoard = [([None] * 9) for row in range(9)]

        for i in range(len(boardContents)-1, -1, -1):
            for row in range(len(newBoard)):
                for col in range(len(newBoard[0])):
                    newBoard[row][col] = boardContents[randint(0,i)]

        if solExists(newBoard):
            return newBoard
        else:
            return shuffle(board)


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
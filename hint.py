from cmu_graphics import *
from random import randint
import copy
from PIL import Image

def getHint(app):
    if app.showHint == True:
        
        copyBoard = copy.deepcopy(app.board)
        best = []
        bestJelly = None

        
        for row in range(app.rows):
            for col in range(app.cols):
                if copyBoard[row][col] != 'seen':
                    target = app.board[row][col]%10 
                    curr = floodFill(app, row, col, target)
                    
                    

                    for i, j  in curr:
                        #keeps track of what we've seen already, no unnecessary repeats
                        copyBoard[i][j] = 'seen'
                    
                    #finds the best valid route within the bounds of the flood fill
                    
                    temp = compareWithinFill(app, curr)
                    
                    
                    x,y = temp[0]

                    #current jelly is the target jelly
                    if app.board[x][y]%10 == app.targetJelly:
                        if len(temp) + 1 > len(best):
                            best = temp
                            bestJelly = best[0]

                    #neither the current or best jelly 
                    elif (len(temp) > len(best)) and (bestJelly != app.targetJelly):
                        if len(temp) > len(best):
                            best = temp
                            x,y = best[0][0], best[0][1]
                            bestJelly = app.board[x][y]

                    #the current best is a solution with the target jellies
                    else:
                        if len(temp)-1  > len(best):
                            best = temp
                            bestJelly = best[0]
        
        if len(best)>2:
            app.hint = best
        

    else: app.hint = []



#referenced articles: https://levelup.gitconnected.com/floodfill-algorithm-explained-all-you-need-to-know-with-code-samples-265d5db87777
#https://www.geeksforgeeks.org/flood-fill-algorithm/
#https://en.wikipedia.org/wiki/Flood_fill#Moving_the_recursion_into_a_data_structure

def floodFill(app, row, col, target):
    
    stack = []

    stack.append((row, col))

    sol = [(row,col)]


    while stack != []:
         
        
        curr = stack.pop()
         
        x = curr[0]
        y = curr[1]
         
        # Check if the jellies next to the current one are valid

        #down
        if isValidFloodFill(app, x + 1, y, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x + 1, y))
            stack.append((x + 1, y))
         
        #right 
        if isValidFloodFill(app, x, y+1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x, y+1))
            stack.append((x, y+1))
         
        #up 
        if isValidFloodFill(app, x - 1, y, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x - 1, y))
            stack.append((x - 1, y))
         
        #right 
        if isValidFloodFill(app, x , y -1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x , y -1 ))
            stack.append((x , y - 1))

        #down-left
        if isValidFloodFill(app, x +1 , y +1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x +1 , y +1 ))
            stack.append((x+1 , y +1))
        
        #up-right
        if isValidFloodFill(app, x -1 , y - 1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x -1 , y -1 ))
            stack.append((x - 1, y - 1))
 
        #down-right
        if isValidFloodFill(app, x +1, y -1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x +1 , y -1 ))
            stack.append((x +1 , y - 1))

        #up-left
        if isValidFloodFill(app, x -1, y +1, sol, target):
             
            # if valid, add to solution and stack
            sol.append((x -1, y +1 ))
            stack.append((x -1, y +1))

    return sol

def isValidFloodFill(app, row, col, sol, target):
    if ((row < 0) or (row >= app.rows) or
        (col < 0) or (col >= app.cols) or
        (app.board[row][col]%10 != target) or 
        (row, col) in sol):
        return False
    return True



def findOptimal(app, possibleStart):
    sol = []
    best = None
    
    copyPossibleStart = copy.deepcopy(possibleStart)

    for max in range(len(possibleStart), -1, -1):
        tryingCurr = findOptimalHelper(app, copyPossibleStart, sol, max)
        
        if  tryingCurr != None:
            return tryingCurr

#only finding first
def findOptimalHelper(app, possible, sol, max):
    if len(sol) == max:
        return sol
    
    #returning too early, not exploring all options
    else:
        for i in range(0, len(possible)):
            
            row, col = possible[i]
            if isValidOptimal(app, row, col, sol):
                sol.append((row,col))
                taken = possible.pop(i)
                newMove = findOptimalHelper(app, possible, sol, max)
                if newMove != None:
                    return sol
                sol.pop()
                possible.insert(i, taken)
    return None

def isValidOptimal(app, row, col, sol):
    if sol == []:
        return True
    
    else: 
        prevRow, prevCol = sol[-1]
        #in neighboring cells or already in solution
        if ((((prevRow+1, prevCol) == (row,col)) or ((prevRow-1, prevCol) == (row,col)) or 
            ((prevRow, prevCol+1) == (row,col)) or ((prevRow, prevCol-1) == (row,col)) or 
            ((prevRow+1, prevCol+1) == (row,col)) or ((prevRow-1, prevCol-1) == (row,col)) or 
            ((prevRow+1, prevCol-1) == (row,col)) or ((prevRow-1, prevCol+1) == (row,col))) and 
            ((row, col) not in sol)):
            return True
        else:
            return False
            
def compareWithinFill(app, possible):
    best = []
   
    # finds path from each jelly in possible
    currPath = findOptimal(app, possible)
        #best check
        
    if best == [] or len(currPath) > len(best):
        best = currPath 
        # possible.insert(i, possible.pop(0))

   
    return best


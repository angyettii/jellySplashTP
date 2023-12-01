from cmu_graphics import *
from random import randint
import copy

def onAppStart(app):
    app.width = 800
    app.height = 800
    app.rows = 9
    app.cols = 9
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.boardWidth = (3/4)*app.width
    app.boardHeight = (3/4)*app.height
    app.boardLeft = (1/8)*app.width
    app.boardTop = (1/6)*app.height
    app.cellBorderWidth = 2
    app.selected = []
    app.centers = loadCenters(app)
    app.notSelected = app.centers
    app.selectedPositions = []
    #what the target jelly is this round 
    app.targetJelly = randint(1,6)
    app.totalMoves = 20
    app.userMoves = app.totalMoves
    app.userScore = 0
    app.hint =[]
    app.showHint =False
    app.scores = dict()
    app.showHintTest = False
    
    


def loadCenters(app):
    L = []
    for row in range(app.rows):
        for col in range(app.cols):
            x, y = row, col
            L.append((x,y))
    return L


def distance(x1, x2, y1, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**.5

def onMouseDrag(app, mouseX, mouseY):

    count = 0
    while count < len(app.notSelected):
        #if distance from a center is less than radius, that circle is selected 
        cxPixel = (rowColToPixel(app, app.notSelected[count][0], app.notSelected[count][1])[0])
        cyPixel = (rowColToPixel(app, app.notSelected[count][0], app.notSelected[count][1])[1])
        if distance(mouseX, cxPixel,  mouseY, cyPixel ) < (app.boardWidth//app.cols)//2:
            #saves the index of the popped element
            app.selectedPositions.append(count)
            app.selected.append(app.notSelected.pop(count))
        
        #else, move on to the next circle
        else:
            count += 1

    #allows user to 'undo' selection
    if len(app.selected) >=2:
        ind = len(app.selected) - 2
        
        if distance(mouseX, rowColToPixel(app, app.selected[ind][0], app.selected[ind][1])[0], 
                    mouseY, rowColToPixel(app, app.selected[ind][0], app.selected[ind][1])[1]) < (app.boardWidth//app.cols)//2:
            
            app.notSelected.insert(app.selectedPositions[ind + 1], app.selected.pop(ind + 1))
        
   
def onMouseRelease(app, mouseX, mouseY):
    
    if len(app.selected) < 3:
        for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
                
    
    #length is greater than or equal to 3
    else:
        
        intial = app.board[app.selected[0][0]][app.selected[0][1]]
        
        for cx, cy in app.selected:
            
            if app.board[cx][cy] != intial:
                for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
                
                break
                
            
            #all the same color 
        
        

        if len(app.selected) != 0:
            #add points to user score
            addScoreToOverall(app, app.selected)

            for row, col in app.selected:
                app.board[row][col] = 0
            app.userMoves -=1

            for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
            


def onMousePress(app, mouseX, mouseY):
    #flood fill algo when hint button pressed, lightbulb png

    pass


def redrawAll(app):
    
    drawGrid(app)
    
    for i in range(len(app.selected)-1):
       
        x,y = rowColToPixel(app, app.selected[i][0],app.selected[i][1])
        nextX, nextY = rowColToPixel(app, app.selected[i+1][0],app.selected[i+1][1])
        drawLine(x, y, nextX, nextY)
    
    makeColors(app)
    for row in range(app.rows):
        for col in range(app.cols):
            val = app.board[row][col]
            color = findColor(app, val)
            x, y = rowColToPixel(app, row, col)
            drawCircle(x, y, (app.boardWidth//app.cols)//3, 
                       fill = color, border = 'black')
            
    textColor = rgb(133, 90, 35)
    drawOval(app.width/2, app.height*(1/20), app.width/4, app.height/5, 
             fill = rgb(244, 206, 157), border = textColor, borderWidth = 10)
    drawLabel("Moves Left:", app.width/2, app.height*(1/28), size = 20, fill = rgb(97, 63, 19))
    drawLabel(f'{app.userMoves}', app.width/2, app.height*(1/12), size = 40)
    drawLabel(f'Score: {int(app.userScore)}', app.width*1/10, app.height*1/15, size = 20)
    drawLabel(f'target: {findColor(app, app.targetJelly)}', app.width*17/20,app.height*1/15, size = 20)

def findColor(app, val):

    if val == 1:
        return 'purple'
    
    elif val == 2:
        return 'green'
    
    elif val == 3:
        return 'red'
    
    elif val == 4:
        return 'blue'
    
    elif val == 5:
        return 'yellow'
    
    elif val == 6:
        return 'orange'
    
def makeColors(app):
    
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == None:
                color = randint(1,6) 
                app.board[row][col] = color

           

def drawGrid(app):
    cellWidth = app.boardWidth//app.cols
    cellHeight = app.boardHeight//app.rows
    for row in range(app.rows):
        for col in range(app.cols):
           
            if (row,col) in app.selected:
                color = rgb(255, 236, 204)

            elif(row,col) in app.hint:
                color = rgb(137, 197, 240)

            elif abs(row-col)%2 == 0:
                color = rgb(222,172,120)

            else:
                color = rgb(234,192,150)
          
            x = app.boardLeft + col*cellHeight
            y = app.boardTop + row*cellWidth
            drawRect(x, y, cellWidth, cellHeight, 
                     fill = color)


             
def rowColToPixel(app, row, col):
    cellWidth = app.boardWidth//app.cols
    cellHeight = app.boardWidth//app.rows
    return (cellWidth*col + cellWidth //2 + app.boardLeft, 
            cellHeight*row + cellHeight // 2 + app.boardTop)
 
def onKeyPress(app, key):
    if key == 'r':
        app.board[0][0] = None
    if key == 'p':
        for row in range(app.rows):
            for col in range(app.cols):
                app.board[row][col] = 0
        
    
    if key == 'h':
        app.showHint = not app.showHint

    if key == 's':
        print(solExists(app.board))
        app.board = shuffle(app)

def onStep(app):
    #'falling'   
    
    for row in range (app.rows-1,-1,-1):
        for col in range(app.cols):
            if app.board[row][col] == 0 and row != 0:
                    app.board[row][col] = app.board[row-1][col]
                    app.board[row-1][col] = 0

            elif app.board[row][col] == 0 and row == 0:
                    app.board[row][col] = None

    getHint(app)


def getHint(app):
    if app.showHint == True:
        
        copyBoard = copy.deepcopy(app.board)
        best = []
        bestJelly = None

        
        for row in range(app.rows):
            for col in range(app.cols):
                if copyBoard[row][col] != 'seen':
                    curr = floodFill(app, row, col)
                    
                    

                    for i, j  in curr:
                        #keeps track of what we've seen already, no unnecessary repeats
                        copyBoard[i][j] = 'seen'
                    
                    #finds the best valid route within the bounds of the flood fill
                    
                    temp = compareWithinFill(app, curr)
                    
                    
                    x,y = temp[0]

                    #current jelly is the target jelly
                    if app.board[x][y] == app.targetJelly:
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
                
    
def floodFill(app, row, col):
    sol = []
    target = app.board[row][col]
    
    return floodFillHelper(app, row, col, target, sol)


def floodFillHelper(app, row, col, target, sol):

    if ((row < 0) or (row >= app.rows) or
        (col < 0) or (col >= app.cols) or
        (app.board[row][col] != target) or 
        (row, col) in sol):
        return sol

    else:
        sol.append((row, col))
        floodFillHelper(app, row-1, col, target, sol) # up
        floodFillHelper(app, row+1, col, target, sol) # down
        floodFillHelper(app, row, col-1, target, sol) # left
        floodFillHelper(app, row, col+1, target, sol) # right
        floodFillHelper(app, row-1, col-1, target, sol) # up-left
        floodFillHelper(app, row-1, col+1, target, sol) # up-right
        floodFillHelper(app, row+1, col-1, target, sol) # down-right
        floodFillHelper(app, row+1, col+1, target, sol) # down-left

        if sol != []:
            return sol
        
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
   
    # for i in range(len(possible)):
    #     possible.insert(0, possible.pop(i))
    #     #finds path from each jelly in possible
    currPath = findOptimal(app, possible)
        #best check
        
    if best == [] or len(currPath) > len(best):
        best = currPath 
        # possible.insert(i, possible.pop(0))

   
    return best


#adds score to user score
def addScoreToOverall(app, popped):
    #bonus for popping target jelly
    x,y = popped[0]
    if app.board[x][y] == app.targetJelly:
            multiplier = 1.5
    else:
            multiplier = 1

    #memoization
    if len(popped) in app.scores:
        addedScore = app.scores[len(popped)] 
    
    else: addedScore = calculateScore(app, len(popped))

    app.userScore += addedScore * multiplier


#calculates score, each jelly popped gives 20% increase in score
def calculateScore(app, length):
    
     #base case
    if length == 3: 
        
        return 600
            
    #recurse
    else:    
        #each jelly popped adds 20% to the score
        app.scores[length] = 6/5 * calculateScore(app, length-1)
        return app.scores[length]
          

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
    #check if there exists a possible match
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
        for row in range(app.rows):
            for col in range(app.cols):
                app.board[row][col] = newBoard[row][col]

    else:
        
        return shuffle(app)
   

def shuffleHelper(app, newBoard, boardContents):
    if findUnshuffled(app, newBoard) == 'not shuffled':
        return 
    
    else:
        row, col = findUnshuffled(app, newBoard)
        index = randint(0,len(boardContents) - 1)
        newBoard[row][col] = boardContents[index]
        boardContents.pop(index)
        shuffleHelper(app, newBoard, boardContents)
        


def findUnshuffled(app, newBoard):
    for row in range(app.rows):
        for col in range(app.cols):
            if newBoard[row][col] == None: 
                
                return row, col
    
    return 'not shuffled'

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
            

def main():
    runApp()

main()
from cmu_graphics import *
from random import randint
import copy
from PIL import Image


def onAppStart(app):
    app.width = 800
    app.height = 800
    app.rows = 9
    app.cols = 9
    app.boardWidth = (3/4)*app.width
    app.boardHeight = (3/4)*app.height
    app.boardLeft = (1/8)*app.width
    app.boardTop = (1/6)*app.height
    app.cellBorderWidth = 2
    app.centers = loadCenters(app)
    app.winningScore = 40000
    onStart(app)
    loadImages(app)
    app.stepsPerSecond = 9
    
    
    
def onStart(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.notSelected = app.centers
    app.selected = []
    app.selectedPositions = []
    #what the target jelly is this round 
    app.targetJelly = randint(1,6)
    app.totalMoves = 20
    app.userMoves = app.totalMoves
    app.player.score = 0
    app.hint =[]
    app.showHint =False
    app.scores = dict()
    app.showHintTest = False
    app.gameOver = False
    app.won = False
    app.canShuffle = False
    app.striped = []


def loadImages(app):
    #https://stock.adobe.com/images/Cartoon-grass-with-small-flowers-daisy-and-marigold.-Grass-field%2C-background/177790791
    app.backgroundImage = Image.open('images/istockphoto-865924416-612x612.jpg')
    app.backgroundImage = CMUImage(app.backgroundImage)

    #https://thenounproject.com/icon/retry-1921228/
    app.retryImage = Image.open('images/retry.png')
    app.retryImage = CMUImage(app.retryImage)

    #https://pngtree.com/freepng/shining-bright-light-bulb_8539561.html
    app.lightbulbImage = Image.open('images/lightbulb.webp')
    app.lightbulbImage = CMUImage(app.lightbulbImage)

    #https://www.flaticon.com/free-icon/shuffle_3580329
    app.shuffleImage = Image.open('images/shuffle.png')
    app.shuffleImage = CMUImage(app.shuffleImage)

    #all jelly illustrations done by me

    app.blueJelly = Image.open('images/blueJelly.png')
    app.blueJelly = CMUImage(app.blueJelly)

    app.greenJelly = Image.open('images/greenJelly.png')
    app.greenJelly = CMUImage(app.greenJelly)

    app.yellowJelly = Image.open('images/yellowJelly.png')
    app.yellowJelly = CMUImage(app.yellowJelly)

    app.orangeJelly = Image.open('images/orangeJelly.png')
    app.orangeJelly = CMUImage(app.orangeJelly)

    app.redJelly = Image.open('images/redJelly.png')
    app.redJelly = CMUImage(app.redJelly)

    app.purpJelly = Image.open('images/purpJelly.png')
    app.purpJelly = CMUImage(app.purpJelly)

    app.emptyImage = Image.open('images/empty.png')
    app.emptyImage = CMUImage(app.emptyImage)

    app.horizontalImage = Image.open('images/horizontal.png')
    app.horizontalImage = CMUImage(app.horizontalImage)

    app.verticalImage = Image.open('images/vertical.png')
    app.verticalImage = CMUImage(app.verticalImage)

    app.winImage = Image.open('images/win.png')
    app.winImage = CMUImage(app.winImage)

    app.loseImage = Image.open('images/lose.png')
    app.loseImage = CMUImage(app.loseImage)

    #https://thenounproject.com/browse/icons/term/plus-sign/
    app.plusImg = Image.open('images/plus.png')
    app.plusImg = CMUImage(app.plusImg)

    #https://pngimg.com/image/41010
    app.minusImg = Image.open('images/minus.png')
    app.minusImg = CMUImage(app.minusImg)



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

    if app.gameOver == False:
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
        
        intial = app.board[app.selected[0][0]][app.selected[0][1]]%10
        
        for cx, cy in app.selected:
            
            if app.board[cx][cy]%10 != intial:
                for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
                
                break
                
            
            #all the same color 
        
        if len(app.selected) != 0:
            #add points to user score
            addScoreToOverall(app, app.selected)

            for row, col in app.selected:
                #checks if is a striped jelly
                
                #if vertical jelly, take all jellies in that column
                if app.board[row][col] > 10 and app.board[row][col]<20:
                        
                        for horizontal in range(app.rows):
                            if (horizontal, col) not in app.selected:
                                app.player.score +=450
                                app.board[horizontal][col] = 0
                        
                        
                #if horizontal jelly, take all jellies in that row
                elif app.board[row][col]>20:
                 
                        for vertical in range(app.cols):
                            if (row, vertical) not in app.selected:
                                app.player.score +=450
                                app.board[row][vertical] = 0
                            
                
                app.board[row][col] = 0
           
            app.userMoves -=1
            if len(app.selected)>=6:
                makeStriped(app)

            for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
        #checks if the game is over after every move
        app.showHint = False
        isGameOver(app)
        
    
            
def makeStriped(app):
    newStriped = randint(0, len(app.notSelected)-1)
    
    if ((app.board[app.notSelected[newStriped][0]][app.notSelected[newStriped][1]] > 10) or 
    (app.board[app.notSelected[newStriped][0]][app.notSelected[newStriped][1]] == 0)):
        
        makeStriped(app)
    else: 
        
        val = randint(1,2)
        if val == 1:
            app.board[app.notSelected[newStriped][0]][app.notSelected[newStriped][1]] +=10
        else: 
            app.board[app.notSelected[newStriped][0]][app.notSelected[newStriped][1]] +=20


def onMousePress(app, mouseX, mouseY):
   
    if app.gameOver == True: 
        pilImage = app.retryImage.image
        if distance(mouseX, app.width/2, mouseY, app.height*(2/3)) < pilImage.width/5:
            onStart(app)
    else: 
        pilImage = app.lightbulbImage.image
        if distance(mouseX, app.width*9/10, mouseY, app.height/15) < pilImage.height/45:
            app.showHint = not app.showHint
        
        pilImage = app.shuffleImage.image
        if distance(mouseX, app.width*3/4, mouseY, app.height/15) < pilImage.width/12:
            shuffle(app)
        
        changeFallSpeed(app, mouseX, mouseY)

def changeFallSpeed(app, mouseX, mouseY):

    if ((distance(mouseX, app.width/20, mouseY, app.height*7/10) < app.boardWidth//(app.rows*2)) and (app.stepsPerSecond < 28)):
        
        app.stepsPerSecond +=4
       
    
    

    if ((distance(mouseX, app.width/20, mouseY, app.height*8/10) < app.boardWidth//(app.rows*2)) and (app.stepsPerSecond > 4)):
     
        app.stepsPerSecond -=4
        



def redrawAll(app):
    pilImage = app.backgroundImage.image
    drawImage(app.backgroundImage, app.width/2, app.height/2, align='center', width = pilImage.width*(4/3), height = pilImage.height*(4/3))
    
    textColor = rgb(163, 99, 3)
    drawRect(app.width*1/10, app.height*31/224, app.width*4/5, app.height*4/5, fill = textColor)
    drawGrid(app)
    
    for i in range(len(app.selected)-1):
       
        x,y = rowColToPixel(app, app.selected[i][0],app.selected[i][1])
        nextX, nextY = rowColToPixel(app, app.selected[i+1][0],app.selected[i+1][1])
        drawLine(x, y, nextX, nextY)
    
    makeColors(app)

    for row in range(app.rows):
        for col in range(app.cols):
            val = app.board[row][col]
          
            image = findColor(app, val)[0]
            x, y = rowColToPixel(app, row, col)
            #vertical
            if val > 10 and val < 20:
                drawCircle(x, y, (app.boardWidth//app.cols)//3, 
                        border = 'black')
                drawImage(image, x, y, align='center')
                drawImage(app.verticalImage,x,y,align='center')
            #horizontal
            elif val>20:
                drawImage(image, x, y, align='center')
                drawImage(app.horizontalImage,x,y,align='center')
            #normal
            else: 
                drawImage(image, x, y, align='center')


            
    drawOval(app.width/2, app.height*(1/20), app.width/4, app.height/5, 
             fill = rgb(244, 206, 157), border = textColor, borderWidth = 10)
    drawLabel("Moves Left:", app.width/2, app.height*(1/28), size = 20, fill = rgb(97, 63, 19))
    drawLabel(f'{app.userMoves}', app.width/2, app.height*(1/12), size = 40)
    drawLabel(f'Score: {int(app.player.score)}', app.width*3/20, app.height*1/25, size = 25)
    drawLabel('target:', app.width*1/10,app.height*1/10, size = 20)
    drawImage(findColor(app, app.targetJelly)[0], app.width*15/80,app.height*1/10, align = 'center')

    pilImage = app.lightbulbImage.image
    drawCircle(app.width*9/10, app.height/15, pilImage.height/45, fill = 'white', border = 'black', borderWidth = 2)
    drawImage(app.lightbulbImage, app.width*9/10, app.height/15, align='center', width = pilImage.width/18, height = pilImage.height/18)

    pilImage = app.shuffleImage.image
    drawCircle(app.width*3/4, app.height/15, pilImage.width/12, fill = 'white', border = 'black', borderWidth = 2)
    drawImage(app.shuffleImage, app.width*3/4, app.height/15, align='center', width = pilImage.width/8, height = pilImage.height/8)

    drawCircle(app.width/20, app.height*7/10, app.boardWidth//(app.rows*2), fill = 'white', border = 'black')
    pilImage = app.plusImg.image
    drawImage(app.plusImg, app.width/20, app.height*7/10, align = 'center', width = pilImage.width/4, height = pilImage.height/4)
    
    drawCircle(app.width/20, app.height*8/10, app.boardWidth//(app.rows*2), fill = 'white', border = 'black')
    pilImage = app.minusImg.image
    drawImage(app.minusImg, app.width/20, app.height*8/10, align = 'center', width = pilImage.width/25, height = pilImage.height/25)
    
    if app.gameOver == True:
        drawRect(0, 0, app.width, app.height, fill = rgb(157, 135, 168), opacity = 78)
        if app.won == True:
            rectColor = rgb(139, 209, 125)
            msg = (f'Congratulations, you scored {int(app.player.score)} and won!')
            retryColor = rgb(10, 107, 24)
            lastPic = app.winImage
        else: 
            rectColor = rgb(227, 104, 79)
            msg = (f"Oh no, you've run out of moves! Your score was {int(app.player.score)}.")
            retryColor = rgb(194, 23, 17)
            lastPic = app.loseImage

        drawRect(app.width/7, app.height/4, app.width*(5/7), app.height/2, fill = rectColor)
        drawLabel(msg, app.width/2, app.height/3, size = 20)
        drawLabel('Play Again?', app.width/2, app.height*(2/5), size = 25)
        drawImage(lastPic, app.width/2, app.height*(107/200), align = 'center')
        pilImage = app.retryImage.image
        drawCircle(app.width/2, app.height*(321/480), pilImage.width/5, fill = retryColor)
        drawImage(app.retryImage, app.width/2, app.height*(2/3), align='center', width = pilImage.width/3, height = pilImage.height/3)


def findColor(app, val):

    if val %10 == 1:
        return app.purpJelly, 'purple'
    
    elif val%10  == 2:
        return app.greenJelly, 'green'
    
    elif val%10  == 3:
        return app.redJelly, 'red'
    
    elif val %10 == 4:
        return app.blueJelly, 'blue'
    
    elif val %10 == 5:
        return app.yellowJelly, 'yellow'
    
    elif val %10 == 6:
        return app.orangeJelly, 'orange'
    
    elif val == 0:
        return app.emptyImage, 'nothing'

    
def makeColors(app):
    
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == None:
                color = randint(1,6) 
                app.board[row][col] = color

def dropDown(app):

    #'falling'   
    
    for row in range (app.rows-1,-1,-1):
        for col in range(app.cols):
            if app.board[row][col] == 0 and row != 0:
                    app.board[row][col] = app.board[row-1][col]
                    app.board[row-1][col] = 0

            elif app.board[row][col] == 0 and row == 0:
                    app.board[row][col] = None

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
 

def onStep(app):
    dropDown(app)
    getHint(app)
    


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

    app.player.score += addedScore * multiplier


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
        
        app.board = newBoard

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
        
            
def isGameOver(app):
    if app.player.score >= app.winningScore:
        app.won = True
        app.gameOver = True


    elif app.userMoves <= 0 :
        app.gameOver = True

def main():
    runApp()

main()
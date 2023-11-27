from cmu_graphics import *
from random import randint

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
            
            app.notSelected.insert(app.selectedPositions[len(app.selected)-1], app.selected.pop())
        
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
            for row, col in app.selected:
                app.board[row][col] = 0
            app.userMoves -=1

            for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
            


def onMousePress(app, mouseX, mouseY):
    pass

def redrawAll(app):

    drawGrid(app)
    
    for i in range(len(app.selected)-1):
       
        x,y = rowColToPixel(app, app.selected[i][0],app.selected[i][1])
        nextX, nextY = rowColToPixel(app, app.selected[i+1][0],app.selected[i+1][1])
        drawLine(x, y, nextX, nextY)
    
    makeColors(app)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            color = findColor(app, row, col)
            x, y = rowColToPixel(app, row, col)
            drawCircle(x, y, (app.boardWidth//app.cols)//3, 
                       fill = color, border = 'black')
            
    textColor = rgb(133, 90, 35)
    drawOval(app.width/2, app.height*(1/20), app.width/4, app.height/5, 
             fill = rgb(244, 206, 157), border = textColor, borderWidth = 10)
    drawLabel("Moves Left:", app.width/2, app.height*(1/28), size = 20, fill = rgb(97, 63, 19))
    drawLabel(f'{app.userMoves}', app.width/2, app.height*(1/12), size = 40)
    


def findColor(app, row, col):
    val = app.board[row][col]

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
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
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
        app.board[7][0] = 0
        app.board[5][3] = 0
    
        #call falling after pop 

            # if len(app.board[row]) != app.cols:
            #     for difference in range(app.cols-len(app.board[row])):
            #         app.board[row].insert(0,None)
    

def onStep(app):
    #'falling'     
    for row in range (app.rows-1,-1,-1):
        for col in range(app.cols):
            if app.board[row][col] == 0 and row != 0:
                    app.board[row][col] = app.board[row-1][col]
                    app.board[row-1][col] = 0

            elif app.board[row][col] == 0 and row == 0:
                    app.board[row][col] = None


    

def main():
    runApp()

main()
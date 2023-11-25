from cmu_graphics import *


def onAppStart(app):
    app.width = 800
    app.height = 800
    app.rows = 9
    app.cols = 9
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.boardWidth = (3/4)*app.width
    app.boardHeight = (3/4)*app.height
    app.boardLeft = (1/10)*app.width
    app.boardTop = (1/10)*app.height
    app.cellBorderWidth = 2


def onMouseDrag(app, mouseX, mouseY):
    pass

def onMousePress(app, mouseX, mouseY):
    pass

def redrawAll(app):
    
    drawBoard(app)
    
def makeColors(app):
    for row in range(app.board):
        for col in range(app.board[0]):
            color = randint(1,6) 
            app.board[row][col] = color


def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])
            
            
            
def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)
           
         
           

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
             
def rowColToPixel(app, row, col):
    cellWidth = app.width//app.cols
    cellHeight = app.height//app.rows
    return cellWidth*col + cellWidth //2 , cellHeight*row + cellHeight // 2
             
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def main():
    runApp()

main()
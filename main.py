from cmu_graphics import *
from random import randint
import copy
from PIL import Image
from starting import *
from hint import *
from shuffle import *




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
                                app.userScore +=450
                                app.board[horizontal][col] = 0
                        
                        
                #if horizontal jelly, take all jellies in that row
                elif app.board[row][col]>20:
                 
                        for vertical in range(app.cols):
                            if (row, vertical) not in app.selected:
                                app.userScore +=450
                                app.board[row][vertical] = 0
                            
                
                app.board[row][col] = 0
           
            app.userMoves -=1
            if len(app.selected)>=6:
                makeStriped(app)

            for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
        #checks if the game is over after every move
        app.showHint = False
        isGameOver(app.winningScore)
        
    
            
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
    drawLabel(f'Score: {int(app.userScore)}', app.width*3/20, app.height*1/25, size = 25)
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
            msg = (f'Congratulations, you scored {int(app.userScore)} and won!')
            retryColor = rgb(10, 107, 24)
            lastPic = app.winImage
        else: 
            rectColor = rgb(227, 104, 79)
            msg = (f"Oh no, you've run out of moves! Your score was {int(app.userScore)}.")
            retryColor = rgb(194, 23, 17)
            lastPic = app.loseImage

        drawRect(app.width/7, app.height/4, app.width*(5/7), app.height/2, fill = rectColor)
        drawLabel(msg, app.width/2, app.height/3, size = 20)
        drawLabel('Play Again?', app.width/2, app.height*(2/5), size = 25)
        drawImage(lastPic, app.width/2, app.height*(107/200), align = 'center')
        pilImage = app.retryImage.image
        drawCircle(app.width/2, app.height*(321/480), pilImage.width/5, fill = retryColor)
        drawImage(app.retryImage, app.width/2, app.height*(2/3), align='center', width = pilImage.width/3, height = pilImage.height/3)


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
    
def distance(x1, x2, y1, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**.5

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
          
            
def isGameOver(app):
    if app.userScore >= app.winningScore:
        app.won = True
        app.gameOver = True


    elif app.userMoves <= 0 :
        app.gameOver = True

def main():
    runApp()

main()

from cmu_graphics import *
from random import randint
import copy
from PIL import Image
from starting import *
from hint import *
from shuffle import *
from userClass import *
from coloring import *


def redrawAll(app):
    #grass background
    pilImage = app.backgroundImage.image
    drawImage(app.backgroundImage, app.width/2, app.height/2, align='center', width = pilImage.width*(4/3), height = pilImage.height*(4/3))
    
    #board background
    borderColor = rgb(163, 99, 3)
    drawRect(app.width*1/10, app.height*31/224, app.width*4/5, app.height*4/5, fill = borderColor)
    
    drawGrid(app)
    
    #drawing line between selected jellies
    for i in range(len(app.selected)-1):
       
        x,y = rowColToPixel(app, app.selected[i][0],app.selected[i][1])
        nextX, nextY = rowColToPixel(app, app.selected[i+1][0],app.selected[i+1][1])
        drawLine(x, y, nextX, nextY)
    
    makeColors(app)

    #drawing jellies
    for row in range(app.rows):
        for col in range(app.cols):
            val = app.board[row][col]
          
            image = findColor(app, val)[0]
            x, y = rowColToPixel(app, row, col)
            #vertical
            if val > 10 and val < 20:
                
                drawImage(image, x, y, align='center')
                drawImage(app.verticalImage,x,y,align='center')
            #horizontal
            elif val>20:
                drawImage(image, x, y, align='center')
                drawImage(app.horizontalImage,x,y,align='center')
            #normal
            else: 
                drawImage(image, x, y, align='center')


    #moves left counter        
    drawOval(app.width/2, app.height*(1/20), app.width/4, app.height/5, 
             fill = rgb(244, 206, 157), border = borderColor, borderWidth = 10)
    drawLabel("Moves Left:", app.width/2, app.height*(1/28), size = 20, fill = rgb(97, 63, 19))
    drawLabel(f'{app.player.moves}', app.width/2, app.height*(1/12), size = 40)
    
    #score and target jelly
    drawLabel(f'Score: {int(app.player.score)}', app.width*3/20, app.height*1/25, size = 25)
    drawLabel('target:', app.width*1/10,app.height*1/10, size = 20)
    drawImage(findColor(app, app.targetJelly)[0], app.width*15/80,app.height*1/10, align = 'center')

    #hint button
    lightbulb = app.lightbulbImage.image
    drawCircle(app.width*33/40, app.height/15, lightbulb.height/45, fill = 'white', border = 'black', borderWidth = 2)
    drawImage(app.lightbulbImage, app.width*33/40, app.height/15, align='center', width = lightbulb.width/18, height = lightbulb.height/18)

    #shuffle button
    shuffleButton = app.shuffleImage.image
    drawCircle(app.width*7/10, app.height/15, shuffleButton.width/12, fill = 'white', border = 'black', borderWidth = 2)
    drawImage(app.shuffleImage, app.width*7/10, app.height/15, align='center', width = shuffleButton.width/8, height = shuffleButton.height/8)

    #falling speed counter
    drawLabel('Falling', app.width/20, app.height*45/80, size = 18)
    drawLabel('Speed:', app.width/20, app.height*47/80, size = 18)
    drawLabel(f'{app.stepsPerSecond//4 + 1}', app.width/20, app.height*25/40, size = 20)

    #falling speed plus button
    drawCircle(app.width/20, app.height*7/10, app.boardWidth//(app.rows*2), fill = 'white', border = 'black')
    plus = app.plusImg.image
    drawImage(app.plusImg, app.width/20, app.height*7/10, align = 'center', width =  plus.width/4, height =  plus.height/4)
    
    #falling speed minus button
    drawCircle(app.width/20, app.height*8/10, app.boardWidth//(app.rows*2), fill = 'white', border = 'black')
    minus= app.minusImg.image
    drawImage(app.minusImg, app.width/20, app.height*8/10, align = 'center', width = minus.width/25, height = minus.height/25)
    
    #instruction button
    info = app.infoImg.image
    drawCircle(app.width*75/80, app.height/15, info.height/7, fill = 'white')
    drawImage(app.infoImg, app.width*75/80, app.height/15, align = 'center', width = info.width/3, height = info.height/3)

    #showing instructions, will only draw if app.showInstructions is true
    makeInstructions(app)


    #end screens, can either be loss or win screen
    if app.player.gameOver == True:
        
        #covers board
        drawRect(0, 0, app.width, app.height, fill = rgb(157, 135, 168), opacity = 78)
        
        #info for win end screen 
        if app.player.won == True:
            rectColor = rgb(139, 209, 125)
            msg = (f'Congratulations, you scored {int(app.player.score)} and won!')
            retryColor = rgb(10, 107, 24)
            lastPic = app.winImage

        else: 
        #info for lose end screen
            rectColor = rgb(227, 104, 79)
            msg = (f"Oh no, you've run out of moves! Your score was {int(app.player.score)}.")
            retryColor = rgb(194, 23, 17)
            lastPic = app.loseImage

        #end screen, changes based on if won or not
        drawRect(app.width/7, app.height/4, app.width*(5/7), app.height/2, fill = rectColor)
        drawLabel(msg, app.width/2, app.height/3, size = 20)
        drawLabel('Play Again?', app.width/2, app.height*(2/5), size = 25)
        drawImage(lastPic, app.width/2, app.height*(107/200), align = 'center')
        #retry button
        retry = app.retryImage.image
        drawCircle(app.width/2, app.height*(321/480), retry.width/5, fill = retryColor)
        drawImage(app.retryImage, app.width/2, app.height*(2/3), align='center', width = retry.width/3, height = retry.height/3)

#draws the grid
def drawGrid(app):
    cellWidth = app.boardWidth//app.cols
    cellHeight = app.boardHeight//app.rows
    for row in range(app.rows):
        for col in range(app.cols):
           
            #if selected, change colors of those grid squares 
            if (row,col) in app.selected:
                color = rgb(255, 236, 204)

            #if in hint, change colors of squares in hint
            elif(row,col) in app.hint:
                color = rgb(137, 197, 240)

            #make checkered patteren 
            elif abs(row-col)%2 == 0:
                color = rgb(222,172,120)

            else:
                color = rgb(234,192,150)
          
            x = app.boardLeft + col*cellHeight
            y = app.boardTop + row*cellWidth
            drawRect(x, y, cellWidth, cellHeight, 
                     fill = color)


#draws instructions
def makeInstructions(app):

    if app.showInstructions == True:
        #cover/background
        drawRect(0, 0, app.width, app.height, fill = rgb(199, 171, 137), opacity = 60)
        drawRect(app.width/7, app.height/5, app.width*(5/7), app.height*2/3, fill = rgb(186, 139, 91), border = rgb(77, 45, 8), borderWidth = 4)
        
        #general game info
        info = app.infoImg.image
        drawImage(app.infoImg, app.width*9/24, app.height/4,align = 'center', width = info.width/3, height = info.height/3)
        drawLabel('How to Play:', app.width*51/96, app.height/4, size = 30, bold = True)
        drawLabel('Match 3 or more of the same color jelly to pop them!', app.width*1/2, app.height*13/40, size = 20)
        drawLabel('The more jellies connected in a match, the higher the score!', app.width*1/2, app.height*3/8, size = 20)
        
        #hint info
        lightbulb = app.lightbulbImage.image
        drawCircle(app.width*3/14, app.height*15/32, lightbulb.height/45, fill = 'white', border = 'black', borderWidth = 2)
        drawImage(app.lightbulbImage, app.width*3/14, app.height*15/32, align='center', width = lightbulb.width/18, height = lightbulb.height/18)
        drawLabel('Click to highlight best move on board!', app.width/2, app.height*15/32, size = 20)
        
        #shuffle info
        pilImage = app.shuffleImage.image
        drawCircle(app.width*3/14, app.height*21/36, pilImage.width/12, fill = 'white', border = 'black', borderWidth = 2)
        drawImage(app.shuffleImage, app.width*3/14, app.height*21/36, align='center', width = pilImage.width/8, height = pilImage.height/8)
        drawLabel('Click to shuffle board!', app.width*23/56, app.height*21/36, size = 20)

        #falling speed info
        drawCircle(app.width*3/14, app.height*7/10, app.boardWidth//(app.rows*3/2), fill = 'white', border = 'black')
        pilImage = app.plusImg.image
        drawImage(app.plusImg, app.width*3/14, app.height*7/10, align = 'center', width = pilImage.width/3, height = pilImage.height/3)
    
        drawCircle(app.width*37/112, app.height*7/10, app.boardWidth//(app.rows*3/2), fill = 'white', border = 'black')
        pilImage = app.minusImg.image
        drawImage(app.minusImg, app.width*37/112, app.height*7/10, align = 'center', width = pilImage.width/20, height = pilImage.height/20)

        drawLabel('Click to make falling speed faster/slower!', app.width*69/112, app.height*7/10, size = 20)

        #final goal
        drawLabel(f'Goal: Reach a score of {app.winningScore} in {app.player.moves} moves or less!', app.width/2, app.height*51/64, size = 23, bold = True)

        #x-out
        xImage = app.xImg.image
        drawImage(app.xImg, app.width*45/56, app.height/4, align = 'center', width = xImage.width/16, height = xImage.height/16)

        
#returns pixel location of the center of each row col pair
def rowColToPixel(app, row, col):
    cellWidth = app.boardWidth//app.cols
    cellHeight = app.boardWidth//app.rows
    return (cellWidth*col + cellWidth //2 + app.boardLeft, 
            cellHeight*row + cellHeight // 2 + app.boardTop)
 


def onMouseDrag(app, mouseX, mouseY):

    if app.player.gameOver == False:
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
                #puts back undone selection back into notSelected
                app.notSelected.insert(app.selectedPositions[ind + 1], app.selected.pop(ind + 1))
            
   

def onMouseRelease(app, mouseX, mouseY):
    
    #nothing will happen if selected connection is 2 jellies or less, put back into notSelected
    if len(app.selected) < 3:
        for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
                
    
    #length is greater than or equal to 3
    else:
        
        intial = app.board[app.selected[0][0]][app.selected[0][1]]%10
        
        #if one of the selected jellies aren't the same color, put all selected back into notSelected
        for cx, cy in app.selected:
            
            if app.board[cx][cy]%10 != intial:
                for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
                
                break
                
            
        #all the same color, valid move
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
            #player makes a move
            app.player.moves -=1
            
            #if user pops 6 or more jellies, special jelly is generated
            if len(app.selected)>=6:
                makeStriped(app)

            for i in range(len(app.selected)-1 , -1, -1):
                    app.notSelected.insert(app.selectedPositions[i], app.selected.pop(i))
        
        #after every move, hint is turned off
        app.showHint = False

        #checks if the game is over after every move
        app.player.isGameOver(app, app.winningScore)
        
    
            


def onMousePress(app, mouseX, mouseY):
   
   #retry button clickable if game is over
    if app.player.gameOver == True: 
        retry = app.retryImage.image
        if distance(mouseX, app.width/2, mouseY, app.height*(2/3)) < retry.width/5:
            onStart(app)
    else: 
        #x out button clickable if instructions are showing
        if app.showInstructions == True:
            xImage = app.xImg.image
            if distance(mouseX, app.width*45/56, mouseY, app.height/4) < xImage.width/30:
                app.showInstructions = not app.showInstructions

        else:
            #hint, shuffle, instruction, and change fall speed buttons are all 
            # clickable when game is being played 
            lightbulb = app.lightbulbImage.image
        
            if distance(mouseX, app.width*33/40, mouseY, app.height/15) < lightbulb.height/45:
                app.showHint = not app.showHint
            
            shuffleIcon = app.shuffleImage.image
            if distance(mouseX, app.width*7/10, mouseY, app.height/15) < shuffleIcon.width/12:
                shuffle(app)

            
            info = app.infoImg.image
            if distance(mouseX, app.width*75/80, mouseY, app.height/15) < info.height/7 :
                app.showInstructions = not app.showInstructions
            
        

            changeFallSpeed(app, mouseX, mouseY)


def changeFallSpeed(app, mouseX, mouseY):
    #if clicked plus, add to stepsPerSec (faster falling)
    if ((distance(mouseX, app.width/20, mouseY, app.height*7/10) < app.boardWidth//(app.rows*2)) and (app.stepsPerSecond < 28)):
        
        app.stepsPerSecond +=4

    #if clicked minus, subtract to stepsPerSec (slower falling)
    if ((distance(mouseX, app.width/20, mouseY, app.height*8/10) < app.boardWidth//(app.rows*2)) and (app.stepsPerSecond > 4)):
     
        app.stepsPerSecond -=4


def onStep(app):
    #speed is changing based on steps per sec
    dropDown(app)
    getHint(app)


#'falling'
def dropDown(app):
  
    for row in range (app.rows-1,-1,-1):
        for col in range(app.cols):
            if app.board[row][col] == 0 and row != 0:
                    app.board[row][col] = app.board[row-1][col]
                    app.board[row-1][col] = 0

            elif app.board[row][col] == 0 and row == 0:
                    app.board[row][col] = None


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

def distance(x1, x2, y1, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**.5


def main():
    runApp()

main()

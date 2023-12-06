from cmu_graphics import *
from random import randint
import copy
from PIL import Image
from userClass import *


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
    app.stepsPerSecond = 13
    app.showInstructions = True
    

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

    #https://thenounproject.com/browse/icons/term/information/
    app.infoImg = Image.open('images/info.png')
    app.infoImg = CMUImage(app.infoImg)

    #https://www.iconfinder.com/icons/2337861/close_close_button_exit_quit_x_icon
    app.xImg = Image.open('images/x.webp')
    app.xImg = CMUImage(app.xImg)

    
#reset each new game
def onStart(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.notSelected = app.centers
    app.selected = []
    
    #keeps app.notSelected ordered when inserting back
    app.selectedPositions = []
    
    #what the target jelly is this round 
    app.targetJelly = randint(1,6)
    
    app.totalMoves = 20
    app.hint =[]
    app.showHint = False
    app.scores = dict()
    app.player = user(0, app.totalMoves)


def loadCenters(app):
    L = []
    for row in range(app.rows):
        for col in range(app.cols):
            x, y = row, col
            L.append((x,y))
    return L



 

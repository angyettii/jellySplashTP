from random import randint

#assigns a color to each value on board
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

#generates colors at start of game
def makeColors(app):
    
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == None:
                color = randint(1,6) 
                app.board[row][col] = color


#makes a striped jelly 
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


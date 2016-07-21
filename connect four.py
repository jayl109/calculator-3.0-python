import pygame, sys, random
from pygame.locals import *

pygame.init()
WINDOWWIDTH=700
WINDOWHEIGHT=600
LIGHTBLUE=(0,255,255)
YELLOW=(255,255,0)
RED=(255,0,0)
BLACK=(0,0,0)
BOARDWIDTH=500
BOARDHEIGHT=BOARDWIDTH*6//7
HEIGHTDIVISION=int(BOARDHEIGHT/6)
WIDTHDIVISION=BOARDWIDTH/7
CIRCLERADIUS=int(WIDTHDIVISION*.47)
pygame.mixer.music.load('yamada.mp3')
pygame.mixer.music.play(-1, 0.0)
#pygame.draw.rect(MAINDISPLAY, YELLOW, (BOARD.left, BOARD.top,BOARD.width, BOARD.height))
def initializeboard(BOARDRECTANGLES): #draws empty board
    for column in BOARDRECTANGLES:
        for rectangle in column:
            pygame.draw.rect(MAINDISPLAY, YELLOW, rectangle, 0)
            pygame.draw.rect(MAINDISPLAY, BLACK, rectangle, 1)
            pygame.draw.circle(MAINDISPLAY, LIGHTBLUE, rectangle.center, CIRCLERADIUS)
            
def restart():
    MAINDISPLAY.fill(LIGHTBLUE)
    global BOARDSTATES
    BOARDSTATES=[[0 for i in range(6)] for j in range(7)]
    initializeboard(BOARDRECTANGLES)
    
def gameover(BOARDSTATES): #returns 1 if red wins, 2 if black wins, False if neither
    def checkhorizontal(BOARDSTATES):
        for x, column in enumerate(BOARDSTATES):
            for y, state in enumerate(column):
                if state==0:
                    continue
                try:
                    if state==BOARDSTATES[x+1][y]==BOARDSTATES[x+2][y]==BOARDSTATES[x+3][y]:
                        return state
                except IndexError:
                    pass
        return False
    def checkvertical(BOARDSTATES):
        for x, column in enumerate(BOARDSTATES):
            for y, state in enumerate(column):
                if state==0:
                    continue
                try:
                    if state==BOARDSTATES[x][y+1]==BOARDSTATES[x][y+2]==BOARDSTATES[x][y+3]:
                        return state
                except IndexError:
                    pass
        return False
    def checkleftdiagonal(BOARDSTATES):
        for x, column in enumerate(BOARDSTATES):
            for y, state in enumerate(column):
                if state==0:
                    continue
                try:
                    if state==BOARDSTATES[x-1][y-1]==BOARDSTATES[x-2][y-2]==BOARDSTATES[x-3][y-3]:
                        return state
                except IndexError:
                    pass
    def checkrightdiagonal(BOARDSTATES):
        for x, column in enumerate(BOARDSTATES):
            for y, state in enumerate(column):
                if state==0:
                    continue
                try:
                    if state==BOARDSTATES[x+1][y-1]==BOARDSTATES[x+2][y-2]==BOARDSTATES[x+3][y-3]:
                        return state
                except IndexError:
                    pass
    if checkhorizontal(BOARDSTATES)==1 or checkvertical(BOARDSTATES)==1 or checkrightdiagonal(BOARDSTATES)==1 or checkleftdiagonal(BOARDSTATES)==1:
        return 1
    elif checkhorizontal(BOARDSTATES)==2 or checkvertical(BOARDSTATES)==2 or checkrightdiagonal(BOARDSTATES)==2 or checkleftdiagonal(BOARDSTATES)==2:
        return 2
    
    return False
                
            
def createboard(board):#RETURNS A LIST OF A LIST OF RECTANGLES BY COLUMN
    list=[]
    toaddlist=[]
    for x in range (7):
        for y in range (6):
            toaddlist.append(pygame.Rect(BOARD.left+x*WIDTHDIVISION,BOARD.top+y*HEIGHTDIVISION, WIDTHDIVISION, HEIGHTDIVISION))
        list.append(toaddlist)
        toaddlist=[]
    return list
def getrectangleat(mousex, mousey): #returns coordinates of rectangle (tuple) at mouse point if applicable
    for x, column in enumerate(BOARDRECTANGLES):
        for y, rectangle in enumerate(column):
            if rectangle.collidepoint(mousex, mousey)==True:
                return (x, y)
    return None
def isvalidlocation(location):
    if location[1]==5:
        if BOARDSTATES[location[0]][5]==0:#checks if that spot is empty and in bottom row
            return True
        else:
            return False
    elif BOARDSTATES[location[0]][location[1]+1]!=0:
        return True
    return False
def player2moveslocation(): #returns a random new location
    while True:
        location=(random.randint(0,6), random.randint(0,5))
        if BOARDSTATES[location[0]][location[1]]==0 and isvalidlocation(location):
            return location
def player2moves():
    location=player2moveslocation()
    BOARDSTATES[location[0]][location[1]]=2
    pygame.draw.circle(MAINDISPLAY, BLACK, BOARDRECTANGLES[location[0]][location[1]].center, CIRCLERADIUS)
    if gameover(BOARDSTATES)==2:        
        MAINDISPLAY.blit(Losemessagesurface,Loserectangle)
        pygame.display.update()
        pygame.time.wait(1000)
        restart()
    pygame.display.update()
    
def main():
    
    global BOARD, MAINDISPLAY, BOARDRECTANGLES, BOARDSTATES, Winmessagesurface, Winrectangle, Losemessagesurface, Loserectangle
    MAINDISPLAY=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MAINDISPLAY.fill(LIGHTBLUE)
    pygame.display.set_caption('Connect Four')
    

    BOARD=pygame.Rect((WINDOWWIDTH-BOARDWIDTH)/2, (WINDOWHEIGHT-BOARDHEIGHT)/2, BOARDWIDTH, BOARDHEIGHT)
    
    #pygame.draw.circle(MAINDISPLAY, RED, (87, 525), 20, 0)
    BOARDRECTANGLES=createboard(BOARD)
    #print BOARDRECTANGLES
    BOARDSTATES=[[0 for i in range(6)] for j in range(7)]
   
    Winmessage = pygame.font.Font('freesansbold.ttf', 12)
    Winmessagesurface = Winmessage.render('YOU WIN!', True, BLACK)
    Winrectangle = Winmessagesurface.get_rect()
    Winrectangle.center=((WINDOWWIDTH//2), (BOARD.midtop[1])//2)
    Losemessage = pygame.font.Font('freesansbold.ttf', 12)
    Losemessagesurface = Losemessage.render('YOU LOSE!', True, BLACK)
    Loserectangle = Losemessagesurface.get_rect()
    Loserectangle.center=((WINDOWWIDTH//2), (BOARD.midtop[1])//2)
    initializeboard(BOARDRECTANGLES)
    
    while True:
        for event in pygame.event.get():
            if event.type==KEYUP and event.key == K_ESCAPE or event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if getrectangleat(mousex, mousey) != None and isvalidlocation(getrectangleat(mousex, mousey)):
                    location=getrectangleat(mousex, mousey)
                    #print ("location clicked: ", location)
                    
                    BOARDSTATES[location[0]][location[1]]=1
                    pygame.draw.circle(MAINDISPLAY, RED, BOARDRECTANGLES[location[0]][location[1]].center, CIRCLERADIUS)
                    #print BOARDSTATES
                    if gameover(BOARDSTATES)==1:
                         print "You win!"
                         MAINDISPLAY.blit(Winmessagesurface,Winrectangle)
                         pygame.display.update()
                         pygame.time.wait(1000)
                         restart()
                         pygame.display.update()
                         continue
                    pygame.display.update()                         
                    player2moves()
                        
            pygame.display.update()

if __name__ == '__main__':
    main()
    

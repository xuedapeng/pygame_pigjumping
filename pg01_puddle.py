import pygame, sys,time,datetime
import random,cmath,math
from pygame.locals import *


# set up the window

TITLE = 'Pappa Jumping' #peiqi jiayou

PIC_H = 200
PIC_W = 149
BK_H =800
BK_W =960
BAL_H = 65
BAL_W = 50

WIDTH = 960
HEIGHT = 600

UP = 'up'
DOWN = 'down'
STOP = 'stop'
MAX_HEIGHT = HEIGHT-PIC_H
MAX_TIME = 800
AIR_TIME = 500
# STEP = 15

GREEN = (0,255,0)
BLUE = (0,0,128)
WHITE = (255,255,255)
RED = (255,0,0)

GAME_TIME = 180

ACTOR_DICT = {pygame.K_1:'images/peiqi0.png'\
              , pygame.K_2:'res/actor/fanken.png'\
              }


G_xRange = [10,WIDTH-PIC_W-50]

STEP_Y = 50
ACC_Y = 2

    
print 'yyy'
assert 2==2,'xxx';


def main():
    global fpsClock, DISPLAYSURF,PIC_W,PIC_H
    global catx,caty,height,direction,xstep,catImg
    global ballx,bally,ballImg,ballImgs,ballx_shift
    global congx,congy,congImg,congFlg
    global score,startTime,remainTime,pauseStartTime,pauseTime
    global isOver,isPause
    global soundObjHaha
    global studyImgs,studyImg,studySounds,studySound
    global xstep,xstep0,ystep,ystep0
    global parachuteImg,paraW,paraH
    
    pygame.init()

    FPS = 30 # frames per second setting
    
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption(TITLE)
    fpsClock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    selectActor(pygame.K_1) #peiqi
    
    background = pygame.image.load('images/nikeng2.png')
    congImg = pygame.image.load('images/great0.png')
    ballImgs = [pygame.image.load('images/ball_yellow0.png')\
                ,pygame.image.load('images/ball_red0.png')\
                ,pygame.image.load('images/ball_purple0.png')\
                ,pygame.image.load('images/ball_pink0.png')\
                ,pygame.image.load('images/ball_green0.png')\
                ,pygame.image.load('images/ball_blue0.png')]
    parachuteImg = pygame.image.load('res/actor/parachute0.png')
    
    setStudyObj()
    setPicSize()


    
    #pygame.mixer.music.load('music/jumpingMuddy.wav')
    #pygame.mixer.music.play(-1,0.0)
    soundObjs = [pygame.mixer.Sound('music/jumpingMuddy.wav')\
                 ,pygame.mixer.Sound('music/jumpingMuddyCn.wav')]
    soundObjHaha = pygame.mixer.Sound('music/haha.wav')

    '''
    height = 0
    catx = WIDTH/2+PIC_W-80
    caty = getY(height)

    print('catY=',caty)
 

    direction = STOP



    ballx = random.randint(G_xRange[0],G_xRange[1])
    bally = 0
    congFlg = -1
    ballx_shift = 0

    score = 100
    startTime = int(round(time.time()))
    remainTime = GAME_TIME
    isOver = 0'''

    restart()
    
    stime = 0
    maxheight = MAX_HEIGHT
    escapTime = 0;
    
    while True: # the main game loop
        DISPLAYSURF.fill(WHITE)

        if isPause :
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    isPause = False
                    pauseTime += (int(round(time.time())) - pauseStartTime)
                    if isOver:
                        isOver = False
                        restart()

            if isPause:
                continue
        
        if direction == UP:
            
            ystep -= ACC_Y
            if ystep<0:
                ystep = 1
            height+=ystep
            caty = getY(height)
            if (not ((catx<G_xRange[0] and xstep<0) or (catx>G_xRange[1] and xstep>0))):
                catx += xstep
            #if height >= maxheight:
            if ystep<5:
                direction = DOWN
                #print 'down:ystep',ystep
                ystep = 0
                #if random.randint(1,3) == 1:
                    #soundObjHaha.play()

            
            #print 'ystep=',ystep
                
        elif direction == DOWN:
            #if ystep < STEP_Y/5:
            if paraH >= parachuteImg.get_rect().height/3:
                ystep = STEP_Y/10
            else:
                ystep += ACC_Y/5.0
            height-=ystep
            caty = getY(height)

            if (not ((catx<G_xRange[0] and xstep<0) or (catx>G_xRange[1] and xstep>0))):
                catx += (xstep if paraH < parachuteImg.get_rect().height/3 else xstep/2)
            if height <= 0:
                direction = STOP
                height = 0
                caty = getY(height)
                escapTime = 0
                #print('catx=',catx)

            
            #print 'ystep=',ystep

                

        DISPLAYSURF.blit(background, (0, HEIGHT-BK_H+30))
        DISPLAYSURF.blit(catImg, (catx, caty))
        if direction == DOWN and maxheight>MAX_HEIGHT/3 and height < MAX_HEIGHT-parachuteImg.get_rect().height/2:
            drawParachute()
        else:
            paraH=0
            paraW=0
        drawPower(100*escapTime/MAX_TIME);
        drawTitle()
        drawBall()
        drawCongratulations()
        drawScore()
        drawOver()

        if (stime>0):
            escapTime = int(round(time.time()*1000)) - stime
            if escapTime > MAX_TIME:
                escapTime = MAX_TIME
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isPause = True
                    pauseStartTime = int(round(time.time()))
                    continue
                if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    selectActor(event.key)
                    continue

                if direction == STOP and event.key == pygame.K_SPACE:
                    stime = int(round(time.time()*1000))

            elif event.type == KEYUP:

                if direction == STOP and event.key == pygame.K_SPACE:
                    direction = UP;
                    stime = 0;

                    maxheight = escapTime*MAX_HEIGHT/MAX_TIME
                    if maxheight<50:
                        maxheight = 50

                    
                    ystep = getYStep0(maxheight)
                    #print 'up:ystep',ystep
                    
                    xstep = getXstep(catx, xstep)
                    #\//soundObjs[0 if xstep>0 else 1].play()
 
        pygame.display.update()
        fpsClock.tick(FPS)

def getXstep(catx, xstep) :
    x = 5 

    if xstep > 0:
        x = -x
        
    if ((catx<G_xRange[0] and x<0) or (catx>G_xRange[1] and x>0)):
        x = -x

    return x
    
def getY(height):
 
    return HEIGHT-height-PIC_H

def drawPower(val):
    pygame.draw.rect(DISPLAYSURF, WHITE, (WIDTH-25, HEIGHT-MAX_TIME/10, 20, MAX_TIME/10))

    if val>0:    
        pygame.draw.rect(DISPLAYSURF, BLUE, (WIDTH-25, HEIGHT-val, 20, val))
        fontObj = pygame.font.Font('freesansbold.ttf',32)
        textSurfaceObject = fontObj.render(str(val),True,GREEN,BLUE)
        textRectObj = textSurfaceObject.get_rect()
        textRectObj.center = (WIDTH-25, HEIGHT-MAX_TIME/10-20)
        DISPLAYSURF.blit(textSurfaceObject,textRectObj)

def drawTitle() :
        '''
        fontObj = pygame.font.Font('freesansbold.ttf',24)
        textSurfaceObject = fontObj.render('Pappa Pig STEP 1 <Muddy Puddles>',True, BLUE,WHITE)
        textRectObj = textSurfaceObject.get_rect()
        textRectObj.center = (WIDTH/2, 20)
        DISPLAYSURF.blit(textSurfaceObject,textRectObj)
        '''
        


def audioControl() :
    random.randint(1,10)

def drawBall():
    global ballx,bally,congx,congy,congFlg,ballx_shift,ballImg,studyImg,studySound
    global score
     
    
    if (bally > HEIGHT) :
        bally = -BAL_H
        ballx = random.randint(G_xRange[0],G_xRange[1])
        score -= 10
                
        ballImg = ballImgs[random.randint(0,5)]
        studyIdx = random.randint(0,1)
        studyImg = studyImgs[studyIdx]
        studySound = studySounds[studyIdx]

    if (isCollide()) :
        congx = ballx-50
        congy = bally-100
        congFlg = 1
        bally = -BAL_H-150
        ballx = random.randint(G_xRange[0],G_xRange[1])
        score += 10
        soundObjHaha.play()
        ballImg = ballImgs[random.randint(0,5)]
        studyIdx = random.randint(0,len(studyImgs)-1)
        studyImg = studyImgs[studyIdx]
        studySound = studySounds[studyIdx]
        
    
    ballx_shift += 1
    if ballx_shift > 20:
        ballx_shift = -20

    if ballx_shift > 0:
        ballx += 0.5
    else:
        ballx -= 0.5
    
    bally += 2
    DISPLAYSURF.blit(ballImg, (ballx, bally))
    
    DISPLAYSURF.blit(studyImg, (ballx+BAL_W/2-studyImg.get_rect().width/2, bally+BAL_H))
    pygame.draw.line(DISPLAYSURF, RED, (ballx+BAL_W/2, bally+BAL_H-5),(ballx+BAL_W/2, bally+BAL_H+5),1)

    
    if bally<HEIGHT/3:
        
        if ((bally+250)/2)%100==1 :
            studySound.play()

def drawCongratulations():

    global congFlg
    
    if (bally < -BAL_H ):
        
        if congFlg>0:
            DISPLAYSURF.blit(congImg, (congx if congx>10 else 10, congy if congy >10 else 10))
            
        congFlg += 1

        if congFlg > 5:
            congFlg = -5

def drawScore():
    global remainTime,pauseTime
    
    remainTime = GAME_TIME - (int(round(time.time())) - startTime) + pauseTime
    mins = remainTime/60
    secs = remainTime%60

    if secs < 10 :
        secs = '0'+ str(secs)

    status = str(mins) + ':' + str(secs) + ' SCORE '+str(score)
        
    fontObj = pygame.font.Font('freesansbold.ttf',18)
    textSurfaceObject = fontObj.render(status,True, BLUE,WHITE)
    textRectObj = textSurfaceObject.get_rect()
    textRectObj.center = (WIDTH-100, 20)
    DISPLAYSURF.blit(textSurfaceObject,textRectObj)

def drawOver():

    global isOver,isPause,pauseStartTime
    tips = ''

    isFail = False
    
    if not isOver :
        if score <= 0:
            isOver = True
            isPause = True
            pauseStartTime = int(round(time.time()))
            tips = 'GAME OVER!'
            isFail = True
            
        elif remainTime <= 0 :
            isOver = True
            isPause = True
            pauseStartTime = int(round(time.time()))
            tips = str(score) + ' Good Job! '

    if isOver:
        fontObj = pygame.font.Font('freesansbold.ttf',36)
        textSurfaceObject = fontObj.render(tips,True, RED if isFail else GREEN,WHITE)
        textRectObj = textSurfaceObject.get_rect()
        textRectObj.center = (WIDTH/2, HEIGHT/2)
        DISPLAYSURF.blit(textSurfaceObject,textRectObj)

        

        

def restart() :
    
    global catx,caty,height,direction,step
    global ballx,bally,ballImg,ballImgs,ballx_shift,xstep
    global congx,congy,congImg,congFlg
    global score,startTime,remainTime,pauseTime
    global isOver,isPause
    global studyImgs,studyImg,studySounds,studySound
    global parachuteImg,paraW,paraH
    
    height = 0
    catx = WIDTH/2+PIC_W-80
    caty = getY(height)



    direction = STOP

    stime = 0
    maxheight = MAX_HEIGHT
    escapTime = 0;

    xshift = 0
    xstep = 2 * random.randint(-1,1)
    xstepCount = 0
    step = 30

    ballx = random.randint(G_xRange[0],G_xRange[1])
    bally = 0
    congFlg = -1
    ballx_shift = 0

    score = 100
    startTime = int(round(time.time()))
    remainTime = GAME_TIME
    isOver = False
    isPause = False
    pauseTime = 0

    ballImg = ballImgs[random.randint(0,5)]

    studyIdx = random.randint(0,1)
    studyImg = studyImgs[studyIdx]
    studySound = studySounds[studyIdx]

    #paraH = parachuteImg.get_rect().height-50
    #paraW = parachuteImg.get_rect().width-50

                                  
    

def isCollide() :
    b = [(ballx,bally),(ballx+BAL_W,bally),(ballx, bally+BAL_H),(ballx+BAL_W,bally+BAL_H)]
    c = [(catx,caty),(catx+PIC_W,caty),(catx, caty+PIC_H),(catx+PIC_W,caty+PIC_H)]

    for apex in b :
        if (apex[0]>c[0][0]+20 and apex[0]<c[1][0]-20 and apex[1]>c[0][1]+20 and apex[1]<c[2][1]-20):
            return True

    return False


def setStudyObj():
    
    global studyImgs,studySounds
    
    studyImgs = [pygame.image.load('res/fruit/apple.png')\
                ,pygame.image.load('images/banana0.png')\
                ,pygame.image.load('res/friends/cat.png')\
                ,pygame.image.load('res/friends/dog.png')\
                ,pygame.image.load('res/friends/pony.png')\
                ,pygame.image.load('res/friends/rabbit.png')\
                ,pygame.image.load('res/friends/sheep.png')\
                 ]
    studySounds = [pygame.mixer.Sound('music/apple.wav')\
                 ,pygame.mixer.Sound('music/banana.wav')\
                 ,pygame.mixer.Sound('res/friends/cat.wav')\
                 ,pygame.mixer.Sound('res/friends/dog.wav')\
                 ,pygame.mixer.Sound('res/friends/pony.wav')\
                 ,pygame.mixer.Sound('res/friends/rabbit.wav')\
                 ,pygame.mixer.Sound('res/friends/sheep.wav')\
                   ]
    
def setPicSize():
    global PIC_H,PIC_W
    PIC_H = catImg.get_rect().height
    PIC_W = catImg.get_rect().width

def selectActor(number):
    global catImg

    if ACTOR_DICT.has_key(number):
        catImg = pygame.image.load(ACTOR_DICT[number])
        setPicSize()

def getYStep0(mh):
    x = mh*1.0/MAX_HEIGHT*3.14/2
    y = math.sin(math.sin(x)*3.14/2)
    #print 'x,y=',x,y,mh/MAX_HEIGHT
    return STEP_Y*y

def drawParachute():

    global paraW,paraH,ystep
    
    pw = parachuteImg.get_rect().width
    ph = parachuteImg.get_rect().height

    if paraW < pw:
        paraW += 10
    if paraH < ph:
        paraH += 10

    
    
    parachuteImg2 = pygame.transform.smoothscale(parachuteImg,(paraW,paraH))
    px = catx+PIC_W/2-paraW/2
    py = caty-paraH+15
    DISPLAYSURF.blit(parachuteImg2, (px, py))
    #pygame.draw.rect(DISPLAYSURF, RED, (catx+PIC_W/2, caty-5),(catx+PIC_W/2, caty+15),1)


if __name__ == '__main__':
    main()

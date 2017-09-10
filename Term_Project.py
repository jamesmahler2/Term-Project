# James Mahler term project
import winsound
import math
import sys
import tkinter
from tkinter import *
import contextlib
import urllib.request
import os
import random
import scipy.stats
##################################
# INITIAL ANIMATION FUNCTIONS
##################################

def init(data):
    data.mode = "splashScreen"
    data.spot = "baselineL"
    data.left = ["baselineL", "leftWing", "topOfKey"]
    data.right = ["rightWing", "baselineR"]
    data.ballR = 8
    data.ballX = data.width//14
    data.ballY = data.height//2
    data.madeIt = None
    data.checkMeter = False
    data.shot = False
    data.meterX0 = data.width//10*8-15
    data.meterX1 = data.width//10*8+15
    data.meterY = data.height//5*3
    data.Yspeed = 50
    data.Xspeed = 29
    data.meterSpeed = -15
    data.time = 0
    data.start = False
    data.count = 0
    data.over = False
    data.bestTime = None
    data.bounce = False
    data.reachedMax = True #ONLY FOR TOK SPOT
    data.difficulty = None #For SPTime mode only
    # For SPP mode only:
    data.level = 1
    data.makes=0
    data.shots=0
    data.beatLevel = False
    data.failedLevel = False
    # For clouds:
    data.CX1 = data.width//7
    data.CX2 = data.width//2
    data.CX3 = data.width//8*7
    # For simulation mode only:
    data.player1 = None
    data.player2 = None
    data.PP1 = None
    data.PP2 = None
    data.selecting = "player1"
    data.open = False # Sees if a textbox is already open
    data.shooting = None # Tells us whose turn it is
    data.P1makes = 0
    data.P1shots = 0
    data.P2makes = 0
    data.P2shots = 0
    data.P1over = False
    data.P2over = False
    data.winner = None
    data.P1Chance = None
    data.P2Chance = None
    data.P1outcome = None
    data.P2outcome = None
    data.invalid = False

def mousePressed(event, data):
    if data.mode == "splashScreen":
        mousePressedSplashScreen(event, data)
    elif data.mode == "instructions": pass
    elif data.mode == "SPtime":
        mousePressedSPtime(event, data)
    elif data.mode == "SPP":
        mousePressedSPP(event, data)
    elif data.mode == "simulation":
        simMousePressed(event, data)

def keyPressed(event, data):
    if event.keysym == "m":
        if data.mode == "SPP":
            resetSPPdata(data)
        elif data.mode == "simulation":
            resetSimData(data)
        data.mode = "splashScreen"
        data.over = False
        resetData(data)
        initBL(data)
        data.start = False
        data.time = 0
        data.over = False
        data.difficulty = None
        data.spot = "baselineL"
    if data.mode == "splashScreen":
        keyPressedSplashScreen(event, data)
    elif data.mode == "instructions":
        keyPressedInstructions(event, data)
    elif data.mode == "SPtime":
        keyPressedSPtime(event, data)
    elif data.mode == "SPP":
        keyPressedSPP(event, data)
    elif data.mode == "simulation":
        simKeyPressed(event, data)

def timerFired(data):
    if data.mode == "splashScreen":
        timerFiredSplashScreen(data)
    elif data.mode == "instructions": pass
    elif data.mode == "SPtime":
        timerFiredSPtime(data)
    elif data.mode == "SPP":
        timerFiredSPP(data)
    elif data.mode == "simulation":
        simTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "splashScreen":
        redrawAllSplashScreen(canvas, data)
    elif data.mode == "instructions":
        redrawAllInstructions(canvas, data)
    elif data.mode == "SPtime":
        redrawAllSPtime(canvas, data)
    elif data.mode == "SPP":
        redrawAllSPP(canvas, data)
    elif data.mode == "simulation":
        simRedrawAll(canvas, data)

##################################
# MODE CALLS
##################################


##################################
# SPLASHSCREEN
##################################
def mousePressedSplashScreen(event, data):
    if event.y>=data.height//2 and event.y<=data.height//10*7:
        if data.width//10*4>=event.x>=data.width//10*2:
            data.mode = "SPtime"
        elif data.width//10*8>=event.x>=data.width//10*6:
            data.mode = "SPP"
    elif event.y>=data.height//10*7 and event.y<=data.height//10*9:
        if data.width//2+120>=event.x>=data.width//2-120:
            data.mode = "simulation"
    else: pass

def keyPressedSplashScreen(event, data):
    if event.keysym == "i":
        data.mode = "instructions"

def timerFiredSplashScreen(data):
    pass

def redrawAllSplashScreen(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    x=data.width//2
    y=data.height//8
    canvas.create_text(x, y, font="times 30", 
        text="Welcome to 112 Basketball! Select a game mode:", fill="red")
    GM1X0 = data.width//10*2
    GM1X1 = data.width//10*4
    GM1Y0 = data.height//2
    GM1Y1 = data.height//10*7
    canvas.create_rectangle(GM1X0, GM1Y0, GM1X1, GM1Y1, fill="red")
    canvas.create_text((GM1X0+GM1X1)//2, (GM1Y0+GM1Y1)//2, 
        text="Single Player for time", font="times 16")
    GM2X0 = data.width//10*6
    GM2X1 = data.width//10*8
    GM2Y0 = data.height//2
    GM2Y1 = data.height//10*7
    canvas.create_rectangle(GM2X0, GM2Y0, GM2X1, GM2Y1, fill="red")
    canvas.create_text((GM2X0+GM2X1)//2, (GM2Y0+GM2Y1)//2, 
        text="Single Player for %", font="times 16")
    canvas.create_text(data.width//2, data.height//3,
        text="press i for instructions", font="times 20 bold", fill="red")
    GM3X0 = data.width//2-120
    GM3X1 = data.width//2+120
    GM3Y0 = data.height//10*7
    GM3Y1 = data.height//10*9
    canvas.create_rectangle(GM3X0, GM3Y0, GM3X1, GM3Y1, fill="red")
    canvas.create_text((GM3X0+GM3X1)//2, (GM3Y0+GM3Y1)//2, 
        text="Simulation Mode!", font="times 16")

####################################
# INSTRUCTIONS
####################################

def keyPressedInstructions(event, data):
    if event.keysym == "m":
        data.mode = "splashScreen"
    else: pass

def redrawAllInstructions(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="red",
        width=0)
    x0 = data.width//4
    y0 = data.height//10
    x1 = data.width//12
    canvas.create_text(data.width//2, y0, 
        text="Here's how to play 112 basketball:", font="times 20")
    canvas.create_text(x1, y0*2, anchor=W,
        text="Single player for time:", font="times 16 bold")
    x='''
    In this game mode, you're trying to make all the shots as fast as you can, no
    matter how many times you miss. There are 3 different levels of difficulty.'''
    canvas.create_text(x0, y0*2.3, anchor=SW, text=x)
    canvas.create_text(x1, y0*3, anchor=W, text="Single player for %:",
        font="times 16 bold")
    y ='''
    In this game mode, you're trying to make all the shots with as high a 
    percentage as possible. There are three levels; to go to the next level, 
    you must make all 5 shots with at least 50% accuracy; as you 
    progress through the levels, the shots become harder to make.'''
    canvas.create_text(x0, y0*3.5, anchor = SW, text=y)
    z = '''
    To shoot, you press the space bar and wait until the bar on the screen goes
    into the green space. Then, press the space bar. If you press the spacebar 
    while the bar is in the green, you will make it. Otherwise, you will miss!'''
    canvas.create_text(x1, y0*4, anchor=W, text="How to shoot:",   
        font="times 16 bold")
    canvas.create_text(x0, y0*4.5, anchor=SW, text=z)
    canvas.create_text(x1, data.height//2, anchor=W, text="Simulation mode:",
        font="times 16 bold")
    simText='''
    In this game mode, you simulate a shooting contest between two NBA players,
    based on their real life career 3-point percentage. Just type in two players
    when prompted, and watch them face off!'''
    canvas.create_text(x0, data.height//2, anchor=W, text=simText)
    canvas.create_text(data.width//2, data.height//3*2, 
     text="Press m at any time to return to the main screen", font="times 16")

####################################
# SPTIME
####################################

def mousePressedSPtime(event, data):
    if data.difficulty != None: pass
    else:
        if 350>=event.y>=250:
            if 475>=event.x>=325:
                data.difficulty = "easy"
            elif 675>=event.x>=525:
                data.difficulty = "medium"
            elif 875>=event.x>=725:
                data.difficulty = "hard"

def keyPressedSPtime(event, data):
    if data.difficulty == None: pass
    elif event.keysym == "space":
        if data.over == True: pass
        elif data.shot == False:
            data.shot = True
        elif data.shot == True:
            data.checkMeter = True
        if data.spot == "topOfKey":
            if data.reachedMax == True: data.reachedMax = False
    if data.over == True:
        if event.keysym == "m":
            data.mode = "splashScreen"
            data.time = 0
            data.start = False
            data.over = False
            data.difficulty = None
            initBL(data)
            resetData(data)

def timerFiredSPtime(data):
    if data.spot == "topOfKey":
        if data.ballY < data.height // 6: data.reachedMax = True
    if data.shot == True:
        data.ballY -= data.Yspeed
        data.ballX+=data.Xspeed
        if data.checkMeter == False: data.meterY += data.meterSpeed
        data.Yspeed -=5
    if data.checkMeter == True:
        checkBarSPtime(data)
        if data.madeIt == True:
            madeIt(data)
        elif data.madeIt == False:
            shootAgain(data)
    if data.shot == True and data.spot == "baselineL": data.start = True
    if data.start == True: data.time+=1
    # For Clouds:
    data.CX1 += 5
    data.CX2 += 5
    data.CX3 += 5


def redrawAllSPtime(canvas, data):
    drawLandscape(canvas, data)
    drawGoal(canvas, data)
    drawBall(canvas, data)
    drawBar(canvas, data)
    x0=data.width//10
    x1 = data.width//5
    y0 = data.height//5
    canvas.create_text(data.width//15*14, data.height//12, 
        text="time: " + str(data.time/10))
    if data.difficulty == None:
        drawDifficultySelecter(canvas, data)
    if data.over == True:
        canvas.create_rectangle(x0, data.height//3, x0*9, y0*4, fill="black")
        canvas.create_text(data.width//2, data.height//2, text='''  Congratulations! You have completed this game mode.
    Your time was: '''+str(data.time/10)+" seconds. "+"Play again for a better time!", font="times 30", fill="blue")
        canvas.create_text(data.width//2, data.height//4*3, 
            text="press m for main screen", font="times 24", fill="blue")
        if data.bestTime == None or data.time < data.bestTime:
            data.bestTime = data.time/10
        canvas.create_text(data.width//2, data.height//3*2, text=("Best Time: " 
            + str(data.bestTime)+" seconds"), font="times 30", fill="blue")

def drawBar(canvas, data):
    if data.difficulty == "easy":
        drawEasyBar(canvas, data)
    elif data.difficulty == "medium":
        drawMediumBar(canvas, data)
    elif data.difficulty == "hard":
        drawHardBar(canvas, data)

def checkBarSPtime(data):
    if data.difficulty == "easy":
        if 275 >= data.meterY >= 240:
            data.madeIt = True
            madeIt(data)
        else: data.madeIt = False
    elif data.difficulty == "medium":
        if 260 >= data.meterY >= 240:
            data.madeIt = True
            madeIt(data)
        else: data.madeIt = False
    elif data.difficulty == "hard":
        if 248 >= data.meterY >= 240:
            data.madeIt = True
            madeIt(data)
        else: data.madeIt = False

###################################
# SPP
###################################

def mousePressedSPP(event, data):
    pass
def keyPressedSPP(event, data):
    if event.keysym == "space":
        if data.spot == "topOfKey":
            if data.reachedMax == True: data.reachedMax = False
        if data.over == True: pass
        elif data.shot == False:
            data.shot = True
            data.shots+=1
        elif data.shot == True:
            data.checkMeter = True
    if data.over == True:
        if event.keysym == "m":
            resetSPPdata(data)
    if data.beatLevel == True:
        if event.keysym == "c":
            continueSPP(data)
    elif data.failedLevel == True:
        if event.keysym == "r":
            data.makes = 0
            data.shots = 0
            data.failedLevel = False
            initBL(data)

def timerFiredSPP(data):
    if data.spot == "topOfKey":
        if data.ballY < data.height // 6: data.reachedMax = True
    if data.shot == True:
        data.ballY -= data.Yspeed
        data.ballX+=data.Xspeed
        if data.checkMeter == False: data.meterY += data.meterSpeed
        data.Yspeed -=5
    if data.checkMeter == True:
        checkBarSPP(data)
        if data.madeIt == True: madeIt(data)
        else: shootAgain(data)
    if data.shot == True and data.spot == "baselineL": data.start = True
    data.CX1 += 5
    data.CX2 += 5
    data.CX3 += 5

def redrawAllSPP(canvas, data):
    drawLandscape(canvas, data)
    drawGoal(canvas, data)
    drawBall(canvas, data)
    if data.over != True:
        canvas.create_line(data.meterX0, data.meterY, data.meterX1, 
            data.meterY, width=2)
    barWidth = data.width//10*8
    if data.level == 1:
        drawEasyBar(canvas, data)
    elif data.level == 2:
        drawMediumBar(canvas, data)
    elif data.level == 3:
        drawHardBar(canvas, data)
    if data.shots > 0: canvas.create_text(data.width//15*14, data.height//12, 
        text=str(round(data.makes/data.shots*100, 3))+"%")
    if data.beatLevel == True:
        beatLevel(canvas, data)
    elif data.failedLevel == True:
        failedLevel(canvas, data)
    if data.over == True:
        SPPOver(canvas, data)

def resetSPPdata(data):
    data.mode = "splashScreen"
    data.time = 0
    data.start = False
    data.over = False
    data.level=1
    data.shots = 0
    data.makes = 0
    initBL(data)
    resetData(data)

def continueSPP(data):
    data.level += 1
    data.beatLevel = False
    data.shots = 0
    data.makes = 0
    initBL(data)
    if data.level>3: data.over = True

def checkBarSPP(data):
    if data.level == 1:
        if 275 >= data.meterY >= 240:
            data.madeIt = True
    elif data.level == 2:
        if 260 >= data.meterY >= 240:
            data.madeIt = True
    elif data.level == 3:
        if 248 >= data.meterY >= 240:
            data.madeIt = True

def beatLevel(canvas, data):
    lb = data.width//4
    rb = data.width//4*3
    tb = data.height//4
    bb = data.height//4*3
    canvas.create_rectangle(lb, tb, rb, bb, fill="gray")
    canvas.create_text(data.width//2, data.height//2, 
        text="You have beaten level %s!!!" % data.level, font="times 24")
    canvas.create_text(data.width//2, data.height//3*2, 
        text="Press c to continue to the next level!", font="times 24")

def failedLevel(canvas, data):
    lb = data.width//4
    rb = data.width//4*3
    tb = data.height//4
    bb = data.height//4*3
    canvas.create_rectangle(lb, tb, rb, bb, fill="red")
    canvas.create_text(data.width//2, data.height//2,
        text="You have failed level %s )-:" % data.level, font="times 24")
    canvas.create_text(data.width//2, data.height//3*2, 
        text="Press r to retry this level", font="times 24")

def SPPOver(canvas, data):
    lb = data.width//4
    rb = data.width//4*3
    tb = data.height//4
    bb = data.height//4*3
    canvas.create_rectangle(lb, tb, rb, bb, fill="green")
    canvas.create_text(data.width//2, data.height//2, text='''
    You have completed this game mode!
    Press m to return to return to the main screen''', font="times 24")

###################################
# SIMULATION MODE
###################################
def simMousePressed(event, data):
    pass

def simKeyPressed(event, data):
    if event.keysym == "b":
        if data.start == False: data.start = True
    elif event.keysym == "c":
        if data.P1over == True and data.P2over == False: data.start = True
    if event.keysym == "m":
        data.mode = "splashScreen"
        data.start = False
        data.over = False
        initBL(data)
        resetData(data)

def simTimerFired(data):
    if data.spot == "topOfKey":
        if data.ballY < data.height // 6 and data.bounce == False:
            data.reachedMax = True
    if data.player1 == None or data.player2 == None:
        if data.open == False:
            data.open = True
            getPlayers(data)
    if data.start == True and data.shot == False:
        seeIfMade(data)
    if data.shot == True:
        data.ballY -= data.Yspeed
        data.ballX += data.Xspeed
        data.Yspeed -= 5
    if data.madeIt == True: madeIt(data)
    elif data.madeIt == False: shootAgain(data)
    data.CX1 += 5
    data.CX2 += 5
    data.CX3 += 5

def simRedrawAll(canvas, data):
    drawLandscape(canvas, data)
    drawGoal(canvas, data)
    drawBall(canvas, data)
    drawPlayers(canvas, data)
    if data.player1 != None and data.player2 != None and data.start == False:
        if data.P1over == False: promptBegin(canvas, data)
        elif data.P2over == False: promptNext(canvas, data)
        elif data.P1over == True and data.P2over == True:
            drawSimOver(canvas, data)

# I got some of the code in the getPlayers function from:
# http://stackoverflow.com/questions/15306197/how-to-use-text-box-in-tkinter-and-use-the-values-python-3
def getPlayers(data):
    root = Tk()
    root.title('112 Basketball')
    if data.invalid == True:
        data.selecting = "Enter a valid player!"
    elif data.player1 != None:
        data.selecting = "player2"
    Label(root, text='Enter a player! %s' % data.selecting).pack(side=TOP,padx=10,pady=10)    
    entry = Entry(root, width=25)
    entry.pack(side=TOP,padx=10,pady=10)
    
    # This function was borrowed, and modified (to work on python3),
    #from the Fall 2014 course website
    def readWebPage(url):
        assert(url.startswith("http://"))
        try:
            with contextlib.closing(urllib.request.urlopen(url)) as response:
                html=response.read()
                data.invalid = False
                return str(html)
        except:
            return False

    def get3pt():
        data.open = False
        first = None
        last = None
        player = entry.get()
        for name in player.split(" "):
            if first == None:
                first = name
            else: last = name
        url = "http://www.basketball-reference.com/players/%s/%s%s01.html" % (last[0], last[:5], first[:2])
        if readWebPage(url) != False:
            if data.player1 == None:
                data.player1 = player
                data.shooting = player
            else: data.player2 = player
            code = readWebPage(url)
            s = code.find("FG3%")
            thingToScan = code[s:s+75]
            percentage = float(thingToScan[20:24])
            if data.PP1 == None: data.PP1 = percentage
            else: data.PP2 = percentage
            return percentage
        else: data.invalid = True
    
    Button(root, text='OK', command=get3pt).pack(side=LEFT)
    root.mainloop()

def seeIfMade(data):
    data.shot = True
    check1 = data.PP1 * 10
    check2 = data.PP2 * 10
    numShot = random.randint(1, 1000)
    if data.shooting == data.player1:
        data.P1shots+=1
        if numShot <= check1:
            data.P1makes+=1
            data.madeIt = True
        else:
            data.madeIt = False
    elif data.shooting == data.player2:
        data.P2shots+=1
        if numShot <= check2:
            data.P2makes+=1
            data.madeIt = True
        else:
            data.madeIt = False

def getWinProb(data):
    # We will say that the variable Y is the difference of the two players' stats
    expected1 = round(5/(data.PP1/100), 2)
    expected2 = round(5/(data.PP2/100), 2)
    muY = expected1 - expected2
    P1D = data.PP1/100
    P2D = data.PP2/100
    variance1 = (5*(1-P1D))/(P1D ** 2)
    variance2 = (5*(1-P2D))/(P2D ** 2)
    vY = math.sqrt(variance1 + variance2)
    data.P1Chance = round(scipy.stats.norm(muY, vY).cdf(0), 3)
    data.P2Chance = 1 - data.P1Chance

def probOfOutcome(data):
    md=100 #make decimal
    data.P1outcome = scipy.stats.nbinom.pmf(data.P1shots, 5, data.PP1/md, loc=5)
    data.P2outcome = scipy.stats.nbinom.pmf(data.P2shots, 5, data.PP2/md, loc=5)

def drawPlayers(canvas, data):
    if data.PP2 != None:
        x0 = data.width//8
        x1 = data.width//8*7
        y0 = data.height//12*11
        y1 = data.height-29
        y2 = data.height
        expected1 = round(5/(data.PP1/100), 2)
        expected2 = round(5/(data.PP2/100), 2)
        S0 = "%   Expected # of shots: "
        canvas.create_text(x0, y0, text=data.player1+": "+str(data.P1makes)+"/"+str(data.P1shots), font="times 16")
        canvas.create_text(x1, y0, text=data.player2+": "+str(data.P2makes)+"/"+str(data.P2shots), font="times 16")
        canvas.create_text(x0, y1, text=str(data.PP1)+S0+str(expected1), 
            font="times 12")
        canvas.create_text(x1, y1, text=str(data.PP2)+S0+str(expected2), 
            font="times 12")
        getWinProb(data)
        S1 = "Win Probability: "
        canvas.create_text(x0, y2, anchor=S, 
            text=S1+str(data.P1Chance*100)+"%", font="times 12")
        canvas.create_text(x1, y2, anchor=S, 
            text=S1+str(data.P2Chance*100)+"%", font="times 12")

###################################
# DRAWING THINGS
###################################

def drawGoal(canvas, data):
    midX = data.width//2
    canvas.create_rectangle(0, data.height//3, data.width, data.height,
        fill="gray") #COURT
    bbdx = 50
    bbdy = 35
    bby = data.height//6
    sdx = 20
    sdy0 = 5
    sdy1 = 25
    canvas.create_rectangle(midX-bbdx, bby-bbdy, midX+bbdx, bby+bbdy, 
        fill="gray") #BACKBOARD
    canvas.create_rectangle(midX-sdx, bby-sdy0, midX+sdx, bby+sdy1, fill="gray",
        width=4) #SQUARE
    canvas.create_line(midX, bby+bbdy, midX, bby+130, width=8) #POST
    rimdx = 20
    rimy0 = data.height//4-15
    rimy1 = data.height//4+15
    canvas.create_oval(midX-rimdx, rimy0, midX+rimdx, rimy1, outline="orange",
        width=3) #RIM
    threePtX0 = data.width//12
    threePtX1 = data.width//12*11
    threePtY0 = -92
    threePtY1 = data.height//12*11
    canvas.create_arc(threePtX0, threePtY0, threePtX1, threePtY1, style=ARC,
        start=175, extent=190, width=3)  #3PTLINE
    lineX = data.width//3
    ldx = 90
    lineY1 = data.height//3
    lineY2 = data.height//10*6+40
    canvas.create_line(lineX+ldx, lineY1, lineX+ldx, lineY2, width=3) #LANE LINE
    canvas.create_line(lineX*2-ldx, lineY1, lineX*2-ldx, lineY2, 
        width=3) #LANE LINE
    canvas.create_line(lineX+ldx, lineY2, lineX*2-ldx, lineY2,
        width=3) #FREE THROW LINE
    kly2 = data.height//12*11
    canvas.create_arc(lineX+ldx, lineY1, lineX*2-ldx, kly2, style=ARC,
        start=180, extent=180, width=3) #KEY LINE

def drawBall(canvas, data):
    canvas.create_oval(data.ballX-data.ballR, data.ballY-data.ballR, 
        data.ballX+data.ballR, data.ballY+data.ballR, fill="orange")

def drawDifficultySelecter(canvas, data): #THIS IS ONLY FOR SPTIME
    boundaryX = data.width//4
    boundaryY = data.height//4
    yText = data.height//2
    xText = data.width//2
    down = 50
    canvas.create_rectangle(boundaryX, boundaryY, boundaryX*3, 
        boundaryY*3, fill="black")
    canvas.create_text(xText, boundaryY+down, text="Select a difficulty:",
        font="times 26", fill="blue")
    L1 = 25
    L2 = 225
    L3 = 425
    R1 = 175
    R2 = 375
    R3 = 575
    Y0 = boundaryY+100
    Y1 = boundaryY+200
    canvas.create_rectangle(boundaryX+L1, Y0, boundaryX+R1, Y1, fill="blue")
    canvas.create_rectangle(boundaryX+L2, Y0, boundaryX+R2, Y1, fill="blue")
    canvas.create_rectangle(boundaryX+L3, Y0, boundaryX+R3, Y1, fill="blue")
    xT1 = data.width//3
    xT2 = data.width//2
    xT3 = data.width//3*2
    canvas.create_text(xT1, yText, text="Easy", font="times 20")
    canvas.create_text(xT2, yText, text="Medium", font="times 20")
    canvas.create_text(xT3, yText, text="Hard", font="times 20")

def drawEasyBar(canvas, data):
    barWidth = data.width//10*8
    gbarTop = data.height//2.5
    rbarTop = data.height//4
    rbarBottom = data.height//5*3
    lenGBar = 35
    canvas.create_line(barWidth, rbarTop, barWidth, gbarTop, 
        fill="red", width=10)
    canvas.create_line(barWidth, gbarTop, barWidth, gbarTop+lenGBar, 
        fill="green", width=10)
    canvas.create_line(barWidth, gbarTop+lenGBar, barWidth, rbarBottom, 
        fill="red", width=10)
    canvas.create_line(data.meterX0, data.meterY, data.meterX1, data.meterY,
        width=2)

def drawMediumBar(canvas, data):
    barWidth = data.width//10*8
    gbarTop = data.height//2.5
    rbarTop = data.height//4
    rbarBottom = data.height//5*3
    lenGBar = 20
    canvas.create_line(barWidth, rbarTop, barWidth, gbarTop, fill="red",
        width=10)
    canvas.create_line(barWidth, gbarTop, barWidth, gbarTop+lenGBar, 
        fill="green", width=10)
    canvas.create_line(barWidth, gbarTop+lenGBar, barWidth, rbarBottom,
        fill="red", width=10)
    canvas.create_line(data.meterX0, data.meterY, data.meterX1, data.meterY,
        width=2)

def drawHardBar(canvas, data):
    barWidth = data.width//10*8
    gbarTop = data.height//2.5
    rbarTop = data.height//4
    rbarBottom = data.height//5*3
    lenGBar = 8
    canvas.create_line(barWidth, rbarTop, barWidth, gbarTop, fill="red", 
        width=10)
    canvas.create_line(barWidth, gbarTop, barWidth, gbarTop+lenGBar, 
        fill="green", width=10)
    canvas.create_line(barWidth, gbarTop+lenGBar, barWidth, rbarBottom, 
        fill="red", width=10)
    canvas.create_line(data.meterX0, data.meterY, data.meterX1, 
        data.meterY, width=2)

def drawLandscape(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height//8, 
        fill="sky blue") #SKY
    drawClouds(canvas, data)
    bottomFence = data.height//5
    topFence = data.height//8
    for x in range(120):
        canvas.create_rectangle(10*x, bottomFence, 10*(x+1), topFence, 
            fill="brown") #FENCE
    canvas.create_rectangle(0, data.height//5, data.width, data.width//3, 
        fill="green") #GRASS
    bushY1 = data.height//6
    bushY2 = data.height//3-30
    canvas.create_oval(data.width//4, bushY1, data.width//3, bushY2, 
        fill="green")
    canvas.create_oval(data.width//5*3, bushY1, data.width//10*7, bushY2, 
        fill="green")
    canvas.create_oval(data.width//20, bushY1, data.width//7, bushY2, 
        fill="green")
    canvas.create_oval(data.width//7*6, bushY1, data.width//20*19, bushY2,
        fill="green")

def drawClouds(canvas, data):
    cloudR = 20
    cloudY = data.height//14
    if data.CX1 > 1240: data.CX1 = 0
    if data.CX2 > 1240: data.CX2 = 0
    if data.CX3 > 1240: data.CX3 = 0
    cx1 = data.CX1-cloudR
    cx2 = data.CX1+cloudR
    cy1 = cloudY-cloudR
    cy2 = cloudY+cloudR
    d1 = 10
    d2 = 15
    #CLOUD 1:
    canvas.create_oval(cx1, cy1, cx2, cy2, fill="white", width=0)
    canvas.create_oval(cx1-d2, cy1+d1, cx2-d2, cy2+d1, fill="white", width=0)
    canvas.create_oval(cx1+d2, cy1+d1, cx2+d2, cy2+d1, fill="white", width=0)
    #CLOUD 2:
    cx3 = data.CX2-cloudR
    cx4 = data.CX2+cloudR
    canvas.create_oval(cx3, cy1, cx4, cy2, fill="white", width=0)
    canvas.create_oval(cx3-d2, cy1+d1, cx4-d2, cy2+d1, fill="white", width=0)
    canvas.create_oval(cx3+d2, cy1+d1, cx4+d2, cy2+d1, fill="white", width=0)
    # CLOUD 3:
    cx5 = data.CX3-cloudR
    cx6 = data.CX3+cloudR
    canvas.create_oval(cx5, cy1, cx6, cy2, fill="white", width=0)
    canvas.create_oval(cx5-d2, cy1+d1, cx6-d2, cy2+d1, fill="white", width=0)
    canvas.create_oval(cx5+d2, cy1+d1, cx6+d2, cy2+d1, fill="white", width=0)

def promptBegin(canvas, data):
    x0 = data.width//4
    x1 = data.width//4*3
    y0 = data.height//3
    y1 = data.height//3*2
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_text((x0+x1)//2, (y0+y1)//2-20, 
     text="Press b to begin the game between: ", font="times 24", fill="blue")
    canvas.create_text((x0+x1)//2, (y0+y1)//2+20, 
     text=data.player1+" and "+data.player2, font="times 24", fill="blue")

def promptNext(canvas, data):
    x0 = data.width//4
    x1 = data.width//4*3
    y0 = data.height//3
    y1 = data.height//3*2
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_text((x0+x1)//2, (y0+y1)//2-20, 
        text="Next Up: "+data.player2+"!", font="times 24", fill="blue")
    canvas.create_text((x0+x1)//2, (y0+y1)//2+20, 
        text="Press c to continue", font="times 24", fill="blue")

def drawSimOver(canvas, data):
    findWinner(data)
    probOfOutcome(data)
    x0 = data.width//4
    x1 = data.width//4*3
    y0 = data.height//3
    y1 = data.height//3*2
    mid = (y0+y1)//2-25
    if data.winner != None:
        canvas.create_rectangle(x0, y0, x1, y1, fill="black")
        canvas.create_text((x0+x1)//2, mid, text=("The winner is: "+
            str(data.winner)+"!"), font="times 24", fill="green")
    elif data.winner == None:
        canvas.create_rectangle(x0, y0, x1, y1, fill="black")
        canvas.create_text((x0+x1)//2, (y0+y1)//2, 
            text="The players tied!!! What are the chances of that?",
            font="times 20", fill="green")
    p1 = (y0+y1)//2 + 20
    p2 = (y0+y1)//2 + 70
    canvas.create_text(data.width//2, p1, text=("Probability of "+
        str(data.player1)+"'s result: "+str(round(data.P1outcome*100, 2))+"%"),
         font="times 20", fill="green")
    canvas.create_text(data.width//2, p2, text=("Probability of "+
        str(data.player2)+"'s result: "+str(round(data.P2outcome*100, 2))+"%"),
         font="times 20", fill="green")

def findWinner(data):
    if data.P1shots < data.P2shots: data.winner = data.player1
    elif data.P2shots < data.P1shots: data.winner = data.player2
    elif data.P1shots == data.P2shots: data.winner = None

####################################
# DRAWING MAKES, MISSES, SETTING NEW SPOTS
####################################
def madeIt(data):
    data.meterSpeed = 0
    rimX = data.width//2
    rimY = data.height//4
    if data.spot in data.left:
        if (data.ballX - rimX>10 or data.spot == "topOfKey") and data.ballY-rimY>20:
            if data.reachedMax == True:
                winsound.PlaySound("swoosh.wav", winsound.SND_FILENAME)
                if data.mode == "SPP": data.makes+=1
                resetData(data)
                setNewSpot(data)
    elif data.spot in data.right:
        if data.ballX - rimX<10 and data.ballY-rimY>20:
            winsound.PlaySound("swoosh.wav", winsound.SND_FILENAME)
            if data.mode == "SPP":
                data.makes+=1
                if data.spot == "baselineR":
                    if data.makes/data.shots >= .5:
                        data.beatLevel = True
                    else: data.failedLevel = True
            resetData(data)
            setNewSpot(data)

def shootAgain(data):
    data.count+=1
    data.meterSpeed = 0
    rimX = data.width//2
    rimY = data.height//4
    if data.count == 1:
        changeSpeed(data)
    if data.spot in data.left:
        if data.ballX - rimX > 0:
            if data.spot == "topOfKey":
                if data.ballY-rimY>=-8:
                    bounceOffRim(data)
                    data.reachedMax = False
            elif data.spot != "topOfKey": bounceOffRim(data)
    elif data.spot in data.right:
        if data.ballX - rimX < 0:
            bounceOffRim(data)
    if data.ballY < 0 and data.bounce == True:
        resetData(data)
        resetSpot(data)

def resetSpot(data): #ONLY FOR MISSES
    if data.spot == "baselineL": initBL(data)
    elif data.spot == "leftWing": initLW(data)
    elif data.spot == "topOfKey": initTOK(data)
    elif data.spot == "rightWing": initRW(data)
    elif data.spot == "baselineR": initBR(data)

def changeSpeed(data): #ONLY FOR MISSES
    if data.mode != "simulation":
        if data.spot == "baselineL":
            data.Xspeed += 3
        elif data.spot == "leftWing":
            data.Xspeed += .7
        elif data.spot == "topOfKey":
            data.Xspeed += .6
        elif data.spot == "rightWing":
            data.Xspeed -= .7
        elif data.spot == "baselineR":
            data.Xspeed -= 2
    elif data.mode == "simulation":
        if data.spot == "baselineL":
            data.Xspeed += 2
        elif data.spot == "leftWing":
            data.Xspeed += .5
        elif data.spot == "topOfKey":
            data.Xspeed += .6
        elif data.spot == "rightWing":
            data.Xspeed -= .5
        elif data.spot == "baselineR":
            data.Xspeed -= 1.5

def bounceOffRim(data): #ONLY FOR MISSES
    if data.reachedMax == True:
        data.bounce = True
        data.Xspeed = -data.Xspeed
        data.Yspeed = -data.Yspeed

def setNewSpot(data):#ONLY FOR MAKES
    if data.spot == "baselineL":
        data.spot = "leftWing"
        initLW(data)
    elif data.spot == "leftWing":
        data.spot = "topOfKey"
        initTOK(data)
        data.reachedMax = False
    elif data.spot == "topOfKey":
        data.spot = "rightWing"
        initRW(data)
    elif data.spot == "rightWing":
        data.spot = "baselineR"
        initBR(data)
    elif data.spot == "baselineR":
        data.spot = "baselineL"
        data.start = False
        initBL(data)
        if data.mode == "SPtime": data.over = True
        elif data.mode == "simulation":
            if data.shooting == data.player1:
                data.shooting = data.player2
                data.P1over = True
            elif data.shooting == data.player2:
                data.P2over = True
                data.shooting = None

####################################
# INITIALIZING SPOTS
####################################

def initBL(data):
    data.ballX = data.width//14
    data.ballY = data.height//2
    data.Xspeed = 29
    data.Yspeed = 50

def initLW(data):
    data.ballX = data.width//6
    data.ballY = data.height//10*8
    data.Yspeed = 65
    data.Xspeed = 20

def initTOK(data):
    data.reachedMax = False
    data.ballX = data.width//2
    data.ballY = data.height - data.ballR*2
    data.Yspeed = 72
    data.Xspeed = 0

def initRW(data):
    data.ballX = data.width//6*5
    data.ballY = data.height//10*8
    data.Yspeed = 65
    data.Xspeed = -20

def initBR(data):
    data.ballX = data.width//14*13
    data.ballY = data.height//2
    data.Yspeed = 50
    data.Xspeed = -29

def resetData(data):
    data.madeIt = None
    data.checkMeter = False
    data.meterY = data.height//5*3
    data.shot = False
    data.meterSpeed = -15
    data.count = 0
    data.bounce = False
    data.reachedMax = True

def resetSimData(data):
    data.player1 = None
    data.player2 = None
    data.PP1 = None
    data.PP2 = None
    data.selecting = "player1"
    data.open = False # Sees if a textbox is already open
    data.shooting = None # Tells us whose turn it is
    data.P1makes = 0
    data.P1shots = 0
    data.P2makes = 0
    data.P2shots = 0
    data.P1over = False
    data.P2over = False
    data.winner = None
    data.P1Chance = None
    data.P2Chance = None
    data.P1outcome = None
    data.P2outcome = None

####################################
# RUN FUNCTION (borrowed from the course website)
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()
    print("bye!")

run(1200, 600)
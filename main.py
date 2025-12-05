# Choose / Continue a problem that is relevant to our learning and record that problem here.
# https://projecteuler.net/archives
# Record your solution below
# --------------------------------------------------------------------------------------------------
# ****This week, your code must incorporate at least one object constructed using a python class****
# ⭐⭐⭐⭐ Build a simple text-based adventure game.
# I am bending the problem a little bit, and making an ascii platformer
# Objects could be of player or enemy classes

# 33:9 charecter resolution. I was having it be 16:9, but the line spacing made it look weird.
# First, I need to make a function to draw 32:9 grids every 0.1 seconds (10 FPS, should be enough)
# Sidenote: this seems hard
# I will use 9 different dictionaries, 32 charecters long each. This way, 
# I will not need to manipulate 288 grid spots manually in the program. 
# It is easier than having one dictionary with 288 spots.
# I have changed the resolution to be more, but the same concept still applies

import time
#Time will be used to make the draw function run every 0.1 seconds
import random
#Random is used for the procedurally generated levels
import readchar
#readchar is used for charecter movement, as it can detect key presses without enter needing to be pressed

import threading
#threading is used for non-blocking input

inlock = threading.Lock()

powerups = []

#this dictionary stores random varibes that I need to be globally accessed. Part is the spacing between generated
#level elements. Lastxmove is the last horizontal direction the player moved, used for autojumping
gamestuff = {
    "part": 4,
    "lastxmove": "right",
    "arrowmove": "---->",
    "name": "NAME HAS NOT BEEN ENTERED",
    "points": 0,
    "bind": "_______________________________________________________________________________________________________________________\nW: UP  S: DOWN  A: LEFT  D: RIGHT  Q: UP-LEFT  E: UP-RIGHT  Z: DOWN-LEFT  X: DOWN-RIGHT  SPACE: SPRING JUMP  C: CLIMB\n\nLEFT ARROW: JUMP DIRECTION LEFT  RIGHT ARROW: JUMP DIRECTION RIGHT  UP ARROW: AUTOJUMP  H: TOGGLE THIS MESSAGE",
    "bindq": 1,
    "hillnum": 0,
    "holenum": 0,
    "powernum": 0,
    "gamestarted": 0
}

class player:

    def __init__(self, name="NAME"):
        self.name = name
        self.xcoord = 0
        self.ycoord = 3

    def moveto(self, x, y):
        self.undraw()
        self.xcoord = x
        self.ycoord = y
        self.draw()

    def moveright(self):
        self.screenscroll()
        if (self.xcoord + 1) > 118:
            print("Cant move off screen!")
            return
        if asc.getpixel((self.xcoord + 1), self.ycoord) == " ":
            self.undraw()
            self.xcoord += 1
            self.draw()
            gamestuff["lastxmove"] = "right"
            gamestuff["arrowmove"] = "---->"

    def moveleft(self):
        #Later, work on scrolling backwards where the level doesnt change
        if (self.xcoord - 1) < 0:
            print("Cant move to negative x coordinate!")
            return
        if asc.getpixel((self.xcoord - 1), self.ycoord) == " ":
            self.undraw()
            self.xcoord -= 1
            self.draw()
            gamestuff["lastxmove"] = "left"
            gamestuff["arrowmove"] = "<----"

    def moveup(self):
        if (self.ycoord + 1) > 9:
            print("Can not move above screen!")
            return
        if asc.getpixel(self.xcoord, (self.ycoord + 1)) == " ":
            self.undraw()
            self.ycoord += 1
            self.draw()
    
    def moveupleft(self):
        if (self.ycoord + 1) > 9 or (self.xcoord - 1) < 0:
            print("Cant move off screen!")
            return
        if asc.getpixel((self.xcoord - 1), (self.ycoord + 1)) == " ":
            self.undraw()
            self.ycoord += 1
            self.xcoord -= 1
            self.draw()

    def moveupright(self):
        self.screenscroll()
        if (self.ycoord + 1) > 9 or (self.xcoord + 1) > 118:
            print("Cant move off screen!")
            return 
        if asc.getpixel((self.xcoord + 1), (self.ycoord + 1)) == " ":
            self.undraw()
            self.xcoord += 1
            self.ycoord += 1
            self.draw()

    def movedown(self):
        if (self.ycoord - 1) < 1:
            print("Cant move off screen!")
            return
        if asc.getpixel(self.xcoord, (self.ycoord - 1)) == " ":
            self.undraw()
            self.ycoord -= 1
            self.draw()
    
    def movedownleft(self):
        if (self.ycoord - 1) < 1 or (self.xcoord - 1) < 0:
            print("Cant move off screen!")
            return
        if asc.getpixel((self.xcoord - 1), (self.ycoord - 1)) == " ":
            self.undraw()
            self.ycoord -= 1
            self.xcoord -= 1
            self.draw()
    
    def movedownright(self):
        if (self.ycoord - 1) < 1 or (self.xcoord + 1) > 118:
            print("Cant move off screen!")
            return
        if asc.getpixel((self.xcoord + 1), (self.ycoord - 1)) == " ":
            self.undraw()
            self.xcoord += 1
            self.ycoord -= 1
            self.draw()
    
    def autojump(self):
        if gamestuff["lastxmove"] == "left":
            if asc.getpixel((self.xcoord - 1), self.ycoord) == " ":
                self.moveup()
                self.moveup()
            else:
                self.moveupleft()

        else:
            if asc.getpixel((self.xcoord + 1), self.ycoord) == " ":
                self.moveup()
                self.moveup()
            else:
                self.moveupright()
    
    def superautojump(self):
        #for climbing walls
        if gamestuff["lastxmove"] == "left":
            self.moveupleft()
            self.moveupleft()
        else:
            self.moveupright()
            self.moveupright()

    def draw(self):
        char_design = "\033[31m$\033[0m"
        asc.edit(self.xcoord, self.ycoord, char_design)

    def undraw(self):
        asc.edit(self.xcoord, self.ycoord, " ")

    def gravity(self):
        while asc.getpixel(self.xcoord, (self.ycoord - 1)) == " ":
            time.sleep(0.085)
            self.movedown()
            asc.draw()

    def screenscroll(self):
        if self.xcoord == 118:
            gamestuff["points"] += 1
            self.undraw()
            initlevel()
            self.moveto(0, 3)
            self.draw()
    def screenscroll_back(self):
        if self.xcoord == 0:
            self.undraw()
            initlevel()
            self.moveto(118, 3)
            self.draw()

    def springjump(self):
        if gamestuff["lastxmove"] == "left":
            self.moveup()
            self.moveup()
            #if asc.getpixel((self.xcoord - 1), self.ycoord) == " " and asc.getpixel((self.xcoord - 1), (self.ycoord - 1)) != " ":
            #    self.moveup()
            #    self.moveup()
            #elif asc.getpixel((self.xcoord - 1), (self.ycoord - 1)) == " ":
            #    self.moveup()
            #    for i in range(1, 7):
            #        self.moveleft()
            #        asc.draw()
            #        time.sleep(0.01)
            #else:
            #    self.moveup()
            #    for i in range(1, 7):
            #        self.moveleft()
            #        asc.draw()
            #        time.sleep(0.01)

        else:
            self.moveup()
            self.moveup()
            #if asc.getpixel((self.xcoord + 1), self.ycoord) == " " and asc.getpixel((self.xcoord + 1), (self.ycoord - 1)) != " ":
            #    self.moveup()
            #    self.moveup()
            #elif asc.getpixel((self.xcoord + 1), (self.ycoord - 1)) == " ":
            #    self.moveup()
            #    for i in range(1, 7):
            #        self.moveright()
            #        asc.draw()
            #        time.sleep(0.01)
            #else:
            #    self.moveup()
            #    for i in range(1, 7):
            #        self.moveright()
            #        asc.draw()
            #        time.sleep(0.01)

class screen:
    def __init__(self):
        self.lines = {
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {},
            9: {},
        }
        for i in range(1, 120):
            self.lines[1][i] = " "
            self.lines[2][i] = " "
            self.lines[3][i] = " "
            self.lines[4][i] = " "
            self.lines[5][i] = " "
            self.lines[6][i] = " "
            self.lines[7][i] = " "
            self.lines[8][i] = " "
            self.lines[9][i] = " "
            groundchar = "\033[32m#\033[0m"
            self.lines[8][i] = groundchar
            self.lines[9][i] = groundchar

    def draw(self):
        #I stole this print statement and the following explination for it from my tic-tac-toe assignment:
        #All it does is clear the screen, so that the draw command can update the screen without each frame
        #being stacked on top of each other
        #\033 stands for the keyboard command, "esc". 
        # It starts the escape sequence instead of printing the others as text. 
        # The bracket states that the escape charecter will have options passed to it. 
        # The H moves the cursor to the home position. 
        # The second \033 initializes another escape charecter. 
        # The bracket, again, shows that the command will have options passed to it. 
        # The 2J is the escape charecter that actually clears the screen. 
        # If the 2 were a different number, it would only clear some of the screen.
        print("\033[H\033[2J")

        ui_top = "_______________________________________________________________________________________________________________________"
        self.linestr1 = ""
        self.linestr2 = ""
        self.linestr3 = ""
        self.linestr4 = ""
        self.linestr5 = ""
        self.linestr6 = ""
        self.linestr7 = ""
        self.linestr8 = ""
        self.linestr9 = ""
        for i in self.lines[1]:
            self.linestr1 += self.lines[1][i]
        for i in self.lines[2]:
            self.linestr2 += self.lines[2][i]
        for i in self.lines[3]:
            self.linestr3 += self.lines[3][i]
        for i in self.lines[4]:
            self.linestr4 += self.lines[4][i]
        for i in self.lines[5]:
            self.linestr5 += self.lines[5][i]
        for i in self.lines[6]:
            self.linestr6 += self.lines[6][i]
        for i in self.lines[7]:
            self.linestr7 += self.lines[7][i]
        for i in self.lines[8]:
            self.linestr8 += self.lines[8][i]
        for i in self.lines[9]:
            self.linestr9 += self.lines[9][i]
        print(ui_top)
        powerstr = ""
        for i in powerups:
            powerstr += i + ", "
        print(f"Powerups: {powerstr}")
        print(ui_top)
        print(self.linestr1)
        print(self.linestr2)
        print(self.linestr3)
        print(self.linestr4)
        print(self.linestr5)
        print(self.linestr6)
        print(self.linestr7)
        print(self.linestr8)
        print(self.linestr9)
        print(ui_top)
        print(f"{gamestuff["name"]}                                                   Points: {gamestuff["points"]}                                   Jump Direction: {gamestuff["arrowmove"]}")
        if gamestuff["bindq"] == 1:
            print(gamestuff["bind"])
            print(ui_top)
        time.sleep(0.005)
    
    def getpixel(self, x, y):
        x += 1
        return self.lines[(10 - y)][x]
    
    def edit(self, x, y, c):
        x += 1
        self.lines[10 - y][x] = c

#This is the main screen object (HAS to be called asc!!!!!!):
asc = screen()

#This is the main player object:
player1 = player()

def misc_checks():
    #Misc. checks that need to be done per draw that do not fit into any other function
    if asc.getpixel(player1.xcoord, (player1.ycoord + 1)) == "\033[33m#\033[0m":
        asc.edit((player1.xcoord), (player1.ycoord + 1), "#")
        powerup = random.randint(1, 7)
        if powerup == 1:
            powerups.append("Jump-Boost")
        if powerup == 2:
            powerups.append("Cloud-Walker")
        if powerup == 3:
            powerups.append("Fireballs")
        if powerup in range (4, 8):
            gamestuff["points"] += 1

def get_input():
    while 1 == 1:
        #this deals with the lock on the process
        with inlock:
            #This makes readchar wait until a key has been pressed. This way, the user does not need to press enter every time
            #they use the keyboard controls to move
            move = readchar.readkey()
            if move == "w":
                player1.moveup()
            if move == "s":
                player1.movedown()
            if move == "a":
                player1.moveleft()
            if move == "d":
                player1.moveright()
            if move == "q":
                player1.moveupleft()
            if move == "e":
                player1.moveupright()
            if move == "z":
                player1.movedownleft()
            if move == "x":
                player1.movedownright()
            #modify this so that you dont need to be one block away from walls to climb walls.
            if move == "c":
                player1.superautojump()
            if move == " ":
                player1.springjump()

            if move == readchar.key.UP:
                player1.autojump()
            #These last two are checking for arrow keys. The arrow keys are changing the autojump position
            if move == readchar.key.LEFT:
                gamestuff["lastxmove"] = "left"
                gamestuff["arrowmove"] = "<----"
            if move == readchar.key.RIGHT:
                gamestuff["lastxmove"] = "right"
                gamestuff["arrowmove"] = "---->"
            if move == "h":
                if gamestuff["bindq"] == 0:
                    gamestuff["bindq"] = 1
                else:
                    gamestuff["bindq"] = 0


def leveldraw(levelpart):
    #print(levelpart)

    feature = random.randint(1,3)
    if feature == 1:
        #Hills
        if gamestuff["hillnum"] < 8:
            for i in range((levelpart + 1),(levelpart + 3)): 
                asc.lines[7][i] = "\033[32m#\033[0m"
                gamestuff["hillnum"] += 1
    if feature == 2:
        #Holes in ground
        if gamestuff["holenum"] < 6:
            for i in range((levelpart),(levelpart + 4)):
                asc.lines[8][i] = " "
                gamestuff["holenum"] += 1
    
    if feature == 3:
        #Powerups!
        if gamestuff["powernum"] < 3:
            for i in range((levelpart), (levelpart + 3)):
                asc.lines[5][i] = "#"
                up = random.randint(levelpart, levelpart + 3)
            asc.lines[5][up] = "\033[33m#\033[0m"
            gamestuff["powernum"] += 1
    for i in range(120, 121):
        asc.lines[1][i] = " "
        asc.lines[2][i] = " "
        asc.lines[3][i] = " "
        asc.lines[4][i] = " "
        asc.lines[5][i] = " "
        asc.lines[6][i] = " "
        asc.lines[7][i] = " "
        asc.lines[8][i] = " "
        asc.lines[9][i] = " "
    gamestuff["part"] += 4

def initlevel():
    #This function ties together the generated parts of the level, and the ground

    gamestuff["part"] = 4
    gamestuff["hillnum"] = 0
    gamestuff["holenum"] = 0
    gamestuff["powernum"] = 0

    for i in range(1, 31):
        leveldraw(gamestuff["part"])

def init_start(charname):
    #This function is the start of the actual game
    #Here, I am changing the player name to the entered one
    player1.name = charname
    player1.draw()

    initlevel()
    player1.moveto(0,8)
    player1.draw()
    gamestuff["gamestarted"] = 1
    inputp = threading.Thread(target=get_input)
    inputp.start()
    while gamestuff["gamestarted"] == 1:
        misc_checks()
        asc.draw()
        player1.gravity()
        time.sleep(0.01)

#Here is the start of the program that the user first sees. It asks if they want to play:
print("Welcome to ASCII BROS (name pending)")
print("Created by: Samuel Locke")
#Here, I am asking the user if they want to play the game
play = input("Would you like to play a new game? (Y/N): ")
if play == "Y":
    playername = input("What would you like your charecter name to be: ")
    gamestuff["name"] = playername
    init_start(playername)
else:
    print("OK! See you soon!")

# --------------------------------------------------------------------------------------------------
# If your code is not complete, please add the following comments in your code
# 1) Where did you get stuck?
# 2) What have you tried so far?
# 3) What do you think you need to do next?

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------MODULES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""
import os, sys

sys.path.append("D:\Documents\CPython\Projet ISN\modules")
# from mainInit import *
from math import *
from winsound import *

from tkinter import *

window = Tk()
window.title("PROJET d'ISN")
window.tk_setPalette(background="white")

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------VARIABLES------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

windowBorder = 50
onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}

gSize = 10
bSize = 40
playerCanvasSize = 30

b = [[0 for i in range(gSize + 1)] for j in range(gSize + 1)]
c = [['' for i in range(gSize + 1)] for j in range(gSize + 1)]

players, player = [[-1 for i in range(gSize + 1)] for j in range(gSize + 1)], 1
scoreDisplay = {-1: StringVar(), 1: StringVar()}
scoreDisplay[-1].set(str(gSize * 2))
scoreDisplay[+1].set(str(gSize * 2))
scorePlayer = {-1: [0 for i in range(gSize * 2)], 1: [0 for i in range(gSize * 2)]}
turn = StringVar()
turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))

selectedPlayer = -1
highlightStuck = False

colour = {
    "red": "#%02X%02X%02X" % (200, 50, 50),
    "green": "#%02X%02X%02X" % (0, 170, 50),
    "white": "#%02X%02X%02X" % (255, 255, 130),
    "black": "#%02X%02X%02X" % (160, 100, 0),
    "blue": "#%02X%02X%02X" % (50, 125, 175),
    "gold": "#%02X%02X%02X" % (255, 160, 60),
    "whitePlayer": "white",
    "blackPlayer": "black"
}

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

playerObjects = []
buttonObjects = []

class Player:

    def __init__(self, _x, _y, _type, _score=0):
        playerObjects.append(self)
        self.score = _score
        parent = board if self.score == 0 else mainFrame
        if self.score == 0:
            self.x, self.y = cellToPixel(_x), cellToPixel(_y)
        else:
            self.x, self.y = _x, _y
        self.xTo, self.yTo, self.sTo = self.x, self.y, playerCanvasSize
        self.type = _type
        self.super = False
        self.refreshRate = 15
        self.col1 = colour["whitePlayer"] if _type == -1 else colour["blackPlayer"]
        self.col2 = colour["whitePlayer"] if _type == +1 else colour["blackPlayer"]
        self.canvas = Canvas(parent, width=playerCanvasSize, \
                             height=playerCanvasSize, \
                             bg=c[i][j], bd=0, highlightthickness=0)
        # self.canvasItem = self.canvas.create_oval(2, 2, playerCanvasSize-2, \
        #                              playerCanvasSize-2, fill=self.col1, width=0)
        self.canvasItem = self.canvas.create_rectangle(0, 0, playerCanvasSize, \
                                                       playerCanvasSize, fill=self.col1, outline=self.col2, \
                                                       width=8)
        self.canvas.place(x=self.x, y=self.y)
        self.canvas.bind("<1>", lambda event, x=i, y=j: click(event, x, y))
        self.update()

    def changePosition(self, _x, _y):
        global players
        if self.score == 0:
            _i, _j = pixelToCell(self.x), pixelToCell(self.y)
            players[_i][_j] = -1
            players[_x][_y] = self
            players[_x][_y].canvas.bind("<1>", lambda event, x=_x, y=_y: \
                click(event, x, y))
            self.x = cellToPixel(_x)
            self.y = cellToPixel(_y)
        else:
            self.x = _x
            self.y = _y
        Misc.lift(self.canvas, aboveThis=None)

    def update(self):
        speed = 0.2 * self.refreshRate * 0.1 if self.score == 0 else 0.15 * self.refreshRate * 0.1
        self.xTo = lerp(self.xTo, self.x, speed)
        self.yTo = lerp(self.yTo, self.y, speed)
        self.canvas.place(x=self.xTo, y=self.yTo)
        if self.score == 1:
            self.sTo = lerp(self.sTo, playerCanvasSize / 2, speed)
            self.canvas.configure(width=self.sTo, height=self.sTo)
            self.canvas.coords(self.canvasItem, 0, 0, self.sTo, self.sTo)
            self.canvas.itemconfigure(self.canvasItem, width=6)
        self.canvas.itemconfigure(self.canvasItem, fill=self.col1, outline=self.col2)
        self.canvas.after(self.refreshRate, self.update)


class Button:

    def __init__(self, _type, _text, _size, _frame, _animationType=0):
        buttonObjects.append(self)
        self.animationType = _animationType
        self.refreshRate = 10
        self.text = _text
        self.size = _size
        self.ww, self.hh = (len(_text)+3) * _size, 1.85 * _size
        self.canvas = Canvas(_frame, width=self.ww, height=self.hh)
        self.canvas.label = self.canvas.create_text(self.ww/2, self.hh/2, text=self.text)
        self.canvas.font = "Trebuchet MS"
        self.canvas.size = self.size
        self.canvas.changeSize= 0
        self.canvas.colourA, self.canvas.colourB, self.canvas.colourT = 255, "white", 255
        self.canvas.arrowSpace = 0
        self.canvas.style = (self.canvas.font, self.canvas.size)
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.bind("<1>", lambda event, type=_type, anim=self.animationType: buttonPress(event, type, anim))
        self.canvas.bind("<Enter>", lambda event, t=+1, anim=self.animationType: buttonMouse(event, t, anim))
        self.canvas.bind("<Leave>", lambda event, t=-1, anim=self.animationType: buttonMouse(event, t, anim))
        ax1 = self.ww / 2 + (len(self.text) / 2) * self.size
        ax2 = self.ww / 2 - (len(self.text) / 2) * self.size
        ay = self.hh / 2
        self.arrow1 = self.canvas.create_polygon(ax1 + 10, ay, ax1, 0+5, ax1, self.hh-5, fill="white", width=2)
        self.arrow2 = self.canvas.create_polygon(ax2 - 10, ay, ax2, 0+5, ax2, self.hh-5, fill="white", width=2)
        self.update()

    def update(self):
        if self.animationType == 0:
            RGBcolourA = RGBToHex((self.canvas.colourA, self.canvas.colourA, self.canvas.colourA))
            RGBcolourB = self.canvas.colourB
            self.canvas.size = lerp(self.canvas.size, self.size, 0.2)
            self.canvas.arrowSpace = lerp(self.canvas.arrowSpace, 0, 0.2)
            self.canvas.itemconfig(self.arrow1, outline=RGBcolourA)
            self.canvas.itemconfig(self.arrow2, outline=RGBcolourA)
            self.canvas.configure(bg=RGBcolourB)
            ax1 = self.ww / 2 + (len(self.text) / 2 + self.canvas.arrowSpace) * self.size
            ax2 = self.ww / 2 - (len(self.text) / 2 + self.canvas.arrowSpace) * self.size
            ay = self.hh / 2
            self.canvas.coords(self.arrow1, ax1 + 10, ay, ax1, 0 + 5, ax1, self.hh - 5)
            self.canvas.coords(self.arrow2, ax2 - 10, ay, ax2, 0 + 5, ax2, self.hh - 5)
        if self.animationType == 1:
            if self.canvas.changeSize == 1: aimedSize = self.size + 5
            if self.canvas.changeSize == -1: aimedSize = self.size
            if self.canvas.changeSize == 0: aimedSize = self.canvas.size
            self.canvas.colourT = clamp(lerp(255, 0, 0.6 + (1 - self.size / self.canvas.size)), 0, 255)
            RGBcolourT = RGBToHex((self.canvas.colourT, self.canvas.colourT, self.canvas.colourT))
            self.canvas.size = lerp(self.canvas.size, aimedSize, 0.2)
            self.canvas.itemconfig(self.canvas.label, fill=RGBcolourT)
        self.canvas.style = (self.canvas.font, int(self.canvas.size))
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.after(self.refreshRate, self.update)

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FONCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""Fonction qui enroule un nombre dans un intervalle [0; a]"""
def wrap(x, a):
    return x % a

"""Fonction d'interpolation linéaire"""
def lerp(a, b, x):
    return a + (b - a) * x

"""Fonction de clamp"""
def clamp(x, a, b):
    if x < a: return a
    elif x > b: return b
    else: return x
    #return min(max(x, a), x, b)

"""Fonction qui retourne si une valeur est entre 2 bornes"""
def isBetween(x, a, b):
    a = min(a, b)
    b = max(a, b)
    if x >= a and x <= b:
        return True
    else:
        return False

"""Fonction qui quantifie combien de cases il y a entre deux coordonnées"""
def movementVector(i1, j1, i2, j2):
    norm = sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)
    return i1 - i2, j1 - j2, norm

"""Fonction qui retourne le type de la case"""
def case(i, j):
    if (i % 2 == 0 and j % 2 == 0) \
            or (i % 2 == 1 and j % 2 == 1):
        return 1
    else:
        return 0

"""Fonction qui convertit des couleurs HEX en RGB et vice versa"""
def hexToRGB(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2 ,4))
def RGBToHex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

"""Fonction qui mélange deux couleurs"""
def mergeColour(c1, c2, x):
    c1 = hexToRGB(c1)
    c2 = hexToRGB(c2)
    r, g, b = lerp(c1[0], c2[0], x), lerp(c1[1], c2[1], x), lerp(c1[2], c2[2], x)
    return RGBToHex((r, g, b))

"""Fonction qui définit la couleur d'une case"""
def caseColour(i, j, col):
    global player, onePlayerCanEat
    if col != -1:
        c[i][j] = col
    else:
        if case(i, j):
            c[i][j] = colour["black"]
        else:
            c[i][j] = colour["white"]
    b[i][j].config(background=c[i][j])

"""Fonction qui reset la couleur des cases"""
def resetCaseColour(withGreen=0):
    for i in range(gSize):
        for j in range(gSize):
            if withGreen == 1 and c[i][j] == colour["green"]: continue
            caseColour(i, j, -1)

"""Fonction qui convertit un nombre en string à deux caractères"""
def intToString(integer):
    integer = int(integer)
    if isBetween(integer, -9, 9):
        return "0" + str(integer)
    else:
        return str(integer)

"""Fonction qui retourne si une case est vide (sans jetons) ou pas"""
def empty(i, j):
    if players[i][j] == -1:
        return True
    else:
        return False

"""Fonction qui convertit des coordonnées en index de tableau et vice verse"""
def pixelToCell(x):
    return (x // bSize)
def cellToPixel(x):
    return int(x * bSize + (bSize - playerCanvasSize) / 2)

"""Fonction qui convertit des coordonnées du board en coordonnées du frame"""
def boardToFrame(a, xOrY):
    if xOrY == "x": return a + 4
    if xOrY == "y": return a + 25 * 2 + 4

"""Fonction appelée lorsqu'on ferme le jeu"""
def closeWindow():
    window.destroy()

"""Fonction qui éxécute un effet sonore"""
def playSound(sound):
    # PlaySound(sound, SND_FILENAME | SND_ASYNC)
    return None

"""Fonctions qui manipulent les boutons"""
def buttonMouse(event, enterOrLeave, anim):
    caller = event.widget
    if anim == 0:
        if enterOrLeave == 1:
            caller.colourA = 75
            caller.colourB = mergeColour(colour["white"], "#FFFFFF", 0.25)
        if enterOrLeave == -1:
            caller.colourA = 255
            caller.colourB = mergeColour(colour["white"], "#FFFFFF", 1)
    if anim == 1:
        caller.changeSize = enterOrLeave
def buttonPress(event, type, anim):
    caller = event.widget
    if anim == 0:
        caller.size += 4
        caller.arrowSpace = 1
    if anim == 1:
        pass
    playSound('menuClicked.wav')
    type(event)
def infoMouse(event, enterOrLeave):
    caller = event.widget
    if enterOrLeave == 1:
        caller.itemconfig(ALL, fill=mergeColour(colour["white"], "#FFFFFF", 0.25))
    if enterOrLeave == -1:
        caller.itemconfig(ALL, fill=mergeColour(colour["white"], "#FFFFFF", 1))
    infoIcon.itemconfig(infoI, fill="black")
def infoPress(event):
    return None

"""Fonctions de boutons"""
def annuler(event):
    print("annuler")
def redemarrer(event):
    print("redemarrer")
def quitter(event):
    print("quitter")
def infoPress(event):
    return None

"""Fonction qui check si on un joueur peut en manger un autre"""
def canMove():
    global player, players, onePlayerCanEat
    onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
    for b in [-1, -2]:
        for _player in [-1, 1]:
            for pi in range(gSize):
                for pj in range(gSize):
                    if players[pi][pj] != -1 and players[pi][pj].type == _player:
                        if highlight(pi, pj, _player, behaviour=b):
                            if b == -1:
                                if _player == player:
                                    onePlayerCanEat[_player].append((pi, pj))
                            if c[pi][pj] != colour["green"]:
                                if _player == player:
                                    caseColour(pi, pj, colour["red"])
                                continue
                            else:
                                resetCaseColour(withGreen=1)
                                window.after(15, canMove)
                                return None
        if b == -1:
            if onePlayerCanEat != {-1: [(-1, -1)], 1: [(-1, -1)]}:
                window.after(15, canMove)
                return None
            else:
                continue
    window.after(15, canMove)

"""Fonction qui check où on peut aller"""
def highlight(i, j, player, behaviour=1):
    global selectedPlayer, highlightStuck, onePlayerCanEat
    direction1 = [player]
    if players[i][j].super: direction1.append(-player)
    direction2 = [-1, 1]
    for playerVar in direction1:
        for direction in direction2:
            # Coordonnées des checks
            ni = lambda a: i - a * direction
            nj = lambda a: j - a * playerVar
            # On définit les conditions des checks
            samePlayerCondition = players[ni(1)][nj(1)] != -1 \
                                  and players[ni(1)][nj(1)].type == player
            otherPlayerCondition = players[ni(1)][nj(1)] != -1 \
                                   and players[ni(1)][nj(1)].type == -player
            outsideGrid = (not isBetween(ni(1), 0, gSize - 1) \
                           or not isBetween(nj(1), 0, gSize - 1)) \
                          or (otherPlayerCondition and ( \
                        not isBetween(ni(2), 0, gSize - 1) \
                        or not isBetween(nj(2), 0, gSize - 1)))
            if behaviour == 1: caseColour(i, j, colour["green"])
            # Si on est hors grille
            if outsideGrid: continue
            # S'il y a un ennemi en diagonale et qu'ensuite la case est vide
            if otherPlayerCondition:
                if empty(ni(2), nj(2)):
                    if behaviour == 1:
                        caseColour(ni(1), nj(1), colour["green"])
                        caseColour(ni(2), nj(2), colour["green"])
                    elif behaviour == 0:
                        highlightStuck = True
                        selectedPlayer = players[i][j]
                        caseColour(i, j, colour["green"])
                        highlight(i, j, player, behaviour=1)
                    if behaviour == -1:
                        return True
                else:
                    continue
            elif behaviour == 0:
                continue
            # S'il y a un de nos jetons en diagonale
            if samePlayerCondition: continue
            # Si la case est vide
            if empty(ni(1), nj(1)):
                if behaviour >= 0 and onePlayerCanEat[player] == [(-1, -1)] \
                        and not highlightStuck:
                    caseColour(ni(1), nj(1), colour["green"])
                if not samePlayerCondition and behaviour == -2:
                    return True
    return False

"""Fonction qui permet de manger un joueur"""
def eat(i, j, player, playerMovement):
    global scoreBoardSize, underScoreBoardSize, halfScoreBoardSize, \
        scoreBoardBorder, halfScoreBoardBorder, playerCanvasSize
    # Définition du joueur mangé
    eatenPlayerX = i + int(playerMovement[0] / 2)
    eatenPlayerY = j + int(playerMovement[1] / 2)
    eatenPlayer = players[eatenPlayerX][eatenPlayerY]
    ePlayerType = eatenPlayer.type
    # Augmentation du score
    scoreDisplay[ePlayerType].set \
        (intToString(int(scoreDisplay[ePlayerType].get()) + 1))
    # Création d'un mini canevas pour l'animation
    scorePlayer[ePlayerType] \
        [int(scoreDisplay[ePlayerType].get())] \
        = Player(boardToFrame(cellToPixel(eatenPlayerX), "x"), \
                 boardToFrame(cellToPixel(eatenPlayerY), "y"), \
                 ePlayerType, _score=1)
    # Mouvement du canevas dans le tableau du score
    playersPerRow, playersPerColumn = 5, 4
    hardCodedCoordinates = (460, 193)
    scorePlayersSpacingX = (halfScoreBoardSize - \
                            ((scoreBoardBorder * 2) + (playersPerRow * playerCanvasSize / 2))) \
                           / (playersPerRow + 1)
    scorePlayersSpacingY = (underScoreBoardSize[1] - \
                            ((scoreBoardBorder / 2) + (playersPerColumn * playerCanvasSize / 2))) \
                           / (playersPerColumn + 1)
    if ePlayerType == 1:
        scorePositionX = hardCodedCoordinates[0] \
                         + scoreBoardBorder + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    if ePlayerType == -1:
        scorePositionX = scoreBoardSize[0] / 2 + hardCodedCoordinates[0] \
                         + 2 + scoreBoardBorder / 4 + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    scorePositionY = hardCodedCoordinates[1] + scoreBoardBorder + scorePlayersSpacingY \
                     + (playerCanvasSize / 2 + scorePlayersSpacingY) \
                     * ((int(scoreDisplay[ePlayerType].get()) - 1) // playersPerRow)
    scorePlayer[ePlayerType] \
        [int(scoreDisplay[ePlayerType].get())] \
        .changePosition(scorePositionX, scorePositionY)
    if eatenPlayer.super:
        scorePlayer[ePlayerType][int(scoreDisplay[ePlayerType].get())] \
            .col1 = eatenPlayer.col2
    # Cleanup des variables
    eatenPlayer.canvas.destroy()
    players[eatenPlayerX][eatenPlayerY] = -1
    # On check si on peut enchainer avec un combo
    highlight(i, j, player, behaviour=0)

"""Fonction Principale"""
def click(event, i, j):
    global player, selectedPlayer, highlightStuck, onePlayerCanEat, \
        blackCount, whiteCount
    # if selectedPlayer != -1: player = selectedPlayer.type
    # Si on clique sur un joueur,
    if players[i][j] != -1 and players[i][j] != selectedPlayer \
            and players[i][j].type == player:
        if not highlightStuck:
            resetCaseColour()
            selectedPlayer = players[i][j]
            player = selectedPlayer.type
            highlight(i, j, player)
            playSound('playerSelected.wav')
    # Si on est sur une case normale,
    else:
        # Si elle est en surbrillance,
        if c[i][j] == colour["green"] and empty(i, j):
            # On bouge le joueur
            resetCaseColour()
            playerMovement = movementVector(pixelToCell(selectedPlayer.x), \
                                            pixelToCell(selectedPlayer.y), i, j)
            selectedPlayer.changePosition(i, j)
            player = selectedPlayer.type
            selectedPlayer = -1
            highlightStuck = False
            playSound('playerMoved.wav')
            # Si on est en train de manger un joueur,
            if playerMovement[2] > sqrt(2):
                eat(i, j, player, playerMovement)
                playSound('playerAte.wav')
            # On change de joueur
            if (highlightStuck == False):
                player = -player
                turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))
            # Si on est arrivés au bout de la grille,
            if ((j == 0 and player == -1) or (j == gSize - 1 and player == 1)) \
                    and players[i][j].super == False:
                players[i][j].super = True
                # players[i][j].col2 = players[i][j].col1
                players[i][j].col2 = colour["gold"]
                players[i][j].canvas.create_polygon(playerCanvasSize / 2, 0 + 4, \
                                                    playerCanvasSize - 4, playerCanvasSize / 2, \
                                                    playerCanvasSize / 2, playerCanvasSize - 4, \
                                                    0 + 4, playerCanvasSize / 2, \
                                                    fill=players[i][j].col1, \
                                                    outline=players[i][j].col2, \
                                                    width=4)
            playSound('playerSuper.wav')
        # Si elle est vierge et qu'on est pas coincés dans un combo,
        elif not highlightStuck:
            resetCaseColour()
            selectedPlayer = -1
            playSound('playerDeselected.wav')

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------PROGRAMME------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""Arrangement des widgets autour du jeu"""
window.configure(bg="white")

mainFrame = Frame(window)
mainFrame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)

topFrame = Frame(mainFrame)
topFrame.grid(column=0, row=0)

board = Frame(mainFrame, borderwidth=5, bg="black")
board.grid(column=0, row=1)

turnText = Label(mainFrame, textvariable=turn, font=("Trebuchet MS", 15))
turnText.grid(column=0, row=2)

sideFrame = Frame(mainFrame)
sideFrame.grid(column=1, row=1)

scoreBoardSize, underScoreBoardSize = (300, 150), (300, 100)
halfScoreBoardSize = scoreBoardSize[0] / 2
scoreBoardBorder, halfScoreBoardBorder = 6, 6 / 2
scoreBoard = Canvas(sideFrame, bg="black", \
                    width=scoreBoardSize[0], \
                    height=scoreBoardSize[1] + underScoreBoardSize[1])

scoreBoard.create_rectangle(scoreBoardBorder, \
                            scoreBoardBorder, \
                            scoreBoardSize[0] / 2 - halfScoreBoardBorder, \
                            scoreBoardSize[1] - halfScoreBoardBorder, \
                            fill=colour["white"])
scoreBoard.create_rectangle(halfScoreBoardSize + halfScoreBoardBorder / 2, \
                            scoreBoardBorder, \
                            scoreBoardSize[0] - halfScoreBoardBorder, \
                            scoreBoardSize[1] - halfScoreBoardBorder, \
                            fill=colour["black"])
scoreBoard.create_rectangle(scoreBoardBorder, \
                            scoreBoardSize[1] + halfScoreBoardBorder / 2, \
                            halfScoreBoardSize - halfScoreBoardBorder, \
                            scoreBoardSize[1] + underScoreBoardSize[1] - halfScoreBoardBorder, \
                            fill=colour["black"])
scoreBoard.create_rectangle(halfScoreBoardSize + halfScoreBoardBorder / 2, \
                            scoreBoardSize[1] + halfScoreBoardBorder / 2, \
                            underScoreBoardSize[0] - halfScoreBoardBorder, \
                            scoreBoardSize[1] + underScoreBoardSize[1] - halfScoreBoardBorder, \
                            fill=colour["white"])

scoreBoard.grid(row=0, column=0)

playerScoreSize = 60
playerScoreOffset = (halfScoreBoardSize - playerScoreSize * 2) / 2 + playerScoreSize / 6
blackPlayerScore = Label(scoreBoard, textvariable=scoreDisplay[-1], \
                         font=("Trebuchet MS", playerScoreSize, "bold"), \
                         fg=colour["blackPlayer"], bg=colour["white"])
blackPlayerScore.place(x=playerScoreOffset, \
                       y=(scoreBoardSize[1] - playerScoreSize) / 4)
whitePlayerScore = Label(scoreBoard, textvariable=scoreDisplay[1], \
                         font=("Trebuchet MS", playerScoreSize, "bold"), \
                         fg=colour["whitePlayer"], bg=colour["black"])
whitePlayerScore.place(x=halfScoreBoardSize + playerScoreOffset, \
                       y=(scoreBoardSize[1] - playerScoreSize) / 4)

emptySpace1 = Canvas(sideFrame, width=400, height=55 / 2)
emptySpace1.grid(row=1, column=0)

cancelText = Button(annuler, "ANNULER", 15, sideFrame)
cancelText.canvas.grid(row=2, column=0)

restartText = Button(redemarrer, "REDEMARRER", 15, sideFrame)
restartText.canvas.grid(row=3, column=0)

quitText = Button(quitter, "QUITTER", 15, sideFrame)
quitText.canvas.grid(row=4, column=0)

emptySpace1 = Canvas(sideFrame, width=400, height=55 / 2)
emptySpace1.grid(row=5, column=0)

infoIconSize = 50
infoIconHalfSize = infoIconSize / 2
infoIcon = Canvas(window, width=infoIconSize, height=infoIconSize)
#infoIcon.create_oval(7, 7, 42, 42, fill="white", outline="black", width=2)
infoIcon.create_polygon(infoIconHalfSize, 5, \
                        45, infoIconHalfSize, \
                        infoIconHalfSize, 45, \
                        5, infoIconHalfSize, \
                        fill="white", outline="black", width=2)
infoI = infoIcon.create_text(infoIconHalfSize, infoIconHalfSize, \
                     text="i", font=("Courier New", 15, "bold"), \
                     fill="black")
infoIcon.place(relx=1, x=-10, y=10, anchor=NE)
infoIcon.bind("<1>", infoPress)
infoIcon.bind("<Enter>", lambda event, t=+1: infoMouse(event, t))
infoIcon.bind("<Leave>", lambda event, t=-1: infoMouse(event, t))

title = Label(topFrame, text="LE JEU DE DAMES", font=("Trebuchet MS", 25), \
              height=1)
title.pack()

window.protocol("WM_DELETE_WINDOW", closeWindow)

"""Arrangement de la grille"""
for j in range(gSize):
    for i in range(gSize):

        # Création des boutons de base
        b[i][j] = Canvas(board, width=bSize, height=bSize, \
                         bd=0, highlightthickness=0)
        b[i][j].grid(column=i, row=j)

        # Si on est sur une case noire
        if case(i, j):
            # Créer la couleur marron
            c[i][j] = colour["black"]

            # Placer des jetons
            if int(scoreDisplay[-1].get()) > 0 and j >= 0:
                players[i][j] = Player(i, j, -1)
                scoreDisplay[-1].set(intToString(int(scoreDisplay[-1].get()) - 1))
            elif int(scoreDisplay[1].get()) > 0 and j >= 6:
                players[i][j] = Player(i, j, 1)
                scoreDisplay[1].set(intToString(int(scoreDisplay[1].get()) - 1))
            else:
                players[i][j] = -1

        # Si on est sur une case blanche
        else:
            # Créer la couleur crème
            c[i][j] = colour["white"]
            # Le reste de la grille est égal à -1
            players[i][j] = -1

        # Fonction des boutons
        b[i][j].bind("<1>", lambda event, x=i, y=j: click(event, x, y))
        # Couleur des boutons
        b[i][j].config(background=c[i][j])

canMove()

"""Main"""
window.mainloop()

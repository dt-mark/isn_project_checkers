"""------------------------------------------------------------------------------------------------------------------"""
"""-------------------------------------------------INITIALISATION---------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""
from tkinter import *

window = Tk()
window.title("PROJET d'ISN")
window.tk_setPalette(background="white")
window.resizable(width=False, height=False)

import os
from basicFunctions import *

from math import *
from winsound import *
import webbrowser

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
    "purple": "#%02X%02X%02X" % (255, 130, 255),
    "whitePlayer": "#%02X%02X%02X" % (255, 255, 255),
    "blackPlayer": "#%02X%02X%02X" % (0, 0, 0)
}
sound = {
    "click":"_menuClicked.wav",
    "eat":"_playerAte.wav",
    "move":"_playerMoved.wav",
    "super":"_playerSuper.wav",
    "select":"_playerSelected.wav",
    "deselect":"_playerDeselected.wav"
}

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""
playerObjects = []
buttonObjects = []
"""----------------------------------------------------PLAYER--------------------------------------------------------"""
class Player:

    def __init__(self, _x, _y, _type, _score=0):
        playerObjects.append(self)
        self.score = _score
        parent = board if self.score == 0 else mainFrame
        if self.score == 0:
            self.x, self.y = cellToPixel(_x), cellToPixel(_y)
            self.i, self.j = _x, _y
        else:
            self.x, self.y = _x, _y
            self.i, self.j = pixelToCell(_x), pixelToCell(_y)
        self.xTo, self.yTo, self.sTo = self.x, self.y, playerCanvasSize
        self.type = _type
        self.super = False
        self.refreshRate = 15
        self.col1 = colour["whitePlayer"] if _type == -1 else colour["blackPlayer"]
        self.col2 = colour["whitePlayer"] if _type == +1 else colour["blackPlayer"]
        self.canvas = Canvas(parent, width=playerCanvasSize, \
                             height=playerCanvasSize, \
                             bg=c[self.i][self.j], bd=0, highlightthickness=0)
        # self.canvasItem = self.canvas.create_oval(2, 2, playerCanvasSize-2, \
        #                              playerCanvasSize-2, fill=self.col1, width=0)
        self.canvasItem = self.canvas.create_rectangle(0, 0, playerCanvasSize, \
                                                       playerCanvasSize, fill=self.col1, outline=self.col2, \
                                                       width=8)
        self.canvas.place(x=self.x, y=self.y)
        self.canvas.bind("<1>", lambda event, x=_x, y=_y: click(event, x, y))
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

"""-----------------------------------------------------BOARD--------------------------------------------------------"""
class Board:

    def __init__(self, _frame, _gSize, _bSize):
        for j in range(_gSize):
            for i in range(_gSize):
                # Création des boutons de base
                b[i][j] = Canvas(_frame, width=_bSize, height=_bSize, \
                                 bd=0, highlightthickness=0)
                b[i][j].grid(row=j, column=i)
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

"""--------------------------------------------------SCORE-BOARD-----------------------------------------------------"""
class ScoreBoard:

    def __init__(self, _frame, _size, _underSize, _border):
        self.scoreBoardSize, self.underScoreBoardSize = _size, _underSize
        self.halfScoreBoardSize = self.scoreBoardSize[0] / 2
        self.scoreBoardBorder = _border
        self.halfScoreBoardBorder = self.scoreBoardBorder / 2
        self.canvas = Canvas(_frame, bg="black", \
                             width=self.scoreBoardSize[0], \
                             height=self.scoreBoardSize[1] + self.underScoreBoardSize[1])
        self.canvas.create_rectangle(self.scoreBoardBorder, \
                                     self.scoreBoardBorder, \
                                     self.scoreBoardSize[0] / 2 - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["white"])
        self.canvas.create_rectangle(self.halfScoreBoardSize + self.halfScoreBoardBorder / 2, \
                                     self.scoreBoardBorder, \
                                     self.scoreBoardSize[0] - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["black"])
        self.canvas.create_rectangle(self.scoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.halfScoreBoardBorder / 2, \
                                     self.halfScoreBoardSize - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.underScoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["black"])
        self.canvas.create_rectangle(self.halfScoreBoardSize + self.halfScoreBoardBorder / 2, \
                                     self.scoreBoardSize[1] + self.halfScoreBoardBorder / 2, \
                                     self.underScoreBoardSize[0] - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.underScoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["white"])
        self.playerScoreSize = 60
        self.playerScoreOffset = (self.halfScoreBoardSize - self.playerScoreSize * 2) / 2 + self.playerScoreSize / 6
        self.blackPlayerScore = Label(self.canvas, textvariable=scoreDisplay[-1], \
                                      font=("Trebuchet MS", self.playerScoreSize, "bold"), \
                                      fg=colour["blackPlayer"], bg=colour["white"])
        self.blackPlayerScore.place(x=self.playerScoreOffset, \
                                    y=(self.scoreBoardSize[1] - self.playerScoreSize) / 4)
        self.whitePlayerScore = Label(self.canvas, textvariable=scoreDisplay[1], \
                                      font=("Trebuchet MS", self.playerScoreSize, "bold"), \
                                      fg=colour["whitePlayer"], bg=colour["black"])
        self.whitePlayerScore.place(x=self.halfScoreBoardSize + self.playerScoreOffset, \
                                    y=(self.scoreBoardSize[1] - self.playerScoreSize) / 4)

"""----------------------------------------------------BUTTON--------------------------------------------------------"""
class Button:

    def __init__(self, _frame, _text, _type, _size, _animationType=0, _font="Trebuchet MS", _tag=""):
        buttonObjects.append(self)
        self.animationType = _animationType
        self.refreshRate = 10
        self.text, self.size, self.type = _text, _size, _type
        self.ww, self.hh = (len(_text)+3) * _size, 1.85 * _size
        self.canvas = Canvas(_frame, width=self.ww, height=self.hh-3)
        self.canvas.label = self.canvas.create_text(self.ww/2, self.hh/2, text=self.text)
        self.canvas.arrowSpace = 0
        self.canvas.colourA, self.canvas.colourT = 1, 0.5
        self.canvas.font, self.canvas.tag = _font, _tag
        self.canvas.size, self.canvas.aimedSize = self.size, self.size
        self.canvas.style = (self.canvas.font, self.canvas.size, self.canvas.tag)
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.bind("<1>", lambda event, type=self.type, anim=self.animationType: self.buttonPress(event, type, anim))
        self.canvas.bind("<Enter>", lambda event, t=+1, anim=self.animationType: self.buttonMouse(event, t, anim))
        self.canvas.bind("<Leave>", lambda event, t=-1, anim=self.animationType: self.buttonMouse(event, t, anim))
        ax1, ax2 = self.ww / 2 + (len(self.text) / 2) * self.size, self.ww / 2 - (len(self.text) / 2) * self.size
        self.arrow1 = self.canvas.create_polygon(ax1+10, self.hh/2, ax1, 0+5, ax1, self.hh-5, fill="white", width=2)
        self.arrow2 = self.canvas.create_polygon(ax2-10, self.hh/2, ax2, 0+5, ax2, self.hh-5, fill="white", width=2)
        self.update()

    def buttonMouse(self, event, enterOrLeave, anim):
        caller = self.canvas
        if anim == 0:
            caller.colourA = clamp(-enterOrLeave, 0, 1)
        if anim == 1:
            caller.aimedSize = self.size + 5*clamp(enterOrLeave, 0, 1)
            caller.colourT = (1 - self.size / caller.size) + 0.25

    def buttonPress(self, event, type, anim):
        caller = self.canvas
        if anim == 0:
            caller.size += 4
            caller.arrowSpace = 1
        if anim == 1:
            caller.size -= 4
        playSound(sound["click"])
        type(event)

    def update(self):
        if self.animationType == 0:
            RGBcolourA = mergeColour(RGBToHex((75, 75, 75)), RGBToHex((255, 255, 255)), self.canvas.colourA)
            RGBcolourB = mergeColour(RGBToHex((215, 215, 215)), RGBToHex((255, 255, 255)), self.canvas.colourA)
            self.canvas.arrowSpace = lerp(self.canvas.arrowSpace, 0, 0.2)
            ax1 = self.ww / 2 + (len(self.text) / 2 + self.canvas.arrowSpace) * self.size
            ax2 = self.ww / 2 - (len(self.text) / 2 + self.canvas.arrowSpace) * self.size
            self.canvas.itemconfig(self.arrow1, outline=RGBcolourA)
            self.canvas.itemconfig(self.arrow2, outline=RGBcolourA)
            self.canvas.configure(bg=RGBcolourB)
            self.canvas.coords(self.arrow1, ax1+10, self.hh/2, ax1, 0+5, ax1, self.hh-5)
            self.canvas.coords(self.arrow2, ax2-10, self.hh/2, ax2, 0+5, ax2, self.hh-5)
            self.canvas.size = lerp(self.canvas.size, self.size, 0.2)
        if self.animationType == 1:
            RGBcolourT = mergeColour(RGBToHex((0, 0, 0)), RGBToHex((255, 255, 255)), self.canvas.colourT)
            self.canvas.itemconfig(self.canvas.label, fill=RGBcolourT)
            self.canvas.size = lerp(self.canvas.size, self.canvas.aimedSize, 0.2)
        self.canvas.style = (self.canvas.font, int(self.canvas.size), self.canvas.tag)
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.after(self.refreshRate, self.update)

"""-----------------------------------------------------POPUP--------------------------------------------------------"""
class Popup:

    def __init__(self, _frame, _text, _textOption1, _textOption2, _funcOption1, _funcOption2):
        self.text, self.tO1, self.tO2 = _text, _textOption1, _textOption2
        self.O1, self.O2 = _funcOption1, _funcOption2
        assignFunction = lambda a: ((lambda event: self.cancelPopup(event)) if a == -1 \
                                     else (lambda event: self.acceptPopup(event, a)))
        self.O1, self.O2 = assignFunction(self.O1), assignFunction(self.O2)
        self.top = Toplevel()
        self.label = Label(self.top, text=self.text, font=("Trebuchet MS", 20), fg=colour["black"])
        self.button1 = Button(self.top, self.tO1, self.O1, 10, _animationType=1)
        self.button2 = Button(self.top, self.tO2, self.O2, 10, _animationType=1)
        self.label.grid(row=0, column=0)
        self.button1.canvas.grid(row=1, column=0)
        self.button2.canvas.grid(row=2, column=0)
        self.top.resizable(width=False, height=False)
        self.top.transient(window)
        self.top.grab_set()
        center(self.top, window)

    def cancelPopup(self, event):
        self.top.destroy()
        del self

    def acceptPopup(self, event, func):
        func(event)
        self.cancelPopup(event)


"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FONCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""--------------------------------------------------SECONDAIRES-----------------------------------------------------"""
"""Fonctions de boutons"""
def restartPopup(event):
    Popup(mainFrame, "Voulez-vous redémarrer?", "Oui", "Non", restart, -1)
def quitPopup(event):
    Popup(mainFrame, "Voulez-vous quitter?", "Oui", "Non", quit, -1)
def restart(event):
    print("restart")
def quit(event):
    print("quit")
def cancel(event):
    print("cancel")
def info(event):
    webbrowser.open(os.path.abspath("_instructions.pdf"))

"""Fonction qui centre un widget/fenêtre par rapport à l'écran"""
def center(widget, root):
    widget.update_idletasks()
    _w, _h = widget.winfo_width(), widget.winfo_height()
    _W, _H = widget.winfo_screenwidth(), widget.winfo_screenheight()
    _X, _Y = 0, 0
    if root != -1:
        root.update_idletasks()
        _W, _H = root.winfo_width(), root.winfo_height()
        _X, _Y = root.winfo_rootx(), root.winfo_rooty()
    widget.geometry("+%d+%d" % (_X + _W/2 - _w/2, _Y + _H/2 - _h/2))

"""Fonction qui retourne si une case est vide (sans jetons) ou pas"""
def empty(i, j):
    if players[i][j] == -1: return True
    else: return False

"""Fonction qui retourne le type de la case"""
def case(i, j):
    if (i % 2 == 0 and j % 2 == 0) \
        or (i % 2 == 1 and j % 2 == 1):
        return 0
    else:
        return 1

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

"""Fonction qui convertit des coordonnées d'index de tableau en pixels et vice verse"""
def pixelToCell(x):
    return (x // bSize)
def cellToPixel(x):
    return int(x * bSize + (bSize - playerCanvasSize) / 2)

"""Fonction qui convertit des coordonnées du board en coordonnées du frame"""
def boardToFrame(a, xOrY):
    if xOrY == "x": return a + 4
    if xOrY == "y": return a + 25 * 2 + 4

"""Fonction qui éxécute un effet sonore"""
def playSound(sound):
    #PlaySound(sound, SND_FILENAME | SND_ASYNC)
    return

"""Fonction appelée lorsqu'on ferme le jeu"""
def closeWindow():
    window.destroy()

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

"""--------------------------------------------------PRINCIPALES-----------------------------------------------------"""
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
    global playerCanvasSize
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
    scorePlayersSpacingX = (scoreBoard.halfScoreBoardSize - \
                            ((scoreBoard.scoreBoardBorder * 2) + (playersPerRow * playerCanvasSize / 2))) \
                           / (playersPerRow + 1)
    scorePlayersSpacingY = (scoreBoard.underScoreBoardSize[1] - \
                            ((scoreBoard.scoreBoardBorder / 2) + (playersPerColumn * playerCanvasSize / 2))) \
                           / (playersPerColumn + 1)
    if ePlayerType == 1:
        scorePositionX = hardCodedCoordinates[0] \
                         + scoreBoard.scoreBoardBorder + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    if ePlayerType == -1:
        scorePositionX = scoreBoard.scoreBoardSize[0] / 2 + hardCodedCoordinates[0] \
                         + 2 + scoreBoard.scoreBoardBorder / 4 + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    scorePositionY = hardCodedCoordinates[1] + scoreBoard.scoreBoardBorder + scorePlayersSpacingY \
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
            playSound(sound["select"])
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
            playSound(sound["move"])
            # Si on est en train de manger un joueur,
            if playerMovement[2] > sqrt(2):
                eat(i, j, player, playerMovement)
                playSound(sound["eat"])
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
            playSound(sound["super"])
        # Si elle est vierge et qu'on est pas coincés dans un combo,
        elif not highlightStuck:
            resetCaseColour()
            selectedPlayer = -1
            playSound(sound["deselect"])

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------PROGRAMME------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""-----------------------------------------------FRAMES-PRINCIPALES-------------------------------------------------"""
mainFrame = Frame(window)
mainFrame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)
sideFrame1 = Frame(mainFrame)
sideFrame1.grid(row=1, column=0)
sideFrame2 = Frame(mainFrame)
sideFrame2.grid(row=1, column=1)

"""-------------------------------------------------WIDGETS-WINDOW---------------------------------------------------"""
infoIcon = Button(window, "?", info, 20, _animationType=1, _tag="bold")
infoIcon.canvas.place(relx=1, x=0, y=20, anchor=NE)

"""-------------------------------------------------WIDGETS-GAUCHE---------------------------------------------------"""
topFrame = Frame(sideFrame1)
topFrame.grid(row=0, column=0)
title = Label(topFrame, text="LE JEU DE DAMES", font=("Trebuchet MS", 25), height=1)
title.pack()

board = Frame(sideFrame1, borderwidth=5, bg="black")
board.grid(row=1, column=0)
Board(board, gSize, bSize)

turnText = Label(sideFrame1, textvariable=turn, font=("Trebuchet MS", 15))
turnText.grid(row=2, column=0)

"""-------------------------------------------------WIDGETS-DROITE---------------------------------------------------"""
scoreBoard = ScoreBoard(sideFrame2, (300, 150), (300, 100), 6)
scoreBoard.canvas.grid(row=0, column=0)

emptySpace1 = Canvas(sideFrame2, width=400, height=55 / 2)
emptySpace1.grid(row=1, column=0)

cancelText = Button(sideFrame2, "ANNULER", cancel, 15)
cancelText.canvas.grid(row=2, column=0)

restartText = Button(sideFrame2, "REDEMARRER", restartPopup, 15)
restartText.canvas.grid(row=3, column=0)

quitText = Button(sideFrame2, "QUITTER", quitPopup, 15)
quitText.canvas.grid(row=4, column=0)

emptySpace1 = Canvas(sideFrame2, width=400, height=55 / 2)
emptySpace1.grid(row=5, column=0)

"""---------------------------------------------------EXECUTION------------------------------------------------------"""
window.configure(bg="white")
window.protocol("WM_DELETE_WINDOW", closeWindow)
center(window, -1)
window.mainloop()

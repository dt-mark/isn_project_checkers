from tkinter import *
from threading import *
from winsound import *
import webbrowser, os

window = Tk()

from constants import *
from globals import *
from functions import *

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""
playerObjects = []
buttonObjects = []
"""----------------------------------------------------PLAYER--------------------------------------------------------"""
class Player:

    def __init__(self, _frame, _x, _y, _type, _score=0):
        playerObjects.append(self)
        self.score = _score
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
        self.canvas = Canvas(_frame, width=playerCanvasSize, height=playerCanvasSize, \
                             bg=c[self.i][self.j], bd=0, highlightthickness=0)
        # self.canvasItem = self.canvas.create_oval(2,2, playerCanvasSize-2,playerCanvasSize-2, fill=self.col1, width=0)
        self.canvasItem = self.canvas.create_rectangle(0, 0, playerCanvasSize, playerCanvasSize, \
                                                       fill=self.col1, outline=self.col2, width=8)
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
                        players[i][j] = Player(_frame, i, j, 1)
                        scoreDisplay[-1].set(intToString(int(scoreDisplay[-1].get()) - 1))
                    elif int(scoreDisplay[1].get()) > 0 and j >= 6:
                        players[i][j] = Player(_frame, i, j, -1)
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
        canMove(_frame)


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

    def __init__(self, _frame, _text, _func, _size, _animationType=0, _font="Trebuchet MS", _tag=""):
        buttonObjects.append(self)
        self.animationType = _animationType
        self.refreshRate = 10
        self.text, self.size, self.func = _text, _size, _func
        self.ww, self.hh = (len(_text) + 3) * _size, 1.85 * _size
        self.canvas = Canvas(_frame, width=self.ww, height=self.hh - 3)
        self.canvas.label = self.canvas.create_text(self.ww / 2, self.hh / 2, text=self.text)
        self.canvas.arrowSpace = 0
        self.canvas.colourA, self.canvas.colourT = 1, 0.5
        self.canvas.font, self.canvas.tag = _font, _tag
        self.canvas.size, self.canvas.aimedSize = self.size, self.size
        self.canvas.style = (self.canvas.font, self.canvas.size, self.canvas.tag)
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.bind("<1>",
                         lambda event, func=self.func, anim=self.animationType: self.buttonPress(event, func, anim))
        self.canvas.bind("<Enter>", lambda event, t=+1, anim=self.animationType: self.buttonMouse(event, t, anim))
        self.canvas.bind("<Leave>", lambda event, t=-1, anim=self.animationType: self.buttonMouse(event, t, anim))
        ax1, ax2 = self.ww / 2 + (len(self.text) / 2) * self.size, self.ww / 2 - (len(self.text) / 2) * self.size
        self.arrow1 = self.canvas.create_polygon(ax1 + 10, self.hh / 2, ax1, 0 + 5, ax1, self.hh - 5, fill="white",
                                                 width=2)
        self.arrow2 = self.canvas.create_polygon(ax2 - 10, self.hh / 2, ax2, 0 + 5, ax2, self.hh - 5, fill="white",
                                                 width=2)
        self.update()

    def buttonMouse(self, event, enterOrLeave, anim):
        caller = self.canvas
        if anim == 0:
            caller.colourA = clamp(-enterOrLeave, 0, 1)
        if anim == 1:
            caller.aimedSize = self.size + 5 * clamp(enterOrLeave, 0, 1)
            caller.colourT = (1 - self.size / caller.size) + 0.25

    def buttonPress(self, event, func, anim):
        caller = self.canvas
        if anim == 0:
            caller.size += 4
            caller.arrowSpace = 1
        if anim == 1:
            caller.size -= 4
        Sound(sound["click"])
        func(event)

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
            self.canvas.coords(self.arrow1, ax1 + 10, self.hh / 2, ax1, 0 + 5, ax1, self.hh - 5)
            self.canvas.coords(self.arrow2, ax2 - 10, self.hh / 2, ax2, 0 + 5, ax2, self.hh - 5)
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

    def __init__(self, _text, _textOption1, _textOption2, _funcOption1, _funcOption2):
        self.text, self.tO1, self.tO2 = _text, _textOption1, _textOption2
        self.O1, self.O2 = _funcOption1, _funcOption2
        assignFunction = lambda a: ((lambda event: self.cancelPopup(event)) if a == -1 \
                                        else (lambda event: self.acceptPopup(event, a)))
        self.O1, self.O2 = assignFunction(self.O1), assignFunction(self.O2)
        self.top = Toplevel()
        self.label = Label(self.top, text=self.text, font=("Trebuchet MS", 20), fg=colour["black"])
        self.button1 = Button(self.top, self.tO1, self.O1, 15, _animationType=1)
        self.button2 = Button(self.top, self.tO2, self.O2, 15, _animationType=1)
        self.label.grid(row=0, column=0, columnspan=2)
        self.button1.canvas.grid(row=1, column=0)
        self.button2.canvas.grid(row=1, column=1)
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


"""-----------------------------------------------------SOUND--------------------------------------------------------"""
class Sound(Thread):

    def __init__(self, _name):
        Thread.__init__(self)
        self.name = _name
        PlaySound(self.name, SND_FILENAME | SND_ASYNC)

    def run(self):
        # Get lock to synchronize threads
        threadLock.acquire()
        # Free lock to release next thread
        threadLock.release()


"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FONCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""Fonction qui détermine si un joueur est coincé"""
def isBlocked(ptype):
    global players, c
    _playerCanMove = 0
    for pi in range(gSize + 1):
        for pj in range(gSize + 1):
            _player = players[pi][pj]
            if _player != -1:
                _type = _player.type
                if _type == ptype and \
                        (highlight(pi, pj, _type, behaviour=-1) \
                         or highlight(pi, pj, _type, behaviour=-2)):
                    _playerCanMove += 1
    if _playerCanMove == 0:
        return True
    else:
        return False

"""Fonction qui détermine s'il reste des joueurs"""
def isAlive(ptype):
    global scoreDisplay
    return ((gSize * 2) - (int(scoreDisplay[ptype].get()) - 1) != 0)

"""Fonction qui check s'il y a eu victoire ou pas"""
def victory():
    global nothingHappened
    if nothingHappened >= 25:
        print("DRAW, no one won, no one lost")
    for _player in [-1, 1]:
        if isBlocked(_player) or not isAlive(_player):
            print("{} has lost".format("WHITE player" if _player == -1 else "BLACK player"))
            print("{} has won".format("BLACK player" if _player == -1 else "WHITE player"))
            break

"""Fonction qui check si on un joueur peut en manger un autre"""
def canMove(widget):
    global player, players, onePlayerCanEat
    canMoveAgain = lambda w=widget: canMove(widget)
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
                                widget.after(15, canMoveAgain)
                                return None
        if b == -1:
            if onePlayerCanEat != {-1: [(-1, -1)], 1: [(-1, -1)]}:
                widget.after(15, canMoveAgain)
                return None
            else:
                continue
    widget.after(15, canMoveAgain)

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
            nj = lambda a: j + a * playerVar
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
    # Définition du joueur mangé
    eatenPlayerX = i + int(playerMovement[0] / 2)
    eatenPlayerY = j + int(playerMovement[1] / 2)
    eatenPlayer = players[eatenPlayerX][eatenPlayerY]
    ePlayerType = eatenPlayer.type
    # Augmentation du score
    scoreDisplay[ePlayerType].set(intToString(int(scoreDisplay[ePlayerType].get()) + 1))
    # Création d'un mini canevas pour l'animation
    scorePlayer[ePlayerType][int(scoreDisplay[ePlayerType].get())] \
    = Player(gameFrame, boardToFrame(cellToPixel(eatenPlayerX), "x"), \
             boardToFrame(cellToPixel(eatenPlayerY), "y"), \
             ePlayerType, _score=1)
    # Mouvement du canevas dans le tableau du score
    playersPerRow, playersPerColumn = 5, 4
    hardCodedCoordinates = (462, 190)
    scorePlayersSpacingX = (gameScoreBoard.halfScoreBoardSize - \
                            ((gameScoreBoard.scoreBoardBorder * 2) + (playersPerRow * playerCanvasSize / 2))) \
                           / (playersPerRow + 1)
    scorePlayersSpacingY = (gameScoreBoard.underScoreBoardSize[1] - \
                            ((gameScoreBoard.scoreBoardBorder / 2) + (playersPerColumn * playerCanvasSize / 2))) \
                           / (playersPerColumn + 1)
    if ePlayerType == 1:
        scorePositionX = hardCodedCoordinates[0] \
                         + gameScoreBoard.scoreBoardBorder + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    if ePlayerType == -1:
        scorePositionX = gameScoreBoard.scoreBoardSize[0] / 2 + hardCodedCoordinates[0] \
                         + 2 + gameScoreBoard.scoreBoardBorder / 4 + scorePlayersSpacingX \
                         + (playerCanvasSize / 2 + scorePlayersSpacingX) \
                         * ((int(scoreDisplay[ePlayerType].get()) - 1) % playersPerRow)
    scorePositionY = hardCodedCoordinates[1] + gameScoreBoard.scoreBoardBorder + scorePlayersSpacingY \
                     + (playerCanvasSize / 2 + scorePlayersSpacingY) \
                     * ((int(scoreDisplay[ePlayerType].get()) - 1) // playersPerRow)
    scorePlayer[ePlayerType][int(scoreDisplay[ePlayerType].get())] \
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
    global player, selectedPlayer, highlightStuck, onePlayerCanEat, nothingHappened
    # Si on clique sur un joueur,
    if players[i][j] != -1 and players[i][j] != selectedPlayer \
            and players[i][j].type == player:
        if not highlightStuck:
            resetCaseColour()
            selectedPlayer = players[i][j]
            player = selectedPlayer.type
            highlight(i, j, player)
            Sound(sound["select"])
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
            # Si on est en train de manger un joueur,
            if playerMovement[2] > sqrt(2):
                eat(i, j, player, playerMovement)
                Sound(sound["eat"])
                nothingHappened = 0
            # On change de joueur
            if (highlightStuck == False):
                player = -player
                turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))
            # Si on est arrivés au bout de la grille,
            endOfGrid = ((j == 0 and player == 1) or (j == gSize - 1 and player == -1)) and players[i][j].super == False
            if endOfGrid:
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
                Sound(sound["super"])
                nothingHappened = 0
            # Si on n'a rien mangé, et qu'on est pas devenu Super Jeton
            elif playerMovement[2] <= sqrt(2):
                Sound(sound["move"])
                nothingHappened += 1
        # Si elle est vierge et qu'on est pas coincés dans un combo,
        elif not highlightStuck:
            resetCaseColour()
            selectedPlayer = -1
            Sound(sound["deselect"])
    victory()

"""Fonction des boutons"""
def gameRestartPopup(event):
    Popup("Voulez-vous redémarrer?", "Oui", "Non", gameRestart, -1)
def gameQuitPopup(event):
    Popup("Voulez-vous quitter?", "Oui", "Non", gameQuit, -1)
def gameRestart(event):
    print("gameRestart")
def gameQuit(event):
    layoutDelete(gameFrame)
    menuLayout(window)
def gameCancel(event):
    print("gameCancel")
def menuOptions(event):
    print("menuOptions")
def menuStats(event):
    print("menuStats")
def menuQuit(event):
    print("menuQuit")
def info(event):
    webbrowser.open(os.path.abspath("_instructions.pdf"))

"""Changements de layout"""
def gameLayout(window):
    global gameFrame
    gameFrame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)
    layoutDelete(menuFrame)
def menuLayout(window):
    global menuFrame
    menuFrame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)
    layoutDelete(gameFrame)
def layoutDelete(frame):
    frame.pack_forget()

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------LAYOUT--------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

globalWidth, globalHeight = 800, 500

"""Main Frames"""
gameFrame = Frame(window, width=globalWidth, height=globalHeight)
gameFrame.grid_propagate(False)
menuFrame = Frame(window, width=globalWidth, height=globalHeight)
menuFrame.grid_propagate(False)

"""Game Widgets"""
gameSideFrame1 = Frame(gameFrame)
gameSideFrame1.grid(row=1, column=0, sticky="E")
gameSideFrame2 = Frame(gameFrame)
gameSideFrame2.grid(row=1, column=1, sticky="W")
gameTitle = Label(gameSideFrame1, text="LE JEU DE DAMES", font=("Trebuchet MS", 25), height=1)
gameTitle.grid(row=0, column=0)
gameBoard = Frame(gameSideFrame1, borderwidth=5, bg="black")
gameBoard.grid(row=1, column=0)
Board(gameBoard, gSize, bSize)
gameTurnText = Label(gameSideFrame1, textvariable=turn, font=("Trebuchet MS", 15))
gameTurnText.grid(row=2, column=0)
gameScoreBoard = ScoreBoard(gameSideFrame2, (300, 150), (300, 100), 6)
gameScoreBoard.canvas.grid(row=0, column=0)
gameEmptySpace1 = Canvas(gameSideFrame2, width=400, height=50 / 2)
gameEmptySpace1.grid(row=1, column=0)
gameCancelText = Button(gameSideFrame2, "ANNULER", gameCancel, 15)
gameCancelText.canvas.grid(row=2, column=0)
gameRestartText = Button(gameSideFrame2, "REDEMARRER", gameRestartPopup, 15)
gameRestartText.canvas.grid(row=3, column=0)
gameQuitText = Button(gameSideFrame2, "QUITTER", gameQuitPopup, 15)
gameQuitText.canvas.grid(row=4, column=0)
gameEmptySpace2 = Canvas(gameSideFrame2, width=400, height=50 / 2)
gameEmptySpace2.grid(row=5, column=0)

"""Menu Widgets"""
menuEmptySpace1 = Canvas(menuFrame, width=globalWidth, height=80)
menuEmptySpace1.grid(row=0)
menuLogo = Label(menuFrame, text="LE JEU DE DAMES", font=("Trebuchet MS", 70))
menuLogo.grid(row=1)
menuEmptySpace2 = Canvas(menuFrame, width=globalWidth, height=50)
menuEmptySpace2.grid(row=2)
menuPlayButton = Button(menuFrame, "JOUER", lambda w=window: gameLayout(window), 20, _animationType=1)
menuPlayButton.canvas.grid(row=3)
menuOptionsButton = Button(menuFrame, "OPTIONS", menuOptions, 20, _animationType=1)
menuOptionsButton.canvas.grid(row=4)
menuStatsButton = Button(menuFrame, "STATISTIQUES", menuStats, 20, _animationType=1)
menuStatsButton.canvas.grid(row=5)
menuQuitButton = Button(menuFrame, "QUITTER", menuQuit, 20, _animationType=1)
menuQuitButton.canvas.grid(row=6)

"""Help Icon (displayed at all times)"""
infoIcon = Button(window, "?", info, 20, _animationType=1, _tag="bold")
infoIcon.canvas.place(relx=1, x=0, y=20, anchor=NE)

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------EXECUTE-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""
threadLock = Lock()

gameLayout(window)

window.title("PROJET d'ISN")
window.configure(bg="white")
window.tk_setPalette(background="white")
window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", lambda w=window: closeWindow(w))
center(window, -1)
window.mainloop()

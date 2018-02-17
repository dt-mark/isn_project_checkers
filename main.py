from tkinter import *
from threading import *
from winsound import *
import webbrowser, os

from constants import *
from globals import *
from functions import *
from layout import *

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------PLAYER--------------------------------------------------------"""
class Player:

    def __init__(self, _frame, _x, _y, _type, _score=0):
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
        speed = 0.2 * refreshRate * 0.1 if self.score == 0 else 0.15 * refreshRate * 0.1
        self.xTo = lerp(self.xTo, self.x, speed)
        self.yTo = lerp(self.yTo, self.y, speed)
        xDif = abs(self.xTo-self.x)
        yDif = abs(self.yTo-self.y)
        farEnough = xDif > 0.01 and yDif > 0.01
        if farEnough: self.canvas.place(x=self.xTo, y=self.yTo)
        if self.score == 1:
            self.sTo = lerp(self.sTo, playerCanvasSize / 2, speed)
            self.canvas.configure(width=self.sTo, height=self.sTo)
            self.canvas.coords(self.canvasItem, 0, 0, self.sTo, self.sTo)
            self.canvas.itemconfigure(self.canvasItem, width=6)
        self.canvas.itemconfigure(self.canvasItem, fill=self.col1, outline=self.col2)
        self.canvas.after(refreshRate, self.update)


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

"""Fonction qui s'éxécute toutes les N millisecondes"""
def updateGame():
    if restart.get() == 1: resetGame()
    canMove()
    window.after(refreshRate, updateGame)

"""Fonction qui reset le jeu"""
def resetGame():
    global b, players, scoreDisplay, onePlayerCanEat, selectedPlayer, \
           player, nothingHappened, highlightStuck, scorePlayer
    for j in range(gSize):
        for i in range(gSize):
            b[i][j].unbind("<1>")
            b[i][j].destroy()
            if players[i][j] != -1:
                players[i][j].canvas.unbind("<1>")
                players[i][j].canvas.destroy()
    for p in [-1, 1]:
        for k in range(len(scorePlayer[p])):
            if type(scorePlayer[p][k]) != int:
                scorePlayer[p][k].canvas.destroy()
    scoreDisplay[-1].set(str(gSize * 2))
    scoreDisplay[+1].set(str(gSize * 2))
    onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
    selectedPlayer, player, nothingHappened, highlightStuck = -1, -1, 0, False
    scorePlayer = {-1: [0 for i in range(gSize * 2 + 1)], 1: [0 for i in range(gSize * 2 + 1)]}
    Board(gameBoard, gSize, bSize)
    restart.set(0)

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
def canMove():
    global player, players, onePlayerCanEat
    onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
    for be in [-1, -2]:
        for _player in [-1, 1]:
            for pi in range(gSize):
                for pj in range(gSize):
                    if players[pi][pj] != -1 and players[pi][pj].type == _player:
                        if highlight(pi, pj, _player, behaviour=be):
                            if be == -1:
                                if _player == player:
                                    onePlayerCanEat[_player].append((pi, pj))
                            if c[pi][pj] != colour["green"]:
                                if _player == player:
                                    caseColour(pi, pj, colour["red"])
                                continue
                            else:
                                resetCaseColour(withGreen=1)
                                return None
        if be == -1:
            if onePlayerCanEat != {-1: [(-1, -1)], 1: [(-1, -1)]}:
                return None
            else:
                continue

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
    hardCodedCoordinates = (460, 190)
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

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------EXECUTE-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

#Éléments d'interface qui ont besoin des classes définies dans "main.py" pour exister
Board(gameBoard, gSize, bSize)

#Son
threadLock = Lock()

#Afficher le menu
layoutCreate(menuFrame)
updateGame()

#Configurer la fenêtre principale
window.title("PROJET d'ISN")
window.configure(bg="white")
window.tk_setPalette(background="white")
window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", lambda w=window: closeWindow(w))
center(window, -1)

#Éxécuter
window.mainloop()

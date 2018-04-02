from tkinter import *
from winsound import *
import webbrowser, threading, random, time, os

from constants import *
from globalvars import *
from functions import *
from layout import *
from filehandling import *
import optionvars

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------PLAYER--------------------------------------------------------"""
class Player:
    def __init__(self, _frame, _x, _y, _type, _score=0):
        self.score = _score
        # Si ce sont des jetons jouables,
        if self.score == 0:
            # Leur position x et y correspond aux coordonnées de grille i, j
            self.x, self.y = cellToPixel(_x), cellToPixel(_y)
            self.i, self.j = _x, _y
        # Si ce sont des jetons à afficher au score,
        else:
            # Leur position x et y correspond aux arguments qui servent à calculer i, j
            self.x, self.y = _x, _y
            self.i, self.j = pixelToCell(_x), pixelToCell(_y)
        self.xTo, self.yTo, self.sTo = self.x, self.y, playerCanvasSize
        self.type = _type
        self.super = False
        # Un jeton de type -1 est blanc, un jeton de type 1 est noir
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
        # Enregistrer le nombre de mouvements
        if (optionvars.ai == 1 and self.type == optionvars.humanPlayer) or (optionvars.ai == 0):
            moves[self.type].set(moves[self.type].get() + 1)
        # Si on est un jeton jouable,
        if self.score == 0:
            # On calcule les coordonnées sur la grille i, j de l'ancienne position
            self.i, self.j = pixelToCell(self.x), pixelToCell(self.y)
            # On reset la case vide derrière
            players[self.i][self.j] = -1
            # On set la case devant
            players[_x][_y] = self
            players[_x][_y].canvas.bind("<1>", lambda event, x=_x, y=_y: click(event, x, y))
            self.x = cellToPixel(_x)
            self.y = cellToPixel(_y)
        # Si on est un jeton de score,
        else:
            # Set la position
            self.x = _x
            self.y = _y
        # Afficher le jeton en mouvement par dessus tout
        Misc.lift(self.canvas, aboveThis=None)
    def update(self):
        # Vitesse de mouvement
        speed = 0.2 * refreshRate * 0.1 if self.score == 0 else 0.15 * refreshRate * 0.1
        # Faire approcher de manière smooth les coordonnées du jeton (xTo, yTo) des coordonnées désirées (x, y)
        self.xTo = lerp(self.xTo, self.x, speed)
        self.yTo = lerp(self.yTo, self.y, speed)
        # Calcul de la différence de mouvement à faire
        xDif = abs(self.xTo-self.x)
        yDif = abs(self.yTo-self.y)
        farEnough = xDif > 0.01 and yDif > 0.01
        # Bouger le jeton si il y a un grand mouvement à faire (pour pas perdre des ressources sur des micromouvements)
        if farEnough: self.canvas.place(x=self.xTo, y=self.yTo)
        # Si on est un jeton à afficher,
        if self.score == 1:
            # Calcul de la différence de mouvement à faire
            sDif = abs(self.sTo - playerCanvasSize / 2)
            bigEnough = sDif > 1
            # Faire baisser la taille du jeton s'il n'est pas déjà petit
            if bigEnough:
                self.sTo = lerp(self.sTo, playerCanvasSize / 2, speed/2)
                self.canvas.configure(width=self.sTo, height=self.sTo)
                self.canvas.coords(self.canvasItem, 0, 0, self.sTo, self.sTo)
                self.canvas.itemconfigure(self.canvasItem, width=6)
        # Colorier le canevas de la bonne couleur
        self.canvas.itemconfigure(self.canvasItem, fill=self.col1, outline=self.col2)
        # Se ré-appeler pour mettre tout à jour
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

"""----------------------------------------------------COUNTER-------------------------------------------------------"""
class Counter:
    #https://stackoverflow.com/questions/35088139/how-to-make-a-thread-safe-global-counter-in-python
    def __init__(self, initialValue=0):
        self.value = initialValue
        self.value2 = initialValue
        self.lock = threading.Lock()
        self.startTime = time.time()
    def increment(self):
        with self.lock:
            self.value += time.time() - self.startTime
            self.startTime = time.time()
            self.value2 += 1

"""-----------------------------------------------------TREE---------------------------------------------------------"""
class Tree:
    def __init__(self):
        self.node = []
        self.nodeData = []
    def add(self, node):
        for i in range(len(node)):
            self.node.append(Tree())
            self.nodeData.append(node[i])
    def get(self, *args):
        path = "self"
        for j, i in enumerate(args):
            beginning = ".node[" if len(args) > 1 and (j != len(args)-1) else ".nodeData["
            path += beginning+str(i)+"]"
        return eval(path)

"""-----------------------------------------------------SOUND--------------------------------------------------------"""
class Sound(threading.Thread):
    def __init__(self, _name):
        threading.Thread.__init__(self)
        self.name = _name
        PlaySound(self.name, SND_FILENAME | SND_ASYNC)
    def run(self):
        # Get lock to synchronize threads
        threadLock.threading.acquire()
        # Free lock to release next thread
        threadLock.threading.release()

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FONCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""Fonction qui s'éxécute toutes les N millisecondes"""
def updateGame():
    global aiState, aiCoords, aiInCombo, gameEnd
    # Si la variable restart == 1, on reset le game
    if restart.get() == 1: resetGame()
    if not gameEnd:
        # On check quels joueurs peuvent bouger/manger et les colorier
        canMove()
        # On incrémente le compteur global
        currentFrame = getCurrentFrame()
        if currentFrame == gameFrame:
            counter.increment()
        # Si l'IA attend, la relancer
        if aiState == None:
            if aiCoords == None or aiCoords == (0, 0):
                aiCoords = aiMoveChoice()
            aiState = aiMove(aiCoords[0], aiCoords[1], combo=aiInCombo)
    # Se ré-appeler pour mettre à jour
    window.after(refreshRate, updateGame)

"""Fonction qui reset le jeu"""
def resetGame():
    global b, players, scoreDisplay, onePlayerCanEat, selectedPlayer, \
           player, nothingHappened, highlightStuck, scorePlayer, \
           aiCoords, aiState, aiInCombo, moves, initialCount, gameEnd
    # On loop dans la grille
    for j in range(gSize):
        for i in range(gSize):
            # Détruire les cases de la grille
            b[i][j].unbind("<1>")
            b[i][j].destroy()
            # Si il y a un jeton,
            if not empty(i, j):
                # Détruire le jeton
                players[i][j].canvas.unbind("<1>")
                players[i][j].canvas.destroy()
    # Pour les deux types de joueurs,
    for p in [-1, 1]:
        # Détruire les joueurs qui sont affichés au score
        for k in range(len(scorePlayer[p])):
            if type(scorePlayer[p][k]) != int:
                scorePlayer[p][k].canvas.destroy()
    # Reset les variables
    scoreDisplay[-1].set(str(gSize * 2))
    scoreDisplay[+1].set(str(gSize * 2))
    onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
    selectedPlayer, player, nothingHappened, highlightStuck = -1, -1, 0, False
    scorePlayer = {-1: [0 for i in range(gSize * 2 + 1)], 1: [0 for i in range(gSize * 2 + 1)]}
    counter.value = 0
    initialCount = 0
    aiState = None
    if (optionvars.humanPlayer == player or optionvars.ai == 0): aiState = True
    aiCoords = (0, 0)
    aiInCombo = 0
    moves[-1].set(0)
    moves[+1].set(0)
    globalTime.set(0)
    gameEnd = False
    # Recréer une table de jeu
    Board(gameBoard, gSize, bSize)
    canMove()
    # Ne plus éxécuter
    restart.set(0)

"""Fonction qui détermine si un joueur est coincé"""
def isBlocked(ptype):
    global players, c
    # Variable déterminant si un des joueurs peut bouger
    _playerCanMove = 0
    # On loop dans la grille
    for pi in range(gSize + 1):
        for pj in range(gSize + 1):
            _player = players[pi][pj]
            if _player != -1:
                _type = _player.type
                # Si un jeton du type indiqué peut bouger,
                if _type == ptype and \
                        (highlight(pi, pj, _type, behaviour=-1) \
                         or highlight(pi, pj, _type, behaviour=-2)):
                    # Incrémenter la variable
                    _playerCanMove += 1
    # Retourner si le joueur est bloqué ou pas
    if _playerCanMove == 0:
        return True
    else:
        return False

"""Fonction qui détermine s'il reste des joueurs"""
def isDead(ptype):
    global scoreDisplay
    return ((gSize * 2) - (int(scoreDisplay[ptype].get()) - 1) == 0)

"""Fonction qui check s'il y a eu victoire ou pas"""
def victory():
    global nothingHappened, winner, gameEnd
    if gameEnd: return
    # Sauvegarder le temps
    globalTime.set(counter.value)
    # Si il ne s'est rien passé depuis 25 tours,
    if nothingHappened >= 25:
        # Déclarer égalité
        endStr = "Il ne s'est rien passé depuis 25 tours\nIl y a donc égalité\n"
        # Créer un popup de fin de jeu
        Popup(text="La partie est terminée!", subtext=endStr, type=1, twoPlayers="draw")
        gameEnd = True
    # On check pour chaque joueur
    for _player in [-1, 1]:
        # S'il est bloqué ou s'il a plus de jetons,
        if isBlocked(_player) or isDead(_player):
            # Le gagnant est l'autre joueur
            if optionvars.ai == 0: winner.set(-_player)
            else: winner.set(_player)
            # Selon le mode de jeu, générer un texte de fin de jeu
            if optionvars.ai == 1:
                endStr = "{0} gagné\n{1} perdu".format(
                    "Vous avez" if -winner.get() == optionvars.humanPlayer else "La machine a", \
                    "La machine a" if -winner.get() == optionvars.humanPlayer else "Vous avez", )
            else:
                endStr = "Le joueur {0} a gagné\nLe joueur {1} a perdu".format(
                    "BLANC" if winner.get() == -1 else "NOIR", \
                    "NOIR" if winner.get() == -1 else "BLANC")
            # Créer un popup de fin de jeu
            Popup(text="La partie est terminée!", subtext=endStr, type=1, twoPlayers=optionvars.ai == 0)
            gameEnd = True
            return

"""Fonction qui transforme un jeton en super jeton"""
def turnSuper(i, j):
    global players, nothingHappened
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

"""Fonction qui check si on un jeton peut en manger un autre"""
def canMove():
    global player, players, onePlayerCanEat, onePlayerCanMove, aiCoords
    # Reset les dictionnnaires déterminant quels joueurs peuvent bouger ou manger/capturer
    onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
    onePlayerCanMove = {-1: [(-1, -1)], 1: [(-1, -1)]}
    # Exécuter deux fois (une pour le mouvement et une pour la capture)
    for be in [-1, -2]:
        # On loop dans la grille
        for pi in range(gSize):
            for pj in range(gSize):
                # S'il y a un jeton et s'il est du joueur actuellement en train de jouer
                if not empty(pi, pj) and players[pi][pj].type == player:
                    # Calculer s'il peut bouger ou manger/capturer
                    if highlight(pi, pj, player, behaviour=be):
                        # S'il peut manger
                        if be == -1:
                            # L'ajouter au dictionnaire de ceux qui peuvent bouger et ceux qui peuvent manger
                            onePlayerCanEat[player].append((pi, pj))
                            onePlayerCanMove[player].append((pi, pj))
                        # S'il peut bouger
                        if be == -2:
                            # L'ajouter au dictionnaire de ceux qui peuvent bouger
                            onePlayerCanMove[player].append((pi, pj))
                        # Si le couleur de la case n'est pas déjà verte
                        if c[pi][pj] != colour["green"]:
                            # Colorier la case en rouge
                            caseColour(pi, pj, colour["red"])
                        # Sinon,
                        else:
                            # Annuler toutes les couleurs rouges et arrêter d'executer la fonction
                            resetCaseColour(withGreen=1)
                            return
        # Si on check si le joueur peut manger un autre,
        if be == -1:
            # Si le joueur peut effectivement en manger un autre,
            if onePlayerCanEat != {-1: [(-1, -1)], 1: [(-1, -1)]}:
                # Arrêter d'exécuter la fonction (on check pas si il peut bouger, il faut qu'il mange obligatoirement)
                return
            # Sinon,
            else:
                # On check si on peut bouger
                continue

"""Fonction qui check où on peut aller"""
def highlight(i, j, player, behaviour=1):
    # Cette fonction retourne/fait différentes choses selon l'argument "behaviour"
    # behaviour == -3: retourne une liste de coordonnées indiquant les différents mouvements que le jeton peut faire
    # behaviour == -2: retourne True si on peut bouger d'une case
    # behaviour == -1: retourne True si on peut manger un autre jeton
    # behaviour ==  0: met en place un combo si possible (se ré-appelle en behaviour == 1, change des variables...)
    # behaviour ==  1: colorie les cases sur lesquelles le jeton peut bouger en vert
    global selectedPlayer, highlightStuck, onePlayerCanEat, aiCoords, aiInCombo
    # Variable stoquant les mouvements possibles (pour behaviour = -3)
    possibleMoves = []
    # Direction verticale (en haut ou en bas, selon le joueur)
    direction1 = [player]
    # Si le jeton est super, il peut aller dans la direction verticale opposée
    if players[i][j].super: direction1.append(-player)
    # Directions horizontales (droite et gauche)
    direction2 = [-1, 1]
    # On check pour toutes les directions
    for playerVar in direction1:
        for direction in direction2:
            # Coordonnées des checks (a étant le nombre de cases dans la direction actuelle du loop)
            ni = lambda a: i - a * direction
            nj = lambda a: j + a * playerVar
            # On définit les conditions des checks:
            # Un jeton de même type (1 case devant)
            samePlayerCondition = players[ni(1)][nj(1)] != -1 \
                                  and players[ni(1)][nj(1)].type == player
            # Un jeton de type opposé (1 case devant)
            otherPlayerCondition = players[ni(1)][nj(1)] != -1 \
                                   and players[ni(1)][nj(1)].type == -player
            # Hors grille (1 ou 2 cases devant)
            outsideGrid = (not isBetween(ni(1), 0, gSize - 1) \
                           or not isBetween(nj(1), 0, gSize - 1)) \
                          or (otherPlayerCondition and ( \
                        not isBetween(ni(2), 0, gSize - 1) \
                        or not isBetween(nj(2), 0, gSize - 1)))
            # En behaviour == 1, colorier la case du jeton selectionné en vert
            if behaviour == 1: caseColour(i, j, colour["green"])
            # Si on est hors grille, continuer dans une autre direction
            if outsideGrid: continue
            # S'il y a un ennemi et qu'ensuite la case est vide
            if otherPlayerCondition:
                if empty(ni(2), nj(2)):
                    # En behaviour == 1, on colorie les cases pour que le jeton puisse bouger normalement
                    if behaviour == 1:
                        # Colorier les 2 cases de devant en vert
                        caseColour(ni(1), nj(1), colour["green"])
                        caseColour(ni(2), nj(2), colour["green"])
                    # En behaviour == 0, on enclenche une séquence de combo
                    elif behaviour == 0:
                        # Bloquer le jeton dans un combo
                        highlightStuck = True
                        # Changer de jeton sélectionné
                        selectedPlayer = players[i][j]
                        # Colorier les cases pour manger
                        highlight(i, j, player, behaviour=1)
                        # Si on est l'IA, ré-appeler la fonction pour continuer la séquence de mouvements
                        aiCoords = ((i, j), (ni(2), nj(2))) #call the aiMoveChoice
                        aiInCombo = 1
                    # En behaviour == -1, on retourne True
                    if behaviour == -1:
                        return True
                    # En behaviour == -3, on ajoute ce mouvement de capture aux mouvements possibles
                    if behaviour == -3:
                        possibleMoves.append((ni(2), nj(2)))
                # Si la case après l'ennemi n'est pas vide, continuer dans une autre direction
                else: continue
            # S'il n'y a pas d'ennemi, continuer dans une autre direction
            elif behaviour == 0: continue
            # S'il y a un de nos jetons, continuer dans une autre direction
            if samePlayerCondition: continue
            # Si la case est vide
            if empty(ni(1), nj(1)):
                # Si on ne peut pas manger et si on est pas coincés dans un combo,
                if onePlayerCanEat[player] == [(-1, -1)] and not highlightStuck:
                    # En behaviour == 0, 1, 2, colorier la case de devant en vert
                    if behaviour >= 0:
                        caseColour(ni(1), nj(1), colour["green"])
                    # En behaviour == -3, ajouter le mouvement vers la case de devant
                    # dans la liste de mouvements possibles
                    if behaviour == -3:
                        possibleMoves.append((ni(1), nj(1)))
                # Si on est en behaviour == -2, retrourner True
                if behaviour == -2: return True
    # A la fin de la fonction, si on est en behaviour == -3, retourner les mouvements possibles
    if behaviour == -3: return possibleMoves
    # Retourner False (si behaviour == -1, -2 n'a pas retourné True)
    return False

"""Fonction qui permet de manger un jeton"""
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
    # Position où le mini canevas va aller
    playersPerRow, playersPerColumn = 5, 4
    hardCodedCoordinates = (460, 186)
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
    # Mouvement du mini canevas
    scorePlayer[ePlayerType][int(scoreDisplay[ePlayerType].get())].changePosition(scorePositionX, scorePositionY)
    # Changement de couleur si le jeton est super
    if eatenPlayer.super:
        scorePlayer[ePlayerType][int(scoreDisplay[ePlayerType].get())].col1 = eatenPlayer.col2
    # Cleanup des variables
    eatenPlayer.canvas.destroy()
    players[eatenPlayerX][eatenPlayerY] = -1
    # On check si on peut enchainer avec un combo
    highlight(i, j, player, behaviour=0)

"""Fonction Principale"""
def click(event, i, j):
    global player, selectedPlayer, highlightStuck, onePlayerCanEat, nothingHappened, onePlayerCanMove, \
           initialCount, aiCoords, aiState, aiInCombo, gameEnd
    # On quitte si c'est la fin du jeu
    if gameEnd: return
    # On quitte si c'est l'IA qui joue et qu'on a cliqué
    if player == -optionvars.humanPlayer and optionvars.ai == 1 and event != None: return
    aiInCombo = 0
    # Si on clique sur un jeton sélectionnable,
    if players[i][j] != -1 and players[i][j] != selectedPlayer and players[i][j].type == player:
        # S'il n'est pas dans un combo
        if not highlightStuck:
            # On enlève les surbrillances
            resetCaseColour()
            # On set le joueur sélectionné
            selectedPlayer = players[i][j]
            player = selectedPlayer.type
            # On met les cases où on peut bouger en surbrillance
            highlight(i, j, player)
            # On joue un effet sonore
            Sound(sound["select"])
    # Si on est sur une case sans jeton sélectionnable,
    else:
        # Si elle est en surbrillance,
        if c[i][j] == colour["green"] and empty(i, j):
            # On enlève les surbrillances
            resetCaseColour()
            playerMovement = movementVector(pixelToCell(selectedPlayer.x), \
                                            pixelToCell(selectedPlayer.y), i, j)
            # On bouge le jeton, on le déselectionne, on le décoince (s'il était dans un combo)
            selectedPlayer.changePosition(i, j)
            player = selectedPlayer.type
            selectedPlayer = -1
            highlightStuck = False
            # Si a bougé de deux cases,
            if playerMovement[2] > sqrt(2):
                # On mange le jeton au milieu
                eat(i, j, player, playerMovement)
                # On joue un effet sonore
                Sound(sound["eat"])
                # On remet le compteur d'inactivité à 0
                nothingHappened = 0
            # Si on est arrivés au bout de la grille,
            if ((j == 0 and player == -1) or (j == gSize - 1 and player == 1)) and players[i][j].super == False:
                # On devient super jeton
                turnSuper(i, j)
            # Si on n'a rien mangé, et qu'on est pas devenu super jeton
            elif playerMovement[2] <= sqrt(2):
                Sound(sound["move"])
                nothingHappened += 1
            # Si on est pas dans un combo,
            if (highlightStuck == False):
                # On change de tour de joueur
                player = -player
                aiState = True
                # Si c'est au tour de l'IA, l'éxécuter
                if optionvars.ai == 1 and player == -optionvars.humanPlayer:
                    # Mettre à jour les mouvements possibles prématurément
                    canMove()
                    # Reset le compteur
                    initialCount = counter.value2
                    # Calculer le mouvement à faire
                    aiCoords = aiMoveChoice()
                    # Engager la séquence de mouvement (clics virtuels à intervalles de temps donnés)
                    aiState = None
                # On change le texte montrant les tours
                turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))
        # Si la case cliquée est vierge et qu'on est pas coincés dans un combo,
        elif not highlightStuck:
            # On enlève les surbrillances
            resetCaseColour()
            # On déselectionne les jetons
            selectedPlayer = -1
            # On joue un effet sonore
            Sound(sound["deselect"])
    # On check si quelqu'un a gagné
    victory()

"""Fonction qui détermine le mouvement de la machine"""
def aiMoveChoice():
    global difficulty, onePlayerCanMove, player, highlightStuck, gameEnd
    if gameEnd: return
    # Le joueur IA est l'inverse du joueur humain
    aiPlayer = -optionvars.humanPlayer
    # En difficulté 0,
    if optionvars.difficulty == 0:
        # On choisit un jeton aléatoire des jetons pouvant bouger
        try: playerToMove = random.choice(onePlayerCanMove[aiPlayer][1:])
        except: return
        # On détermine les mouvements que ce jeton peut faire
        possibleMoves = highlight(playerToMove[0], playerToMove[1], aiPlayer, behaviour=-3)
        # On choisit un de ces mouvements au hazard
        targetMove = random.choice(possibleMoves)
        # On retourne le jeton et le mouvement choisi
        return (playerToMove, targetMove)

"""Fonction qui éxécute le mouvement de la machine"""
def aiMove(playerToMove, targetMove, combo=0):
    # Intervalle de temps entre les clics virtuels
    interval = 30
    # Si on doit faire un combo,
    if combo == 1:
        # Au moment venu,
        if (counter.value2 - initialCount) == (interval * 2.5):
            # Cliquer sur la case pour bouger
            click(None, targetMove[0], targetMove[1])
            # Arrêter d'appeler cette fonction
            return True
        # Sinon, on attend encore en appelant cette fonction
        else: return None
    # Si il s'agit d'un mouvement normal,
    else:
        # Au moment venu de sélectionner le joueur,
        if (counter.value2 - initialCount) == (interval * 1):
            # On le sélectionne
            click(None, playerToMove[0], playerToMove[1])
            # On attend encore en appelant cette fonction (pour bouger une prochaine fois)
            return None
        # Au moment venu de sélectionner une case,
        elif (counter.value2 - initialCount) == (interval * 1.6):
            # On sélectionne la case, en faisant cela, la fonction highlight affecte True à aiState,
            # cela fait qu'on arrête d'appeler la fonction
            click(None, targetMove[0], targetMove[1])
        # Sinon, on attend encore en appelant cette fonction
        else: return None

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------EXECUTE-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

#Éléments d'interface qui ont besoin des classes définies dans "main.py" pour exister
Board(gameBoard, gSize, bSize)

#Son
threadLock = threading.Lock()

#Compteur
initialCount = 0
counter = Counter()

#IA
aiState = None
if (optionvars.humanPlayer == player or optionvars.ai == 0): aiState = True

#Afficher le menu
layoutCreate(menuFrame)
updateGame()

#Configurer la fenêtre principale
window.title("PROJET d'ISN")
window.tk_setPalette(background="white")
window.resizable(width=False, height=False)
window.protocol("WM_DELETE_WINDOW", lambda w=window: closeWindow(w))
center(window, -1)

#Éxécuter
window.mainloop()

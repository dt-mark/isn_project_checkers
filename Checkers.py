"""--------------------------------------------------------------------------"""
"""--------------------------------MODULES-----------------------------------"""
"""--------------------------------------------------------------------------"""
import os, sys
sys.path.append("D:\Documents\CPython\Projet ISN\modules")
#from mainInit import *

from tkinter import *
window = Tk()
window.title("PROJET d'ISN")

"""--------------------------------------------------------------------------"""
"""-------------------------------VARIABLES----------------------------------"""
"""--------------------------------------------------------------------------"""

windowBorder = 50
onePlayerCanEat = {-1:[(-1, -1)], 1:[(-1, -1)]}

gSize = 10
bSize = 40
playerCanvasSize = 30

b = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
c = [['' for i in range(gSize+1)] for j in range(gSize+1)]

players = [[-1 for i in range(gSize+1)] for j in range(gSize+1)]
player = -1
blackCount, whiteCount = 0, 0

selectedPlayer = -1
highlightStuck = False

colour = {
    "red":"#%02X%02X%02X" % (200, 50, 50),
    "green":"#%02X%02X%02X" % (0, 170, 50),
    "white":"#%02X%02X%02X" % (255, 255, 130),
    "black":"#%02X%02X%02X" % (160, 100, 0),
    "whitePlayer":"white",
    "blackPlayer":"black"
}
"""--------------------------------------------------------------------------"""
"""--------------------------------CLASSES-----------------------------------"""
"""--------------------------------------------------------------------------"""

class Player:
    def __init__(self, _x, _y, _type):
        self.x = int(_x*bSize+(bSize-playerCanvasSize)/2) 
        self.y = int(_y*bSize+(bSize-playerCanvasSize)/2)
        self.xTo, self.yTo = self.x, self.y
        self.type = _type
        self.refreshRate = 9
        col1 = colour["whitePlayer"] if _type == +1 else colour["blackPlayer"]
        col2 = colour["whitePlayer"] if _type == -1 else colour["blackPlayer"]
        self.canvas = Canvas(board, width=playerCanvasSize, \
                             height=playerCanvasSize, \
                             bg=c[i][j], bd=0, highlightthickness=0)
        #self.canvas.create_oval(2, 2, playerCanvasSize-2, playerCanvasSize-2, \
        #                        fill=col1, width=0)
        self.canvas.create_rectangle(0, 0, playerCanvasSize, playerCanvasSize, \
                                     fill=col1, outline=col2, width=8)
        self.canvas.place(x=self.x, y=self.y)
        self.canvas.bind("<1>", lambda event, x=i, y=j : click(event,x,y))
        self.update()
    def changePosition(self, _x, _y):
        global players
        _i, _j = cell(self.x), cell(self.y)
        players[_i][_j] = -1
        players[_x][_y] = self
        players[_x][_y].canvas.bind("<1>", lambda event, x=_x, y=_y : \
                                    click(event,x,y))
        self.x = int(_x*bSize+(bSize-playerCanvasSize)/2)
        self.y = int(_y*bSize+(bSize-playerCanvasSize)/2)
        Misc.lift(self.canvas, aboveThis=None)
    def update(self):
        self.xTo = lerp(self.xTo, self.x, 0.2)
        self.yTo = lerp(self.yTo, self.y, 0.2)
        self.canvas.place(x=self.xTo, y=self.yTo)
        self.canvas.after(self.refreshRate, self.update)

"""--------------------------------------------------------------------------"""
"""-------------------------------FONCTIONS----------------------------------"""
"""--------------------------------------------------------------------------"""

"""Fonction qui enroule un nombre dans un intervalle [0; a]"""
def wrap(x, a):
    return x % a
"""Fonction d'interpolation linéaire"""
def lerp(a, b, x):
    return a + (b-a)*x
"""Fonction de clamp"""
def clamp(x, a, b):
    return min(max(x, a), x, b)
"""Fonction qui retourne si une valeur est entre 2 bornes"""
def isBetween(x, a, b):
    a = min(a, b)
    b = max(a, b)
    if x >= a and x <= b: return True
    else: return False
"""Fonction qui retourne le type de la case"""
def case(i, j):
    if (i%2 == 0 and j%2 == 0)\
    or (i%2 == 1 and j%2 == 1):
        return 1 
    else:
        return 0 
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
        for keys in onePlayerCanEat.keys():
            if keys == player:
                for coords in onePlayerCanEat[keys]:
                    if isBetween(coords[0], 0, gSize-1) \
                    and isBetween(coords[1], 0, gSize-1):
                        c[coords[0]][coords[1]] = colour["red"]
    b[i][j].config(background=c[i][j])
"""Fonction qui reset la couleur des cases"""
def resetCaseColour():
    for i in range(gSize):
        for j in range(gSize):
            caseColour(i, j, -1)
"""Fonction qui retourne si une case est vide (sans jetons) ou pas"""
def empty(i, j):
    if players[i][j] == -1: return True
    else: return False
"""Fonction qui convertit des coordonnées en index de tableau"""
def cell(x):
    return (x//bSize)
"""Fonction appelée lorsqu'on ferme le jeu"""
def closeWindow():
    window.destroy()
    
"""Fonction qui check où on peut aller"""
def highlight(i, j, player, behaviour=1):
    global selectedPlayer, highlightStuck, onePlayerCanEat
    for direction in [-1, 1]:
        #Coordonnées des checks
        ni = lambda a: i-a*direction
        nj = lambda a: j-a*player
        #On définit les conditions des checks
        samePlayerCondition = players[ni(1)][nj(1)] != -1 \
                              and players[ni(1)][nj(1)].type == player
        otherPlayerCondition = players[ni(1)][nj(1)] != -1 \
                               and players[ni(1)][nj(1)].type == -player
        outsideGrid = (not isBetween(ni(1), 0, gSize-1) \
                      or not isBetween(nj(1), 0, gSize-1)) \
                      or (otherPlayerCondition and ( \
                      not isBetween(ni(2), 0, gSize-1) \
                      or not isBetween(nj(2), 0, gSize-1)))
        if behaviour == 1: caseColour(i, j, colour["green"])
        #Si on est hors grille
        if outsideGrid: continue
        #S'il y a un ennemi en diagonale et qu'ensuite la case est vide 
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
            else: continue
        elif behaviour == 0: continue
        #S'il y a un de nos jetons en diagonale
        if samePlayerCondition: continue
        #Si la case est vide
        if empty(ni(1), nj(1)) and behaviour != -1 \
        and onePlayerCanEat[player] == [(-1, -1)] and not highlightStuck:
            caseColour(ni(1), nj(1), colour["green"])
    return False
    
"""Fonction Principale"""
def click(event, i, j):
    global player, selectedPlayer, highlightStuck, onePlayerCanEat
    if selectedPlayer != -1: player = selectedPlayer.type
    #Si on clique sur un joueur,
    if players[i][j] != -1 and players[i][j] != selectedPlayer:
        if not highlightStuck:
            resetCaseColour() 
            selectedPlayer = players[i][j]
            player = selectedPlayer.type
            highlight(i, j, player)
    #Si on est sur une case normale,
    else:
        #Si elle est en surbrillance,
        if c[i][j] == colour["green"] and empty(i, j):
            onePlayerCanEat = {-1:[(-1, -1)], 1:[(-1, -1)]}
            resetCaseColour() 
            selectedPlayer.changePosition(i, j)
            player = selectedPlayer.type
            selectedPlayer = -1
            highlightStuck = False
            highlight(i, j, player, behaviour=0)
        #Si elle est vierge et qu'on est pas coincés dans un combo,
        elif not highlightStuck:
            resetCaseColour() 
            selectedPlayer = -1
    #Détecte si un des joueurs peut manger un autre
    for _player in [-1, 1]:
        for pi in range(gSize):
            for pj in range(gSize):
                if players[pi][pj] != -1 and players[pi][pj].type ==_player:
                    if highlight(pi, pj, _player, behaviour=-1): 
                        onePlayerCanEat[_player].append((pi, pj))
    
"""--------------------------------------------------------------------------"""
"""-------------------------------PROGRAMME----------------------------------"""
"""--------------------------------------------------------------------------"""

"""Arrangement des frames principales"""
mainFrame = Frame(window)
mainFrame.pack(padx=windowBorder, pady=windowBorder, fill="both")

topFrame = Frame(mainFrame)
topFrame.grid(column=0, row=0)

board = Frame(mainFrame, borderwidth=4, bg="black")
board.grid(column=0, row=1)

sideFrame = Frame(mainFrame)
sideFrame.grid(column=1, row=1)

"""Arrangement de la grille"""
for j in range(gSize):
    for i in range(gSize):
        
        #Création des boutons de base
        b[i][j] = Canvas(board, width=bSize, height=bSize, \
                  bd=0, highlightthickness=0)
        b[i][j].grid(column=i, row=j)
        
        #Si on est sur une case noire
        if case(i, j):
            #Créer la couleur marron
            c[i][j] = colour["black"]
            
            #Placer des jetons
            if blackCount < gSize*2 and j >= 0:
                players[i][j] = Player(i, j, -1)
                blackCount += 1
            elif whiteCount < gSize*2 and j >= 6:
                players[i][j] = Player(i, j, 1)
                whiteCount += 1
            else:
                players[i][j] = -1
                
        #Si on est sur une case blanche
        else:
            #Créer la couleur crème
            c[i][j] = colour["white"]
            #Le reste de la grille est égal à -1
            players[i][j] = -1
       
        #Fonction des boutons
        b[i][j].bind("<1>", lambda event, x=i, y=j : click(event,x,y))
        #Couleur des boutons   
        b[i][j].config(background=c[i][j])

        
"""Arrangement du reste"""
title = Label(topFrame, text="LE JEU DE DAMES", font=("Trebuchet MS", 25), height=1)
title.pack()
sideCanvas = Canvas(sideFrame, width=500)
sideCanvas.pack()

window.protocol("WM_DELETE_WINDOW", closeWindow)

"""Main"""
window.mainloop()

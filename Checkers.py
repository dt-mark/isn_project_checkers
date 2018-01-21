#Importation fonctions
from tkinter import *
from colorsys import *

#Tkinter
window = Tk()
window.title("PROJET d'ISN")

#Variables
windowBorder = 50

gSize = 10
bSize = 40

b = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
c = [[0 for i in range(gSize+1)] for j in range(gSize+1)]

blackPlayers = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
whitePlayers = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
initialBlackCount, initialWhiteCount = 0, 0

selectedPlayer = -1

#Arrangement des frames principales
mainFrame = Frame(window)
mainFrame.pack(padx=windowBorder, pady=windowBorder, fill="both")

topFrame = Frame(mainFrame)
topFrame.grid(row=0, column=0)

board = Frame(mainFrame, borderwidth=4, bg="black")
board.grid(row=1, column=0)

sideFrame = Frame(mainFrame)
sideFrame.grid(row=1, column=1)

#Fonction qui enroule un nombre dans un intervalle [0; a]
def wrap(x, a):
    return x % a
#Fonction d'interpolation linéaire
def lerp(a, b, x):
    return a + (b-a)*x
#Fonction de clamp
def clamp(x, a, b):
    return min(max(x, a), x, b)
#Fonction qui retourne si une valeur est entre 2 bornes
def is_between(x, a, b):
    a = min(a, b)
    b = max(a, b)
    if x >= a and x <= b: return True
    else: return False
#Fonction qui retourne la couleur de la case
def case(i, j):
    if (i%2 == 0 and j%2 == 0)\
    or (i%2 == 1 and j%2 == 1):
        return 1 
    else:
        return 0 
#Fonction qui définit la couleur d'une case
def caseColour(i, j, colour):
    if colour != -1:
        c[i][j] = colour
    else:
        if case(i, j):
            c[i][j] = "#%02X%02X%02X" % (150, 90, 0)
        else:
            c[i][j] = "#%02X%02X%02X" % (255, 255, 150)
    b[i][j].config(background=c[i][j])
#Fonction qui reset la couleur des cases
def resetCaseColour():
    for i in range(gSize):
        for j in range(gSize):
            caseColour(i, j, -1)
        
#Fonctions Principales
def click(event, i, j):
    global selectedPlayer
    #Si on est sur une case avec un joueur,
    if whitePlayers[i][j] != -1 and whitePlayers[i][j] != selectedPlayer: 
        player = -1
    elif blackPlayers[i][j] != -1 and blackPlayers[i][j] != selectedPlayer: 
        player = 1
    #Si on est sur une case normale,
    else: 
        resetCaseColour() 
        selectedPlayer = -1
        return -1
    #Reset la couleur des cases
    resetCaseColour()
    #On sélectionne et on colorie la case du jeton
    caseColour(i, j, "#%02X%02X%02X" % (0, 170, 50))
    if player == -1: selectedPlayer = whitePlayers[i][j]
    elif player == 1: selectedPlayer = blackPlayers[i][j]
    #Surbrillance des cases: check dans les deux directions en face
    for direction in [-1, 1]:
        k = 0
        keepIterating = 1
        outsideGrid = 0
        #Loop cherchant une case vide
        while keepIterating:
            k += 1
            ii = i+k*player
            jj = j+k*direction
            #Condition pour que le loop itère encore
            #à la recherche d'une case vide
            if player == -1: keepIterating = (whitePlayers[ii][jj] != -1)
            elif player == 1: keepIterating = (blackPlayers[ii][jj] != -1)
            outsideGrid = not is_between(ii, 0, gSize-1) \
                          or not is_between(jj, 0, gSize-1)
            #Si on est hors grille, on sort du while
            if outsideGrid: break
        #En sortie de while, si on est bien hors grille,
        #on passe à l'autre direction
        if outsideGrid: continue
        #On met en surbrillance les cases auxquelles on peut aller
        caseColour(ii, jj, "#%02X%02X%02X" % (0, 170, 50))

        
    
#Arrangement de la grille
for i in range(gSize):
    for j in range(gSize):
        
        #Création des boutons de base
        b[i][j] = Canvas(board, width=bSize, height=bSize, \
                  bd=0, highlightthickness=0)
        b[i][j].grid(row=i, column=j)
        
        #Création des jetons
        #Si on est sur une case noire
        if case(i, j):
            #Créer la couleur marron
            c[i][j] = "#%02X%02X%02X" % (150, 90, 0)
            
            #Si on a pas encore placé tous les jetons noirs (haut de la grille)
            if initialBlackCount < gSize*2 and i >= 0:
                #Créer un cercle
                blackPlayers[i][j] = Canvas(board, width=34, height=34, \
                                     bg=c[i][j], bd=0, highlightthickness=0)
                blackPlayers[i][j].create_oval(2, 2, 32, 32, \
                                   fill="black", width=0)
                blackPlayers[i][j].grid(row=i, column=j)
                #Augmenter le compteur
                initialBlackCount += 1
            #Si on a placé tous les jetons noirs, le reste de la grille vaut -1
            else:
                blackPlayers[i][j] = -1
            
            #Si on a pas encore placé tous les jetons blancs (bas de la grille)
            if initialWhiteCount < gSize*2 and i >= 6:
                #Créer un cercle
                whitePlayers[i][j] = Canvas(board, width=34, height=34, \
                                     bg=c[i][j], bd=0, highlightthickness=0)
                whitePlayers[i][j].create_oval(2, 2, 32, 32, \
                                   fill="white", width=0)
                whitePlayers[i][j].grid(row=i, column=j)
                #Augmenter le compteur
                initialWhiteCount += 1
            else:
                whitePlayers[i][j] = -1
                
        #Si on est sur une case blanche
        else:
            #Créer la couleur crème
            c[i][j] = "#%02X%02X%02X" % (255, 255, 150)
            #Le reste de la grille est égal à -1
            blackPlayers[i][j] = -1
            whitePlayers[i][j] = -1
       
        #Fonction des boutons
        b[i][j].bind("<1>", lambda event, x=i, y=j : click(event,x,y))
        #Fonction des jetons (si jamais ils sont au dessus d'un bouton)
        if blackPlayers[i][j] != -1: blackPlayers[i][j].bind("<1>", \
        lambda event, x=i, y=j : click(event,x,y))
        if whitePlayers[i][j] != -1: whitePlayers[i][j].bind("<1>", \
        lambda event, x=i, y=j : click(event,x,y))
        #Couleur des boutons   
        b[i][j].config(background=c[i][j])

        
#Arrangement du reste
title = Label(topFrame, text="LE JEU DE DAMES", font=("Verdana", 25), height=1)
title.pack()
sideCanvas = Canvas(sideFrame, width=500)
sideCanvas.pack()

#Main
window.mainloop()

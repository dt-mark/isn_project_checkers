#Importation fonctions
from tkinter import *
from colorsys import *

#Tkinter
window = Tk()
window.title("Checkers")

#Variables
gSize = 10
bSize = 4

b = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
c = [[0 for i in range(gSize+1)] for j in range(gSize+1)]

blackPlayers = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
whitePlayers = [[0 for i in range(gSize+1)] for j in range(gSize+1)]
initialBlackIterator, initialWhiteIterator = 0, 0

#Arrangement des frames principales
mainFrame = Frame(window)
mainFrame.pack(padx=50, pady=50)

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
#Fonction qui retourne la couleur de la case
def case(i, j):
    if (i%2 == 0 and j%2 == 0)\
    or (i%2 == 1 and j%2 == 1):
        return 1 
    else:
        return 0 
        
#Fonction Principale 
def click(button):
    return button
    
#Arrangement de la grille
for i in range(gSize):
    for j in range(gSize):
              
        b[i][j] = Button(board, width=int(bSize), height=int(bSize/2), \
                         command=lambda x=i, y=j : click(b[x][y]))
        b[i][j].grid(row=i, column=j)
        
        if case(i, j):
            whitePlayers[i][j] = -1
            c[i][j] = "#%02X%02X%02X" % (255, 255, 150)
            if initialBlackIterator < gSize*2 and i >= 0:
                blackPlayers[i][j] = Canvas(board, width=25, height=25, bg=c[i][j], bd=0, highlightthickness=0)
                blackPlayers[i][j].create_oval(0, 0, 25, 25, fill="black", activewidth=0)
                blackPlayers[i][j].grid(row=i, column=j)
                initialBlackIterator += 1
            else:
                blackPlayers[i][j] = -1
        else:
            blackPlayers[i][j] = -1
            c[i][j] = "#%02X%02X%02X" % (50, 30, 0)
            if initialWhiteIterator < gSize*2 and i >= 6:
                whitePlayers[i][j] = Canvas(board, width=25, height=25, bg=c[i][j], bd=0, highlightthickness=0)
                whitePlayers[i][j].create_oval(0, 0, 25, 25, fill="white", activewidth=0)
                whitePlayers[i][j].grid(row=i, column=j)
                initialWhiteIterator += 1
            else: 
                whitePlayers[i][j] = -1
                
        b[i][j].config(relief=FLAT, state=NORMAL, background=c[i][j], activebackground=c[i][j])

        
#Arrangement du reste
title = Label(topFrame, text="CHECKERS GAME", font=("Verdana", 25), height=1)
title.pack()
sideCanvas = Canvas(sideFrame, width=500)
sideCanvas.pack()

#Main
window.mainloop()
from tkinter import *
from math import *

from constants import *
from globals import *

"""Fonction qui enroule un nombre dans un intervalle [0; a]"""
def wrap(x, a):
    return x % a

"""Fonction qui échange deux valeurs"""
def switch(a, b):
    newa = b
    newb = a
    return newa, newb

"""Fonction d'interpolation linéaire"""
def lerp(a, b, x):
    return a + (b - a) * x

"""Fonction de clamp"""
def clamp(x, a, b):
    if x < a: return a
    elif x > b: return b
    else: return x

"""Fonction qui retourne la somme des membres d'une liste entre deux bornes"""
def listSum(l, a, b):
    result = 0
    for i, j in enumerate(l):
        if isBetween(i, a, b):
            result += j
    return result

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

"""Fonctions qui convertissent des couleurs HEX en RGB et vice versa"""
def hexToRGB(value):
    #https://stackoverflow.com/a/29643643
    value = value.lstrip('#')
    return tuple(int(value[i:i+2], 16) for i in (0, 2 ,4))
def RGBToHex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

"""Fonction qui mélange deux couleurs"""
def mergeColour(c1, c2, x):
    c1 = hexToRGB(c1)
    c2 = hexToRGB(c2)
    r, g, b = int(lerp(c1[0], c2[0], x)), int(lerp(c1[1], c2[1], x)), int(lerp(c1[2], c2[2], x))
    return RGBToHex((r, g, b))

"""Fonction qui met à jour les couleurs d'une frame de score"""
def scoreBoardUpdateColours(frame):
    frame.canvas.itemconfig(frame.rec1, fill=colour["white"])
    frame.canvas.itemconfig(frame.rec2, fill=colour["black"])
    frame.canvas.itemconfig(frame.rec3, fill=colour["black"])
    frame.canvas.itemconfig(frame.rec4, fill=colour["white"])
    frame.blackPlayerScore.configure(bg=colour["white"])
    frame.whitePlayerScore.configure(bg=colour["black"])

"""Fonction qui définit la couleur d'une case"""
def caseColour(i, j, col):
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

"""Fonction qui coupe un string trop long à N caractères"""
def cutString(str, c):
    if len(str) >= c:
        return str[:c] + "..."
    else:
        return str

"""Fonction qui convertit des coordonnées d'index de tableau en pixels et vice verse"""
def pixelToCell(x):
    return (x // bSize)
def cellToPixel(x):
    return int(x * bSize + (bSize - playerCanvasSize) / 2)

"""Fonction qui convertit des coordonnées du board en coordonnées du frame"""
def boardToFrame(a, xOrY):
    boardBorder = 5
    titleHeight = 50
    if xOrY == "x": return a + boardBorder
    if xOrY == "y": return a + titleHeight + boardBorder

"""Fonction appelée lorsqu'on ferme le jeu"""
def closeWindow(window):
    window.destroy()

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

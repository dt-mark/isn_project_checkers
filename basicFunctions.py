from math import *

"""Fonction qui enroule un nombre dans un intervalle [0; a]"""
def wrap(x, a):
    return x % a

"""Fonction qui échange deux valeurs"""
def switch(a, b):
    t = a
    a = b
    b = t
    return a, b

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

"""Fonction qui convertit des couleurs HEX en RGB et vice versa"""
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

"""Fonction qui convertit un nombre en string à deux caractères"""
def intToString(integer):
    integer = int(integer)
    if isBetween(integer, -9, 9):
        return "0" + str(integer)
    else:
        return str(integer)


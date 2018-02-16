from tkinter import *

from constants import *

b = [[0 for i in range(gSize + 1)] for j in range(gSize + 1)]
c = [['' for i in range(gSize + 1)] for j in range(gSize + 1)]

players, player = [[-1 for i in range(gSize + 1)] for j in range(gSize + 1)], -1
onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
scoreDisplay = {-1: StringVar(), 1: StringVar()}
scoreDisplay[-1].set(str(gSize * 2))
scoreDisplay[+1].set(str(gSize * 2))
scorePlayer = {-1: [0 for i in range(gSize * 2 +1)], 1: [0 for i in range(gSize * 2 +1)]}
turn = StringVar()
turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))

selectedPlayer = -1
highlightStuck = False
nothingHappened = 0

cpu = False

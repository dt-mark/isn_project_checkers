from tkinter import *

from constants import *
import optionvars

window = Tk()

b = [[0 for i in range(gSize + 1)] for j in range(gSize + 1)]
c = [['' for i in range(gSize + 1)] for j in range(gSize + 1)]

player = -1
selectedPlayer = -1
players = [[-1 for i in range(gSize + 1)] for j in range(gSize + 1)]

onePlayerCanEat = {-1: [(-1, -1)], 1: [(-1, -1)]}
onePlayerCanMove = {-1: [(-1, -1)], 1: [(-1, -1)]}

scoreDisplay = {-1: StringVar(), 1: StringVar()}
scoreDisplay[-1].set(str(gSize * 2))
scoreDisplay[+1].set(str(gSize * 2))

scorePlayer = {-1: [0 for i in range(gSize * 2 +1)], 1: [0 for i in range(gSize * 2 +1)]}

turn = StringVar()
turn.set("c'est au joueur {0} de jouer".format("BLANC" if player == -1 else "NOIR"))

highlightStuck = False
nothingHappened = 0

aiState = None
if (optionvars.humanPlayer == player or optionvars.ai == 0): aiState = True
aiCoords = (0, 0)
aiInCombo = 0
gameEnd = False

winner = IntVar()
winner.set(-1)

moves = {-1: IntVar(), 1: IntVar()}
moves[-1].set(0)
moves[+1].set(0)
globalTime = IntVar()
globalTime.set(0)

restart = IntVar()
restart.set(0)

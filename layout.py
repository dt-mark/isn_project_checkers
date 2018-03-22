from tkinter import *
from tkinter import ttk
from math import *
from collections import OrderedDict
import os

from constants import *
from globalvars import *
from functions import *
from filehandling import *
import optionvars

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------BUTTON--------------------------------------------------------"""
class Button:
    def __init__(self, frame, text="", func=lambda:None, size=0, animationType=0, font=mainFont, tag="", \
                 colour=colour["blackPlayer"]):
        self.disabled = False
        self.animationType = animationType
        self.refreshRate = 10
        self.text, self.size, self.func = text, size, func
        extraSpace = 3 if animationType == 0 else 1
        self.ww, self.hh = (len(self.text) + extraSpace) * size, 1.85 * size
        self.canvas = Canvas(frame, width=self.ww, height=self.hh - 3)
        self.canvas.label = self.canvas.create_text(self.ww / 2, self.hh / 2, text=self.text)
        self.canvas.arrowSpace = 0
        self.canvas.colourA, self.canvas.colourT = 1, 0.5
        self.canvas.font, self.canvas.tag, self.canvas.colour = font, tag, colour
        self.canvas.size, self.canvas.aimedSize = self.size, self.size
        self.canvas.style = (self.canvas.font, self.canvas.size, self.canvas.tag)
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.bind("<1>", lambda event, func=self.func, anim=self.animationType: self.buttonPress(event, func, anim))
        self.canvas.bind("<Enter>", lambda event, t=+1, anim=self.animationType: self.buttonMouse(event, t, anim))
        self.canvas.bind("<Leave>", lambda event, t=-1, anim=self.animationType: self.buttonMouse(event, t, anim))
        ax1, ax2 = self.ww / 2 + (len(self.text) / 2) * self.size, self.ww / 2 - (len(self.text) / 2) * self.size
        self.arrow1 = self.canvas.create_polygon(ax1 + 10, self.hh / 2, ax1, 0 + 5, ax1, self.hh - 5, fill="white",
                                                 width=2)
        self.arrow2 = self.canvas.create_polygon(ax2 - 10, self.hh / 2, ax2, 0 + 5, ax2, self.hh - 5, fill="white",
                                                 width=2)
        self.counter = 0
        self.update()
    def buttonMouse(self, event, enterOrLeave, anim):
        self.counter = 0
        caller = self.canvas
        if anim == 0:
            caller.colourA = clamp(-enterOrLeave, 0, 1)
        if anim == 1:
            caller.aimedSize = self.size + 5 * clamp(enterOrLeave, 0, 1)
            caller.colourT = (1 - self.size / caller.size) + 0.25
            if enterOrLeave == -1: caller.colourT = 0.5
    def buttonPress(self, event, func, anim):
        self.counter = 0
        if self.disabled:
            return
        caller = self.canvas
        if anim == 0:
            caller.size += 4
            caller.arrowSpace = 1
        if anim == 1:
            caller.size -= 4
        #Sound(sound["click"])
        func(event)
    def update(self):
        self.counter += 1
        if self.disabled:
            self.canvas.itemconfig(self.canvas.label, \
                                   fill=mergeColour(RGBToHex((0, 0, 0)), RGBToHex((255, 255, 255)), 0.75))
            return
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
            RGBcolourT = mergeColour(self.canvas.colour, RGBToHex((255, 255, 255)), self.canvas.colourT)
            self.canvas.itemconfig(self.canvas.label, fill=RGBcolourT)
            self.canvas.size = lerp(self.canvas.size, self.canvas.aimedSize, 0.2)
        self.canvas.style = (self.canvas.font, int(self.canvas.size), self.canvas.tag)
        if self.counter <= 100: self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.after(self.refreshRate, self.update)

"""-----------------------------------------------------POPUP--------------------------------------------------------"""
class Popup:
    def __init__(self, text="", subtext="", textOption1="", textOption2="", funcOption1=-1, funcOption2=-1, \
                 twoPlayers=False, type=0):
        self.text, self.subtext, self.tO1, self.tO2 = text, subtext, textOption1, textOption2
        if type == 2: self.text = self.text.upper()
        self.O1, self.O2 = funcOption1, funcOption2
        assignFunction = lambda a: ((lambda event: self.cancelPopup(event)) if a == -1 \
                                        else (lambda event: self.acceptPopup(event, a)))
        self.O1, self.O2 = assignFunction(self.O1), assignFunction(self.O2)
        self.top = Toplevel()
        self.canvas = Canvas(self.top, bd=0, highlightthickness=0, selectborderwidth=0)
        self.label = Label(self.canvas, text=self.text, font=(mainFont, 20, "bold"), fg=colour["black"])
        self.label.grid(row=0, column=0, columnspan=2)
        self.sublabel = Label(self.canvas, text=self.subtext, font=(mainFont, 15), fg=colour["blackPlayer"])
        if self.subtext != "": self.sublabel.grid(row=1, column=0, columnspan=2)
        else: self.canvas.grid_rowconfigure(1, minsize=15*2)
        if type == 0:
            self.button1 = Button(self.canvas, text=self.tO1, func=self.O1, size=15, animationType=1)
            self.button2 = Button(self.canvas, text=self.tO2, func=self.O2, size=15, animationType=1)
            self.button1.canvas.grid(row=2, column=0)
            self.button2.canvas.grid(row=2, column=1)
        elif type == 1:
            self.subsubtext = "\nVeuillez entrer vo{0} nom{1} ci-dessous:". format("s" if twoPlayers else "tre", \
                                                                                     "s" if twoPlayers else "")
            self.subsublabel = Label(self.canvas, text=self.subsubtext, font=(mainFont, 12), fg=colour["blackPlayer"])
            self.subsublabel.grid(row=2, column=0, columnspan=2)
            entryTextColour = mergeColour(colour["whitePlayer"], colour["blackPlayer"], 0.4)
            entryHighlightBgColour = mergeColour(colour["whitePlayer"], colour["white"], 0.6)
            entryHighlightFgColour = mergeColour(colour["whitePlayer"], colour["black"], 0.6)
            entry1Text = "nom du joueur {0}". format("blanc" if twoPlayers else "")
            self.entry1 = Entry(self.canvas, font=(mainFont, 10), fg=entryTextColour, justify=CENTER, relief=FLAT, \
                                selectbackground=entryHighlightBgColour, selectforeground=entryHighlightFgColour)
            self.entry1.insert(0, entry1Text)
            self.entry1.bind("<FocusIn>", lambda event, t=entry1Text: self.entryFocusIn(event, t))
            self.entry1.bind("<FocusOut>", lambda event, t=entry1Text: self.entryFocusOut(event, t))
            self.entry1.grid(row=3, column=0, columnspan=2)
            if twoPlayers:
                entry2Text = "nom du joueur noir"
                self.entry2 = Entry(self.canvas, font=(mainFont, 10), fg=entryTextColour, justify=CENTER, relief=FLAT, \
                                    selectbackground=entryHighlightBgColour, selectforeground=entryHighlightFgColour)
                self.entry2.insert(0, entry2Text)
                self.entry2.bind("<FocusIn>", lambda event, t=entry2Text: self.entryFocusIn(event, t))
                self.entry2.bind("<FocusOut>", lambda event, t=entry2Text: self.entryFocusOut(event, t))
                self.entry2.grid(row=4, column=0, columnspan=2)
            okFunction = lambda event, g=gameSaveName: self.acceptPopup(event, g)
            self.canvas.grid_rowconfigure(5, minsize=15)
            self.button = Button(self.canvas, text="OK", func=okFunction, size=15, animationType=1)
            self.button.canvas.grid(row=6, column=0, columnspan=2)
        elif type == 2:
            stats = readFile("stats", emptyStats)
            columnSize, frameSize = 300, 475
            beginningCanvas, middleCanvas = 60, 260
            lineWidth = 3
            self.canvas.grid_columnconfigure(0, minsize=columnSize)
            self.canvas.grid_columnconfigure(1, minsize=columnSize)
            self.canvas.create_line(lineWidth/2, beginningCanvas, \
                                    2*columnSize-lineWidth//2, beginningCanvas, \
                                    2*columnSize-lineWidth//2, frameSize, \
                                    lineWidth/2, frameSize, \
                                    lineWidth / 2, beginningCanvas, \
                                    width=1.5)
            self.canvas.create_line(lineWidth/2, middleCanvas, \
                                    2*columnSize-lineWidth//2, middleCanvas, \
                                    width=1.5)
            self.canvas.create_line(columnSize, beginningCanvas, \
                                    columnSize, middleCanvas, \
                                    width=1.5)
            resultsPieItems = [("victoires", stats[text]["wins"], colour["green"]), \
                               ("pertes", stats[text]["losses"], colour["blue"]), stats[text]["games"]]
            self.resultsPie = PieChart(self.canvas, items=resultsPieItems)
            self.resultsPie.canvas.grid(row=2, column=0, columnspan=1)
            modesPieItems = [("contre l'ia", stats[text]["ai"], colour["green"]), \
                             ("contre l'humain", stats[text]["notai"], colour["blue"]), stats[text]["games"]]
            self.modesPie = PieChart(self.canvas, items=modesPieItems)
            self.modesPie.canvas.grid(row=2, column=1, columnspan=1)
            self.canvas.grid_rowconfigure(3, minsize=50)
            self.frame = Frame(self.canvas)
            extraLabel = lambda text, label: Label(self.frame, text=text, font=(mainFont, 12, ("bold" if not label else "")), \
                                                  fg=(colour["black"] if label else "black"))
            extraLabel("Nombre de parties jouées: ", 1).grid(row=1, column=0, columnspan=2, sticky=E)
            extraLabel(str(stats[text]["games"]), 0).grid(row=1, column=2, columnspan=1, sticky=W)
            extraLabel("Couleur préférée: ", 1).grid(row=2, column=0, columnspan=2, sticky=E)
            extraLabel(("blanc" if stats[text]["col"] <= 0 else "noir"), 0).grid(row=2, column=2, columnspan=1, sticky=W)
            extraLabel("Difficulté la plus jouée: ", 1).grid(row=3, column=0, columnspan=2, sticky=E)
            extraLabel(str(int(stats[text]["diff"]/stats[text]["games"])), 0).grid(row=3, column=2, columnspan=1, sticky=W)
            extraLabel("Nombre total de mouvements: ", 1).grid(row=4, column=0, columnspan=2, sticky=E)
            extraLabel(str(stats[text]["moves"]), 0).grid(row=4, column=2, columnspan=1, sticky=W)
            extraLabel("Nombre total de captures: ", 1).grid(row=5, column=0, columnspan=2, sticky=E)
            extraLabel(str(stats[text]["eats"]), 0).grid(row=5, column=2, columnspan=1, sticky=W)
            extraLabel("Temps total de jeu: ", 1).grid(row=6, column=0, columnspan=2, sticky=E)
            extraLabel(str(stats[text]["time"]), 0).grid(row=6, column=2, columnspan=1, sticky=W)
            self.frame.grid(row=4, column=0, columnspan=2)
            self.canvas.grid_rowconfigure(6, minsize=50)
            okFunction = lambda event, f=nothing: self.acceptPopup(event, f)
            self.button = Button(self.canvas, text="OK", func=okFunction, size=20, animationType=1)
            self.button.canvas.grid(row=7, column=0, columnspan=2)
        self.canvas.pack(padx=15, pady=15, fill="both")
        self.top.resizable(width=False, height=False)
        self.top.transient(window)
        self.top.grab_set()
        center(self.top, window)
    def cancelPopup(self, event):
        self.top.destroy()
        del self
    def acceptPopup(self, event, func):
        func(event)
        if func != menuQuit:
            self.cancelPopup(event)
    def entryFocusIn(self, event, defaultText):
        if event.widget.get() == defaultText:
            event.widget.delete(0, END)
    def entryFocusOut(self, event, defaultText):
        if event.widget.get() == "":
            event.widget.insert(0, defaultText)

"""-----------------------------------------------------APERCU-------------------------------------------------------"""
class BoardPreview:
    def __init__(self, frame):
        self.frame = Frame(frame, borderwidth=3, bg="black")
        self.g = [[0 for i in range(gSize + 1)] for j in range(gSize + 1)]
        self.p = [[0 for i in range(gSize + 1)] for j in range(gSize + 1)]
        for i in range(gSize+1):
            for j in range(gSize+1):
                self.g[i][j] = Canvas(self.frame, width=18, height=18, bd=0, highlightthickness=0)
                self.g[i][j].grid(row=i, column=j)

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
        self.rec1 = self.canvas.create_rectangle(self.scoreBoardBorder, \
                                                 self.scoreBoardBorder, \
                                                 self.scoreBoardSize[0] / 2 - self.halfScoreBoardBorder, \
                                                 self.scoreBoardSize[1] - self.halfScoreBoardBorder, \
                                                 fill=colour["white"])
        self.rec2 = self.canvas.create_rectangle(self.halfScoreBoardSize + self.halfScoreBoardBorder / 2, \
                                     self.scoreBoardBorder, \
                                     self.scoreBoardSize[0] - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["black"])
        self.rec3 = self.canvas.create_rectangle(self.scoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.halfScoreBoardBorder / 2, \
                                     self.halfScoreBoardSize - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.underScoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["black"])
        self.rec4 = self.canvas.create_rectangle(self.halfScoreBoardSize + self.halfScoreBoardBorder / 2, \
                                     self.scoreBoardSize[1] + self.halfScoreBoardBorder / 2, \
                                     self.underScoreBoardSize[0] - self.halfScoreBoardBorder, \
                                     self.scoreBoardSize[1] + self.underScoreBoardSize[1] - self.halfScoreBoardBorder, \
                                     fill=colour["white"])
        self.playerScoreSize = 60
        self.playerScoreOffset = (self.halfScoreBoardSize - self.playerScoreSize * 2) / 2 + self.playerScoreSize / 6
        self.blackPlayerScore = Label(self.canvas, textvariable=scoreDisplay[-1], \
                                      font=(mainFont, self.playerScoreSize, "bold"), \
                                      fg=colour["blackPlayer"], bg=colour["white"])
        self.blackPlayerScore.place(x=self.playerScoreOffset, \
                                    y=(self.scoreBoardSize[1] - self.playerScoreSize) / 4)
        self.whitePlayerScore = Label(self.canvas, textvariable=scoreDisplay[1], \
                                      font=(mainFont, self.playerScoreSize, "bold"), \
                                      fg=colour["whitePlayer"], bg=colour["black"])
        self.whitePlayerScore.place(x=self.halfScoreBoardSize + self.playerScoreOffset, \
                                    y=(self.scoreBoardSize[1] - self.playerScoreSize) / 4)

"""---------------------------------------------------DIAGRAMME------------------------------------------------------"""
class PieChart:
    def __init__(self, frame, items={}, size=100):
        self.items, self.size = items, size
        xOffset, yOffset = 80, 60
        self.canvas = Canvas(frame, width=self.size+xOffset, height=self.size+yOffset)
        self.pieCanvas = Canvas(self.canvas, width=self.size, height=self.size)
        elementSum = self.items[len(self.items)-1]
        del self.items[len(self.items)-1]
        self.rawPercentage = {}
        self.colour = {}
        stepNumbersCumulation = 90
        for element in range(len(self.items)):
                self.rawPercentage[element] = self.items[element][1]/elementSum
                stepNumbers = self.rawPercentage[element] * 360
                self.colour[element] = self.items[element][2]
                if stepNumbers < 360 and stepNumbers > 0:
                    self.pieCanvas.create_arc(2, 2, self.size, self.size, \
                                              start=stepNumbersCumulation, extent=stepNumbers,\
                                              fill=self.colour[element], width=5, outline="white")
                elif stepNumbers == 360:
                    self.pieCanvas.create_oval(2, 2, self.size, self.size, \
                                               fill=self.colour[element], width=5, outline="white")
                    self.pieCanvas.create_line(self.size/2, self.size/2, self.size/2, 0, width=5, fill="white")
                stepNumbersCumulation += stepNumbers
        self.pieCanvas.place(x=xOffset/2, y=yOffset/2)
        if len(self.items) == 2:
            side = 0
            for element in range(len(self.items)):
                around = lambda side, mainStr, smallStr: smallStr*(side)+mainStr+smallStr*(not side)
                elementTextX = (xOffset/2-xOffset/4+2) + (xOffset/4+self.size+xOffset/4)*side
                self.canvas.create_text(elementTextX, (self.size+yOffset)/2, \
                                        text=around(side, intToString(int(self.rawPercentage[element]*100)) \
                                                    + ("0" if self.rawPercentage[element] == 0 else ""), "%"), \
                                        font=(mainFont, 12, "bold"), fill=self.colour[element])
                elementTextY = (yOffset/2-yOffset/4+2) + (yOffset/4+self.size+yOffset/4)*side
                self.canvas.create_text((self.size+xOffset)/2, elementTextY, \
                                        text=str(self.items[element][1]) + " " + self.items[element][0].upper(),
                                        font=(mainFont, 12, "bold"), fill=self.colour[element])
                side += 1

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FONCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""------------------------------------------------BOUTONS-DU-MENU---------------------------------------------------"""
def menuPlay(event):
    layoutCreate(gameFrame)
def menuOptions(event):
    layoutCreate(optionsFrame)
def menuStats(event):
    layoutCreate(statsFrame)
def menuQuitPopup(event):
    Popup(text="Voulez-vous quitter?", \
          textOption1="Oui", textOption2="Non", funcOption1=menuQuit, funcOption2=-1)
def menuQuit(event):
    closeWindow(window)

"""------------------------------------------------BOUTONS-DU-JEU----------------------------------------------------"""
def gameRestartPopup(event):
    Popup(text="Voulez-vous redémarrer?", \
          textOption1="Oui", textOption2="Non", funcOption1=gameRestart, funcOption2=-1)
def gameQuitPopup(event):
    Popup(text="Voulez-vous quitter?", subtext="Vous perdrez la progression de la partie! \n", \
          textOption1="Oui", textOption2="Non", funcOption1=gameQuit, funcOption2=-1)
def gameRestart(event):
    resetCaseColour()
    reset()
def gameQuit(event):
    reset()
    layoutCreate(menuFrame)
def gameCancel(event):
    global winner
    print("gameCancel")
    #Debug
    if optionvars.ai == 1:
        endStr = "{0} gagné\n{1} perdu".format("Vous avez" if winner.get() == optionvars.humanPlayer else "La machine a", \
                                               "La machine a" if winner.get() == optionvars.humanPlayer else "Vous avez",)
    else:
        endStr = "Le joueur {0} a gagné\nLe joueur {1} a perdu".format("BLANC" if winner.get() == -1 else "NOIR", \
                                                                       "NOIR" if winner.get() == -1 else "BLANC")
    Popup(text="La partie est terminée!", subtext=endStr, twoPlayers=optionvars.ai==0, type=1)
def gameSaveName(event):
    global winner
    names = []
    caller = event.widget
    canvasName = caller.winfo_parent()
    canvas = caller._nametowidget(canvasName)
    for i in canvas.winfo_children():
        if i.winfo_class() == "Entry":
            names.append(i.get())
    for i, n in enumerate(names):
        cWinner = clamp(winner.get(), 0, 1)
        _wins = 1 if i == cWinner else 0
        _losses = 0 if i == cWinner else 1
        _col = -1 if i == 0 else 1
        _moves = int(moves[i - (i==0)].get())
        _eats = int(scoreDisplay[i - (i==0)].get())
        _time = time.get()
        configStats(file=readFile("stats", emptyStats), name=n.lower(), games=1, wins=_wins, losses=_losses, \
                    ai=optionvars.ai, notai=1-optionvars.ai, diff=optionvars.difficulty, col=_col, \
                    moves=_moves, eats=_eats, time=_time)

"""----------------------------------------------BOUTONS-DES-OPTIONS-------------------------------------------------"""
def optionsMode(event, value):
    optionvars.ai = value
    updateOptionsButtons()
def optionsPlayer(event, value):
    optionvars.humanPlayer = value
    updateOptionsButtons()
def optionsDifficulty(event, value):
    optionvars.difficulty = value
    updateOptionsButtons()
def optionsGrid(event, value):
    optionvars.gColours = value
    colour["white"] = colour["white"+str(optionvars.gColours)]
    colour["black"] = colour["black" + str(optionvars.gColours)]
    updateOptionsButtons()
    resetCaseColour()
    scoreBoardUpdateColours(gameScoreBoard)
def optionsStats(event):
    Popup(text="Êtes-vous sûrs de vouloir\nsupprimer les données?", \
          textOption1="Oui", textOption2="Non", funcOption1=deleteStats, funcOption2=-1)
    updateOptionsButtons()
def deleteStats(event):
    os.remove("stats.pkl")

"""-----------------------------------------------BOUTONS-DES-STATS--------------------------------------------------"""
def statsMore(event, name):
    Popup(text=name, type=2)

"""------------------------------------------------BOUTONS-DIVERS----------------------------------------------------"""
def info(event):
    webbrowser.open(os.path.abspath("_instructions.pdf"))
def back(event):
    layoutCreate(menuFrame)
def nothing(event):
    return

"""---------------------------------------------CRÉATION-DESTRUCTION-------------------------------------------------"""
def layoutCreate(frame):
    global options
    frame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)
    layoutDelete(allBut=frame)
    global currentFrame
    currentFrame = frame
    if currentFrame == gameFrame:
        gameRestart(0)
        backIcon.canvas.place_forget()
    if currentFrame == optionsFrame:
        options = readFile("options", emptyOptions)
        updateOptionsButtons()
        backIcon.canvas.place(relx=0, x=20, y=20, anchor=NW)
    if currentFrame == statsFrame:
        updateStatsValues()
        backIcon.canvas.place(relx=0, x=20, y=20, anchor=NW)
    if currentFrame == menuFrame:
        backIcon.canvas.place_forget()
def layoutDelete(frame=None, allBut=None):
    if frame != None:
        frame.pack_forget()
    if allBut != None:
        global mainFrames
        for i in mainFrames:
            if i != allBut:
                i.pack_forget()

"""-----------------------------------------------AUTRES-FONCTIONS---------------------------------------------------"""
h = lambda n: " " + "-" * n + " "
def updateOptionsButtons():
    global options
    options["ai"] = optionvars.ai
    options["humanPlayer"] = optionvars.humanPlayer
    options["difficulty"] = optionvars.difficulty
    options["gColours"] = optionvars.gColours
    saveObj(options, "options")
    col = lambda condition: colour["green"] if condition else colour["blackPlayer"]
    optionsModeChoice[0].canvas.colour = col(optionvars.ai == 1)
    optionsModeChoice[1].canvas.colour = col(optionvars.ai == 0)
    optionsPlayerChoice[0].canvas.colour = col(optionvars.humanPlayer == -1)
    optionsPlayerChoice[1].canvas.colour = col(optionvars.humanPlayer == 1)
    for i in range(6):
        optionsDifficultyChoice[i].canvas.colour = col(optionvars.difficulty == i)
    for i in range(5):
        optionsGridChoice[i].canvas.colour = col(optionvars.gColours == i)
    for i in optionsTable.find_withtag("text"):
        optionsTable.itemconfig(i, fill=colour["black"])
    for i in range(gSize + 1):
        for j in range(gSize + 1):
            if case(i, j): optionsPreviewChoice1.g[i][j].configure(bg=colour["black"])
            else: optionsPreviewChoice1.g[i][j].configure(bg=colour["white"])
def updateStatsValues():
    noStatsValues()
    stats = readFile("stats", emptyStats)
    tempSortedStats = {}
    for i in stats.keys():
        if i != "": tempSortedStats[i] = (stats[i]["wins"], stats[i]["games"])
    #t[0] contient un tuple avec le nombre de victoires et le nombre de jeux
    tempSortedStats = OrderedDict(sorted(tempSortedStats.items(), reverse=True, key=lambda t: (t[1][0], t[1][0]/t[1][1])))
    sortedStats = {}
    rowNumber = 0
    if stats != emptyStats:
        for i in tempSortedStats.keys():
            sortedStats[i] = OrderedDict(stats[i])
            if i != "":
                statsNames[rowNumber] = Label(statsTableFrameC, text=cutString(i.upper(), 18), font=(mainFont, 15))
                statsRanks[rowNumber] = Label(statsTableFrameC, text=str(rowNumber + 1), font=(mainFont, 15))
                statsGames[rowNumber] = Label(statsTableFrameC, text=sortedStats[i]["games"], font=(mainFont, 15))
                statsWins[rowNumber] = Label(statsTableFrameC, text=sortedStats[i]["wins"], font=(mainFont, 15))
                statsLosses[rowNumber] = Label(statsTableFrameC, text=sortedStats[i]["losses"], font=(mainFont, 15))
                if sortedStats[i]["games"] != 0:
                    winPercentage[rowNumber] = str(int((sortedStats[i]["wins"] / sortedStats[i]["games"]) * 100)) + "%"
                    lossPercentage[rowNumber] = str(int((sortedStats[i]["losses"] / sortedStats[i]["games"]) * 100)) + "%"
                else:
                    winPercentage[rowNumber] = "0%"
                    lossPercentage[rowNumber] = "0%"
                statsWinsP[rowNumber] = Label(statsTableFrameC, text=winPercentage[rowNumber], font=(mainFont, 15))
                statsLossesP[rowNumber] = Label(statsTableFrameC, text=lossPercentage[rowNumber], font=(mainFont, 15))
                buttonXOffset[rowNumber] = listSum(statsTableSize,0,4)-statsTableHardCodedValues[4]+statsTableSize[5]/2-20
                buttonYOffset[rowNumber] = (2 * rowNumber + 1) * (statsTableEntryHeight / 2) - 20
                moreFunc = lambda event, n=i: statsMore(event, n)
                moreButton[rowNumber] = Button(statsTableFrame, text=">", func=moreFunc, size=20, animationType=1)
                statsNames[rowNumber].grid(row=rowNumber, column=0)
                statsRanks[rowNumber].grid(row=rowNumber, column=1)
                statsGames[rowNumber].grid(row=rowNumber, column=2)
                statsWins[rowNumber].grid(row=rowNumber, column=3)
                statsWinsP[rowNumber].grid(row=rowNumber, column=4)
                statsLosses[rowNumber].grid(row=rowNumber, column=5)
                statsLossesP[rowNumber].grid(row=rowNumber, column=6)
                moreButton[rowNumber].canvas.place(x=buttonXOffset[rowNumber], y=buttonYOffset[rowNumber])
                rowNumber += 1
def noStatsValues():
    for row in range(len(statsNames)):
        if statsNames[row] != "": statsNames[row].configure(text="")
        if statsRanks[row] != "": statsRanks[row].configure(text="")
        if statsGames[row] != "": statsGames[row].configure(text="")
        if statsWins[row] != "": statsWins[row].configure(text="")
        if statsWinsP[row] != "": statsWinsP[row].configure(text="")
        if statsLosses[row] != "": statsLosses[row].configure(text="")
        if statsLossesP[row] != "": statsLossesP[row].configure(text="")
        if moreButton[row] != "": moreButton[row].canvas.place_forget()

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------LAYOUT--------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""--------------------------------------------------MAIN-FRAMES-----------------------------------------------------"""
"""Jeu"""
gameFrame = Frame(window, width=globalWidth, height=globalHeight)
gameFrame.grid_propagate(False)
"""Menu"""
menuFrame = Frame(window, width=globalWidth, height=globalHeight)
menuFrame.grid_propagate(False)
"""Options"""
optionsFrame = Frame(window, width=globalWidth, height=globalHeight)
optionsFrame.grid_propagate(False)
"""Statistiques"""
statsFrame = Frame(window, width=globalWidth, height=globalHeight)
statsFrame.grid_propagate(False)
"""Tout"""
currentFrame = 0
mainFrames = [gameFrame, menuFrame, optionsFrame, statsFrame]
def getCurrentFrame(): return currentFrame

"""-----------------------------------------------------MENU---------------------------------------------------------"""
"""Espace Vide"""
menuFrame.grid_rowconfigure(0, minsize=80)
menuFrame.grid_columnconfigure(0, minsize=globalWidth)
"""Logo"""
menuLogo = Label(menuFrame, text="LE JEU DE DAMES", font=(mainFont, 70))
menuLogo.grid(row=1)
"""Espace Vide"""
menuFrame.grid_rowconfigure(2, minsize=50)
"""Boutons"""
menuPlayButton = Button(menuFrame, text="JOUER", func=menuPlay, size=20, animationType=1)
menuPlayButton.canvas.grid(row=3)
menuOptionsButton = Button(menuFrame, text="PARAMÈTRES", func=menuOptions, size=20, animationType=1)
menuOptionsButton.canvas.grid(row=4)
menuStatsButton = Button(menuFrame, text="STATISTIQUES", func=menuStats, size=20, animationType=1)
menuStatsButton.canvas.grid(row=5)
menuQuitButton = Button(menuFrame, text="QUITTER", func=menuQuitPopup, size=20, animationType=1)
menuQuitButton.canvas.grid(row=6)

"""-----------------------------------------------------GAME---------------------------------------------------------"""
"""Frames Secondaires"""
gameSideFrame1 = Frame(gameFrame)
gameSideFrame1.grid(row=1, column=0, sticky="E")
gameSideFrame2 = Frame(gameFrame)
gameSideFrame2.grid(row=1, column=1, sticky="W")
"""Titre"""
gameTitle = Label(gameSideFrame1, text="LE JEU DE DAMES", font=(mainFont, 25), height=1)
gameTitle.grid(row=0, column=0)
"""Planche de jeu"""
gameBoard = Frame(gameSideFrame1, borderwidth=5, bg="black")
gameBoard.grid(row=1, column=0)
#Board(gameBoard, gSize, bSize)
"""Texte indiquant quel joueur doit jouer"""
gameTurnText = Label(gameSideFrame1, textvariable=turn, font=(mainFont, 15))
#gameTurnText.grid(row=2, column=0)
gameSideFrame1.grid_rowconfigure(2, minsize=15*2)
"""Planche de score"""
gameScoreBoard = ScoreBoard(gameSideFrame2, (300, 150), (300, 100), 6)
gameScoreBoard.canvas.grid(row=0, column=0)
"""Espace Vide"""
gameSideFrame2.grid_rowconfigure(1, minsize=30)
gameSideFrame2.grid_columnconfigure(0, minsize=400)
"""Boutons"""
gameCancelText = Button(gameSideFrame2, text="ANNULER", func=gameCancel, size=15)
gameCancelText.canvas.grid(row=2, column=0)
gameRestartText = Button(gameSideFrame2, text="REDEMARRER", func=gameRestartPopup, size=15)
gameRestartText.canvas.grid(row=3, column=0)
gameQuitText = Button(gameSideFrame2, text="QUITTER", func=gameQuitPopup, size=15)
gameQuitText.canvas.grid(row=4, column=0)
"""Espace Vide"""
gameSideFrame2.grid_rowconfigure(5, minsize=30)

"""---------------------------------------------------OPTIONS--------------------------------------------------------"""
"""Variables"""
optionsTableLineWidth = 3
optionsHeaderSize = 50
optionsHeaderDistance = 25
optionsLabelSpace = 40
optionsButtonSpace = 80
tableHeight = globalHeight-2*optionsHeaderSize
"""Frames Secondaires"""
optionsTopFrame = Frame(optionsFrame)
optionsTopFrame.grid(row=0)
optionsFrame.grid_rowconfigure(0, minsize=optionsHeaderSize)
optionsFrame.grid_rowconfigure(1, minsize=optionsHeaderDistance)
optionsTable = Canvas(optionsFrame, width=globalWidth, height=tableHeight)
optionsTable.grid(row=2)
"""Titre"""
optionsTitle = Label(optionsTopFrame, text="PARAMÈTRES", font=(mainFont, 25), height=1)
optionsTitle.grid(column=0)
optionsTopFrame.grid_columnconfigure(1, minsize=int(globalWidth/2))
"""Lignes du Tableau"""
optionsTable.create_line(optionsTableLineWidth/2, optionsTableLineWidth/2, \
                         globalWidth-optionsTableLineWidth/2, optionsTableLineWidth/2, \
                         globalWidth-optionsTableLineWidth/2, tableHeight+optionsTableLineWidth//2, \
                         optionsTableLineWidth/2, tableHeight+optionsTableLineWidth//2, \
                         optionsTableLineWidth/2, optionsTableLineWidth/2, \
                         width=optionsTableLineWidth)
optionsTable.create_line(globalWidth/2+optionsTableLineWidth/2, optionsTableLineWidth/2, \
                         globalWidth/2+optionsTableLineWidth/2, tableHeight+optionsTableLineWidth//2, \
                         width=optionsTableLineWidth/2)
createLine = lambda xx, yy: optionsTable.create_line(\
                            xx, yy, xx + globalWidth/2, yy, \
                            width=optionsTableLineWidth / 2)
cellHeights = [1*optionsLabelSpace+0*optionsButtonSpace, \
               1*optionsLabelSpace+1*optionsButtonSpace, \
               2*optionsLabelSpace+1*optionsButtonSpace, \
               2*optionsLabelSpace+2*optionsButtonSpace, \
               3*optionsLabelSpace+2*optionsButtonSpace, \
               4*optionsLabelSpace+2*optionsButtonSpace, \
               5*optionsLabelSpace+2*optionsButtonSpace, \
               6*optionsLabelSpace+2*optionsButtonSpace,]
for j, i in enumerate(cellHeights):
    createLine(optionsTableLineWidth/2, i)
    if j <= 2:
        createLine(globalWidth/2+optionsTableLineWidth/2, i)
"""Titres du Tableau"""
optionsTableLabels1 = ["MODE DE JEU", "", "COULEUR DU JETON", "", "DIFFICULTÉ", "", "COULEURS DE LA GRILLE", ""]
optionsTableLabels2 = ["STATISTIQUES", "", "APERÇU", "", "", "", "", ""]
for j, i in enumerate(cellHeights):
    if j%2 == 0: optionsTable.create_text(globalWidth/4, cellHeights[j]-optionsLabelSpace/2, \
                              text=optionsTableLabels1[j], fill=colour["black"], font=(mainFont, 14, "bold"), \
                              width=globalWidth/2, tags="text")
for j, i in enumerate(cellHeights):
    if j%2 == 0: optionsTable.create_text(3*globalWidth/4, cellHeights[j]-optionsLabelSpace/2, \
                              text=optionsTableLabels2[j], fill=colour["black"], font=(mainFont, 14, "bold"), \
                              width=globalWidth/2, tags="text")
"""Frames du Tableau"""
optionsTableFrames1 = [(Frame(window) if j%2 != 0 else 0) for j in range(7+1)]
optionsTableFrames2 = [(Frame(window) if j%2 != 0 else 0) for j in range(7+1)]
for j, i in enumerate(cellHeights):
    if j%2 != 0:
        optionsButtonSpaceHalf = optionsButtonSpace/2 if j <= 3 else optionsLabelSpace/2
        optionsTable.create_window(globalWidth/4, i-optionsButtonSpaceHalf, window=optionsTableFrames1[j])
        if j <= 3:
            optionsButtonSpaceHalf = optionsButtonSpace/2 if j <= 1 else -optionsLabelSpace
            optionsTable.create_window(3*globalWidth/4, i-optionsButtonSpaceHalf, window=optionsTableFrames2[j])
"""Contenu des Frames"""
createButton = lambda frame, text, function, value: Button(frame, text=text, size=15, animationType=1, \
                                                           func=lambda event, v=value: function(event, v))
"""Options Mode de Jeu"""
optionsModeChoice = [0 for i in range(2)]
optionsModeTexts = ["AVEC LA MACHINE", "À DEUX JOUEURS"]
optionsModeValues = [1, 0]
for j in range(2):
    optionsModeChoice[j] = createButton(optionsTableFrames1[1], optionsModeTexts[j], \
                                        optionsMode, optionsModeValues[j])
    optionsModeChoice[j].canvas.grid(row=j, column=0)
"""Options Couleur de son Jeton"""
optionsPlayerChoice = [0 for i in range(2)]
optionsPlayerTexts = ["BLANC", "NOIR"]
optionsPlayerValues = [-1, 1]
for j in range(2):
    optionsPlayerChoice[j] = createButton(optionsTableFrames1[3], optionsPlayerTexts[j], \
                                          optionsPlayer, optionsPlayerValues[j])
    optionsPlayerChoice[j].canvas.grid(row=j, column=0)
"""Options Difficulté"""
optionsDifficultyChoice = [0 for i in range(6)]
optionsDifficultyTexts = [" 0 ", " 1 ", " 2 ", " 3 ", " 4 ", " + "]
for j in range(6):
    optionsDifficultyChoice[j] = createButton(optionsTableFrames1[5], optionsDifficultyTexts[j], optionsDifficulty, j)
    optionsDifficultyChoice[j].canvas.grid(row=0, column=j)
"""Options Esthétiques"""
optionsGridChoice = [0 for i in range(5)]
optionsGridTexts = [" A ", " B ", " C ", " D ", " E "]
for j in range(5):
    optionsGridChoice[j] = createButton(optionsTableFrames1[7], optionsGridTexts[j], optionsGrid, j)
    optionsGridChoice[j].canvas.grid(row=0, column=j)
"""Options Statistiques"""
optionsStatsChoice1=Button(optionsTableFrames2[1],text="SUPPRIMER LES DONNÉES",func=optionsStats,size=15,animationType=1)
optionsStatsChoice1.canvas.grid(row=0)
optionsStatsChoice2=Button(optionsTableFrames2[1],text="",func=nothing,size=15,animationType=1)
optionsStatsChoice2.canvas.grid(row=1)
"""Aperçu des couleurs"""
optionsPreviewChoice1 = BoardPreview(optionsTableFrames2[3])
optionsPreviewChoice1.frame.grid(row=0)
"""Chargement des paramètres sauvegardés"""
options = readFile("options", emptyOptions)

"""-----------------------------------------------------STATS--------------------------------------------------------"""
"""Variables de taille"""
statsTopFrameHeight = 50
statsTopFrameDistance = 25
statsTopFrameTotalHeight = statsTopFrameHeight + statsTopFrameHeight
statsTableLineWidth = 3
statsTableHeight = globalHeight-statsTopFrameTotalHeight
statsTableHeaderSize = 50
statsTableSize = [0 for i in range(6)]
statsTableSize[0] = 275
statsTableSize[1] = 75
statsTableSize[2] = 100
statsTableSize[3] = 150
statsTableSize[4] = 150
statsTableSize[5] = 50
statsTableHeaders = ["" for i in range(6)]
statsTableHeaders[0] = "NOMS DES JOUEURS"
statsTableHeaders[1] = "TOP"
statsTableHeaders[2] = "PARTIES"
statsTableHeaders[3] = "VICTOIRES"
statsTableHeaders[4] = "DÉFAITES"
statsTableHeaders[5] = "+"
"""Frames Secondaires"""
statsTopFrame = Frame(statsFrame)
statsTopFrame.grid(row=0)
statsFrame.grid_rowconfigure(1, minsize=statsTopFrameDistance)
statsTable = Canvas(statsFrame, width=globalWidth, height=globalHeight-statsTopFrameTotalHeight, bg="white")
statsTable.grid(row=2)
"""Titre"""
statsTitle = Label(statsTopFrame, text="STATISTIQUES", font=(mainFont, 25), height=1)
statsTitle.grid(row=0, column=0)
statsTopFrame.grid_rowconfigure(0, minsize=statsTopFrameHeight)
statsTopFrame.grid_columnconfigure(0, minsize=int(globalWidth/2))
"""Barre de Recherche"""
entryTextColour = mergeColour(colour["whitePlayer"], colour["blackPlayer"], 0.4)
entryHighlightBgColour = mergeColour(colour["whitePlayer"], colour["white"], 0.6)
entryHighlightFgColour = mergeColour(colour["whitePlayer"], colour["black"], 0.6)
statsSearch = Entry(statsTopFrame, font=(mainFont, 15), width=int(globalWidth/30), \
                    highlightbackground=mergeColour(colour["blackPlayer"], colour["whitePlayer"], 0), \
                    background=mergeColour(colour["blackPlayer"], colour["whitePlayer"], 0.92), \
                    highlightthickness=2, relief=FLAT, fg=entryTextColour, \
                    selectbackground=entryHighlightBgColour, selectforeground=entryHighlightFgColour)
statsSearch.grid(row=0, column=1)
statsTopFrame.grid_rowconfigure(0, minsize=statsTopFrameHeight)
statsTopFrame.grid_columnconfigure(1, minsize=int(globalWidth/2))
"""Lignes du Tableau"""
statsTable.create_line(statsTableLineWidth/2, statsTableLineWidth/2, \
                       statsTableLineWidth/2, statsTableHeight-statsTableLineWidth/2+2, \
                       globalWidth-statsTableLineWidth/2, statsTableHeight-statsTableLineWidth/2+2,\
                       globalWidth-statsTableLineWidth/2, statsTableLineWidth/2, \
                       statsTableLineWidth/2, statsTableLineWidth/2, \
                       width=statsTableLineWidth)
statsTable.create_line(0, statsTableHeaderSize, globalWidth, statsTableHeaderSize, \
                       width=statsTableLineWidth/2)
for i in range(6):
    statsTable.create_line(listSum(statsTableSize, 0, i), 0, listSum(statsTableSize, 0, i), statsTableHeaderSize, \
                           width=statsTableLineWidth/2)
"""Titres du Tableau"""
for i in range(6):
    xx = listSum(statsTableSize, 0, i) - statsTableSize[i]/2
    tt = statsTableHeaders[i]
    ww = statsTableSize[i]
    statsTable.create_text(xx, statsTableHeaderSize/2, text=tt, width=ww, \
                           font=(mainFont, 14, "bold"), fill=colour["black"])
"""Canevas Contenant une Frame (pour le contenu du tableau)"""
statsTableHardCodedValues = (3, 1.75, 4, 6, 7, 4.5+1)
statsTableFrameSize = (globalWidth-statsTableHardCodedValues[0]*statsTableLineWidth-1, \
                       statsTableHeight-statsTableHeaderSize-statsTableHardCodedValues[1]*statsTableLineWidth)
statsTableCanvas = Canvas(statsTable, bd=0, width=statsTableFrameSize[0], height=statsTableFrameSize[1])
statsTableFrame = Frame(statsTableCanvas, width=statsTableFrameSize[0], height=statsTableFrameSize[1])
statsTableCanvas.create_window(0, 0, window=statsTableFrame, anchor=NW)
statsTableCanvas.place(x=statsTableLineWidth+1, y=statsTableHeaderSize+1)
"""ScrollBar"""
scrollBarStyle = ttk.Style()
scrollBarStyle.theme_use('clam')
scrollBarStyle.configure("Vertical.TScrollbar", background="white", darkcolor="black", lightcolor="black", \
                         troughcolor="white", bordercolor="white")
yScrollBar = ttk.Scrollbar(statsTableCanvas,orient=VERTICAL,command=statsTableCanvas.yview,style="Vertical.TScrollbar")
statsTableCanvas.configure(yscrollcommand=yScrollBar.set)
yScrollBar.place(x=2, y=0, relheight=1.0)
statsTableCanvas.yview_moveto(0.0)
yScrollSizeChange = lambda event, c=statsTableCanvas: \
                    c.configure(scrollregion=(c.bbox("all")[0], c.bbox("all")[1]+statsTableHardCodedValues[2], \
                                              c.bbox("all")[2], c.bbox("all")[3]-statsTableHardCodedValues[3]))
statsTableFrame.bind("<Configure>", yScrollSizeChange)
statsTableCanvas.configure(scrollregion=(statsTableCanvas.bbox("all")[0], \
                                         statsTableCanvas.bbox("all")[1]+statsTableHardCodedValues[2], \
                                         statsTableCanvas.bbox("all")[2], \
                                         statsTableCanvas.bbox("all")[3]-statsTableHardCodedValues[3]))
"""Contenu de la Frame (donc le contenu du tableau)"""
statsTableEntries = len(readFile("stats", emptyStats).keys())
statsTableEntryHeight = 38
statsTableContentHeight = statsTableEntries * statsTableEntryHeight
while statsTableContentHeight < statsTableFrameSize[1]:
    statsTableEntries += 1
    statsTableContentHeight = statsTableEntries * statsTableEntryHeight
statsTableFrame.configure(height=statsTableContentHeight)
statsTableFrameC = Canvas(statsTableFrame, bd=0, width=listSum(statsTableSize, 0, 4), height=statsTableContentHeight)
statsTableFrameC.place(x=-statsTableHardCodedValues[5], y=0)
for i in range(6):
    statsTableFrameC.create_line(listSum(statsTableSize, 0, i), 0, \
                                 listSum(statsTableSize, 0, i), statsTableContentHeight+1000, \
                                 width=statsTableLineWidth/2)
statsTableFrameC.create_line(listSum(statsTableSize, 0, 2)+statsTableSize[3]/2, 0, \
                             listSum(statsTableSize, 0, 2)+statsTableSize[3]/2, statsTableContentHeight+1000, \
                             width=statsTableLineWidth/2)
statsTableFrameC.create_line(listSum(statsTableSize, 0, 3)+statsTableSize[4]/2, 0, \
                             listSum(statsTableSize, 0, 3)+statsTableSize[4]/2,
                             statsTableContentHeight + 1000, \
                             width=statsTableLineWidth / 2)
for i in range(8):
    if isBetween(i, 0, 2): statsTableFrameC.grid_columnconfigure(i, minsize=statsTableSize[i])
    if isBetween(i, 3, 4): statsTableFrameC.grid_columnconfigure(i, minsize=statsTableSize[3]/2)
    if isBetween(i, 5, 6): statsTableFrameC.grid_columnconfigure(i, minsize=statsTableSize[4]/2)
    if isBetween(i, 7, 7): statsTableFrameC.grid_columnconfigure(i, minsize=statsTableHardCodedValues[4])
for i in range(statsTableEntries):
    statsTableFrameC.grid_rowconfigure(i, minsize=statsTableEntryHeight)
statsNames = ["" for i in range(1000)]
statsRanks = ["" for i in range(1000)]
statsGames = ["" for i in range(1000)]
statsWins = ["" for i in range(1000)]
winPercentage = ["" for i in range(1000)]
statsWinsP = ["" for i in range(1000)]
statsLosses = ["" for i in range(1000)]
lossPercentage = ["" for i in range(1000)]
statsLossesP = ["" for i in range(1000)]
buttonXOffset = [0 for i in range(1000)]
buttonYOffset = [0 for i in range(1000)]
moreButton = ["" for i in range(1000)]
updateStatsValues()

"""-----------------------------------------------------MISC---------------------------------------------------------"""
"""Bouton d'aide"""
infoIcon = Button(window, text="?", func=info, size=20, animationType=1, tag="bold")
infoIcon.canvas.place(relx=1, x=-20, y=20, anchor=NE)
"""Bouton de retour"""
backIcon = Button(window, text="<", func=back, size=20, animationType=1, tag="bold")
backIcon.canvas.place(relx=0, x=20, y=20, anchor=NW)

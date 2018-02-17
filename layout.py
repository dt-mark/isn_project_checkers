from tkinter import *

from constants import *
from globals import *
from functions import *

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------CLASSES-------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------BUTTON--------------------------------------------------------"""
class Button:

    def __init__(self, frame, text="", func=lambda:None, size=0, animationType=0, font=mainFont, tag="", \
                 colour=colour["blackPlayer"]):
        self.animationType = animationType
        self.refreshRate = 10
        self.text, self.size, self.func = text, size, func
        self.ww, self.hh = (len(self.text) + 3) * size, 1.85 * size
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
        self.update()
    def buttonMouse(self, event, enterOrLeave, anim):
        caller = self.canvas
        if anim == 0:
            caller.colourA = clamp(-enterOrLeave, 0, 1)
        if anim == 1:
            caller.aimedSize = self.size + 5 * clamp(enterOrLeave, 0, 1)
            caller.colourT = (1 - self.size / caller.size) + 0.25
            if enterOrLeave == -1: caller.colourT = 0.5
    def buttonPress(self, event, func, anim):
        caller = self.canvas
        if anim == 0:
            caller.size += 4
            caller.arrowSpace = 1
        if anim == 1:
            caller.size -= 4
        #Sound(sound["click"])
        func(event)
    def update(self):
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
        self.canvas.itemconfig(self.canvas.label, font=self.canvas.style)
        self.canvas.after(self.refreshRate, self.update)

"""-----------------------------------------------------POPUP--------------------------------------------------------"""
class Popup:

    def __init__(self, text="", textOption1="", textOption2="", funcOption1=-1, funcOption2=-1):
        self.text, self.tO1, self.tO2 = text, textOption1, textOption2
        self.O1, self.O2 = funcOption1, funcOption2
        assignFunction = lambda a: ((lambda event: self.cancelPopup(event)) if a == -1 \
                                        else (lambda event: self.acceptPopup(event, a)))
        self.O1, self.O2 = assignFunction(self.O1), assignFunction(self.O2)
        self.top = Toplevel()
        self.canvas = Canvas(self.top)
        self.label = Label(self.canvas, text=self.text, font=(mainFont, 20), fg=colour["black"])
        self.button1 = Button(self.canvas, text=self.tO1, func=self.O1, size=15, animationType=1)
        self.button2 = Button(self.canvas, text=self.tO2, func=self.O2, size=15, animationType=1)
        self.label.grid(row=0, column=0, columnspan=2)
        self.button1.canvas.grid(row=1, column=0)
        self.button2.canvas.grid(row=1, column=1)
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
        self.cancelPopup(event)

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

"""------------------------------------------------------------------------------------------------------------------"""
"""---------------------------------------------------FUNCTIONS------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""------------------------------------------------BOUTONS-DU-JEU----------------------------------------------------"""
def gameRestartPopup(event):
    Popup(text="Voulez-vous redémarrer?\n", \
          textOption1="Oui", textOption2="Non", funcOption1=gameRestart, funcOption2=-1)
def gameQuitPopup(event):
    Popup(text="Voulez-vous quitter?\n", \
          textOption1="Oui", textOption2="Non", funcOption1=gameQuit, funcOption2=-1)
def gameRestart(event):
    print("gameRestart")
def gameQuit(event):
    layoutCreate(menuFrame)
def gameCancel(event):
    print("gameCancel")

"""------------------------------------------------BOUTONS-DU-MENU---------------------------------------------------"""
def menuOptions(event):
    layoutCreate(optionsFrame)
def menuStats(event):
    print("menuStats")
def menuQuit(event):
    print("menuQuit")

"""----------------------------------------------BOUTONS-DES-OPTIONS-------------------------------------------------"""
def optionsMode(event, value):
    global ai
    ai = value
    updateOptionsButtons()
def optionsPlayer(event, value):
    global humanPlayer
    humanPlayer = value
    updateOptionsButtons()
def optionsDifficulty(event, value):
    global difficulty
    difficulty = value
    updateOptionsButtons()
def optionsGrid(event, value):
    global gColours
    gColours = value
    if gColours == 0:
        colour["white"] = "#%02X%02X%02X" % (255, 255, 130)
        colour["black"] = "#%02X%02X%02X" % (160, 100, 0)
    elif gColours == 1:
        colour["white"] = "#%02X%02X%02X" % (150, 150, 200)
        colour["black"] = "#%02X%02X%02X" % (50, 50, 200)
    elif gColours == 2:
        colour["white"] = "#%02X%02X%02X" % (65, 225, 10)
        colour["black"] = "#%02X%02X%02X" % (180, 50, 176)
    elif gColours == 3:
        colour["white"] = "#%02X%02X%02X" % (21, 189, 123)
        colour["black"] = "#%02X%02X%02X" % (46, 98, 0)
    elif gColours == 4:
        colour["white"] = "#%02X%02X%02X" % (99, 23, 125)
        colour["black"] = "#%02X%02X%02X" % (0, 16, 0)
    elif gColours == 5:
        colour["white"] = "#%02X%02X%02X" % (180, 180, 180)
        colour["black"] = "#%02X%02X%02X" % (75, 75, 75)
    updateOptionsButtons()
    resetCaseColour()
    scoreBoardUpdateColours(gameScoreBoard)
def optionsStats(event):
    Popup(text="Êtes-vous sûrs de vouloir\nsupprimer les données?\n", \
          textOption1="Oui", textOption2="Non", funcOption1=deleteStats, funcOption2=-1)
    updateOptionsButtons()
def deleteStats(event):
    print("deleteStats")

"""------------------------------------------------BOUTONS-DIVERS----------------------------------------------------"""
def info(event):
    webbrowser.open(os.path.abspath("_instructions.pdf"))
def back(event):
    layoutCreate(menuFrame)

"""---------------------------------------------CRÉATION-DESTRUCTION-------------------------------------------------"""
def layoutCreate(frame):
    frame.pack(padx=windowBorder, pady=windowBorder, fill=BOTH)
    layoutDelete(frame=None, allBut=frame)
    if frame == optionsFrame or frame == statsFrame:
        backIcon.canvas.place(relx=0, x=0, y=20, anchor=NW)
    else:
        backIcon.canvas.place_forget()
    global currentFrame
    currentFrame = frame
    if currentFrame == optionsFrame:
        updateOptionsButtons()

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
    col = lambda condition: colour["green"] if condition else colour["blackPlayer"]
    optionsModeChoice1.canvas.colour = col(ai == 0)
    optionsModeChoice2.canvas.colour = col(ai == 1)
    optionsPlayerChoice1.canvas.colour = col(humanPlayer == -1)
    optionsPlayerChoice2.canvas.colour = col(humanPlayer == 1)
    optionsDifficultyChoice1.canvas.colour = col(difficulty == 0)
    optionsDifficultyChoice2.canvas.colour = col(difficulty == 1)
    optionsDifficultyChoice3.canvas.colour = col(difficulty == 2)
    optionsDifficultyChoice4.canvas.colour = col(difficulty == 3)
    optionsDifficultyChoice5.canvas.colour = col(difficulty == 4)
    optionsDifficultyChoice6.canvas.colour = col(difficulty == 5)
    optionsGridChoice1.canvas.colour = col(gColours == 0)
    optionsGridChoice2.canvas.colour = col(gColours == 1)
    optionsGridChoice3.canvas.colour = col(gColours == 2)
    optionsGridChoice4.canvas.colour = col(gColours == 3)
    optionsGridChoice5.canvas.colour = col(gColours == 4)
    optionsGridChoice6.canvas.colour = col(gColours == 5)
    optionsModeLabel.configure(fg=colour["black"])
    optionsPlayerLabel.configure(fg=colour["black"])
    optionsDifficultyLabel.configure(fg=colour["black"])
    optionsGridLabel.configure(fg=colour["black"])
    optionsStatsLabel.configure(fg=colour["black"])
    optionsPreviewLabel.configure(fg=colour["black"])
    for i in range(gSize + 1):
        for j in range(gSize + 1):
            if case(i, j): optionsPreviewChoice1.g[i][j].configure(bg=colour["black"])
            else: optionsPreviewChoice1.g[i][j].configure(bg=colour["white"])

"""------------------------------------------------------------------------------------------------------------------"""
"""----------------------------------------------------LAYOUT--------------------------------------------------------"""
"""------------------------------------------------------------------------------------------------------------------"""

"""--------------------------------------------------MAIN-FRAMES-----------------------------------------------------"""
currentFrame = 0
gameFrame = Frame(window, width=globalWidth, height=globalHeight)
gameFrame.grid_propagate(False)
menuFrame = Frame(window, width=globalWidth, height=globalHeight)
menuFrame.grid_propagate(False)
optionsFrame = Frame(window, width=globalWidth, height=globalHeight)
optionsFrame.grid_propagate(False)
statsFrame = Frame(window, width=globalWidth, height=globalHeight)
statsFrame.grid_propagate(False)
mainFrames = [gameFrame, menuFrame, optionsFrame, statsFrame]

"""-----------------------------------------------------GAME---------------------------------------------------------"""
gameSideFrame1 = Frame(gameFrame)
gameSideFrame1.grid(row=1, column=0, sticky="E")
gameSideFrame2 = Frame(gameFrame)
gameSideFrame2.grid(row=1, column=1, sticky="W")
gameTitle = Label(gameSideFrame1, text="LE JEU DE DAMES", font=(mainFont, 25), height=1)
gameTitle.grid(row=0, column=0)
gameBoard = Frame(gameSideFrame1, borderwidth=5, bg="black")
gameBoard.grid(row=1, column=0)
#Board(gameBoard, gSize, bSize)
gameTurnText = Label(gameSideFrame1, textvariable=turn, font=(mainFont, 15))
gameTurnText.grid(row=2, column=0)
gameScoreBoard = ScoreBoard(gameSideFrame2, (300, 150), (300, 100), 6)
gameScoreBoard.canvas.grid(row=0, column=0)
gameEmptySpace1 = Canvas(gameSideFrame2, width=400, height=50 / 2)
gameEmptySpace1.grid(row=1, column=0)
gameCancelText = Button(gameSideFrame2, text="ANNULER", func=gameCancel, size=15)
gameCancelText.canvas.grid(row=2, column=0)
gameRestartText = Button(gameSideFrame2, text="REDEMARRER", func=gameRestartPopup, size=15)
gameRestartText.canvas.grid(row=3, column=0)
gameQuitText = Button(gameSideFrame2, text="QUITTER", func=gameQuitPopup, size=15)
gameQuitText.canvas.grid(row=4, column=0)
gameEmptySpace2 = Canvas(gameSideFrame2, width=400, height=50 / 2)
gameEmptySpace2.grid(row=5, column=0)

"""-----------------------------------------------------MENU---------------------------------------------------------"""
menuEmptySpace1 = Canvas(menuFrame, width=globalWidth, height=80)
menuEmptySpace1.grid(row=0)
menuLogo = Label(menuFrame, text="LE JEU DE DAMES", font=(mainFont, 70))
menuLogo.grid(row=1)
menuEmptySpace2 = Canvas(menuFrame, width=globalWidth, height=50)
menuEmptySpace2.grid(row=2)
menuPlayButton = Button(menuFrame, text="JOUER", func=lambda w=window:layoutCreate(gameFrame), size=20, animationType=1)
menuPlayButton.canvas.grid(row=3)
menuOptionsButton = Button(menuFrame, text="OPTIONS", func=menuOptions, size=20, animationType=1)
menuOptionsButton.canvas.grid(row=4)
menuStatsButton = Button(menuFrame, text="STATISTIQUES", func=menuStats, size=20, animationType=1)
menuStatsButton.canvas.grid(row=5)
menuQuitButton = Button(menuFrame, text="QUITTER", func=menuQuit, size=20, animationType=1)
menuQuitButton.canvas.grid(row=6)

"""---------------------------------------------------OPTIONS--------------------------------------------------------"""
optionsSideFrame1 = Frame(optionsFrame, width=int(globalWidth/2), height=globalHeight)
optionsSideFrame1.grid_propagate(False)
optionsSideFrame1.grid(row=0, column=0, sticky="E")
optionsSideFrame2 = Frame(optionsFrame, width=int(globalWidth/2), height=globalHeight)
optionsSideFrame2.grid_propagate(False)
optionsSideFrame2.grid(row=0, column=1, sticky="W")
optionsTitle = Label(optionsSideFrame1, text="PARAMÈTRES", font=(mainFont, 25), height=1)
optionsTitle.grid(row=0, column=0, columnspan=6)
optionsSideFrame1.grid_rowconfigure(1, minsize=30)
optionsModeLabel = Label(optionsSideFrame1, text=h(11)+"Mode de Jeu"+h(11), fg=colour["black"], font=(mainFont, 20))
optionsModeLabel.grid(row=2, column=0, columnspan=6)
optionsModeChoice1 = Button(optionsSideFrame1, text="AVEC LA MACHINE", func=lambda event, v=0: optionsMode(event, v), \
                            size=15, animationType=1)
optionsModeChoice1.canvas.grid(row=3, column=0, columnspan=6)
optionsModeChoice2 = Button(optionsSideFrame1, text="À DEUX JOUEURS", func=lambda event, v=1: optionsMode(event, v), \
                            size=15, animationType=1)
optionsModeChoice2.canvas.grid(row=4, column=0, columnspan=6)
optionsSideFrame1.grid_rowconfigure(5, minsize=15)
optionsPlayerLabel = Label(optionsSideFrame1, text=h(8)+"Couleur du Jeton"+h(8), fg=colour["black"],font=(mainFont, 20))
optionsPlayerLabel.grid(row=6, column=0, columnspan=6)
optionsPlayerChoice1 = Button(optionsSideFrame1, text="BLANC", func=lambda event, v=-1: optionsPlayer(event, v), \
                              size=15, animationType=1)
optionsPlayerChoice1.canvas.grid(row=7, column=0, columnspan=6)
optionsPlayerChoice2 = Button(optionsSideFrame1, text="NOIR", func=lambda event, v=1: optionsPlayer(event, v), \
                              size=15, animationType=1)
optionsPlayerChoice2.canvas.grid(row=8, column=0, columnspan=6)
optionsSideFrame1.grid_rowconfigure(9, minsize=15)
optionsDifficultyLabel = Label(optionsSideFrame1, text=h(12)+"Difficulté"+h(12), fg=colour["black"],font=(mainFont, 20))
optionsDifficultyLabel.grid(row=10, column=0, columnspan=6)
optionsDifficultyChoice1 = Button(optionsSideFrame1, text="0", func=lambda event, v=0: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice1.canvas.grid(row=11, column=0, columnspan=1)
optionsDifficultyChoice2 = Button(optionsSideFrame1, text="1", func=lambda event, v=1: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice2.canvas.grid(row=11, column=1, columnspan=1)
optionsDifficultyChoice3 = Button(optionsSideFrame1, text="2", func=lambda event, v=2: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice3.canvas.grid(row=11, column=2, columnspan=1)
optionsDifficultyChoice4 = Button(optionsSideFrame1, text="3", func=lambda event, v=3: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice4.canvas.grid(row=11, column=3, columnspan=1)
optionsDifficultyChoice5 = Button(optionsSideFrame1, text="4", func=lambda event, v=4: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice5.canvas.grid(row=11, column=4, columnspan=1)
optionsDifficultyChoice6 = Button(optionsSideFrame1, text="+", func=lambda event, v=5: optionsDifficulty(event, v), \
                                  size=15, animationType=1)
optionsDifficultyChoice6.canvas.grid(row=11, column=5, columnspan=1)
optionsSideFrame1.grid_rowconfigure(12, minsize=15)
optionsGridLabel = Label(optionsSideFrame1,text=h(6)+"Couleurs de la Grille"+h(6),fg=colour["black"],font=(mainFont,20))
optionsGridLabel.grid(row=13, column=0, columnspan=6)
optionsGridChoice1 = Button(optionsSideFrame1, text="A", func=lambda event, v=0: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice1.canvas.grid(row=14, column=0, columnspan=1)
optionsGridChoice2 = Button(optionsSideFrame1, text="B", func=lambda event, v=1: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice2.canvas.grid(row=14, column=1, columnspan=1)
optionsGridChoice3 = Button(optionsSideFrame1, text="C", func=lambda event, v=2: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice3.canvas.grid(row=14, column=2, columnspan=1)
optionsGridChoice4 = Button(optionsSideFrame1, text="D", func=lambda event, v=3: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice4.canvas.grid(row=14, column=3, columnspan=1)
optionsGridChoice5 = Button(optionsSideFrame1, text="E", func=lambda event, v=4: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice5.canvas.grid(row=14, column=4, columnspan=1)
optionsGridChoice6 = Button(optionsSideFrame1, text="F", func=lambda event, v=5: optionsGrid(event, v), \
                            size=15, animationType=1)
optionsGridChoice6.canvas.grid(row=14, column=5, columnspan=1)
optionsSideFrame2.grid_rowconfigure(0, minsize=(48+30))
optionsStatsLabel = Label(optionsSideFrame2, text=h(11)+"Statistiques"+h(11), fg=colour["black"], font=(mainFont, 20))
optionsStatsLabel.grid(row=1)
optionsStatsChoice1 = Button(optionsSideFrame2, text="SUPPRIMER LES DONNÉES", func=optionsStats, \
                             size=15, animationType=1)
optionsStatsChoice1.canvas.grid(row=2)
optionsSideFrame2.grid_rowconfigure(3, minsize=15*1.85+1+15)
optionsPreviewLabel = Label(optionsSideFrame2, text=h(14)+"Aperçu"+h(14), fg=colour["black"], font=(mainFont, 20))
optionsPreviewLabel.grid(row=4)
optionsSideFrame2.grid_rowconfigure(5, minsize=20)
optionsPreviewChoice1 = BoardPreview(optionsSideFrame2)
optionsPreviewChoice1.frame.grid(row=6)

"""-----------------------------------------------------MISC---------------------------------------------------------"""
infoIcon = Button(window, text="?", func=info, size=20, animationType=1, tag="bold")
infoIcon.canvas.place(relx=1, x=0, y=20, anchor=NE)
backIcon = Button(window, text="<", func=back, size=20, animationType=1, tag="bold")
backIcon.canvas.place(relx=0, x=0, y=20, anchor=NW)
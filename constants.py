import optionvars

windowBorder = 50
globalWidth, globalHeight = 800, 500

gSize = 10
bSize = 40
playerCanvasSize = 30

refreshRate = 15

mainFont = "Trebuchet MS"
colour = {
    "white": "#%02X%02X%02X" % (255, 255, 130),
    "black": "#%02X%02X%02X" % (160, 100, 0),

    "red": "#%02X%02X%02X" % (200, 50, 50),
    "green": "#%02X%02X%02X" % (0, 170, 50),
    "blue": "#%02X%02X%02X" % (50, 125, 175),
    "gold": "#%02X%02X%02X" % (255, 160, 60),
    "purple": "#%02X%02X%02X" % (255, 130, 255),
    "whitePlayer": "#%02X%02X%02X" % (255, 255, 255),
    "blackPlayer": "#%02X%02X%02X" % (0, 0, 0),

    "white0": "#%02X%02X%02X" % (255, 255, 130),
    "black0": "#%02X%02X%02X" % (160, 100, 0),
    "white1": "#%02X%02X%02X" % (255, 255, 200),
    "black1": "#%02X%02X%02X" % (50, 75, 225),
    "white2": "#%02X%02X%02X" % (255, 200, 100),
    "black2": "#%02X%02X%02X" % (50, 75, 255),
    "white3": "#%02X%02X%02X" % (255, 255, 180),
    "black3": "#%02X%02X%02X" % (255, 100, 150),
    "white4": "#%02X%02X%02X" % (180, 180, 180),
    "black4": "#%02X%02X%02X" % (100, 23, 125),
    "white5": "#%02X%02X%02X" % (180, 180, 180),
    "black5": "#%02X%02X%02X" % (75, 75, 75)
}
sound = {
    "click":"_menuClicked.wav",
    "eat":"_playerAte.wav",
    "move":"_playerMoved.wav",
    "super":"_playerSuper.wav",
    "select":"_playerSelected.wav",
    "deselect":"_playerDeselected.wav"
}

colour["white"] = colour["white" + str(optionvars.gColours)]
colour["black"] = colour["black" + str(optionvars.gColours)]
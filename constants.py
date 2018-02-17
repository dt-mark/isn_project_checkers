windowBorder = 50
globalWidth, globalHeight = 800, 500

gSize = 10
bSize = 40
playerCanvasSize = 30

ai = 1
humanPlayer = -1
difficulty = 0
gColours = 0

refreshRate = 15

mainFont = "Trebuchet MS"
colour = {
    "red": "#%02X%02X%02X" % (200, 50, 50),
    "green": "#%02X%02X%02X" % (0, 170, 50),
    "white": "#%02X%02X%02X" % (255, 255, 130),
    "black": "#%02X%02X%02X" % (160, 100, 0),
    "blue": "#%02X%02X%02X" % (50, 125, 175),
    "gold": "#%02X%02X%02X" % (255, 160, 60),
    "purple": "#%02X%02X%02X" % (255, 130, 255),
    "whitePlayer": "#%02X%02X%02X" % (255, 255, 255),
    "blackPlayer": "#%02X%02X%02X" % (0, 0, 0)
}
sound = {
    "click":"_menuClicked.wav",
    "eat":"_playerAte.wav",
    "move":"_playerMoved.wav",
    "super":"_playerSuper.wav",
    "select":"_playerSelected.wav",
    "deselect":"_playerDeselected.wav"
}

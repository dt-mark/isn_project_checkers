dico = {
  "windowBorder":"The border between the window and everything else (mainFrame)",
  "onePlayerCanEat":"Dictionnary which stores tuples of the coordinates of the players \nthat are able to eat another player for each player type",
  "gSize":"Stands for grid size, defines the size of the grid (10x10 by default)",
  "bSize":"Defines the size, in pixels, of one cell (40px by default)",
  "playerCanvasSize":"Defines the size, in pixels, of one player \n(smaller than the size of the cell)",
  "b":" ",
  "c":" ",
  "players":" ",
  "player":" ",
  "blackCount":" ",
  "whiteCount":" ",
  "selectedPlayer":" ",
  "highlightStuck":" ",
  "colour":"Dictionary which makes easier the colour selection.",
  "Player":" ",
  "changePosition":" ",
  "update":" ",
  "wrap":" ",
  "lerp":" ",
  "clamp":" ",
  "isBetween":"Function, checks if a value is between two limits.",
  "movementVector":"Fonction, quantifies how many squares there are between two \ncoordinates. Takes four arguments, the coordinates.",
  "case":" ",
  "caseColour":"Function to define the colour of the square.\nTakes three arguments, two for the coordinates and one \nfor the colour. See colour dictionary to know what to write \nfor each colour.",
  "resetCaseColour":"Function used to reset the colour of the squares.",
  "intToString":"Function, converts an integer given as an argument into \na string made of two characters. For example, 12 will return \n'12', 9 will return '09'.",
  "empty":"Function to check if a case is empty or not. Takes two arguments \n , which are the coordinates of the square.",
  "pixelToCell":"Function, converts coordinates into table index.",
  "cellToPixel":"Function, converts table index into coordinates.",
  "boardToFrame":" ",
  "closeWindow":"Function, just a window.destroy() to close the game.",
  "highlight":" ",
  "click":" "
}

while True:
    uInput = input(">>>")
    try:
        print(dico[uInput])
    except:
        print("Not in the database")
    finally:
        if uInput == "exit" or uInput == "EXIT" or uInput == "Exit":
            break

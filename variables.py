dico = {
  "windowBorder":"The border between the window and everything else (mainFrame)"
  "onePlayerCanEat":"Dictionnary which stores tuples of the coordinates of the players \
                    that are able to eat another player for each player type"
  "gSize":"Stands for grid size, defines the size of the grid (10x10 by default)"
  "bSize":"Defines the size, in pixels, of one cell (40px by default)"
  "playerCanvasSize":"Defines the size, in pixels, of one player \
                     (smaller than the size of the cell)"
  "b":" "
  "c":" "
  "players":" "
  "player":" "
  "blackCount":" "
  "whiteCount":" "
  "selectedPlayer":" "
  "highlightStuck":" "
  "colour":" "
  "Player":" "
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

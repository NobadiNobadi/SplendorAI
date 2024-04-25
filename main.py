from game import SplendorGame


predefined_board = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

t = SplendorGame(players=["Bot"])
t.setupBoard(predefined=predefined_board)
t.printBoard()
t.startGame()

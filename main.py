from game import SplendorGame


# predefined_board = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]
# predefined_board = [[15, 2, 30, 32], [19, 25, 15, 20], [2, 19, 3, 7]]

t = SplendorGame(players=["Bot"])
t.setupBoard()
# t.printBoard()
end = t.startGame()
print(end)
from components import nobles, cards, token_max_qty


class SplendorGame:
    def __init__(self, players_number=2, cards=cards, nobles=nobles, token_max_qty=token_max_qty):
        
        # setup
        self.players_number = players_number
        self.cards = cards
        self.nobles = nobles
        self.token_max_qty = token_max_qty

        # game
        self.active_game = False
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]
        self.cards_in_deck = self.cards

        # players
        self.active_player = [False for _ in range(players_number)]
        self.players_cards = [[] for _ in range(players_number)]
        self.players_points = [[] for _ in range(players_number)]
        

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
    

t = SplendorGame()
t.players_cards = [[[1, 0, 4, 0, 0, 0, 5],[0, 1, 1, 1, 0, 1, 4]], [[2, 0, 0, 5, 3, 0, 5],[3, 0, 0, 0, 0, 6, 5]]]
# print(t.players_cards)
# print(t.players_points)
# t.update_players_points()
# print(t.players_points)
print(t.board)
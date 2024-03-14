from components import nobles, cards, token_max_qty


class SplendorGame:
    def __init__(self, players=["Bob", "Steve"], cards=cards, nobles=nobles, token_max_qty=token_max_qty):
        
        # setup
        self.players_number = len(players)
        self.players = players
        self.cards = cards
        self.nobles = nobles
        self.token_max_qty = token_max_qty
        self.logHistory = []

        # game
        self.turn_counter = 0
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]
        self.cards_in_deck = self.cards

        # players
        self.active_player = [False for _ in range(self.players_number)]
        self.players_cards = [[] for _ in range(self.players_number)]
        self.players_points = [[] for _ in range(self.players_number)]
        self.players_tokens = [[0 for _ in range(len(self.token_max_qty))] for _ in range(self.players_number)]
        
    def log(self, round, player, action):
        self.logHistory.append([round, player, action])

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
        return True

    def take_tokens(self, player, tokens_array):
        for i in range(len(self.players_tokens[player])):
            self.players_tokens[player][i] += tokens_array[i]
        return True

    def buy_card(self, player, tier, col_num):
        return False
    

t = SplendorGame()
t.players_cards = [[[1, 0, 4, 0, 0, 0, 5],[0, 1, 1, 1, 0, 1, 4]], [[2, 0, 0, 5, 3, 0, 5],[3, 0, 0, 0, 0, 6, 5]]]
# print(t.players_cards)
# print(t.players_points)
# t.update_players_points()
# print(t.players_points)
print(t.board)
print(t.players_tokens)
t.take_tokens(0, [1, 1, 1, 0, 0, 0])
print(t.players_tokens)
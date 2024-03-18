from components import nobles, cards, token_max_qty


class SplendorGame:
    def __init__(self, players=["Bob", "Steve"], cards=cards, nobles=nobles, token_max_qty=token_max_qty):
        
        # setup
        self.players_number = len(players)
        self.players = players
        self.cards = cards
        self.nobles = nobles
        self.token = token_max_qty
        self.logHistory = []

        # game
        self.turn_counter = 0
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]
        self.cards_in_deck = self.cards

        # players
        self.active_player = -1
        self.players_cards = [[] for _ in range(self.players_number)]
        self.players_points = [0 for _ in range(self.players_number)]
        self.players_tokens = [[0 for _ in range(len(self.token))] for _ in range(self.players_number)]
        self.players_reserve = [[None for _ in range(3)] for _ in range(self.players_number)]
        
    def log(self, player, action):
        self.logHistory.append([self.turn_counter, player, action])

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
        return True

    def take_tokens(self, player, tokens):
        for i in range(len(self.players_tokens[player])):
            self.players_tokens[player][i] += tokens[i]
        
        self.log(player, "Take tokens")
        return True

    def buy_card(self, player, tier, col_num, tokens):
        self.players_cards[player].append(self.board[tier][col_num])
        self.board[tier][col_num] = None
        for i in range(len(self.players_tokens[player])):
            self.players_tokens[player][i] -= tokens[i]

        self.log(player, "Buy a card") 
        return True
    
    def refill_board(self):
        for tier in self.board:
            for col in tier:
                if col is None: self.board[tier][col] = self.cards_in_deck[0] 
        self.cards_in_deck.pop[0]
        return True
    
    def reserve_card(self, player, tier, col_num):
        self.players_cards[player].append(self.board[tier][col_num])
        self.board[tier][col_num] = None
        if self.tokens[-1] > 1: self.players_tokens[player][-1] += 1

        self.log(player, "Reserve a card")
        return True
    
    def startGame(self):
        # main loop
        round = 1
        while True:
            for index, player in enumerate(self.players, start=0):
                self.active_player = player
                print(f"Round: {round}, player: {player}")
            round += 1
            for points in self.players_points:
                if points >= 15: break
            if round > 5: break
        return True
    
    def botRandomTurn(self, player_id):
        # check if can buy
        for tier in self.cards:
            for card in tier:
                for token_index in range(1, 6):
                    discount = sum([1 for card in self.players_cards[player_id] if card[-1] == token_index])
                    if self.players_tokens[player_id][token_index] + discount - card[token_index] < 0: continue

t = SplendorGame()
t.players_cards = [[[1, 0, 4, 0, 0, 0, 5],[0, 1, 1, 1, 0, 1, 4]], [[2, 0, 0, 5, 3, 0, 5],[3, 0, 0, 0, 0, 6, 5]]]
# print(t.players_cards)
# print(t.players_points)
# t.update_players_points()
# print(t.players_points)
# print(t.board)
# print(t.players_tokens)
# t.take_tokens(0, [1, 1, 1, 0, 0, 0])
# print(t.players_tokens)
# t.startGame()
t.botRandomTurn(1)
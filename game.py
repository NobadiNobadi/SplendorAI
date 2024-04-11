from components import nobles, cards, token_max_qty
import time
import random


class SplendorGame:
    def __init__(self, players=["Bob", "Steve"], cards=cards, nobles=nobles, token_max_qty=token_max_qty):
        
        # setup
        self.players_number = len(players)
        self.players = players
        self.cards = cards
        self.nobles = nobles
        self.tokens = token_max_qty
        self.logHistory = []

        # game
        self.turn_counter = 0
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]

        # players
        self.active_player = -1
        self.players_cards = [[] for _ in range(self.players_number)]
        self.players_points = [0 for _ in range(self.players_number)]
        self.players_tokens = [[0 for _ in range(len(self.tokens))] for _ in range(self.players_number)]
        self.players_reserve = [[None for _ in range(3)] for _ in range(self.players_number)]
        
    def log(self, player, action):
        self.logHistory.append([self.turn_counter, player, action])

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
        return True

    # def take_tokens(self, player, tokens):
    #     for i in range(len(self.players_tokens[player])):
    #         self.players_tokens[player][i] += tokens[i]
        
    #     self.log(player, "Take tokens")
    #     return True

    def buy_card(self, player, tier, col_num):
        for i in range(0,5):
            self.players_tokens[player][i] -= (self.board[tier][col_num][i+1] - sum([1 for card in self.players_cards[player] if card[-1] == i]))
        self.players_cards[player].append(self.board[tier][col_num])
        self.board[tier][col_num] = [None]
        self.log(player, "Buy a card") 
        self.refill_board()
        return True
    
    def refill_board(self):
        for tier_index, tier in enumerate(self.board, start=0):
            for col_index, col in enumerate(tier, start=0):
                if col[0] is None:      
                    self.board[tier_index][col_index] = self.cards[tier_index][0]
                self.cards[tier_index].pop(0)
        return True
    
    def reserve_card(self, player, tier, col_num):
        self.players_cards[player].append(self.board[tier][col_num])
        self.board[tier][col_num] = None
        if self.tokens[-1] > 1: self.players_tokens[player][-1] += 1

        self.log(player, "Reserve a card")
        return True
    
    def setupBoard(self):
        for tier in range(len(self.cards)):
            random.shuffle(self.cards[tier])
        self.refill_board()

    def startGame(self):
        # main loop
        round = 1
        while True:
            # print(len(self.cards[0]))
            for index, player in enumerate(self.players, start=0):
                self.active_player = player
                self.botRandomTurn(index)
            round += 1
            self.update_players_points()
            for points in self.players_points:
                if points >= 15: break
            # if round > 5: break
        return True
    
    def printBoard(self):
        print(f"Tier 1: {[card for card in self.board[0]]}")
        print(f"Tier 2: {[card for card in self.board[1]]}")
        print(f"Tier 3: {[card for card in self.board[2]]}")

    def botRandomTurn(self, player_id):
        # print("bot is thinking")
        time.sleep(1)

        # check if can buy
        for tier_index, tier in enumerate(self.board, start=0):
            for index, card in enumerate(tier, start=0):
                not_enough = False
                for token_index in range(1, 6):
                    discount = sum([1 for card in self.players_cards[player_id] if card[-1] == token_index])
                    # print(f"{discount} for {token_index}")
                    if self.players_tokens[player_id][token_index-1] + discount - card[token_index] < 0: not_enough = True
                if not_enough: continue
                print(f"{self.players[player_id]} bought a card: {self.board[tier_index][index]}")
                self.buy_card(player_id, tier_index, index)
                return 
        # take tokens random tokens
        random_order = [0, 1, 2, 3, 4]
        random.shuffle(random_order)
        
        taken_tokens = [0, 0, 0, 0, 0]
        while True:
            if random.randint(0, 1) > 0: # take two
                for index in random_order:
                    if self.tokens[index] > 4: 
                        self.players_tokens[player_id][index] += 2
                        self.tokens[index] -= 2
                        taken_tokens[index] += 2
                        print(f"{self.players[player_id]} took tokens: {taken_tokens}")
                        while sum([qty for qty in self.players_tokens[player_id]]) > 10:
                            random_order = [0, 1, 2, 3, 4]
                            random.shuffle(random_order)
                            index = random_order[0]
                            if self.players_tokens[player_id][index] > 0: self.players_tokens[player_id][index] -= 1
                        return
                continue
            else:
                taken = 0
                for index in random_order:
                    if self.tokens[index] > 0:
                        self.players_tokens[player_id][index] += 1
                        self.tokens[index] -= 1
                        taken_tokens[index] += 1
                        taken += 1
                        if taken == 3: 
                            print(f"{self.players[player_id]} took tokens: {taken_tokens}")
                            while sum([qty for qty in self.players_tokens[player_id]]) > 10:
                                random_order = [0, 1, 2, 3, 4]
                                random.shuffle(random_order)
                                index = random_order[0]
                                if self.players_tokens[player_id][index] > 0: self.players_tokens[player_id][index] -= 1
                            return
            

                 

                


t = SplendorGame()
t.setupBoard()
print(len(t.cards[0]))
t.printBoard()
t.startGame()
# print(t.cards[0][0])
# print(t.cards)
# t.printBoard()
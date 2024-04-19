from components import nobles, cards, token_max_qty
import time
import random


class SplendorGame:
    def __init__(self, players=["Bob", "Steve"], cards=cards, nobles=nobles, token_max_qty=token_max_qty):
        
        # setup
        self.players = players
        self.players_number = len(self.players)
        self.cards = cards
        self.nobles = random.sample(nobles, len(self.players)+1)
        self.tokens = [qty-4+len(self.players) for qty in token_max_qty]
        self.logHistory = []

        # game
        self.turn_counter = 0
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]

        # players
        self.active_player = -1
        self.players_cards = [[] for _ in range(self.players_number)]
        self.players_points = [0 for _ in range(self.players_number)]
        self.players_tokens = [[0 for _ in range(len(self.tokens))] for _ in range(self.players_number)]
        self.players_nobles = [[] for _ in range(self.players_number)]
        
    def log(self, player, action):
        self.logHistory.append([self.turn_counter, player, action])

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
        for player_index, player in enumerate(self.players_points,start=0):
            for noble in self.players_nobles[player_index]:
                self.players_points[player_index] += noble[0]
        return True

    # def take_tokens(self, player, tokens):
    #     for i in range(len(self.players_tokens[player])):
    #         self.players_tokens[player][i] += tokens[i]
        
    #     self.log(player, "Take tokens")
    #     return True

    def buy_card(self, player, tier, col_num):
        can_buy = True
        for i in range(0,5):
            if self.players_tokens[player][i] - (self.board[tier][col_num][i+1] - sum([1 for card in self.players_cards[player] if card[-1] == i])) < 0: can_buy = False
        if can_buy:
            for i in range(0,5):
                self.players_tokens[player][i] -= (self.board[tier][col_num][i+1] - sum([1 for card in self.players_cards[player] if card[-1] == i]))
                self.tokens[i] += (self.board[tier][col_num][i+1] - sum([1 for card in self.players_cards[player] if card[-1] == i]))
            self.players_cards[player].append(self.board[tier][col_num])
            self.board[tier][col_num] = [None]
            self.log(player, "Buy a card") 
            self.refill_board()
            return True
        else:
            return False
        
    def take_tokens(self, player_id, white, blue, green, red, black):
        token_array = [white, blue, green, red, black]
        if (
            (sum(token_array) == 3 and all(0 <= x <= 1 for x in token_array) # check if only 3 tokens, max 1 per color
            and all(self.tokens[color] - token_array[color] >= 0 for color in range(0, 5))) # check if there are not negative qty. of tokens
        or (sum(1 for x in token_array if x == 2) == 1 and sum(1 for x in token_array if x == 0) == len(token_array) - 1 # check if only 2 tokens, 2 in the same color
            and self.tokens[token_array.index(2)] - 2 >= 2) # check if there are at least 2 token of taken color
            ):   
            for color in range(0,5):
                self.players_tokens[player_id][color] += token_array[color]
                self.tokens[color] -= token_array[color]
            print(f"Player {self.players[player_id]} took tokens: {token_array}")          
            return True
        else:
            return False

    def refill_board(self):
        for tier_index, tier in enumerate(self.board, start=0):
            for col_index, col in enumerate(tier, start=0):
                if col[0] is None:      
                    self.board[tier_index][col_index] = self.cards[tier_index][0]
                    self.cards[tier_index].pop(0)
        return True

    
    def setupBoard(self):
        for tier in range(len(self.cards)):
            random.shuffle(self.cards[tier])
        self.refill_board()

    def startGame(self):
        # main loop
        round = 0
        while True:
            round += 1
            # print(len(self.cards[0]))
            print(f"\nTurn {round}")
            for player_index, player in enumerate(self.players, start=0):
                self.active_player = player
                self.botRandomTurn(player_index)
                # noble check
                nobles_to_take = []
                for noble_index, noble in enumerate(self.nobles, start=0):
                    take_noble = True
                    for i in range(0, 5):
                        if not sum([1 for card in self.players_cards[player_index] if card[-1] == i]) >= noble[i+1]: take_noble = False    
                    if take_noble: nobles_to_take.append(noble_index)
                if nobles_to_take: 
                    random_noble = random.choice(nobles_to_take)
                    print(f"{self.players[player_index]} took noble {self.nobles[random_noble]}")
                    self.players_nobles[player_index].append(random_noble)    
                    del self.nobles[random_noble]
                    
                    
            self.update_players_points()
            for player_index, points in enumerate(self.players_points, start=0):
                if points >= 1: 
                    print(f"Game has been ended, {self.players[player_index]}")

                    return True
            # if round > 5: break
        return True
    
    def printBoard(self):
        print(f"Tier 1: {[card for card in self.board[0]]}")
        print(f"Tier 2: {[card for card in self.board[1]]}")
        print(f"Tier 3: {[card for card in self.board[2]]}")

    def botRandomTurn(self, player_id):
        # print("bot is thinking")
        # time.sleep(1)

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
            
        # take random tokens
        random_order = [0, 1, 2, 3, 4]
        random.shuffle(random_order)
        
        debugger = 0
        taken_tokens = [0, 0, 0, 0, 0]
        while True:
            debugger += 1
            if debugger > 10:
                # print(f"{self.board}\n{self.cards}\n{self.players_cards}")
                time.sleep(5)
                return
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
                            if self.players_tokens[player_id][index] > 0: 
                                drop_tokens = [0, 0, 0, 0, 0]
                                self.players_tokens[player_id][index] -= 1
                                drop_tokens[index] = 1
                                print(f"{self.players[player_id]} drop token: {drop_tokens}")
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
                                if self.players_tokens[player_id][index] > 0: 
                                    drop_tokens = [0, 0, 0, 0, 0]
                                    self.players_tokens[player_id][index] -= 1
                                    drop_tokens[index] = 1
                                    print(f"{self.players[player_id]} drop token: {drop_tokens}")
                            return
            
    def playerTurn(self, player_id):
        # choose action
        action = None
        # 1 - take tokens, 2 - buy a card
        while action not in [1, 2, 3]: 
            action = int(input("Please choose an action: \n1 - to take tokens\n2 - to buy a card\n3 - to show a board\n"))
        
        if action == 3: self.printBoard()
        
                 

                


t = SplendorGame()
t.setupBoard()
# print(len(t.cards[0]))
t.printBoard()
t.playerTurn(1)
# print(t.tokens)
# print(t.nobles)
# t.startGame()
# print(t.cards[0][0])
# print(t.cards)
# t.printBoard()
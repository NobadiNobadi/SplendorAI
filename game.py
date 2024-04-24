from components import nobles, cards, token_max_qty
import time
import random
import numpy as np


class SplendorGame:
    def __init__(self, players=["Bob", "Steve"], cards=cards, nobles=nobles, token_max_qty=token_max_qty, points=15):
        
        # setup
        self.players = players
        self.players_number = len(self.players)
        self.cards = cards
        self.nobles = random.sample(nobles, len(self.players)+1)
        self.tokens = [qty-4+len(self.players) for qty in token_max_qty]
        self.logHistory = []
        self.points = points

        # game
        self.turn_counter = 0
        self.board = [[[None] for _ in range(4)] for _ in range(len(self.cards))]

        # players
        self.active_player = -1
        self.players_cards = [[] for _ in range(self.players_number)]
        self.players_points = [0 for _ in range(self.players_number)]
        self.players_tokens = [[0 for _ in range(len(self.tokens))] for _ in range(self.players_number)]
        self.players_nobles = [[] for _ in range(self.players_number)]

        # bot parameters
        self.discount_value = 2.2
        self.hard_to_buy = 0.008
        self.owned_discount = 0.1
        self.discount_value_in_time = 0.95
        self.tier_value = [0.5, 0.35, 0.15]
        
    def log(self, player, action):
        self.logHistory.append([self.turn_counter, player, action])

    def update_players_points(self):
        self.players_points = [sum(card[0] for card in player) for player in self.players_cards]
        for player_index, player in enumerate(self.players_points,start=0):
            for noble in self.players_nobles[player_index]:
                self.players_points[player_index] += noble[0]
        return True

    def buy_card(self, player, tier, col_num):
        can_buy = True
        for i in range(0,5):
            discount = min(sum([1 for card in self.players_cards[player] if card[-1] == i+1]),self.board[tier][col_num][i+1])
            if self.players_tokens[player][i] - (self.board[tier][col_num][i+1] - discount) < 0: can_buy = False # if can buy
        if can_buy:
            for i in range(0,5):
                discount = min(sum([1 for card in self.players_cards[player] if card[-1] == i+1]),self.board[tier][col_num][i+1])
                self.players_tokens[player][i] -= (self.board[tier][col_num][i+1] - discount)
                self.tokens[i] += (self.board[tier][col_num][i+1] - discount)
            self.players_cards[player].append(self.board[tier][col_num])
            self.board[tier][col_num] = [None]
            print(f"{self.players[player]} bought a card {self.players_cards[player][-1]}")
            # self.log(player, "Buy a card") 
            self.refill_board()
            return True
        else:
            return False
        
    def take_tokens(self, player_id, token_array):
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
   
    def setupBoard(self, predefined):
        if predefined:
            for tier in range(0, 3):
                for col_index, col in enumerate(predefined[tier], start=0):
                    self.board[tier][col_index] = self.cards[tier][col]
            for tier in range(0, 3):
                for col in sorted(predefined[tier], reverse=True):
                    del self.cards[tier][col]
        else:
            for tier in range(len(self.cards)):
                random.shuffle(self.cards[tier])
            self.refill_board()
        return True

    def startGame(self):
        # main loop
        round = 0
        print(f"Players {self.players}")
        while True:
            round += 1
            # print(len(self.cards[0]))
            print(f"\nTurn {round}")
            for player_index, player in enumerate(self.players, start=0):
                self.active_player = player
                if player == "Bot":
                    self.botTurn(player_index)
                else:
                    self.playerTurn(player_index)
                    
                    
            self.update_players_points()
            for player_index, points in enumerate(self.players_points, start=0):
                if points >= self.points: 
                    print(f"Game has been ended, {self.players[player_index]}")

                    return True
            # if round > 5: break
        return True
    
    def printBoard(self):
        print(f"Tier 1: {[card for card in self.board[0]]}")
        print(f"Tier 2: {[card for card in self.board[1]]}")
        print(f"Tier 3: {[card for card in self.board[2]]}")

    def printPlayersCards(self):
        for player_id, player in enumerate(self.players, start=0):
            print(f"Player {player}: {self.players_cards[player_id]}")

    def printPlayersTokens(self):
        for player_id, player in enumerate(self.players, start=0):
            print(f"Player {player}: {self.players_tokens[player_id]}")                     

    def playersTokens(self, player_id):
        return self.players_tokens[player_id]      

    def printPlayersDiscounts(self):
        for player_id, player in enumerate(self.players, start=0):
            discounts = [0, 0, 0, 0, 0]
            for token_id in range(1, 6):
                discounts[token_id-1] += sum([1 for card in self.players_cards[player_id] if card[-1] == token_id])
            print(f"Player {player}: {discounts}")    

    def playersDiscounts(self, player_id):
        discounts = [0, 0, 0, 0, 0]
        for token_id in range(1, 6):
            discounts[token_id-1] += sum([1 for card in self.players_cards[player_id] if card[-1] == token_id])
        return discounts   

    def botRandomTurn_old(self, player_id):
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
        while action not in [1, 2]: 
            try:
                action = int(input("""Please choose an action: \n1 - to take tokens\n2 - to buy a card\n3 - to show a board\n4 - to show player's cards\n5 - to show player's tokens\n6 - to show player's discounts\n"""))
            except:
                print("wrong syntax")
                continue
            if action == 3: # print board
                self.printBoard()
            if action == 4: # print player's cards
                self.printPlayersCards()
            if action == 5: # print player's tokens
                self.printPlayersTokens()
            if action == 6: # print player's discounts
                self.printPlayersDiscounts()
        if action == 1: # take tokens
            exit = False
            while not exit:
                try:
                    token_array = list(input("Please choose tokens (numbers separated by comma):").split(","))
                    token_array = [int(x) for x in token_array]
                    if len(token_array) != 5: 0 + "0"
                    if self.take_tokens(player_id, token_array):
                        print(self.players_tokens[player_id])
                        exit = True
                    else:
                        print("not allowed move")
                except:
                    print("wrong syntax")
            while sum(self.players_tokens[player_id]) > 10:
                token_id = 0
                exit = False
                while not exit and token_id not in [1, 2, 3, 4, 5]:
                    try:
                        token_id = int(input("Please choose token to discard (1-white,2-blue,3-green,4-red,5-black):"))
                        exit = True
                    except:
                        print("wrong syntax")
                if exit:
                    self.discardToken(player_id, token_id-1)
        elif action == 2: # buy a card
            exit = False
            while not exit:
                try:
                    card_index = list(input("Please input row and column index (separated by comma):").split(","))
                    card_index = [int(x) for x in card_index]
                    if len(card_index) != 2: 0 + "0"
                    if self.buy_card(player_id,card_index[0]-1, card_index[1]-1):
                        exit = True
                    else:
                        print("not allowed move")
                except:
                    print("wrong syntax")
            
    def discardToken(self, player_id, token_id):
        if self.players_tokens[player_id][token_id] - 1 >= 0:
            self.players_tokens[player_id][token_id] -= 1
            self.tokens[token_id] += 1
            discarded = [0, 0, 0, 0, 0]
            discarded[token_id] = 1
            print(f"Player {self.players[player_id]} discarded tokens: {discarded}")
            return True
        else:
            return False

    def botTurn(self, player_id):    
        # parameters 
        token_value = [0, 0, 0, 0, 0]
        token_qty = [0, 0, 0, 0, 0]
        
        focus = [[tier, col, 0] for tier in range(0,3) for col in range(0,4)]

        for tier in range(0, 3): # calculate focus on tokens
            for col in range(0, 4):
                for token in range(1, 6):
                    token_qty[token-1] += self.board[tier][col][token]
                    token_value[token-1] += self.board[tier][col][token] * self.tier_value[tier]

        token_focus = [[index, value] for index, value in enumerate(token_value, start=0)]            
        token_focus = sorted(token_focus, key=lambda x: x[1], reverse=True)
        
        for tier in range(0, 3): # calculate focus on cards
            for col in range(0, 4):
                t1 = ((self.discount_value + self.board[tier][col][0]) / sum(self.board[tier][col][1:][:-1])) # discount val + vps / sum of tokens
                t2 = sum([((qty-min(sum([1 for card in self.players_cards[player_id] if card[-1] == token_id+1]),self.board[tier][col][token_id+1]))**2)*self.hard_to_buy for token_id, qty in enumerate(self.board[tier][col][1:][:-1], start=0)]) # sum of particular (tokens qty-discounts)^2
                t3 = sum([min(sum([1 for card in self.players_cards[player_id] if card[-1] == token_id+1]),self.board[tier][col][token_id+1]) for token_id in range(0,5)])*self.owned_discount # sum of owned discounts
                focus[tier*4+col][-1] = t1 - t2 + t3
        
        focus = sorted(focus, key=lambda x: x[2], reverse=True)  

        self.discount_value *= self.discount_value_in_time

        # buy card first
        
        for card in focus:
            if self.buy_card(player_id, card[0], card[1]): 
                return True
        # take tokens on focus

        while True:
            most_focus = [self.board[focus[0][0]][focus[0][1]], self.board[focus[1][0]][focus[1][1]]]
            first, second, discounts, tokens = np.array(most_focus[0][1:][:-1]), np.array(most_focus[1][1:][:-1]), np.array(self.playersDiscounts(player_id)), np.array(self.playersTokens(player_id))
            
            first -= (discounts + tokens)
            second -= (discounts + tokens)
            
            indexes_first = [i for i, x in enumerate(first) if x > 0]
            indexes_second = [i for i, x in enumerate(second) if x > 0]

            indexes_to_take = []

            if len(indexes_first) >= 3:
                indexes_to_take = random.sample(indexes_first, 3)
            elif len(indexes_first) == 2:
                indexes_to_take = random.sample(indexes_first, 2)
                if len(indexes_second) >= 1:
                    indexes_to_take.append(random.sample(indexes_second, 1)[0])
            elif len(indexes_first) == 1:
                indexes_to_take = random.sample(indexes_first, 1)
                if len(indexes_second) >= 2:
                    temp = random.sample(indexes_second, 2)
                    for i in temp:
                        indexes_to_take.append(i)
                else: 
                    indexes_to_take.append(indexes_second[0])
                    for i in token_focus:
                        if i[0] not in indexes_to_take: 
                            indexes_to_take.append(i[0])
                            break
            else:
                if len(indexes_second) >= 3:
                    indexes_to_take = random.sample(indexes_second, 3)
                elif len(indexes_second) == 2:
                    indexes_to_take = random.sample(indexes_second, 2)
                    for i in token_focus:
                        if i[0] not in indexes_to_take: 
                            indexes_to_take.append(i[0])
                elif len(indexes_second) == 1:
                    indexes_to_take = random.sample(indexes_second, 1)
                    for i in token_focus:
                        if i[0] not in indexes_to_take: 
                            indexes_to_take.append(i[0])
                            if len(indexes_to_take) == 3: break
                            
                            
                else:
                    indexes_to_take.append(token_focus[0])
                    indexes_to_take.append(token_focus[1])
                    indexes_to_take.append(token_focus[2])

            tokens_to_take = [0, 0, 0, 0, 0]
            for i in indexes_to_take:
                tokens_to_take[i] = 1
            if self.take_tokens(player_id, tokens_to_take):
                return True    
            else:
                while True:
                    random_tokens = [0] * 2 + [1] * 3
                    random.shuffle(random_tokens)
                    if self.take_tokens(player_id, random_tokens):
                        return True   
     

                
predefined = [[0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3]]

t = SplendorGame(players=["Bot"])
t.setupBoard(predefined=predefined)
t.printBoard()
t.startGame()

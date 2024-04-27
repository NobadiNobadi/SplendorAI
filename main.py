from game import SplendorGame
from components import nobles, cards, token_max_qty
import json
import copy

results = []
# discount_value, hard_to_buy, owned_discount, discount_value_in_time, tier1, tier2 , tier3

for _ in range(1000):
    learn_game = SplendorGame(players=["Bot"], cards=copy.deepcopy(cards), )
    learn_game.setupBoard()
    end_stats = learn_game.startGame()
    results.append(end_stats)
# Zapisujemy wyniki do pliku JSON
with open('results.json', 'w') as f:
    json.dump(results, f)

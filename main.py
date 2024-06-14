from game import SplendorGame
from components import nobles, cards, token_max_qty
import json
import copy


# discount_value, hard_to_buy, owned_discount, discount_value_in_time, tier1, tier2 , tier3
# tiersV = [[0.35, 0.35, 0.30], [0.40, 0.40, 0.2], [0.25, 0.25, 0.50]]
tiersV = [[0.4, 0.4, 0.2], [0.45, 0.45, 0.1], [0.33, 0.33, 0.33]]
discount_valueV = [1.7, 1.8, 1.9]
hard_to_buyV = [0.016, 0.018, 0.02, 0.022, 0.024]
owned_discountV = [0.16, 0.12, 0.1, 0.08, 0.04]
discount_value_in_timeV = [0.97, 0.96, 0.95, 0.94, 0.93]

saved_files = 0
for tierV in tiersV:
    for divV in discount_valueV:
        for htbV in hard_to_buyV:
            for owdV in owned_discountV:
                for dvtV in discount_value_in_timeV:
                    results = []
                    for _ in range(1000):
                        try:
                            learn_game = SplendorGame(players=["Bot"], cards=copy.deepcopy(cards), tier1=tierV[0], tier2=tierV[1], tier3=tierV[2]
                                                    ,discount_value=divV, discount_value_in_time=dvtV, owned_discount=owdV, hard_to_buy=htbV)
                            learn_game.setupBoard()
                            end_stats = learn_game.startGame()
                            results.append(end_stats)
                        except:
                            results.append(False)
                    
                    with open(f'data2/results{saved_files}.json', 'w') as f:
                        json.dump(results, f)
                    print(saved_files)
                    saved_files += 1


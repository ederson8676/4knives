import random
import time
from itertools import permutations
from math import sqrt

class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.points = 0
        self.dice = []
        self.group1 = []
        self.group2 = []
        self.is_human = is_human
        self.win_rate = 0
        self.round_score = 0
        self.actions_made = 0

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(4)]
        if self.is_human:
            print(f"{self.name} 擲出骰子: {self.dice}")

    def split_dice(self):
        if self.is_human:
            while True:
                try:
                    print(f"{self.name}, 請輸入你的組合1的兩顆骰子編號（範例：1.2 或 4.1）:")
                    group1_str = input().strip()
                    group1_indices = list(map(int, group1_str.split('.')))

                    if len(group1_indices) != 2:
                        raise ValueError("組合1必須恰好包含兩顆骰子的編號 (例如 1.2)。")
                    if any(i < 1 or i > 4 for i in group1_indices):
                        raise ValueError("骰子編號範圍必須是 1 到 4。")
                    if len(set(group1_indices)) != 2:
                        raise ValueError("請輸入兩個不同的骰子編號。")

                    self.group1 = [self.dice[i - 1] for i in group1_indices]
                    leftover_indices = [x for x in [1,2,3,4] if x not in group1_indices]
                    self.group2 = [self.dice[i - 1] for i in leftover_indices]
                    break
                except ValueError as e:
                    print(f"輸入錯誤: {e}，請重新輸入。")
        else:
            # 電腦玩家自動分組
            dice_counts = {val: self.dice.count(val) for val in set(self.dice)}
            pairs = [val for val, cnt in dice_counts.items() if cnt >= 2]
            if len(pairs) == 1:
                pair_value = pairs[0]
                group2_indices = [i for i, val in enumerate(self.dice) if val == pair_value][:2]
                group1_indices = [i for i in range(4) if i not in group2_indices]
            elif len(pairs) == 2:
                pair1, pair2 = pairs
                pair1_indices = [i for i, val in enumerate(self.dice) if val == pair1]
                pair2_indices = [i for i, val in enumerate(self.dice) if val == pair2]
                if pair1 <= pair2:
                    group1_indices = pair1_indices[:2]
                    group2_indices = pair2_indices[:2]
                else:
                    group1_indices = pair2_indices[:2]
                    group2_indices = pair1_indices[:2]
            else:
                from itertools import combinations
                best_diff = float('inf')
                best_g1 = None
                best_g2 = None
                for combo1 in combinations(range(4), 2):
                    combo2 = [x for x in range(4) if x not in combo1]
                    g1 = [self.dice[i] for i in combo1]
                    g2 = [self.dice[i] for i in combo2]
                    if self.group_strength(g1) <= self.group_strength(g2):
                        diff = abs(self.group_strength(g1)-self.group_strength(g2))
                        if diff < best_diff:
                            best_diff = diff
                            best_g1 = combo1
                            best_g2 = combo2
                group1_indices = best_g1
                group2_indices = best_g2

            self.group1 = [self.dice[i] for i in group1_indices]
            self.group2 = [self.dice[i] for i in group2_indices]

    def group_strength(self, group):
        if len(group) != 2:
            return -1
        if len(set(group)) == 1:
            return 12 + group[0]
        else:
            return sum(group) + max(group)/10

    def validate_groups(self):
        if self.group_strength(self.group1) <= self.group_strength(self.group2):
            return True
        elif not self.is_human:
            print(f"{self.name} 分組無效，重新分組...")
            self.split_dice()
            return self.group_strength(self.group1) <= self.group_strength(self.group2)
        return False

def compare_groups(players, group_index):
    strengths = []
    for p in players:
        val = p.group_strength(p.group1) if group_index==1 else p.group_strength(p.group2)
        strengths.append((p, val))
    strengths.sort(key=lambda x: x[1], reverse=True)
    max_str = strengths[0][1]
    winners = [p for p, v in strengths if v == max_str]
    for w in winners:
        w.round_score += 1
    return winners

def calculate_win_probability(player):
    from itertools import permutations
    all_combos = [list(perm) for perm in permutations(range(1,7),2)] + [[i,i] for i in range(1,7)]
    g1_val = player.group_strength(player.group1)
    g2_val = player.group_strength(player.group2)
    g1_wins = sum(1 for c in all_combos if g1_val > player.group_strength(c))
    g2_wins = sum(1 for c in all_combos if g2_val > player.group_strength(c))

    g1_rate = g1_wins / len(all_combos)
    g2_rate = g2_wins / len(all_combos)
    if sorted(player.group1) == [1,2] and g1_rate == 0:
        g1_rate=0.05
    if sorted(player.group2) == [1,2] and g2_rate == 0:
        g2_rate=0.05

    geo = sqrt(g1_rate * g2_rate)
    return g1_rate, g2_rate, geo

def computer_player_decision(player, max_bet, pot):
    win_rate = player.win_rate
    if win_rate>0.7:
        if max_bet==0:
            return "+"
        return "="
    elif 0.4<=win_rate<=0.7:
        if max_bet==0:
            return "+"
        if max_bet<70:
            return "="
        return "*"
    else:
        return random.choice(["-","*"])

def determine_bet_size(prob):
    if 0.2<= prob<0.4:
        return 20
    elif 0.4<= prob<0.7:
        return 40
    elif 0.7<= prob<=1.0:
        return 70
    return 0

def reorder_players(player_list, starter):
    if starter in player_list:
        idx = player_list.index(starter)
        return player_list[idx:] + player_list[:idx]
    return player_list

def betting_phase(players, pot):
    active_players = [p for p in players]
    current_bets = {p.name: 0 for p in players}
    max_bet = 0

    while True:
        all_pass = True
        for player in active_players[:]:
            if len(active_players)==1:
                break
            if len(set(current_bets.values()))==1 and max_bet!=0:
                break
            if player.actions_made>=3:
                print(f"{player.name} 本回合已達下注次數上限，跳過。")
                continue

            if not player.is_human:
                thinking_time= random.randint(1,5)
                print(f"\n{player.name} 正在思考中...")
                time.sleep(thinking_time)

            if player.is_human:
                print(f"\n輪到 {player.name} 行動:")
                print(f"剩餘點數: {player.points}, 當前最高下注額: {max_bet}, 底池: {pot}")
                action= input("輸入並Enter動作後方括號內的符號 (raise(+)/call(=)/pass(-)/fold(*)): ").strip().lower()
            else:
                action= computer_player_decision(player, max_bet, pot)

            if action=="+":
                bet= determine_bet_size(player.win_rate)
                current_bets[player.name]+= bet
                player.points-= bet
                pot+= bet
                max_bet= max(max_bet, current_bets[player.name])
                player.actions_made+=1
                print(f"{player.name} 選擇 raise {bet} 點 → 此輪玩家共下注: {current_bets[player.name]}。")
                print(f"更新後底池：{pot} 點")
                all_pass=False

            elif action=="=":
                diff= max_bet - current_bets[player.name]
                if diff>0:
                    current_bets[player.name]+= diff
                    player.points-= diff
                    pot+= diff
                player.actions_made+=1
                print(f"{player.name} 選擇 call {diff} 點 → 此輪玩家共下注: {current_bets[player.name]}。")
                print(f"更新後底池：{pot} 點")
                all_pass=False

            elif action=="-":
                if max_bet>0:
                    print(f"{player.name} 選擇 fold，退出本輪。")
                    active_players.remove(player)
                else:
                    player.actions_made+=1
                    print(f"{player.name} 選擇 pass。")
                print(f"更新後底池：{pot} 點")

            elif action=="*":
                active_players.remove(player)
                print(f"{player.name} 選擇 fold，退出本輪。")
                print(f"更新後底池：{pot} 點")

            else:
                print(f"{player.name} 輸入動作 ({action}) 不合法，系統自動判定為 fold。")
                active_players.remove(player)
                print(f"更新後底池：{pot} 點")

        if len(active_players)==1:
            break
        if all_pass:
            print("本輪所有玩家都選擇 pass，結束下注，進入比較。")
            break

        bets_active= [current_bets[p.name] for p in active_players]
        if len(set(bets_active))==1 and max_bet!=0:
            break

    return active_players, pot

def tie_breaker(tied_players, pot, round_number, next_starter):
    """
    有平手 => 進入加賽
    回傳 (tie_winner, pot, tie_winner, final_opponents)：
      tie_winner => 加賽最終勝者
      第三個回傳值 => 下一局先行 => tie_winner (新的一局必定由最終贏家先行)
      final_opponents => 所有「最後一輪加賽」裡的玩家（含中途 fold）
    """

    # ★ 用來累積「所有最終加賽輪」的玩家(包含 fold)
    #   只要有新一輪加賽，就把該輪 tied_players 都 union 進去
    all_tiebreak_players = set()

    current_round_players = reorder_players(tied_players, next_starter)

    while True:
        # 先把當前這輪加賽的玩家整批 union 進 all_tiebreak_players
        all_tiebreak_players |= set(current_round_players)

        # 重置分數、行動次數
        for p in current_round_players:
            p.round_score=0
            p.actions_made=0

        # 檢查分組
        for p in current_round_players[:]:
            p.roll_dice()
            p.split_dice()
            if not p.validate_groups():
                print(f"{p.name} 分組無效，強制退出加賽。")
                current_round_players.remove(p)

        if len(current_round_players)==1:
            # 只剩一人 => 沒對決 => fold 或其他原因
            # 回傳空 set 表示沒實際最後對決
            return current_round_players[0], pot, current_round_players[0], set()

        # 計算勝率
        for p in current_round_players:
            _,_, p.win_rate= calculate_win_probability(p)

        # 下注
        active_players, pot= betting_phase(current_round_players, pot)
        if len(active_players)==1:
            # 沒有真正比對 => 回傳空 set
            return active_players[0], pot, active_players[0], set()

        # 正式比較
        compare_groups(active_players,1)
        compare_groups(active_players,2)
        max_score= max(p.round_score for p in active_players)
        new_tied= [p for p in active_players if p.round_score== max_score]

        # 組合2贏家 => 下一輪先行
        g2_winners= compare_groups(active_players,2)
        if len(g2_winners)>1:
            next_starter= random.choice(g2_winners)
        else:
            next_starter= g2_winners[0]

        if len(new_tied)==1:
            # 已產生唯一贏家 => 所有這輪(或之前輪)參與加賽的玩家都是 final_opponents
            final_winner= new_tied[0]
            return final_winner, pot, final_winner, all_tiebreak_players
        else:
            print("加賽結果仍然平手，繼續加賽...\n")
            # 新一輪 => 需要把 new_tied reorder
            current_round_players = reorder_players(new_tied, next_starter)

def display_table(players, pot, round_number, phase="",
                  final_winner=None, final_opponents=None):
    if final_opponents is None:
        final_opponents= set()

    print("\n"+"="*55)
    print(f"               階 段 顯 示  ( {phase})")
    print("="*55)
    print(f"回合數：{round_number}   |   底池：{pot} 點")
    print("-"*55)
    print(f"{'player':<8} | {'point':<6} | {'dice':<15} | {'first':<7} | {'second':<7}")
    print("-"*55)
    for p in players:
        mark_str= ""
        # 若該玩家在 final_opponents 裏，且不是 winner => [T]
        if p in final_opponents and p!= final_winner:
            mark_str+="[T]"
        if p== final_winner:
            mark_str+="[W]"

        disp_name= p.name+ mark_str
        print(f"{disp_name:<10} | {p.points:<6} | {str(p.dice):<15} | {str(p.group1):<7} | {str(p.group2):<7}")
    print("="*55+"\n")

def play_game():
    num_players= int(input("請輸入玩家總數 (2-4): "))
    players= [Player("1P", True)]
    players+= [Player(f"{i}P") for i in range(2, num_players+1)]

    for pl in players:
        pl.points=0
        pl.points-=10
    pot= 10* len(players)
    round_number=1
    next_starter= players[0]

    while True:
        # 每局先行：上一局(或加賽)的贏家
        players= reorder_players(players, next_starter)

        print(f"\n===== 第 {round_number} 局 =====\n")
        print(f"底池目前累積: {pot} 點")

        for pl in players:
            pl.actions_made=0
            pl.round_score=0

        # 擲骰
        for p in players:
            p.roll_dice()

        # 分組
        for p in players:
            p.split_dice()
            if not p.validate_groups():
                print(f"{p.name} 分組分錯了，出去是要被剁手的，下次給我注意點。遊戲結束。")
                return

        # 計算勝率
        for p in players:
            _,_, p.win_rate= calculate_win_probability(p)

        # 下注
        active_players, pot= betting_phase(players, pot)

        final_winner= None
        final_opponents= set()

        if len(active_players)==1:
            # 只剩一人 => 無平手 => no_tie_final
            winner = active_players[0]
            winner.points+= pot
            pot=0
            final_winner= winner
            next_starter= final_winner
            print(f"\n{winner.name} 獲得本局底池中的所有積分！")

            display_table(players, pot, round_number, phase="no_tie_final",
                          final_winner= final_winner, final_opponents= final_opponents)
        else:
            # 比較組合
            compare_groups(active_players,1)
            compare_groups(active_players,2)
            max_score= max(p.round_score for p in active_players)
            round_winners= [p for p in active_players if p.round_score== max_score]

            # 組合2贏家 => 下局先行
            g2_winners= compare_groups(active_players,2)
            if len(g2_winners)>1:
                next_starter= random.choice(g2_winners)
            else:
                next_starter= g2_winners[0]

            # 若只有1 => 無平手 => no_tie_final
            if len(round_winners)==1:
                winner= round_winners[0]
                winner.points+= pot
                pot=0
                final_winner= winner
                next_starter= final_winner
                print(f"\n{winner.name} 獲得本局底池中的所有積分！")

                display_table(players, pot, round_number, phase="no_tie_final",
                              final_winner= final_winner, final_opponents= final_opponents)
            else:
                # 有平手 => 進加賽 => final_result
                print("\n出現平手，進行加賽！")

                tie_winner, pot, _, final_opponents= tie_breaker(
                    round_winners, pot, round_number, next_starter
                )
                tie_winner.points+= pot
                pot=0
                final_winner= tie_winner
                next_starter= tie_winner
                print(f"\n加賽結束，{tie_winner.name} 獲得本局底池中的所有積分！")

                display_table(players, pot, round_number, phase="final_result",
                              final_winner= final_winner, final_opponents= final_opponents)

        print("\n所有玩家現有點數:")
        for pp in players:
            print(f"{pp.name}: {pp.points} 點")

        go_on= input("是否繼續遊玩？按 Enter 繼續，輸入其他鍵結束遊戲: ").strip()
        if go_on:
            print("遊戲結束，感謝遊玩！")
            break

        # 新局
        for pp in players:
            pp.points-=10
        pot+= 10* len(players)
        round_number+=1


if __name__=="__main__":
    play_game()

# 4knives: A Simple Python Game 

Welcome to 4knives, a rough and simple game created using python. The purpose of designing this program is partly to practice on my own, and partly because after starting college, I have much less time to reunite with my high school friends, so this serves as a way to reminisce about those times. This README provides a comprehensive overview of the project, including its features, usage, architecture, development process, references, and enhancements. 

## (1) 程式的功能 Features

4knives provides the following functionalities:

- **Entertainment**: 感覺被娛樂，如果你有被娛樂到的話
- **Education**: 體驗並了解一些非常基本的賭博邏輯，了解輕易涉賭可能造成的後果(負債)

## (2) 使用方式 Usage

Follow these rules and instructions to play 4knives:

### 1. Main Rules

1. 基本設置：
玩家數： 2 至 4 位玩家。
骰子： 每位玩家擁有 4 顆骰子。
遊戲目標： 目標是透過最佳的骰子組合獲得最高分數，贏得底池。

2. 骰子分組：
每位玩家需要將 4 顆骰子分為兩組：
組合1： 由兩顆骰子組成，為較弱的組合。
組合2： 另外兩顆骰子，必須比組合1強。

3. 組合大小：
對子： 兩顆骰子點數相同（例如 [6,6]）。所有對子按大小順序排列： [6,6] > [5,5] > [4,4] > …。
點數： 兩顆骰子點數不相同（例如 [6,5]）。比較兩顆骰子的總和。若總和相同，則比較最大的一顆骰子來決定大小。
每輪比賽會比較每位玩家的組合1與組合2的大小。

4. 下注階段：
每一局開始前，每位玩家都需將 10 積分放入底池。然後，玩家依序進行以下動作選擇：
加注(raise)： 可選擇 +20、+40 或 +70 積分，並放入底池(會自動判斷加注尺寸)。
跟注(call)： 同意前一位玩家的加注，並將相應分數放入底池。
過牌(pass)： 前面的玩家沒有人加注的情況下，若勝率較低，可以選擇跳過本輪。
棄牌(fold)： 放棄本輪遊戲，放入底池的積分不退還。

5. 比較手牌：
在所有玩家都已經平等下注後，比較每位玩家的組合1和組合2。在組合1(組合2)的比較中有最大組合的玩家得1分臨時分數。擁有最高臨時分數玩家贏得本輪的底池。最終勝者在新的一局首先動作。
如果出現平手(有2位以上的玩家臨時分數同樣高)，則進行加賽，直到分出勝負。由組合2較大者首先在新的一輪加賽中首先動作。

這些規則會在每一輪中重複，每位玩家的積分會根據贏得的底池來更新，並且最終贏家將獲得所有底池中的分數。

### 2. Instructions

Follow the lead after you start.

## (3) 程式的架構 Program Architecture

The project is organized as follows:

```
4knives/
├── class Player # 初始設定及有效分組
│   ├── def __init__
│   ├── def roll_dice
│   ├── def split_dice
│   ├── def group_strength
│   ├── def validate_groups  
├── def compare_groups
├── def calculate_win_probability
├── def computer_player_decision
├── def determine_bet_size
├── def reorder_players #使最終勝者下一局先行
├── def betting_phase
├── def tie_breaker
├── def display_table
├── def play_game
```

## (4) 開發過程 Development Process

The development of 4knives followed these steps:

1. **Ideation and Planning**: Write down the main rules and explanation for these rules.
2. **Implementation**: Provide GPT with guidelines to form the flowchart and build core functionalities.
3. **Testing**: Me as a player, after pain and tears, going through trial and error, to fix some problems with GPT. Below is one of the conversations with GPT(others deleted or not able to share):
                1.check for mistake-https://chatgpt.com/share/676b59cc-eacc-8000-aa41-969b28af9e4b
                

## (5) 參考資料來源 References

1.  ChatGPT - Assisted with documentation and architectural structuring of the project.

## (6) 未來可增強的內容 Future Enhancements 

Due to the lack of time and ability, this is a really rough game. The following modifications and enhancements are welcomed to be added to the project in the future:

### 視覺化
- 如提供的截圖檔案所示，也可以進行更多的美化。

### 自由下注
- 可以自己選擇下注尺寸

### 電腦玩家性格差異化
1. 可以輸入名字(例如高中同學)，並依據對他們的了解設定不同的下注策略(例如激進型、平衡型、保守型等)。
2. 隨著輸贏，到某個程度時可以讓電腦玩家"上頭"，做出更不理智的行為。
3. 可自由選擇要與幾位這幾種性格的玩家對戰。

We encourage further modifications and look forward to community contributions to improve 4knives further.

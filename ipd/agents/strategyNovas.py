# Estrategieas para o grupo nesse file implementar: per_cd, tf2t, hard_tft, slow_tft, gradual.


#First
class PerCD (Strategy):
    """ PerCD Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "PerCD"
        self.strategy = ["C", "D"]

#Second
class HardTitForTat (Strategy):
    """ Hard Tif for tat strategy 
    
    Will cooperate on the first turn.
    If the opponent has defected on the last or the second-last turn, will defect.
    Else, cooperate.

    Notes
    -----
    If defected, he will always defect one more time than the opponent.    
    """
    def __init__(self):
        super().__init__()
        self.strategy_name = "hard_tft"
        self.strategy = ["C", "D"]
        self.selected_strategy =  "C"

        self.game = Game("", "C", 3, "", "C", 3)
        self.last_game = Game("", "C", 3, "", "C", 3)
        self.second_last_game = Game("", "C", 3, "", "C", 3)


        self.other_last_strategy = "C"
        self.others = {}

        

    def update_game(self, aGame):
        """ Get a game """

        self.second_last_game = copy.copy(self.last_game)
        self.last_game = copy.copy(self.game)
        
        self.game = aGame
        self.update_memory(aGame)

    def select_game(self, other_player):
        """ Hard tif fot tat strategy """

        self.recall_games(other_player)

        if self.last_game.other_play == "D" or self.second_last_game.other_play == "D":
            self.selected_strategy = "D"
        else:
            self.selected_strategy = "C"

        return self.selected_strategy
    
    def recall_games(self, other_player):
        """ Recall last play from the opponent"""
        history =  self.others.get(other_player.name, [])
        
        if len(history) >= 2:
            self.second_last_game.other_play = history[-2]
            self.last_game.other_play = history[-1]
        elif len(history) == 1:
            self.second_last_game.other_play = "C"
            self.last_game.other_play = history[-1]
        else:
            self.second_last_game.other_play = "C"
            self.last_game.other_play = "C"


    def update_memory(self, aGame):
        if aGame.other_name not in self.others:
            self.others[aGame.other_name] = []
        self.others[aGame.other_name].append(aGame.other_play)

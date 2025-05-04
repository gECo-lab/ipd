# Estrategieas para o grupo nesse file implementar: per_cd, tf2t, hard_tft, slow_tft, gradual.


##First: PerCD

"""Irá para o arquivo ipd/ipd/agents/ipd_action_set.py :"""
class PerCD (Strategy):
    """ PerCD Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "PerCD"
        self.strategy = ["C", "D"]
        self.selected_strategy =  "C"

    def select_game(self):
        """ PerCD strategy """
        if self.selected_strategy == "C":
            self.selected_strategy = "D"
        else:
            self.selected_strategy = "C"

        return self.selected_strategy

    

##Second: HardTFT
 
"""Irá para o arquivo ipd/ipd/agents/ipd_action_set.py :"""
class HardTifForTat (Strategy):
    """ Hard Tif For Tat Strategy 
    
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

## Third: SlowTFT
"""Irá para o arquivo ipd/ipd/agents/ipd_action_set.py :"""

class SlowTifForTat (Strategy):
    """ Slow Tif For Tat Strategy 
    
    Cooperates the two first moves, then begin to defect after two consecutive defections of its opponent.
    Returns to cooperation after two consecutive cooperations of its opponent.
    
    """
    def __init__(self):
        super().__init__()
        self.strategy_name = "slow_tft"
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
        """ Slow tif fot tat strategy """

        self.recall_games(other_player)

        if self.last_game.other_play == "D" and self.second_last_game.other_play == "D":
            self.selected_strategy = "D"
        elif self.last_game.other_play == "C" and self.second_last_game.other_play == "C":  
            self.selected_strategy = "C"

        return self.selected_strategy
    
    def recall_games(self, other_player):
        """ Recall last two plays from the opponent"""
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

##Fourth: TF2t
"""Irá para o arquivo ipd/ipd/agents/ipd_action_set.py :"""

class TitFor2Tat (Strategy):
    """
    Tit For 2 Tat Strategy

    Cooperates the two first moves, then defects only if the opponent has defected during the two previous moves

    """

    def __init__(self):
        super().__init__()
        self.strategy_name = "tf2t"
        self.strategy = ["C", "D"]
        self.selected_strategy = "C"

        self.game = Game("", "C", 3, "", "C", 3)
        self.last_game = Game("", "C", 3, "", "C", 3)
        self.second_last_game = Game("", "C", 3, "", "C", 3)

        self.other_last_strategy = "C"
        self.others = {}

    def update_game(self, aGame):
        """Get a game"""
        self.second_last_game = copy.copy(self.last_game)
        self.last_game = copy.copy(self.game)
        
        self.game = aGame
        self.update_memory(aGame)

    def select_game(self, other_player):
        """Tif for 2 Tat Strategy"""

        self.recall_games(other_player)

        if self.last_game.other_play == "D" and self.second_last_game.other_play == "D":
            self.selected_strategy = "D"
        else:
            self.selected_strategy = "C"

        return self.selected_strategy

    def recall_games(self, other_player):
        """Recalls the last two plays from the opponent"""
        history = self.others.get(other_player.name, [])

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
        """Stores opponent's play history"""
        if aGame.other_name not in self.others:
            self.others[aGame.other_name] = []
        self.others[aGame.other_name].append(aGame.other_play)



## Fifth: Gradual
"""Irá para o arquivo ipd/ipd/agents/ipd_action_set.py :"""
class Gradual (Strategy):
    """
    Gradual Strategy

    Cooperates on the first move, then defect n times after nth defections of its opponent, and calms down with 2 cooperations (Beaufils et al. 1996).
    """
    def __init__(self):
        super().__init__()
        self.strategy_name = "gradual"
        self.strategy = ["C", "D"]
        self.selected_strategy = "C"

        self.game = Game("", "C", 3, "", "C", 3)
        self.last_game = Game("", "C", 3, "", "C", 3)
        self.second_last_game = Game("", "C", 3, "", "C", 3)

        self.other_last_strategy = "C"
        self.others = {}

        self.total_defections = {}
        self.remaining_punishments = {}
        self.cooling_down = {}
    
    def update_game(self, aGame):
        """Get a game"""
        self.second_last_game = copy.copy(self.last_game)
        self.last_game = copy.copy(self.game)
        
        self.game = aGame
        self.update_memory(aGame)

        name = aGame.other_name
        if name not in self.total_defections:
            self.total_defections[name] = 0
            self.remaining_punishments[name] = 0
            self.cooling_down[name] = False

        if aGame.other_play == "D":
            self.total_defections[name] += 1
            self.remaining_punishments[name] = self.total_defections[name]
            self.cooling_down[name] = False

        elif self.remaining_punishments[name] == 0 and not self.cooling_down[name]:
            history = self.others.get(name, [])
            if len(history) >= 2 and history[-1] == "C" and history[-2] == "C":
                self.cooling_down[name] = True
    

    def select_game(self, other_player):    
        """Gradual Strategy"""
        name = other_player.name
        self.recall_games(other_player)

        if name not in self.remaining_punishments:
            self.remaining_punishments[name] = 0
            self.cooling_down[name] = False

        if self.remaining_punishments[name] > 0:
            self.selected_strategy = "D"
            self.remaining_punishments[name] -= 1
        elif self.cooling_down[name]:
            self.selected_strategy = "C"
        else:
            self.selected_strategy = "C"

        return self.selected_strategy
        


    def recall_games(self, other_player):   
        """Recalls the last two plays from the opponent"""
        history = self.others.get(other_player.name, [])

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
        """Stores opponent's play history"""
        if aGame.other_name not in self.others:
            self.others[aGame.other_name] = []
        self.others[aGame.other_name].append(aGame.other_play)
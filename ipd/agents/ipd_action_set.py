# -*- coding: utf-8 -*-
""" Basic Strategy Class implementation """

import random
import copy


class Game:
    """ Class Representing a Game """

    def __init__(self, my_name=None, my_play=None, my_payoff=None,
                 other_name=None, other_play=None, other_payoff=None):
        self.my_name = my_name
        self.my_play = my_play
        self.my_payoff = my_payoff
        self.other_name = other_name
        self.other_play = other_play
        self.other_payoff = other_payoff


class Strategy:
    """ Implementation of the strategy class """
    def __init__(self):
        self.strategy_name = "general"
        self.strategy = "C"
        self.game = Game("", "C", 3, "", "C", 3)
        self.last_game = Game("", "C", 3, "", "C", 3)

    def select_game(self, other_player):
        return self.strategy

    def update_game(self, aGame):
        """ Get a game """
        self.last_game = copy.copy(self.game)
        self.game = aGame

    def name(self):
        return self.strategy_name


class AlwaysCooperate(Strategy):
    """ Always Cooperate Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "always_cooperate"
        self.strategy = "C"


class AlwaysDefect(Strategy):
    """ Never Cooperate Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "always_defect"
        self.strategy = "D"


class RandomPlay(Strategy):
    """ Cooperate randomly """
    def __init__(self):
        super().__init__()
        self.strategy_name = "random"
        self.strategy = ["D", "C"]

    def select_game(self, other_player):
        """ Random Strategy """
        return random.choice(self.strategy)


class SimpleTitForTat(Strategy):
    def __init__(self):
        super().__init__()
        self.strategy_name = "simpleTitForTat"
        self.other_last_strategy = "C"
        self.selected_strategy = "C"

    def select_game(self, other_player):
        """ Simple Tit for tat strategy """
        if self.last_game.other_play == "C":
            self.selected_strategy = "C"
        else:
            self.selected_strategy = "D"

        return self.selected_strategy
    
class TitForTat(Strategy):
    def __init__(self):
        super().__init__()
        self.strategy_name = "TitForTat"
        self.strategy = ["D", "C"]

        self.other_last_strategy = random.choice(self.strategy)
        self.selected_strategy = random.choice(self.strategy)
        self.others = {}

    def update_game(self, aGame):
        """ Get a game """
        self.last_game = copy.copy(self.game)
        self.game = aGame
        self.update_memory(aGame)

    def select_game(self, other_player):
        """ Tit for tat strategy """

        self.recall_games(other_player)
        if self.last_game.other_play == "C":
            self.selected_strategy = "C"
        else:
            self.selected_strategy = "D"

        return self.selected_strategy
    
    def recall_games(self, other_player):
        """ Recall the last play from the opponent"""
        strategy =  ["D", "C"]
        if other_player.name in self.others:
            self.last_game.other_play = self.others[other_player.name]
        else:
            #game = random.choice(["D","C"])
            game = "C"
            self.others[other_player.name] = game
            self.last_game.other_play = game
    
            #self.others[other_player.name] = "C"
            #self.last_game.other_play = "C"
    
            
    def update_memory(self, aGame):
        self.others[aGame.other_name] = aGame.other_play
 


class SimpleRancorous(Strategy):
    """ Simple Rancorous Strategy
        Agente always defects after somebody defects """
    def __init__(self):
        super().__init__()
        self.strategy_name = "simpleRancorous"
        self.other_last_strategy = "C"
        self.selected_strategy = "C"


    def select_game(self, other_player):
        """ Simple Rancorous Strategy """
        if self.last_game.other_play == "D":
            self.selected_strategy = "D"

        return self.selected_strategy
    

class Rancorous(Strategy):
    """ Simple Rancorous Strategy
        Agent always defects after somebody defects 
        Impl: Lucas 2023-10-25
    """
    def __init__(self):
        super().__init__()
        self.strategy_name = "Rancorous"
        self.other_last_strategy = "C"
        self.selected_strategy = "C"
        self.defectors = {}
        self.anyone_defected = False

    def update_game(self, aGame):
        """ Get a game """
        self.last_game = copy.copy(self.game)
        self.game = aGame
        self.update_memory(aGame)

    def select_game(self, other_player):
        """ Rancorous Strategy """
        self.recall_games(other_player)
        
        if self.anyone_defected:
            self.selected_strategy = "D"
        elif self.last_game.other_play == "D":
            self.selected_strategy = "D"
            self.anyone_defected = True
        else:
            self.selected_strategy = "C"
        
        return self.selected_strategy
    
    def recall_games(self, other_player):
        """ Recall the last play from the opponent"""
        
        if other_player.name in self.defectors:
            self.last_game.other_play = "D"
        else:
            self.last_game.other_play = "C"


    def update_memory(self, aGame):

        if aGame.other_play == "D":
            self.defectors[aGame.other_name] = aGame.other_play


class Generic(Strategy):
    """ Never Cooperate Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "always_defect"
        self.strategy = "D"


##Estrategieas para o grupo Nathan implementar: per_cd, tf2t, hard_tft, slow_tft, gradual.

#First PerCD
"""Nathan"""
class PerCD (Strategy):
   """ PerCD Strategy 
   Periodic Plays 'C' 'D'
   """
   def __init__(self):
       super().__init__()
       self.strategy_name = "PerCD"
       self.strategy = ["C", "D"]
       self.selected_strategy =  "C"

   def select_game(self, other_player):
       """ PerCD strategy """
       self.selected_strategy = "D" if self.selected_strategy == "C" else "C"
       
       return self.selected_strategy




##Second: HardTFT
""" Nathan"""
class HardTitForTat (Strategy):
   """ Hard Tit For Tat Strategy
  
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
       """ Hard tit for tat strategy """


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
"""Nathan"""

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


##FIM Estratégias grupo Nathan


#### Estrategias  Ariana
#Pavlov
#Começa cooperando e só retalia se o outro jogador jogar D,e depois volta a cooperar

class Pavlov (Strategy):
    """Pavlov strategy"""
    def __init__(self):
        super().__init__()
        self.strategy_name = "Pavlov"
        self.strategy = ["C", "D"]
        self.selected_strategy = "C"
        self.last_other_play=None #Deixa em aberto qual a primeira rodada do J2
        self.is_retaliating = False #True o jogador retalia na próxima rodada

    def update_game(self, aGame): #atualiza a ultima rodada do oponente
        self.last_other_play=aGame.Other_play
        if not self.is_retaliating and aGame.other_play=="D":
            self.is_retaliating = True

    def select_game(self):
        if self.is_retaliating:
            self.selected_strategy = "D"
            self.is_retaliating = False
        else:
            self.selected_strategy = "C"

        return self.selected_strategy



#Prober

class Prober(Strategy):
    def __init__(self):
        super().__init__()
        self.strategy_name = "Prober"
        self.strategy = ["C", "D"]
        self.selected_strategy = "D"
        self.other_play = []
        self.current_round = 0 
        self.back_strategy = TitForTat()

    def update_game(self, aGame):
        self.other_play.append(aGame.other_play)
        self.current_round += 1
    
    def select_game(self):
        if self.current_round == 0:
            self.strategy = "D"

        if self.current_round == 1 or self.current_round == 2:
            self.strategy = "C"

        if self.other_play[1] == "C" and self.other_play[2] == "C":
                self.strategy = "D"
        
        else:
            return self.back_strategy.select_game()
        
        return self.strategy

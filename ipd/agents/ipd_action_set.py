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



"""Nathan"""

class SlowTitForTat (Strategy):
   """ Slow Tit For Tat Strategy
  
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

class Pavlov(Strategy):
    """ Pavlov (Win-Stay, Lose-Shift) strategy
        Cooperates on the first move.
        If both players made the same move (CC or DD), repeats the same move.
        If the moves were different (CD or DC), switches.
        (Wedekind & Milinski 1996)
    """
    def __init__(self):
        super().__init__()
        self.strategy_name = "Pavlov"
        self.selected_strategy = "C"
        self.last_game = None

    def update_game(self, aGame):
        self.last_game = aGame

    def select_game(self, other_player):
        if self.last_game is None:
            self.selected_strategy = "C"
        else:
            my_last = self.last_game.my_play
            other_last = self.last_game.other_play

            if my_last == other_last:
                
                self.selected_strategy = my_last
            else:
                
                self.selected_strategy = "D" if my_last == "C" else "C"

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




class Prober(Strategy):
    """plays the sequence d,c,c, then always defects if its opponent has cooperated in the moves 2 and 3.
    Plays as tit_for_tat in other cases (Mathieu et al. 1999)
"""
    def __init__(self):
        super().__init__()
        self.strategy_name = "Prober"
        self.strategy = "D"
        self.other_play = []
        self.current_round = 0 
        self.back_strategy = TitForTat()
        self.status = {}

    def update_game(self, aGame):
        self.other_play.append(aGame.other_play)
        self.current_round += 1
    
    def select_game(self, other_player):
        if self.current_round == 0:
            self.strategy = "D"

        if self.current_round == 1 or self.current_round == 2:
            self.strategy = "C"

        if self.current_round == 3:
            if self.other_play[1] == "C" and self.other_play[2] == "C":
                self.strategy = "D"

        if self.current_round > 3:
            if self.strategy == "D":
                return "D"
        
            else:
                return self.back_strategy.select_game(other_player)
        
        return self.strategy
    
    def update_memory(self, aGame):
        """Stores opponent's play and statistics history"""    
        
        name = aGame.other_name

        if name not in self.others:
            self.others[name] = []

        self.others[name].append(aGame.other_play)

        if name not in self.stats:
            self.stats[name] = {'C': 0, 'D': 0}

        if self.last_game.other_play == "C":
            self.stats[name]['C'] += 1
        elif self.last_game.other_play == "D":
            self.stats[name]['D'] += 1



class Mistrust(Strategy):
  """
  Mistrust

  Mistrust
  Defect first turn, copy last opponent play
  """
  def __init__(self):
      super().__init__()
      self.strategy_name = "mis"
      self.strategy = ["C", "D"]
      self.selected_strategy = "D"
      self.others = {}

  def update_game(self, aGame):
      """ Get a game """
      self.second_last_game = copy.copy(self.last_game)
      self.last_game = copy.copy(self.game)
    
      self.game = aGame
      self.update_memory(aGame)

  def select_game(self, other_player):
       """ Mistrust """
       if self.last_game.other_play == "C":
           self.selected_strategy = "C"
       else:
           self.selected_strategy = "D"

       return self.selected_strategy
  
  def update_memory(self, aGame):
      """Stores opponent's play history"""
      if aGame.other_name not in self.others:
          self.others[aGame.other_name] = []
      self.others[aGame.other_name].append(aGame.other_play)

class SoftMajority(Strategy):
   """Soft Majority
    -------------------------
   Will count the number of cooperation and defection of the opponent.
   If they are an equal number or more cooperation, will cooperate.
   Else, will defect.


   Notes
   -----
   Will always cooperate on the first turn.
   Is the "cooperate" counterpart of the `Hard Majority` strategy.
   """
   def __init__(self):
      super().__init__()
      self.strategy_name = "SoftMajo"
      self.strategy = ["C", "D"]
      self.selected_strategy = "C"
      self.others = {}
      self.stats = {}

   def update_game(self, aGame):
      """ Get a game """
      self.second_last_game = copy.copy(self.last_game)
      self.last_game = copy.copy(self.game)
    
      self.game = aGame
      self.update_memory(aGame)
   
   def select_game(self, other_player):
        """Soft Majority """

        name = other_player.name

        if name not in self.stats:
            self.selected_strategy = "C"
            return self.selected_strategy

        cooperations = self.stats[name]['C']
        defects = self.stats[name]['D']

        if cooperations >= defects:
            self.selected_strategy = "C"
        else:
            self.selected_strategy = "D"

        return self.selected_strategy

   def update_memory(self, aGame):
        """Stores opponent's play and statistics history"""    
        
        name = aGame.other_name

        if name not in self.others:
            self.others[name] = []

        self.others[name].append(aGame.other_play)

        if name not in self.stats:
            self.stats[name] = {'C': 0, 'D': 0}

        if self.last_game.other_play == "C":
            self.stats[name]['C'] += 1
        elif self.last_game.other_play == "D":
            self.stats[name]['D'] += 1


class HardMajority(Strategy):
   """Hard Majority

    Defects on the first move and defects if the number of defections of the opponent is greater than
    or equal to the number of times she has cooperated. Else she cooperates (Axelrod 2006).
    -------------------------
   
   """
   def __init__(self):
      super().__init__()
      self.strategy_name = "HardMajo"
      self.strategy = ["C", "D"]
      self.selected_strategy = "D"
      self.others = {}
      self.stats = {}

   def update_game(self, aGame):
      """ Get a game """
      self.second_last_game = copy.copy(self.last_game)
      self.last_game = copy.copy(self.game)
    
      self.game = aGame
      self.update_memory(aGame)

   def select_game(self, other_player):
        """Hard Majority """

        name = other_player.name

        if name not in self.stats:
            self.selected_strategy = "D"
            return self.selected_strategy

        cooperations = self.stats[name]['C']
        defects = self.stats[name]['D']

        if cooperations > defects:
            self.selected_strategy = "C"
        else:
            self.selected_strategy = "D"

        return self.selected_strategy


   def update_memory(self, aGame):
        """Stores opponent's play and statistics history"""    
        
        name = aGame.other_name

        if name not in self.others:
            self.others[name] = []

        self.others[name].append(aGame.other_play)

        if name not in self.stats:
            self.stats[name] = {'C': 0, 'D': 0}

        if self.last_game.other_play == "C":
            self.stats[name]['C'] += 1
        elif self.last_game.other_play == "D":
            self.stats[name]['D'] += 1

class Mem(Strategy):
   """mem2 behaves like tit_for_tat: in the first two moves,
   and then shifts among three strategies all_d, tit_for_tat,
   tf2t according to the interaction with the opponent on last two moves
   """
   def __init__(self):
       super().__init__()
       self.strategy_name = "mem"
       self.strategy = "C"
       self.selected_strategy = "C"
       self.others = {}
       self.round = 0
       self.current_strategy = "TFT"

       self.tft = TitForTat()
       self.alld = AlwaysDefect()
       self.tf2t = TitFor2Tat()

   def update_game(self, aGame):
      """ Get a game """
      self.second_last_game = copy.copy(self.last_game)
      self.last_game = copy.copy(self.game)
    
      self.game = aGame
      self.update_memory(aGame)

      self.tft.update_game(aGame)
      self.alld.update_game(aGame)
      self.tf2t.update_game(aGame)

   def select_play(self, other_player):
       """Select a strategy for round"""
       
       if self.round != 0:
           self.round -=1
           return self.current_strategy

       last_two = self.opponent_last_plays(other_player, n=2, default="C")

       if last_two[0] == "C" and last_two[1] == "C":
          self.round = 2
          self.current_strategy = "TFT"

       elif last_two[0] == "D" and last_two[1] == "D":
          self.round = 2
          self.current_strategy = "ALLD"
      
       elif last_two[0] == "D" or last_two[1] == "D":
          self.round = 2
          self.current_strategy = "TF2T"
       
       self.selected_strategy = self.current_strategy
       return self.current_strategy

   def select_game(self, other_player):
       """Mem strategy"""

       if self.current_strategy == "TFT":
          self.selected_strategy = self.tft.select_game(other_player)
       elif self.current_strategy == "ALLD":
          self.selected_strategy = self.alld.select_game(other_player)
       elif self.current_strategy == "TF2T":
          self.selected_strategy = self.tf2t.select_game(other_player)

       return self.selected_strategy   
   
   def update_memory(self, aGame):
      """Stores opponent's play history"""
      if aGame.other_name not in self.others:
          self.others[aGame.other_name] = []
      self.others[aGame.other_name].append(aGame.other_play)

class Proba(Strategy):
    """
    Proba strategy
    --------------
    A probabilistic strategy that adjusts its actions based on the previous actions of both players.

    It uses four probabilities:
      - p1: Prob of cooperating after (C, C)
      - p2: Prob of cooperating after (C, D)
      - p3: Prob of cooperating after (D, C)
      - p4: Prob of cooperating after (D, D)

    Attributes:
    -----------
    - first: Action on the first turn ('C' or 'D')
    - my_prev, its_prev: store last moves for each opponent
    - stats: dictionary with last moves by opponent
    """
    def __init__(self, first, p1, p2, p3, p4, name=None):
        super().__init__()
        self.strategy_name = "Proba"
        self.first = first
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        #self.strategy_name = name if name else f"proba{first}_{p1:.1f}_{p2:.1f}_{p3:.1f}_{p4:.1f}"
        self.stats = {}  # Guarda histórico de cada oponente

    def update_game(self, aGame):
        """Atualiza a memória da última jogada"""
        self.second_last_game = copy.copy(self.last_game)
        self.last_game = copy.copy(self.game)
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}
        self.stats[name]["its_prev"] = aGame.other_play
        self.stats[name]["my_prev"] = aGame.my_play  # Jogada na rodada anterior

    def select_game(self, other_player):
        """Decide a próxima jogada"""
        name = other_player.name

        if name not in self.stats or self.stats[name]["my_prev"] is None:
            return self.first  

        my_prev = self.stats[name]["my_prev"]
        its_prev = self.stats[name]["its_prev"]

        rnd = random.uniform(0, 1)

        if my_prev == "C" and its_prev == "C":
            return "C" if rnd < self.p1 else "D"

        if my_prev == "C" and its_prev == "D":
            return "C" if rnd < self.p2 else "D"

        if my_prev == "D" and its_prev == "C":
            return "C" if rnd < self.p3 else "D"

        # Caso (D, D)
        return "C" if rnd < self.p4 else "D"


class ZeroDeterminant(Strategy):
    """
    Base class for memory-one Zero-Determinant (ZD) strategies in the
    Iterated Prisoner's Dilemma (IPD).

    A ZD strategy is defined by five cooperation probabilities:
        p0 : probability of cooperating in the first round against a given opponent
        p1 : probability of cooperating after CC
        p2 : probability of cooperating after CD
        p3 : probability of cooperating after DC
        p4 : probability of cooperating after DD

    Here, each two-letter state is written from this player's perspective:
        CC -> both players cooperated in the previous round
        CD -> this player cooperated and the opponent defected
        DC -> this player defected and the opponent cooperated
        DD -> both players defected

    This class stores opponent-specific memory, updates the last observed state
    after each interaction, and uses the corresponding conditional probability
    to choose the next action. Subclasses must implement the parameterization
    that determines p1, p2, p3, and p4.
    """

    def __init__(self):
        super().__init__()

        self.strategy_name = "ZD"
        self.strategy = ["C", "D"]

        # Payoffs matrix
        self.payoff_matrix = {
            "R": 3,
            "S": 0,
            "T": 5,
            "P": 1
        }

        # Memory
        self.stats = {}

        # First meet probability
        self.p0 = None

        # memory-1
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None

    def probability_validate(self, valor, probability):
        """
        Compute and validate the full set of ZD probabilities.

        This method must be called at the end of each subclass constructor
        after all free parameters have been assigned. It computes
        p1, p2, p3, and p4 through `compute()`, validates p0 through p4,
        and stores them as floats.
        """
        
        if valor is None:
            raise ValueError(f"{probability} not defined.")
        if not (0.0 <= float(valor) <= 1.0):
            raise ValueError(f"{probability} = {valor} out of [0,1].")

    def probabilities(self):

        p1, p2, p3, p4 = self.compute()

        self.probability_validate(self.p0, "p0")
        self.probability_validate(p1, "p1")
        self.probability_validate(p2, "p2")
        self.probability_validate(p3, "p3")
        self.probability_validate(p4, "p4")

        self.p0 = float(self.p0)
        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)
        self.p4 = float(p4)

    def compute(self):
        """
        Compute the conditional cooperation probabilities of the strategy.

        Returns
        -------
        list[float]
            A list in the form [p1, p2, p3, p4].

        Notes
        -----
        This method must be implemented by subclasses.
        """

    def vetor_p(self):
        """ 
        Return the memory-one cooperation vector.
        """

        return (self.p1, self.p2, self.p3, self.p4)

    def test(self):
        """
        Return a compact diagnostic summary of the strategy parameters.

        Returns
        -------
        dict
            A dictionary containing the strategy name, p0, the memory-one
            vector p, and the payoff matrix. If available, additional
            parameters such as chi and phi are also included.
        """

        info = {
            "strategy_name": self.strategy_name,
            "p0": self.p0,
            "p": self.vetor_p(),
            "payoff_matrix": self.payoff_matrix
        }

        if hasattr(self, "chi"):
            info["chi"] = self.chi
        if hasattr(self, "phi"):
            info["phi"] = self.phi

        return info

    def update_game(self, aGame):
        self.last_game = copy.copy(getattr(self, "game", None))
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}

        self.stats[name]["my_prev"] = aGame.my_play
        self.stats[name]["its_prev"] = aGame.other_play

    def cooperation(self, my_prev, its_prev):
        """
        Return the probability of cooperating given the previous state.

        Parameters
        ----------
        my_prev : str
            This player's previous action, expected to be "C" or "D".
        its_prev : str
            Opponent's previous action, expected to be "C" or "D".

        Returns
        -------
        float
            The corresponding cooperation probability among p1, p2, p3, p4.
        """

        if my_prev == "C" and its_prev == "C":
            return self.p1
        elif my_prev == "C" and its_prev == "D":
            return self.p2
        elif my_prev == "D" and its_prev == "C":
            return self.p3
        elif my_prev == "D" and its_prev == "D":
            return self.p4
        else:
            raise ValueError(f"Estado inválido: my_prev={my_prev}, its_prev={its_prev}")

    def select_game(self, other_player):
        name = other_player.name
        state = self.stats.get(name)

        if state is None or state["my_prev"] is None:
            return "C" if random.random() < self.p0 else "D"

        prob = self.cooperation(
            state["my_prev"],
            state["its_prev"]
        )

        return "C" if random.random() < prob else "D"
    

class ZDEqualizer(ZeroDeterminant):
    """
    Equalizer Zero-Determinant strategy.

    An equalizer strategy is designed to fix the opponent's long-run
    expected payoff at a specific value, regardless of the opponent's
    memory-one strategy, provided the underlying theoretical assumptions
    hold.

    This implementation uses p0, p1, and p4 as free inputs, and computes
    p2 and p3 from the Press and Dyson equalizer equations.
    """

    def __init__(self):
        """
        Initialize a fixed equalizer strategy.

        The free 'livre' parameters are chosen internally and the remaining
        conditional probabilities are computed and validated.
        """
        
        super().__init__()

        self.strategy_name = "ZD_Equalizer"

        self.p0 = 1.0
        self._p1_livre = 0.7
        self._p4_livre = 0.1

        self.probabilities()


    def compute(self):
        """
        Compute the equalizer probability vector.

        Returns
        -------
        list[float]
            The list [p1, p2, p3, p4] implied by the equalizer formulas.

        Raises
        ------
        ValueError
            If the payoff structure makes the equalizer formula undefined.
        """
                
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        p1 = self._p1_livre
        p4 = self._p4_livre

        p2 = (p1 * (T - P) - (1 + p4) * (T - R)) / (R - P)
        p3 = ((1 - p1) * (P - S) + p4 * (R - S)) / (R - P)

        return [p1, p2, p3, p4]

    def score_imposed(self):
        """
        Compute the payoff level imposed on the opponent.

        Returns
        -------
        float
            The long-run payoff that the equalizer strategy is intended
            to force on the opponent.

        Raises
        ------
        ValueError
            If the expression is undefined because the denominator is zero.

        Press & Dyson, Eq. (9)
        """

        R = self.payoff_matrix["R"]
        P = self.payoff_matrix["P"]

        denom = (1 - self.p1) + self.p4
        if denom == 0:
            raise ValueError("the denominator is zero in score_imposed().")

        return ((1 - self.p1) * P + self.p4 * R) / denom
    
class ZDExtortion(ZeroDeterminant):
    """
    
    Extortionate Zero-Determinant strategy.

    An extortion strategy enforces a linear relation between the long-run
    payoffs of the two players, making any gain above the punishment payoff
    P disproportionately favor the extortioner.

    This implementation follows the Press and Dyson parameterization,
    using an extortion factor chi >= 1 and a scaling factor phi within
    its feasible range.
    
    chi = extortion factor >= 1
    phi = midpoint
    """

    def __init__(self):
        """
        Initialize a fixed extortionate strategy.

        The strategy uses a preset extortion factor chi, computes the
        maximum feasible phi, sets phi at the midpoint of its admissible
        range, and then computes the memory-one probabilities.
        """

        super().__init__()

        self.strategy_name = "ZD_Extortion"

        self.p0 = 1.0
        self.chi = 3.0

        phi_max = self.phi_max()
        self.phi = phi_max / 2.0

        if not (0.0 < self.phi <= phi_max):
            raise ValueError(
                f"phi = {self.phi} is outside the feasible range (0, {phi_max}]."
            )
        
        self.probabilities()


    def phi_max(self):
        """
        Compute the maximum feasible value of phi.

        Returns
        -------
        float
            The upper bound of the admissible interval for phi.
        """

        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        return (P - S) / ((P - S) + self.chi * (T - P))

    def compute(self):
        """
        Compute the extortionate probability vector.

        Returns
        -------
        list[float]
            The list [p1, p2, p3, p4] implied by the extortion formulas.

        Raises
        ------
        """

        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        chi = self.chi
        phi = self.phi

        p1 = 1 - phi * (chi - 1) * ((R - P) / (P - S))
        p2 = 1 - phi * (1 + chi * ((T - P) / (P - S)))
        p3 = phi * (chi + ((T - P) / (P - S)))
        p4 = 0.0

        return [p1, p2, p3, p4]

    def extortionate(self, s_x, s_y):
        """
        Evaluate the extortion relation for a pair of payoffs.

        Parameters
        ----------
        s_x : float
            Long-run payoff of the extortion strategy.
        s_y : float
            Long-run payoff of the opponent.

        Returns
        -------
        tuple[float, float]
            A pair (lhs, rhs) corresponding to:

                lhs = s_x - P
                rhs = chi * (s_y - P)

            These two values should be equal when the extortion relation
            holds exactly.
        """
                
        P = self.payoff_matrix["P"]
        lhs = s_x - P
        rhs = self.chi * (s_y - P)
        return lhs, rhs
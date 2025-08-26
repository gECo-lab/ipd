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
    """Base strategy class for Prisoner's Dilemma agents."""

    def __init__(self):
        self.strategy_name = "general"
        self.strategy = "C"
        self.game = Game("", "C", 3, "", "C", 3)
        self.last_game = Game("", "C", 3, "", "C", 3)
        self.others = {} 

    def select_game(self, other_player):
        """Decide the play"""
        return self.strategy

    def update_game(self, aGame):
        """Update the last play"""
        self.last_game = copy.copy(self.game)
        self.game = aGame

    def name(self):
        """Return strategy name"""
        return self.strategy_name

    def opponent_last_plays(self, other_player, n=2, default = "C"):
        """Retorna as últimas n jogadas do oponente, preenchidas com `default`,
        n é o tamanho das jogadas anteriores que a estratégia precisa acessar
        """
        history = self.others.get(other_player.name, [])
        stand_history = [default] * n + history
        
        return stand_history[-n:] 

class AlwaysCooperate(Strategy):
    """ Always Cooperate Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "always_cooperate"
        self.strategy = "C"

    def select_game(self, other_player):
        return "C"


class AlwaysDefect(Strategy):
    """ Never Cooperate Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "always_defect"
        self.strategy = "D"

    def select_game(self, other_player):
        return "D"

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

class PerCD (Strategy):
   """ PerCD Strategy """
   def __init__(self):
       super().__init__()
       self.strategy_name = "PerCD"
       self.strategy = ["C", "D"]
       self.selected_strategy =  "C"

   def select_game(self, other_player):
       """ PerCD strategy """
       self.selected_strategy = "D" if self.selected_strategy == "C" else "C"
       
       return self.selected_strategy

class HardTitForTat (Strategy):
   """ Hard Tif For Tat Strategy
  
   Will cooperate on the first turn.
   If the opponent has defected on the last or the second-last turn, will defect.
   Else, cooperate.

   Notes
   -----
   Nova memória.   
   """
   def __init__(self):
       super().__init__()
       self.strategy_name = "hard_tft"
       self.strategy = ["C", "D"]
       self.selected_strategy =  "C"

       self.others = {}

   def update_game(self, aGame):
       """ Get a game """

       self.last_game = copy.copy(self.game)
      
       self.game = aGame
       self.update_memory(aGame)


   def select_game(self, other_player):
       """ Hard tif fot tat strategy """

       last_two = self.opponent_last_plays(other_player, n=2 , default="C"  )


       if "D" in last_two:
           self.selected_strategy = "D"
       else:
           self.selected_strategy = "C"


       return self.selected_strategy
  
   def update_memory(self, aGame):
       if aGame.other_name not in self.others:
           self.others[aGame.other_name] = []
       self.others[aGame.other_name].append(aGame.other_play)

class SlowTitForTat (Strategy):
   """ Slow Tif For Tat Strategy
  
   Cooperates the two first moves, then begin to defect after two consecutive defections of its opponent.
   Returns to cooperation after two consecutive cooperations of its opponent.
  
   """
   def __init__(self):
       super().__init__()
       self.strategy_name = "slow_tft"
       self.strategy = ["C", "D"]
       self.selected_strategy =  "C"
      
       self.others = {}

   def update_game(self, aGame):
       """ Get a game """
       
       self.last_game = copy.copy(self.game)
      
       self.game = aGame
       self.update_memory(aGame)

   def select_game(self, other_player):
       """ Slow tif fot tat strategy """
       
       history = self.others.get(other_player.name, [])

       if len(history) < 2:
            self.selected_strategy = "C"
       else:
            last_two = self.opponent_last_plays(other_player, n=2, default="C")
            if last_two == ["D", "D"]:
                self.selected_strategy = "D"
            elif last_two == ["C", "C"]:
                self.selected_strategy = "C"

       return self.selected_strategy
  
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

       self.others = {}
    
   def update_game(self, aGame):
       """ Get a game """
       
       self.last_game = copy.copy(self.game)
      
       self.game = aGame
       self.update_memory(aGame)



   def select_game(self, other_player):
       """Tif for 2 Tat Strategy"""
       last_two = self.opponent_last_plays(other_player, n=2, default="C")

       if last_two == ["D", "D"]:
           self.selected_strategy = "D"
       else:
           self.selected_strategy = "C"

       return self.selected_strategy

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

class DeterminantZero (Strategy):

   def __init__(self,):
      super().__init__()
      self.strategy_name = "ZD"
      self.strategy = ["C", "D"]
      self.first = "C"
      #self.alpha = alpha
      #self.beta = beta
      #self.gamma = gamma
      self.payoff_matrix ={ "R": 3, "S": 0, "T": 5,"P": 1}

      self.stats = {}

      self.p1, self.p2, self.p3, self.p4 = self.computar()

   def update_game(self, aGame):
        """Atualiza a memória da última jogada"""
        self.last_game = copy.copy(self.game)
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}

        self.stats[name]["its_prev"] = aGame.other_play
        self.stats[name]["my_prev"] = aGame.my_play 

   def computar(self):
    # implementar fórmula Press & Dyson
    return [0.8, 0.3, 0.4, 0.1]
   
   def select_game(self, other_player):
    name = other_player.name

    if name not in self.stats or self.stats[name]["my_prev"] is None:
        return self.first

    my_prev = self.stats[name]["my_prev"]
    its_prev = self.stats[name]["its_prev"]

    r = random.random()

    if my_prev == "C" and its_prev == "C":
        return "C" if r < self.p1 else "D"
    elif my_prev == "C" and its_prev == "D":
        return "C" if r < self.p2 else "D"
    elif my_prev == "D" and its_prev == "C":
        return "C" if r < self.p3 else "D"
    else:
        return "C" if r < self.p4 else "D"

   
class ZDEqualizer(DeterminantZero):
    
   def __init__(self):
       super().__init__()
       self.strategy_name = "equalizer"

       self.p1, self.p2, self.p3, self.p4 = self.computar()
       
   def computar(self):
       return [3/4, 1/4, 1/2, 1/4] #0.75, 0.25, 0.5, 0.25

class ZDExtortion(DeterminantZero):
    
    def __init__(self):
        super().__init__()
        self.strategy_name = "extortion"

        self.p1, self.p2, self.p3, self.p4 = self.computar()

    def computar(self):
        return [11/13, 1/2, 7/26, 0] 
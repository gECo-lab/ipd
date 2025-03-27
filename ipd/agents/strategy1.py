import json

class Strategy:
    """Representa uma estratégia carregada de um arquivo externo."""
    
    def __init__(self, name, first_move, response_rules):
        self.name = name
        self.first_move = first_move
        self.response_rules = response_rules
        self.history = []

    def decide(self):
        """Decide a próxima jogada com base no histórico."""
        if not self.history:
            return self.first_move
        last_opponent_move = self.history[-1][1]
        return self.response_rules.get(last_opponent_move, "C")  # Default para "C" se não houver regra
    
    def update_history(self, my_move, opponent_move):
        """Atualiza o histórico de jogadas."""
        self.history.append((my_move, opponent_move))

    def reset(self):
        """Reseta o histórico da estratégia."""
        self.history = []



{
    "tft": {
        "first_move": "C",
        "response": {"C": "C", "D": "D"}
    },
    "allc": {
        "first_move": "C",
        "response": {"C": "C", "D": "C"}
    },
    "alld": {
        "first_move": "D",
        "response": {"C": "D", "D": "D"}
    },
    "pavlov": {
        "first_move": "C",
        "response": {"CC": "C", "CD": "D", "DC": "D", "DD": "D"}
    }
}


{
    "tft": {
        "first_move": "C",
        "mem_depth": 3,
        "strategy_lenght": 1,
        "condition_action": {"CCC": "C", 
                             "CCD": "D",
                             "CDC": "D",
                             "DCC": "C",
                             "CCC": "C"}
    },
    "tftt": {
        "first_move": "C",
        "mem_depth": 3,
        "strategy_lenght": 2,
        "condition_action": {"CCC": "CC", 
                             "CCD": "DD",
                             "CDC": "DD",
                             "DCC": "CC",
                             "CDD": "DD",
                             "DDC": "DD",
                             "DDD": "DD"}
    }
}

{
  "tftt": {
        "first_move": "C",
        "mem_depth": 3,
        "strategy_lenght": 2,
        "condition_action": {"CCCCCCCDDDCDCDDDCCCCCCCCC"}
    }
}

# CCCCCCCDDDCDCDDDCCCCCCCCC
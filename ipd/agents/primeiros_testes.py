#Estratégias em dados
strategies_data = {
    "tft": {
        "first_move": "c",
        "response": {"c": "c", "d": "d"},
    },
    "allc": {
        "first_move": "c",
        "response": {"c": "c", "d": "c"},
    },
    "alld": {
        "first_move": "d",
        "response": {"c": "d", "d": "d"},
    },
    "rn": {
        "first_move": "random",
        "response": {"c": "random", "d": "random"},
    },
    "tft^-1": {
        "first_move": "d",
        "response": {"c": "d", "d": "c"  } 
    },
    "grim": {
        "first_move": "c",
        "response": {"c": "c", "d": "d"  },
        "status_angry": False
        } 
}


#Agente
import random
def agente(strategy_data, hist_op):
    # Decisão da primeira jogada
    if not hist_op:
        if strategy_data["first_move"] == "random":
            return random.choice(["c", "d"])
        return strategy_data["first_move"]
   
   # Status 
    if "status_angry" in strategy_data:
        if not strategy_data["status_angry"] and "d" in hist_op:
            strategy_data["status_angry"] = True
        if strategy_data["status_angry"]:
            return "d"

    # Decisão com base no histórico do oponente
    last_move_op = hist_op[-1]
    response_action = strategy_data["response"][last_move_op]
    if response_action == "random":
        return random.choice(["c", "d"])
    return response_action

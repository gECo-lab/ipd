# Estratégias dos agentes em dados

#Ideias após 19/11
#IDEIAS, uso da memoria ("memory") para as definições do que o agente responde
#IDEIAS, up_memory para definir as modificações e o que interessa colocar na memoria do agente

strategies_data = {
    "tft": {
        "first_move": "C",
        "response": {"C": "C", "D": "D"},
        "memory": {},
        "up_memory": {},
    },
    "allc": {
        "first_move": "C",
        "response": {"C": "C", "D": "C"},
        "memory": {},
        "up_memory": {},
    },
    "alld": {
        "first_move": "D",
        "response": {"C": "D", "D": "D"},
        "memory": {},
        "up_memory": {},
    },
    "rn": {
        "first_move": "random",
        "response": {"C": "random", "D": "random"},
        "memory": {},
        "up_memory": {},
    },
    "tft^-1": {
        "first_move": "D",
        "response": {"C": "D", "D": "C"},
        "memory": {},
        "up_memory": {},
    },
    "grim": {
        "first_move": "C",
        "response": {"C": "C", "D": "D"},
        "memory": {},
        "up_memory": {},
        "status_angry": False
        }
}

def agente(strategy_data, hist_op):
    memory = strategy_data["memory"]

    if not hist_op:
        return strategy_data["first_move"]

    strategies_data["up_memory"](memory, hist_op)

    return strategies_data["response"](memory, hist_op)
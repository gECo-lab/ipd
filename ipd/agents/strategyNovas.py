# Estrategieas para o grupo nesse file implementar: per_cd, tf2t, hard_tft, slow_tft, gradual.


#First
class PerCD (Strategy):
    """ PerCD Strategy """
    def __init__(self):
        super().__init__()
        self.strategy_name = "PerCD"
        self.strategy = ["C", "D"]

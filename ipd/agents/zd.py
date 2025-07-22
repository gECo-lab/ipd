class DeterminatZero (Strategy):

   def __init__(self, alpha, beta, gamma, payoff_matrix):
      super().__init__()
      self.strategy_name = "ZD"
      self.strategy = ["C", "D"]
      self.first = "C"
      self.alpha = alpha
      self.beta = beta
      self.gamma = gamma
      self.payoff_matrix = payoff_matrix
      self.stats = {}

      self.p1, self.p2, self.p3, self.p4 = self.computar()

   def update_game(self, aGame):
        """Atualiza a memória da última jogada"""
        self.second_last_game = copy.copy(self.last_game)
        self.last_game = copy.copy(self.game)
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}
        self.stats[name]["its_prev"] = aGame.other_play
        self.stats[name]["my_prev"] = aGame.my_play 

   def computar(self):
        # Extrai os payoffs do dilema
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        Sx = [R, S, T, P]
        Sy = [R, T, S, P]

        # vetor αS_X + βS_Y + γ
        linear_combo = [
            self.alpha * Sx[i] + self.beta * Sy[i] + self.gamma
            for i in range(4)
        ]

        # normaliza para [0,1]
        min_v = min(linear_combo)
        max_v = max(linear_combo)
        probs = [(v - min_v) / (max_v - min_v + 1e-9) for v in linear_combo]

        return probs  # p1, p2, p3, p4


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


# Novo com base em Lin e Sun (2026)

class ZeroDeterminant(Strategy):
    """
    Classe base para estratégias ZD memória-1 no IPD.

    Estados do último lance:
        p1 -> P(C | CC)
        p2 -> P(C | CD)
        p3 -> P(C | DC)
        p4 -> P(C | DD)

    p0 = probabilidade de cooperar no primeiro encontro com cada oponente.
    """

    def __init__(self, payoff_matrix=None):
        super().__init__()

        self.strategy_name = "ZD"
        self.strategy = ["C", "D"]

        # Payoffs padrão do PD "convencional" de Press & Dyson
        self.payoff_matrix = payoff_matrix or {
            "R": 3,
            "S": 0,
            "T": 5,
            "P": 1
        }

        # Memória por oponente
        self.stats = {}

        # Primeiro lance: deve ser definido na subclasse
        self.p0 = None

        # Probabilidades memória-1: serão definidas na subclasse
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None

    def _finalizar_parametros(self):
        """
        Chamar no fim do __init__ da subclasse.
        Calcula p1..p4 e valida p0..p4.
        """
        if self.p0 is None:
            raise ValueError("A subclasse deve definir self.p0.")

        p1, p2, p3, p4 = self.computar()

        self._validar_probabilidade(self.p0, "p0")
        self._validar_probabilidade(p1, "p1")
        self._validar_probabilidade(p2, "p2")
        self._validar_probabilidade(p3, "p3")
        self._validar_probabilidade(p4, "p4")

        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)
        self.p4 = float(p4)

    def _validar_probabilidade(self, valor, nome):
        if not (0.0 <= valor <= 1.0):
            raise ValueError(f"{nome} = {valor} está fora de [0,1]. Estratégia inviável.")

    def computar(self):
        """
        Deve retornar [p1, p2, p3, p4].
        """
        raise NotImplementedError("A subclasse deve implementar computar().")

    def vetor_p(self):
        return (self.p1, self.p2, self.p3, self.p4)


    def update_game(self, aGame):

        self.last_game = copy.copy(getattr(self, "game", None))
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}

        self.stats[name]["my_prev"] = aGame.my_play
        self.stats[name]["its_prev"] = aGame.other_play


    def _prob_cooperar(self, my_prev, its_prev):
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
        """
        Primeiro encontro: usa p0.
        Depois: usa memória-1.
        """
        name = other_player.name
        state = self.stats.get(name)

        # Sem histórico com esse oponente
        if state is None or state["my_prev"] is None:
            return "C" if random.random() < self.p0 else "D"

        prob = self._prob_cooperar(
            state["my_prev"],
            state["its_prev"]
        )

        return "C" if random.random() < prob else "D"


class ZDEqualizer(ZeroDeterminant):
    """
    Equalizer: X fixa o score de Y.

    Parâmetros livres:
        p0 : cooperação no primeiro lance
        p1, p4 : escolhidos livremente, desde que gerem p2,p3 viáveis
    """

    def __init__(self, p0=1.0, p1=0.7, p4=0.1, payoff_matrix=None):
        super().__init__(payoff_matrix=payoff_matrix)

        self.strategy_name = "ZD-Equalizer"

        self.p0 = p0
        self._p1_livre = p1
        self._p4_livre = p4

        self._finalizar_parametros()

    def computar(self):
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        if R == P:
            raise ValueError("R não pode ser igual a P nas fórmulas do equalizer.")

        p1 = self._p1_livre
        p4 = self._p4_livre

        # Press & Dyson, Eq. (8)
        p2 = (p1 * (T - P) - (1 + p4) * (T - R)) / (R - P)
        p3 = ((1 - p1) * (P - S) + p4 * (R - S)) / (R - P)

        return [p1, p2, p3, p4]

    def score_imposto_ao_oponente(self):
        """
        Score que X força para Y.
        Press & Dyson, Eq. (9)
        """
        R = self.payoff_matrix["R"]
        P = self.payoff_matrix["P"]

        denom = (1 - self.p1) + self.p4
        if denom == 0:
            raise ValueError("Denominador nulo em score_imposto_ao_oponente().")

        return ((1 - self.p1) * P + self.p4 * R) / denom


class ZDExtortion(ZeroDeterminant):
    """
    Extortion de Press & Dyson.

    chi >= 1
    phi em (0, phi_max], onde:
        phi_max = (P-S) / ((P-S) + chi*(T-P))

    Se phi=None, usa o ponto médio da faixa viável.
    """

    def __init__(self, p0=1.0, chi=3.0, phi=None, payoff_matrix=None):
        super().__init__(payoff_matrix=payoff_matrix)

        self.strategy_name = "ZD-Extortion"

        if chi < 1:
            raise ValueError("chi deve ser >= 1.")

        self.p0 = p0
        self.chi = float(chi)

        phi_max = self.phi_max()
        self.phi = (phi_max / 2.0) if phi is None else float(phi)

        if not (0.0 < self.phi <= phi_max):
            raise ValueError(
                f"phi = {self.phi} fora da faixa viável (0, {phi_max}]."
            )

        self._finalizar_parametros()

    def phi_max(self):
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        if P <= S:
            raise ValueError("É preciso P > S para usar a forma extorsiva de Press & Dyson.")

        return (P - S) / ((P - S) + self.chi * (T - P))

    def computar(self):
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        chi = self.chi
        phi = self.phi

        if P <= S:
            raise ValueError("É preciso P > S para usar a forma extorsiva de Press & Dyson.")

        # Press & Dyson, Eq. (12)
        p1 = 1 - phi * (chi - 1) * ((R - P) / (P - S))
        p2 = 1 - phi * (1 + chi * ((T - P) / (P - S)))
        p3 = phi * (chi + ((T - P) / (P - S)))
        p4 = 0.0

        return [p1, p2, p3, p4]


class ZDExtortionPressDysonExample(ZDExtortion):
    """
    Exemplo numérico clássico citado no artigo:
        chi = 3
        phi = ponto médio da faixa viável

    Para T,R,P,S = 5,3,1,0, isso gera:
        (11/13, 1/2, 7/26, 0)
    """

    def __init__(self, p0=1.0, payoff_matrix=None):
        super().__init__(p0=p0, chi=3.0, phi=None, payoff_matrix=payoff_matrix)
        self.strategy_name = "ZD-Extortion-PressDyson"


# Segundo código


class ZeroDeterminant(Strategy):
    """
    Classe base para estratégias ZD memória-1 no IPD.

    p0 = probabilidade de cooperar no primeiro encontro
    p1 = P(C | CC)
    p2 = P(C | CD)
    p3 = P(C | DC)
    p4 = P(C | DD)
    """

    def __init__(self):
        super().__init__()
        self.strategy_name = "ZD"
        self.strategy = ["C", "D"]

        # payoffs padrão do PD de Press & Dyson
        self.payoff_matrix = {
            "R": 3,
            "S": 0,
            "T": 5,
            "P": 1
        }

        self.stats = {}

        # definidos nas subclasses
        self.p0 = None
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None

    def validar_probabilidade(self, valor, nome):
        if not (0.0 <= valor <= 1.0):
            raise ValueError(f"{nome} = {valor} está fora de [0,1].")

    def finalizar_parametros(self):
        """
        Chamar no final do __init__ da subclasse.
        """
        if self.p0 is None:
            raise ValueError("A subclasse deve definir p0.")

        p1, p2, p3, p4 = self.computar()

        self._validar_probabilidade(self.p0, "p0")
        self._validar_probabilidade(p1, "p1")
        self._validar_probabilidade(p2, "p2")
        self._validar_probabilidade(p3, "p3")
        self._validar_probabilidade(p4, "p4")

        self.p1 = float(p1)
        self.p2 = float(p2)
        self.p3 = float(p3)
        self.p4 = float(p4)

    def computar(self):
        raise NotImplementedError("A subclasse deve implementar computar().")

    def vetor_p(self):
        return [self.p1, self.p2, self.p3, self.p4]

    def update_game(self, aGame):
        self.last_game = copy.copy(getattr(self, "game", None))
        self.game = aGame

        name = aGame.other_name
        if name not in self.stats:
            self.stats[name] = {"my_prev": None, "its_prev": None}

        self.stats[name]["my_prev"] = aGame.my_play
        self.stats[name]["its_prev"] = aGame.other_play

    def prob_cooperar(self, my_prev, its_prev):
        if my_prev == "C" and its_prev == "C":
            return self.p1
        elif my_prev == "C" and its_prev == "D":
            return self.p2
        elif my_prev == "D" and its_prev == "C":
            return self.p3
        elif my_prev == "D" and its_prev == "D":
            return self.p4
        else:
            raise ValueError(f"Estado inválido: {my_prev}, {its_prev}")

    def select_game(self, other_player):
        name = other_player.name

        if name not in self.stats or self.stats[name]["my_prev"] is None:
            return "C" if random.random() < self.p0 else "D"

        my_prev = self.stats[name]["my_prev"]
        its_prev = self.stats[name]["its_prev"]

        prob = self._prob_cooperar(my_prev, its_prev)
        return "C" if random.random() < prob else "D"
    
class ZDEqualizer(ZeroDeterminant):
    def __init__(self):
        super().__init__()
        self.strategy_name = "equalizer"

        self.p0 = 1.0
        self.p1_livre = 0.7
        self.p4_livre = 0.1

        self.finalizar_parametros()

    def computar(self):
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        p1 = self.p1_livre
        p4 = self.p4_livre

        # Press & Dyson, Eq. (8)
        p2 = (p1 * (T - P) - (1 + p4) * (T - R)) / (R - P)
        p3 = ((1 - p1) * (P - S) + p4 * (R - S)) / (R - P)

        return [p1, p2, p3, p4]

    def score_imposto_ao_oponente(self):
        R = self.payoff_matrix["R"]
        P = self.payoff_matrix["P"]

        denom = (1 - self.p1) + self.p4
        if denom == 0:
            raise ValueError("Denominador nulo no score do oponente.")

        # Press & Dyson, Eq. (9)
        return ((1 - self.p1) * P + self.p4 * R) / denom
    
class ZDExtortion(ZeroDeterminant):
    def __init__(self):
        super().__init__()
        self.strategy_name = "extortion"

        
        self.p0 = 1.0
        self.chi = 3.0

        # usar o ponto médio na faixa viável
        self.phi = self.phi_max() / 2.0

        self.finalizar_parametros()

    def phi_max(self):
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        return (P - S) / ((P - S) + self.chi * (T - P))

    def computar(self):
        R = self.payoff_matrix["R"]
        S = self.payoff_matrix["S"]
        T = self.payoff_matrix["T"]
        P = self.payoff_matrix["P"]

        chi = self.chi
        phi = self.phi

        # Press & Dyson, Eq. (12)
        p1 = 1 - phi * (chi - 1) * ((R - P) / (P - S))
        p2 = 1 - phi * (1 + chi * ((T - P) / (P - S)))
        p3 = phi * (chi + ((T - P) / (P - S)))
        p4 = 0.0

        return [p1, p2, p3, p4]
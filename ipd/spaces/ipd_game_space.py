# -*- coding: utf-8 -*-
""" Basic IPD game space implementation """

#from kernel.space.basicSpaces import Space
from EcoSimpy import Space
# from EcoSimpy.agent import AgentCreator
# import random

# from ipd.agents import agents

class IpdGame(Space):
    """ Abstract Market """
    STRATEGY = ['C', 'D']
    PAYOFFS = {'CC': [3, 3],
               'CD': [0, 5],
               'DC': [5, 0],
               'DD': [1, 1]}

    def __init__(self, 
                 model, 
                 name, 
                 variables
                 ):
        """ Intialize abstract market """
        super().__init__(model, 
                         name, 
                         variables
                         )
        self.players = []
        #self.birth_counter = 0

    def update(self):
        """ Update game space """
        self.matching()
        self.play()

        # # if self.model.schedule.step > 0 and self.model.schedule.step % 100 == 0:
        # #     self.moran_step()

        # if self.model.schedule.step == 100:
        #     self.random_birth_death_test()
        
    def matching(self):
        """ Match the agents in pairs"""
        agents  = list(self.model.mixed_agents())
        half = len(agents) // 2
        players1 = agents[:half]
        players2 = agents[half:]
        self.players = zip(players1, players2)

    def play(self):
        """ Here the players play the game """
        for player1, player2 in self.players:
                    player1.select_game(player2)
                    player2.select_game(player1)
                    p1 = player1.play()
                    p2 = player2.play()
                    game = p1 + p2
                    player1.game_payoff(player2.name, p2,
                                        self.PAYOFFS[game][1],
                                        self.PAYOFFS[game][0]
                                        )
                    player2.game_payoff(player1.name, p1, 
                                        self.PAYOFFS[game][0],
                                        self.PAYOFFS[game][1]
                                        )

class IpdGame_BRxEUA(Space):
    """ Abstract Market """
    STRATEGY = ['C', 'D']
    PAYOFFS = {'CC': [3, 3],
               'CD': [0, 5],
               'DC': [5, 0],
               'DD': [1, 1]}

    def __init__(self, 
                 model, 
                 name, 
                 variables
                 ):
        """ Intialize abstract market """
        super().__init__(model, 
                         name, 
                         variables
                         )
        self.players = []
        #self.birth_counter = 0

    def update(self):
        """ Update game space """
        self.matching()
        self.play()

        # # if self.model.schedule.step > 0 and self.model.schedule.step % 100 == 0:
        # #     self.moran_step()

        # if self.model.schedule.step == 100:
        #     self.random_birth_death_test()
        
    def matching(self):
        """ Match the agents in pairs"""
        agents  = list(self.model.mixed_agents())
        half = len(agents) // 2
        players1 = agents[:half]
        players2 = agents[half:]
        self.players = zip(players1, players2)

    def play(self):
        """ Here the players play the game """
        for player1, player2 in self.players:
                    player1.select_game(player2)
                    player2.select_game(player1)
                    p1 = player1.play()
                    p2 = player2.play()
                    game = p1 + p2
                    player1.game_payoff(player2.name, p2,
                                        self.PAYOFFS[game][1],
                                        self.PAYOFFS[game][0]
                                        )
                    player2.game_payoff(player1.name, p1, 
                                        self.PAYOFFS[game][0],
                                        self.PAYOFFS[game][1]
                                        )


    # # def moran_step(self):
    # #     """ Moran process in each scenario """
    # #     reproducer = self.select_reproducer()

    # #     dead = self.select_dead()

    # #     child = self.clone_player(reproducer)

    # #     self.model.exit_simulation(dead.name)

    # #     self.model.enter_simulation(child.name, child)

    # def get_agent_def(self, agent_type):

    #     for agent_def in self.model.agents_original_def:
    #         if agent_def["agent_type"] == agent_type:
    #             return agent_def
    #     raise ValueError(f"Agent type {agent_type} not found.")

    # def select_reproducer(self):
    #     agents = list(self.model.agents.values())

    #     weights = []
    #     for agent in agents:
    #         fitness = max(agent.mean_payoff, 0.01)
    #         weights.append(fitness)

    #     return random.choices(agents, weights=weights, k=1)[0]

    # def select_dead(self):
    #     agents = list(self.model.agents.values())

    #     return random.choice(agents)
    
    # def create_child(self, parent):
    #     agent_def = self.get_agent_def(parent.type)

    #     self.birth_counter += 1
    #     agent_number = f"born_{self.birth_counter}"

    #     creator = AgentCreator(
    #         self.model,
    #         self.model.active_scenario,
    #         agent_def,
    #         agent_number
    #     )

    #     child = creator.new_agent

    #     self.model.active_scenario.initialize_one_agent_vars(child)

    #     return child
    
    # def moran_step(self):
    #     if len(self.model.agents) < 2:
    #         return

    #     reproducer = self.select_reproducer()
    #     dead = self.select_dead()

    #     while dead.name == reproducer.name:
    #         dead = self.select_dead()

    #     self.model.exit_simulation(dead.name)

    #     child = self.create_child(reproducer)


    # def get_agent_def(self, agent_type):
    #     for agent_def in self.model.agents_original_def:
    #         if agent_def["agent_type"] == agent_type:
    #             return agent_def

    #     raise ValueError(f"Agent type {agent_type} not found in model definitions.")

    # def random_birth_death_test(self):
    #     agents = list(self.model.agents.values())

    #     if len(agents) < 2:
    #         return

    #     parent = random.choice(agents)
    #     dead = random.choice(agents)

    #     while dead.name == parent.name:
    #         dead = random.choice(agents)

    #     print("\n--- BIRTH/DEATH TEST ---")
    #     print(f"Step: {self.model.schedule.step}")
    #     print(f"Before: {len(self.model.agents)} agents")
    #     print(f"Dead: {dead.name} ({dead.type})")
    #     print(f"Parent: {parent.name} ({parent.type})")

    #     self.model.exit_simulation(dead.name)

    #     agent_def = self.get_agent_def(parent.type)

    #     self.birth_counter += 1
    #     new_agent_number = f"born_{self.birth_counter}"

    #     creator = AgentCreator(
    #         self.model,
    #         self.model.active_scenario,
    #         agent_def,
    #         new_agent_number
    #     )

    #     child = creator.new_agent

    #     self.model.active_scenario.initialize_one_agent_vars(child)

    #     print(f"Born: {child.name} ({child.type})")
    #     print(f"After: {len(self.model.agents)} agents")
    #     print("------------------------\n")
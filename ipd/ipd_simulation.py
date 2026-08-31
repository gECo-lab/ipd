"""IPD-specific simulation configuration."""

import random as _random

from EcoSimpy import Simulation


DEFAULT_SEED = 42


class IPDSimulation(Simulation):
    """Simulation with an explicit, reproducible random-number generator.

    EcoSimpy currently seeds ``Simulation.random`` from the clock.  IPD keeps
    the library untouched and replaces that generator locally with one seeded
    from the value supplied by the experiment runner.
    """

    def __init__(
        self,
        app_dir,
        config_file="config.json",
        model_file="model.json",
        scenarios_file="scenarios.json",
        clean_run=True,
        seed=DEFAULT_SEED,
    ):
        super().__init__(
            app_dir,
            config_file,
            model_file,
            scenarios_file,
            clean_run,
        )
        self.seed = seed
        self.random = _random.Random(seed)

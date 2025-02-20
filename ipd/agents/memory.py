### Ideias para desenvolver.


class Memory:
    def __init__(self, size):
        self.size = size
        self.memory_dict = {f"agent_{i}": None for i in range(size)}
        self.memory_list = [None] * size

    def __repr__(self):
        return f"Memory(size={self.size}, memory_dict={self.memory_dict})"

    def insert_event(self, agent, event):
        if agent not in self.memory_dict:
            raise ValueError(f"Agent {agent} does not exist in memory.")

        if None not in self.memory_dict.values():
            # Memory is full, remove the first inserted event
            first_agent = next(iter(self.memory_dict))
            self.memory_dict[first_agent] = None

        self.memory_dict[agent] = event

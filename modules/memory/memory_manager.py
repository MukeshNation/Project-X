import json
import os


class MemoryManager:
    def __init__(self):
        self.memory_file = "data/memory.json"
        self.memory = self.load_memory()

    def load_memory(self):
        if not os.path.exists(self.memory_file):
            return {}

        with open(self.memory_file, "r") as file:
            try:
                return json.load(file)
            except:
                return {}

    def save_memory(self):
        with open(self.memory_file, "w") as file:
            json.dump(self.memory, file, indent=4)

    def get(self, key):
        return self.memory.get(key)

    def set(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def get_all(self):
        return self.memory

    def update(self, data):
        self.memory.update(data)
        self.save_memory()
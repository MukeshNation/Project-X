from queue import Queue


class TaskManager:

    def __init__(self):
        self.tasks = Queue()

    def add_task(self, task):
        self.tasks.put(task)
        return f"Task added: {task}"

    def next_task(self):
        if self.tasks.empty():
            return None
        return self.tasks.get()

    def has_tasks(self):
        return not self.tasks.empty()

    def clear(self):
        while not self.tasks.empty():
            self.tasks.get()

    def list_tasks(self):
        return list(self.tasks.queue)
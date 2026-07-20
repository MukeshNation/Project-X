from modules.actions.action_manager import ActionManager


class Executor:

    def __init__(self):
        self.actions = ActionManager()

    def execute(self, command: str):

        result = self.actions.execute(command)

        if result:
            return result

        return None
    
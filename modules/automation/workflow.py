from modules.automation.task_manager import TaskManager


class Workflow:

    def __init__(self):
        self.tasks = TaskManager()

    def website(self, description):

        self.tasks.clear()

        self.tasks.add_task("Create project folder")
        self.tasks.add_task("Generate HTML")
        self.tasks.add_task("Generate CSS")
        self.tasks.add_task("Generate JavaScript")
        self.tasks.add_task("Save files")
        self.tasks.add_task("Run website")

        return self.tasks.list_tasks()

    def python_project(self):

        self.tasks.clear()

        self.tasks.add_task("Create project")
        self.tasks.add_task("Generate Python")
        self.tasks.add_task("Save file")
        self.tasks.add_task("Run project")

        return self.tasks.list_tasks()
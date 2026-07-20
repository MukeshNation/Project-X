from modules.actions.app_actions import AppActions
from modules.actions.file_actions import FileActions
from modules.actions.terminal_actions import TerminalActions
from modules.coding.project_builder import ProjectBuilder
from modules.coding.deploy import DeployManager


apps = AppActions()
files = FileActions()
terminal = TerminalActions()
builder = ProjectBuilder()
deploy = DeployManager()


class ActionManager:

    def execute(self, command: str):

        cmd = command.lower().strip()

        # ---------- Terminal Commands ----------

        if cmd.startswith("terminal "):
            return terminal.run(command[9:].strip())

        if cmd.startswith("run python "):
            return terminal.python(command[11:].strip())

        # ---------- Apps ----------

        if cmd == "open terminal":
            return apps.open_terminal()

        if cmd == "open chrome" or cmd == "chrome":
            return apps.open_chrome()

        if cmd == "open finder" or cmd == "finder":
            return apps.open_finder()

        if cmd == "open gmail" or cmd == "gmail":
            return apps.open_gmail()

        if cmd == "open whatsapp" or cmd == "whatsapp":
            return apps.open_whatsapp()

        if cmd == "open vs code" or cmd == "vs code":
            return apps.open_vscode()

        # ---------- Google ----------

        if cmd.startswith("search google"):
            query = command[len("search google"):].strip()

            if query:
                return apps.google_search(query)

            return "Please enter a search query."

        # ---------- YouTube ----------

        if cmd.startswith("search youtube"):
            query = command[len("search youtube"):].strip()

            if query:
                return apps.youtube_search(query)

            return "Please enter a search query."

        # ---------- Files ----------

        if cmd.startswith("create folder "):
            return files.create_folder(command[14:].strip())

        if cmd.startswith("create file "):
            return files.create_file(command[12:].strip())

        if cmd.startswith("read file "):
            return files.read_file(command[10:].strip())

        # ---------- Website ----------

        if cmd.startswith("create website"):

            name = "MyWebsite"

            if "called" in cmd:
                name = command.split("called", 1)[1].strip().replace(" ", "_")

            return builder.create_website(name, command)

        if cmd.startswith("run website"):

            folder = command[len("run website"):].strip()

            if not folder:
                folder = "MyWebsite"

            return deploy.run_html(folder)

        # ---------- Git ----------

        if cmd == "git status":
            return terminal.git_status()

        if cmd == "git push":
            return deploy.git_push()

        if cmd == "git add":
            return terminal.git_add()

        if cmd.startswith("git commit "):
            message = command[len("git commit "):].strip()

            if not message:
                message = "Update"

            return terminal.git_commit(message)

        if cmd == "git pull":
            return terminal.git_pull()

        return None
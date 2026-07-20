from modules.actions.app_actions import AppActions
from modules.actions.file_actions import FileActions
from modules.coding.project_builder import ProjectBuilder

apps = AppActions()
files = FileActions()
builder = ProjectBuilder()


class ActionManager:

    def execute(self, command: str):

        cmd = command.lower().strip()

        # ---------- Apps ----------

        if "vs code" in cmd:
            return apps.open_vscode()

        if "chrome" in cmd:
            return apps.open_chrome()

        if "finder" in cmd:
            return apps.open_finder()

        if "terminal" in cmd:
            return apps.open_terminal()

        if "whatsapp" in cmd:
            return apps.open_whatsapp()

        if "gmail" in cmd or "email" in cmd:
            return apps.open_gmail()

        # ---------- Google ----------

        if cmd.startswith("search google"):
            query = cmd.replace("search google", "").strip()
            return apps.google_search(query)

        # ---------- YouTube ----------

        if cmd.startswith("search youtube"):
            query = cmd.replace("search youtube", "").strip()
            return apps.youtube_search(query)

        # ---------- Website ----------

        if cmd.startswith("create website"):

            name = "MyWebsite"

            if "called" in cmd:
                name = cmd.split("called")[-1].strip().replace(" ", "_")

            return builder.create_website(
                name,
                command
            )

        # ---------- Files ----------

        if cmd.startswith("create folder "):
            name = command[14:].strip()
            return files.create_folder(name)

        if cmd.startswith("create file "):
            name = command[12:].strip()
            return files.create_file(name)

        if cmd.startswith("delete file "):
            name = command[12:].strip()
            return files.delete_file(name)

        if cmd.startswith("list files"):
            return files.list_files()

        if cmd.startswith("rename file "):
            try:
                text = command[12:]
                old_name, new_name = text.split(" to ")
                return files.rename(
                    old_name.strip(),
                    new_name.strip()
                )
            except Exception:
                return "Use: rename file old.txt to new.txt"

        return None
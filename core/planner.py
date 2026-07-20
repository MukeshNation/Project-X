from core.logic import Logic


class Planner:

    def __init__(self):
        self.logic = Logic()

    def plan(self, command: str):

        intent = self.logic.detect(command)

        plans = {
            "website": [
                "create_project",
                "generate_html",
                "generate_css",
                "generate_js",
                "save_files",
                "run_website"
            ],

            "run_website": [
                "run_website"
            ],

            "create_folder": [
                "create_folder"
            ],

            "create_file": [
                "create_file"
            ],

            "read_file": [
                "read_file"
            ],

            "google": [
                "google_search"
            ],

            "youtube": [
                "youtube_search"
            ],

            "git": [
                "git_command"
            ],

            "terminal": [
                "terminal_command"
            ],

            "python": [
                "python_command"
            ],

            "chat": [
                "chat"
            ]
        }

        return plans.get(intent, ["chat"])
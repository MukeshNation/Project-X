import subprocess
from pathlib import Path


class TerminalActions:

    def run(self, command: str):

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            output = result.stdout.strip()

            if not output:
                output = result.stderr.strip()

            return output or "Done."

        except Exception as e:
            return str(e)

    def python(self, file):

        return self.run(f'python "{file}"')

    def pip_install(self, package):

        return self.run(f"pip install {package}")

    def npm_install(self):

        return self.run("npm install")

    def npm_start(self):

        return self.run("npm start")

    def npm_dev(self):

        return self.run("npm run dev")

    def git_status(self):

        return self.run("git status")

    def git_add(self):

        return self.run("git add .")

    def git_commit(self, message):

        return self.run(f'git commit -m "{message}"')

    def git_push(self):

        return self.run("git push")

    def git_pull(self):

        return self.run("git pull")

    def open_folder(self, folder):

        path = Path(folder)

        if not path.exists():
            return "Folder not found."

        subprocess.run(["open", str(path)])

        return "Folder opened."

    def run_html(self, folder):

        index = Path(folder) / "index.html"

        if not index.exists():
            return "index.html not found."

        subprocess.run(["open", str(index)])

        return "Website launched."

    def run_python_project(self, folder):

        path = Path(folder)

        if not path.exists():
            return "Folder not found."

        return self.run(
            f'cd "{folder}" && python app.py'
        )

    def run_streamlit(self, folder):

        return self.run(
            f'cd "{folder}" && streamlit run app.py'
        )

    def run_react(self, folder):

        return self.run(
            f'cd "{folder}" && npm install && npm start'
        )

    def run_next(self, folder):

        return self.run(
            f'cd "{folder}" && npm install && npm run dev'
        )
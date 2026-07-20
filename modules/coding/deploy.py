import subprocess
import webbrowser
from pathlib import Path


class DeployManager:

    def run_command(self, command, cwd=None):

        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return result.stdout.strip() or "Done."

        return result.stderr.strip()

    def run_html(self, folder):

        index = Path(folder) / "index.html"

        if not index.exists():
            return "index.html not found."

        webbrowser.open(index.resolve().as_uri())

        return "Website opened."

    def run_python(self, folder):

        return self.run_command(
            "python app.py",
            cwd=folder
        )

    def run_streamlit(self, folder):

        return self.run_command(
            "streamlit run app.py",
            cwd=folder
        )

    def run_react(self, folder):

        subprocess.Popen(
            "npm install && npm start",
            shell=True,
            cwd=folder
        )

        webbrowser.open("http://localhost:3000")

        return "React project starting..."

    def run_next(self, folder):

        subprocess.Popen(
            "npm install && npm run dev",
            shell=True,
            cwd=folder
        )

        webbrowser.open("http://localhost:3000")

        return "Next.js project starting..."

    def git_push(self):

        self.run_command("git add .")
        self.run_command('git commit -m "Auto Update"')

        return self.run_command("git push")
import subprocess
import webbrowser
from urllib.parse import quote


class AppActions:

    def open_vscode(self):
        subprocess.run(["open", "-a", "Visual Studio Code"])
        return "Opening Visual Studio Code."

    def open_chrome(self):
        subprocess.run(["open", "-a", "Google Chrome"])
        return "Opening Google Chrome."

    def open_finder(self):
        subprocess.run(["open", "."])
        return "Opening Finder."

    def open_gmail(self):
        subprocess.run([
            "open",
            "https://mail.google.com"
        ])
        return "Opening Gmail."

    def open_terminal(self):
        subprocess.run(["open", "-a", "Terminal"])
        return "Opening Terminal."

    def open_whatsapp(self):
        subprocess.run(["open", "-a", "WhatsApp"])
        return "Opening WhatsApp."

    def google_search(self, query):
        webbrowser.open(
            f"https://www.google.com/search?q={quote(query)}"
        )
        return f"Searching Google for '{query}'."

    def youtube_search(self, query):
        webbrowser.open(
            f"https://www.youtube.com/results?search_query={quote(query)}"
        )
        return f"Searching YouTube for '{query}'."
class Logic:

    def detect(self, message: str):

        msg = message.lower()

        if "create website" in msg:
            return "website"

        if "run website" in msg:
            return "run_website"

        if "create folder" in msg:
            return "create_folder"

        if "create file" in msg:
            return "create_file"

        if "read file" in msg:
            return "read_file"

        if "search google" in msg:
            return "google"

        if "search youtube" in msg:
            return "youtube"

        if "git" in msg:
            return "git"

        if "terminal " in msg:
            return "terminal"

        if "python" in msg:
            return "python"

        return "chat"
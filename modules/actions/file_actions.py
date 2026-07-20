from pathlib import Path
import shutil


class FileActions:

    def create_folder(self, folder_name):
        Path(folder_name).mkdir(parents=True, exist_ok=True)
        return f"Folder '{folder_name}' created."

    def create_file(self, file_path, content=""):
        path = Path(file_path)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return f"File '{file_path}' created."

    def read_file(self, file_path):
        path = Path(file_path)

        if not path.exists():
            return "File not found."

        return path.read_text(encoding="utf-8")

    def write_file(self, file_path, content):
        path = Path(file_path)

        path.write_text(content, encoding="utf-8")

        return f"Saved '{file_path}'."

    def delete_file(self, file_path):
        path = Path(file_path)

        if not path.exists():
            return "File not found."

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

        return f"Deleted '{file_path}'."

    def rename(self, old_path, new_path):
        old = Path(old_path)

        if not old.exists():
            return "File not found."

        old.rename(new_path)

        return f"Renamed '{old_path}' to '{new_path}'."

    def list_files(self, folder="."):
        path = Path(folder)

        if not path.exists():
            return "Folder not found."

        files = []

        for item in path.iterdir():
            files.append(item.name)

        return "\n".join(files)
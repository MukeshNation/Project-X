from pathlib import Path

from modules.coding.code_generator import CodeGenerator


class ProjectBuilder:

    def __init__(self):
        self.generator = CodeGenerator()

    def create_website(self, name: str, description: str):

        project = Path(name)
        project.mkdir(parents=True, exist_ok=True)

        website = self.generator.generate_website(description)

        html = website["html"]
        css = website["css"]
        js = website["js"]

        (project / "index.html").write_text(html, encoding="utf-8")
        (project / "style.css").write_text(css, encoding="utf-8")
        (project / "script.js").write_text(js, encoding="utf-8")

        return f"✅ Website '{name}' created successfully."
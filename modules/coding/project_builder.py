from pathlib import Path

from modules.coding.code_generator import CodeGenerator


class ProjectBuilder:

    def __init__(self):
        self.generator = CodeGenerator()

    def create_website(self, name, description):

        folder = Path(name)

        folder.mkdir(parents=True, exist_ok=True)

        html = self.generator.generate_html(description)
        css = self.generator.generate_css(description)
        js = self.generator.generate_js(description)

        (folder / "index.html").write_text(html, encoding="utf-8")
        (folder / "style.css").write_text(css, encoding="utf-8")
        (folder / "script.js").write_text(js, encoding="utf-8")

        return f"Website '{name}' created successfully."
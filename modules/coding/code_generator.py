from core.ai_client import client


class CodeGenerator:

    def __init__(self):
        self.model = "qwen3:4b"

    def generate(self, request: str):

        prompt = f"""
You are an expert Full Stack Software Engineer.

Rules:

- Return ONLY code.
- Never explain.
- Never use markdown.
- Never write ```.

The user requested:

{request}
"""

        return client.chat(self.model, prompt).strip()

    def generate_html(self, description: str):

        prompt = f"""
Create a complete HTML5 page.

Requirements:

{description}

Return only HTML.
"""

        return client.chat(self.model, prompt).strip()

    def generate_css(self, description: str):

        prompt = f"""
Create professional CSS.

Requirements:

{description}

Return only CSS.
"""

        return client.chat(self.model, prompt).strip()

    def generate_js(self, description: str):

        prompt = f"""
Create JavaScript.

Requirements:

{description}

Return only JavaScript.
"""

        return client.chat(self.model, prompt).strip()

    def generate_python(self, description: str):

        prompt = f"""
Write Python code.

Requirements:

{description}

Return only Python code.
"""

        return client.chat(self.model, prompt).strip()

    def generate_react(self, description: str):

        prompt = f"""
Create React code.

Requirements:

{description}

Return only code.
"""

        return client.chat(self.model, prompt).strip()
import json

from config.personality import SYSTEM_PROMPT
from core.ai_client import client
from modules.memory.memory_manager import MemoryManager
from modules.actions.action_manager import ActionManager

memory = MemoryManager()
actions = ActionManager()


class ChatbotService:

    def observe(self, message):

        prompt = f"""
Extract only permanent user information.

Return ONLY valid JSON.

Possible fields:
- name
- city
- profession
- education
- goal
- favorite_language
- favorite_food
- hobby

If nothing important exists, return:

{{}}

User message:
{message}
"""

        try:
            text = client.chat("qwen3:4b", prompt)

            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            if isinstance(data, dict):
                memory.update(data)

        except Exception:
            pass

    def ask(self, message: str) -> str:

        self.observe(message)

        # Computer Actions
        result = actions.execute(message)
        if result:
            return result

        history = memory.get("history")

        if history is None:
            history = []

        history.append(f"User: {message}")

        prompt = f"{SYSTEM_PROMPT}\n\n" + "\n".join(history)

        # AI Router
        coding_words = [
            "code",
            "python",
            "java",
            "javascript",
            "bug",
            "error",
            "react",
            "html",
            "css",
            "program"
        ]

        model = "qwen3:4b"

        if any(word in message.lower() for word in coding_words):
            model = "deepseek-r1:7b"

        reply = client.chat(model, prompt)

        history.append(f"AI: {reply}")

        memory.set("history", history)

        return reply
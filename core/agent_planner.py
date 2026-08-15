import json
import re

from core.ai_client import client


class AgentPlanner:
    FULLSTACK_INTENT = re.compile(
        r"\b(full[ -]?stack|next\.?js|postgres|supabase|database|backend|api|"
        r"multiplayer|leaderboard|subscription|saas|admin dashboard)\b",
        re.IGNORECASE,
    )

    def _extract_json(self, text: str):
        text = (text or "").strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        if text.startswith("```"):
            text = text.replace("```", "").strip()

        try:
            return json.loads(text)
        except Exception:
            pass

        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        raise ValueError("AI did not return valid JSON.")

    def create_plan(self, goal: str):
        # Full-stack generation must remain available even when the free planner
        # model is rate-limited or returns malformed JSON.
        if self.FULLSTACK_INTENT.search(goal or ""):
            return {
                "goal": goal,
                "steps": [
                    {"action": "build_fullstack_app", "args": {"request": goal}},
                    {"action": "qa_fullstack_app", "args": {"path": ""}},
                ],
            }

        prompt = f"""
You are Autarch Agent Planner.

Create a safe executable plan for the user's goal.

Allowed actions:

create_folder
args:
{{"path":"folder"}}

create_file
args:
{{"path":"folder/file.ext","content":"full content"}}

write_file
args:
{{"path":"folder/file.ext","content":"full content"}}

read_file
args:
{{"path":"folder/file.ext"}}

verify_file
args:
{{"path":"folder/file.ext"}}

run_python
args:
{{"path":"folder/main.py"}}

build_website
args:
{{"request":"complete original website request"}}

build_fullstack_app
args:
{{"request":"complete original full-stack application request"}}

qa_fullstack_app
args:
{{"path":"project-folder"}}

qa_website
args:
{{"path":"project-folder"}}

fix_website
args:
{{"path":"project-folder"}}

deploy_website
args:
{{"path":"project-folder"}}

publish_github
args:
{{"path":"project-folder"}}

Rules:
- Return ONLY JSON.
- No explanation.
- No markdown.
- Use relative paths only.
- If code is requested, include actual code in content.
- If testing is requested, use run_python.
- After building a website, use qa_website to verify the generated website before considering the task complete.
- If the user asks to test or verify a website, use qa_website.
- If website QA reports errors or warnings, use fix_website and then run qa_website again.
- Never modify a website that already passes QA with zero errors and zero warnings.
- If the user asks for intentionally broken code,
  create the broken code and then run_python.
- If the user explicitly asks for full-stack, Next.js, React with a backend, database, authentication, multiplayer, subscriptions, SaaS, dashboard, or an application with APIs, use build_fullstack_app instead of build_website.
- After build_fullstack_app always use qa_fullstack_app.
- A full-stack product is incomplete without a landing page, responsive navigation,
  login, signup, logout, password recovery, profile, help, contact, privacy, terms,
  pricing, admin controls, database schema, working internal links and a detailed footer.
- When the request mentions premium design, games, animation, images or previews,
  preserve those requirements in the build request and never accept placeholder-only UI.
- A button that has no navigation, form submission or event behavior is a QA failure.
- Use build_website only for static or simple marketing websites that do not need a backend/database.
- Pass the user's complete website request in the "request" argument.
- For website requests, normally build_website should be the main build step.
- Keep the plan short.
- If the user explicitly asks only to publish or push a generated project to GitHub, use publish_github as the FINAL step.
- If the user asks to deploy, host, publish live, or make a generated website live, use deploy_website as the FINAL step.
- Before deploy_website, the website must pass qa_website with zero errors and zero warnings.
- Do not use both publish_github and deploy_website for the same website task because deploy_website already publishes the repository.
- Never publish the Autarch source project.

Required format:

{{
  "goal": "{goal}",
  "steps": [
    {{
      "action": "create_folder",
      "args": {{
        "path": "example"
      }}
    }}
  ]
}}
"""

        last_error = None

        for _ in range(3):
            try:
                text = client.chat("qwen3:4b", prompt)
                plan = self._extract_json(text)

                if not isinstance(plan, dict):
                    raise ValueError("Plan must be a JSON object.")

                if not isinstance(plan.get("steps"), list):
                    raise ValueError("Plan must contain steps.")

                return plan

            except Exception as error:
                last_error = error

                prompt += """

IMPORTANT:
Your previous response was invalid.
Return ONLY one valid JSON object.
Do not return explanations or markdown.
"""

        raise RuntimeError(
            f"Autarch planner failed after 3 attempts: {last_error}"
        )

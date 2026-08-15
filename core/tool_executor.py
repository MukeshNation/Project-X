from pathlib import Path
import subprocess

from core.code_fixer import CodeFixer
from core.website_qa import WebsiteQA
from core.site_builder_v2 import SiteBuilderV2
from core.full_stack_builder import FullStackBuilder

from app.config import WORKSPACE
from modules.actions.file_actions import FileActions
from modules.coding.github_publisher import GitHubPublisher


class ToolExecutor:
    def __init__(self):
        self.files = FileActions()
        self.github = GitHubPublisher()
        self.fixer = CodeFixer()
        self.website_qa = WebsiteQA()
        self.last_built_project = None
        self.site_builder = SiteBuilderV2()
        self.full_stack_builder = FullStackBuilder()

    def safe_path(self, value: str):
        path = (WORKSPACE / value).resolve()
        workspace = WORKSPACE.resolve()

        if path != workspace and workspace not in path.parents:
            raise ValueError("Path outside Autarch workspace is blocked.")

        return path

    def execute(self, step):
        action = step.get("action")
        args = step.get("args", {})

        if action == "create_folder":
            path = self.safe_path(args["path"])
            return self.files.create_folder(str(path))

        if action == "create_file":
            path = self.safe_path(args["path"])
            content = args.get("content", "")
            return self.files.create_file(str(path), content)

        if action == "write_file":
            path = self.safe_path(args["path"])
            content = args.get("content", "")
            return self.files.write_file(str(path), content)

        if action == "read_file":
            path = self.safe_path(args["path"])
            return self.files.read_file(str(path))

        if action == "verify_file":
            path = self.safe_path(args["path"])

            if path.exists():
                return f"Verified: '{path}' exists."

            raise FileNotFoundError(
                f"Expected file '{path}' was not created."
            )

        if action == "run_python":
            path = self.safe_path(args["path"])

            if not path.exists():
                raise FileNotFoundError(
                    f"Python file '{path}' not found."
                )

            result = subprocess.run(
                ["python", str(path)],
                cwd=str(path.parent),
                capture_output=True,
                text=True,
                timeout=20,
            )

            output = result.stdout.strip()
            error = result.stderr.strip()

            if result.returncode != 0:
                last_error = error or "Python program failed."

                for attempt in range(1, 4):
                    current_code = path.read_text(encoding="utf-8")

                    fixed_code = self.fixer.fix_python(
                        current_code,
                        last_error
                    )

                    path.write_text(
                        fixed_code,
                        encoding="utf-8"
                    )

                    retry = subprocess.run(
                        ["python", str(path)],
                        cwd=str(path.parent),
                        capture_output=True,
                        text=True,
                        timeout=20,
                    )

                    if retry.returncode == 0:
                        retry_output = retry.stdout.strip()

                        return (
                            f"Error detected -> fixed on attempt {attempt} -> "
                            + (
                                retry_output
                                or "program completed successfully."
                            )
                        )

                    last_error = retry.stderr.strip()

                raise RuntimeError(
                    "Auto-fix failed after 3 attempts:\n"
                    + last_error
                )

            return output or "Python program completed successfully."

        if action == "build_website":
            request = args.get("request", "").strip()

            if not request:
                raise ValueError(
                    "Website request is required."
                )

            result = self.site_builder.build(
                request
            )

            if (
                isinstance(result, dict)
                and result.get("project")
            ):
                self.last_built_project = str(
                    result["project"]
                )

            return result

        if action == "build_fullstack_app":
            request = args.get("request", "").strip()
            if not request:
                raise ValueError("Full-stack application request is required.")
            result = self.full_stack_builder.build(request)
            if result.get("project"):
                self.last_built_project = str(result["project"])
            return result

        if action == "qa_fullstack_app":
            requested_path = str(args.get("path", "")).strip()
            if self.last_built_project:
                path = Path(self.last_built_project).resolve()
            elif requested_path:
                path = self.safe_path(requested_path)
            else:
                raise ValueError("Full-stack project path is required.")
            result = self.full_stack_builder.validate(str(path))
            if not result.get("success"):
                raise RuntimeError(
                    "Full-stack QA failed: " + "; ".join(result.get("errors", []))
                )
            return result

        if action == "deploy_website":
            requested_path = str(
                args.get("path", "")
            ).strip()

            if self.last_built_project:
                project = Path(
                    self.last_built_project
                ).resolve()
            elif requested_path:
                project = self.safe_path(
                    requested_path
                )
            else:
                raise ValueError(
                    "Website path is required."
                )

            # Never deploy a website that fails QA.
            qa = self.website_qa.check(
                str(project)
            )

            if (
                not qa.get("success")
                or qa.get("errors")
                or qa.get("warnings")
            ):
                raise RuntimeError(
                    "Website deployment blocked because QA did not fully pass: "
                    + str(qa)
                )

            return self.github.deploy_pages(
                str(project)
            )

        if action == "publish_github":
            project = self.safe_path(args["path"])

            return self.github.publish_public(
                str(project)
            )

        if action == "fix_website":
            requested_path = str(
                args.get("path", "")
            ).strip()

            if self.last_built_project:
                path = Path(
                    self.last_built_project
                ).resolve()
            elif requested_path:
                path = self.safe_path(
                    requested_path
                )
            else:
                raise ValueError(
                    "Website path is required."
                )

            first_qa = self.website_qa.check(
                str(path)
            )

            problems = (
                first_qa.get("errors", [])
                + first_qa.get("warnings", [])
            )

            if not problems:
                return {
                    "success": True,
                    "status": "already_clean",
                    "project": str(path),
                    "qa": first_qa,
                }

            editable_files = [
                path / "index.html",
                path / "about.html",
                path / "menu.html",
                path / "contact.html",
                path / "style.css",
                path / "script.js",
            ]

            changed = []

            for file in editable_files:
                if not file.exists():
                    continue

                current = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                fixed = self.fixer.fix_website_file(
                    file.name,
                    current,
                    problems
                )

                if (
                    fixed
                    and fixed.strip()
                    and fixed != current
                ):
                    file.write_text(
                        fixed,
                        encoding="utf-8"
                    )
                    changed.append(file.name)

            final_qa = self.website_qa.check(
                str(path)
            )

            return {
                "success": final_qa.get(
                    "success",
                    False
                ),
                "status": (
                    "fixed"
                    if final_qa.get("success")
                    else "needs_attention"
                ),
                "project": str(path),
                "changed_files": changed,
                "before": first_qa,
                "after": final_qa,
            }

        if action == "qa_website":
            requested_path = str(
                args.get("path", "")
            ).strip()

            # After build_website always QA the actual
            # project returned by SiteBuilderV2.
            if self.last_built_project:
                path = Path(
                    self.last_built_project
                ).resolve()
            elif requested_path:
                path = self.safe_path(
                    requested_path
                )
            else:
                raise ValueError(
                    "Website path is required."
                )

            result = self.website_qa.check(
                str(path)
            )

            return result

        raise ValueError(
            f"Tool '{action}' is not enabled yet."
        )

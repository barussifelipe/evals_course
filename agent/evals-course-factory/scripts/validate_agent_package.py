"""Validate invariants that do not require third-party packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    ".codex-plugin/plugin.json",
    "config/agents.json",
    "references/operating-contract.md",
    "references/methodology.md",
    "references/git-protocol.md",
    "templates/CONTEXT.template.md",
    "schemas/lesson-plan.schema.json",
    "schemas/research.schema.json",
    "schemas/review.schema.json",
    "rubrics/orchestrator.md",
    "rubrics/searcher.md",
    "rubrics/builder.md",
    "rubrics/behavior-penalties.md",
]
SKILLS = ["evals-course-orchestrator", "evals-course-searcher", "evals-course-builder", "orchestrator-judge", "searcher-judge", "builder-judge"]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing {relative}")
    for skill in SKILLS:
        if not (ROOT / "skills" / skill / "SKILL.md").is_file():
            errors.append(f"missing skill {skill}")

    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if manifest.get("name") != ROOT.name:
        errors.append("plugin name does not match directory")
    agents = json.loads((ROOT / "config" / "agents.json").read_text(encoding="utf-8"))
    expected = {
        "orchestrator": ("gpt-5.6-sol", "low"),
        "orchestrator_judge": ("gpt-5.6-sol", "medium"),
        "searcher": ("gpt-5.6-luna", "low"),
        "searcher_judge": ("gpt-5.6-terra", "medium"),
        "builder": ("gpt-5.6-sol", "low"),
        "builder_judge": ("gpt-5.6-sol", "low"),
    }
    for role, values in expected.items():
        actual = agents.get(role, {})
        if (actual.get("model"), actual.get("reasoning_effort")) != values:
            errors.append(f"wrong model configuration for {role}")

    text = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*") if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".py"})
    unfinished_marker = "[" + "TODO:"
    if unfinished_marker in text:
        errors.append("unfinished TODO placeholder")
    required_merge_rule = "Only the human user may merge"
    if required_merge_rule not in (ROOT / "templates" / "CONTEXT.template.md").read_text(encoding="utf-8"):
        errors.append("CONTEXT template lacks human-only merge rule")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: agent plugin package invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())

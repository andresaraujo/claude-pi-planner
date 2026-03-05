#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib

from state_utils import load_state, project_dir


def _read_skill(plugin_root: pathlib.Path) -> str:
    skill_path = plugin_root / "skills" / "pi-planner" / "SKILL.md"
    if not skill_path.exists():
        return ""
    return skill_path.read_text(encoding="utf-8")


def main() -> int:
    _ = json.load(__import__("sys").stdin)

    state = load_state()
    plugin_root = pathlib.Path(os.environ.get("CLAUDE_PLUGIN_ROOT", ".")).resolve()

    if state.get("planning_mode"):
        skill = _read_skill(plugin_root)
        if not skill:
            print("{}")
            return 0

        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"[PLANNING MODE ACTIVE]\\n\\n{skill}",
            }
        }
        print(json.dumps(payload))
        return 0

    active_feature = state.get("active_feature")
    if active_feature:
        root = project_dir()
        feature_dir = root / ".pi-plans" / active_feature
        plan = feature_dir / "plan.md"
        todo = feature_dir / "todo.md"
        progress = feature_dir / "progress.md"

        rules = f"""[IMPLEMENTATION MODE - Feature: {active_feature}]

You are working on a feature with tracked plan, todo, and progress files.

## File Locations
- Plan: {plan}
- Todo: {todo}
- Progress: {progress}

## Rules
- Keep plan/todo/progress synchronized with real implementation state.
- When tasks are completed, mark todo checkboxes and log concise progress entries.
- If requirements change, update plan and todo before implementation diverges.
"""

        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": rules,
            }
        }
        print(json.dumps(payload))
        return 0

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

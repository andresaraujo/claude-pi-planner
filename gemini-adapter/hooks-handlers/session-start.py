#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

from state_utils import load_state, project_dir


def _read_skill(extension_path: pathlib.Path) -> str:
    skill_path = extension_path / "skills" / "pi-planner" / "SKILL.md"
    if not skill_path.exists():
        return ""
    return skill_path.read_text(encoding="utf-8")


def main() -> int:
    _ = json.load(sys.stdin)

    state = load_state()
    extension_path = pathlib.Path(__file__).resolve().parents[1]

    if state.get("planning_mode"):
        skill = _read_skill(extension_path)
        if not skill:
            print("{}")
            return 0

        print(json.dumps({"hookSpecificOutput": {"additionalContext": f"[PLANNING MODE ACTIVE]\\n\\n{skill}"}}))
        return 0

    active_feature = state.get("active_feature")
    if active_feature:
        root = project_dir()
        feature_dir = root / ".pi-plans" / active_feature
        rules = f"""[IMPLEMENTATION MODE - Feature: {active_feature}]

## File Locations
- Plan: {feature_dir / 'plan.md'}
- Todo: {feature_dir / 'todo.md'}
- Progress: {feature_dir / 'progress.md'}

Keep plan/todo/progress synchronized with reality while implementing.
"""
        print(json.dumps({"hookSpecificOutput": {"additionalContext": rules}}))
        return 0

    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

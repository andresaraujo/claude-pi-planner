#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

from state_utils import load_state, project_dir, resolve_tool_file_path, state_path


ALLOWED_PLAN_FILES = {"plan.md", "todo.md", "progress.md"}


def _is_allowed_planning_write(path: pathlib.Path) -> bool:
    path = path.resolve()
    if path == state_path().resolve():
        return True

    root = project_dir().resolve()
    plans_root = root / ".pi-plans"
    try:
        rel = path.relative_to(plans_root)
    except ValueError:
        return False

    parts = rel.parts
    if len(parts) != 2:
        return False

    return parts[1] in ALLOWED_PLAN_FILES


def main() -> int:
    payload = json.load(__import__("sys").stdin)
    tool_input = payload.get("tool_input") or {}

    state = load_state()
    if not state.get("planning_mode"):
        print("{}")
        return 0

    file_path = resolve_tool_file_path(tool_input)
    if file_path and _is_allowed_planning_write(file_path):
        print("{}")
        return 0

    print(
        json.dumps(
            {
                "decision": "deny",
                "reason": "Planning mode active: implementation edits are blocked. Only plan artifacts are allowed.",
                "systemMessage": "Planning mode active: implementation edits are blocked."
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

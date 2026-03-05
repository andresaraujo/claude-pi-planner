#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import pathlib
import re
import sys

from state_utils import (
    load_state,
    mark_todo_snapshot,
    project_dir,
    resolve_tool_file_path,
    save_state,
    snapshot_path,
)

EXTENSION_PATH = pathlib.Path(__file__).resolve().parents[1]
SHARED_CORE = (EXTENSION_PATH.parent / "shared-core").resolve()
if str(SHARED_CORE) not in sys.path:
    sys.path.insert(0, str(SHARED_CORE))

from planner_core import content_hash, find_newly_completed, generate_progress_entry  # noqa: E402


def _ensure_progress(path: pathlib.Path, feature: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    initial = f"# {feature} - Progress\n"
    path.write_text(initial, encoding="utf-8")
    return initial


def main() -> int:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input") or {}

    changed_file = resolve_tool_file_path(tool_input)
    if not changed_file:
        print("{}")
        return 0

    changed_file = changed_file.resolve()
    root = project_dir().resolve()

    state = load_state()
    notices: list[str] = []

    plan_match = re.search(r"\.pi-plans/([^/]+)/plan\.md$", str(changed_file))
    if plan_match:
        feature = plan_match.group(1)
        state["active_feature"] = feature
        state["planning_mode"] = False
        save_state(state)
        notices.append(f"Active feature set to: {feature}")

    active_feature = state.get("active_feature")
    if active_feature:
        todo_path = root / ".pi-plans" / active_feature / "todo.md"
        progress_path = root / ".pi-plans" / active_feature / "progress.md"

        if changed_file == todo_path.resolve() and todo_path.exists():
            new_todo = todo_path.read_text(encoding="utf-8")
            old_todo = snapshot_path().read_text(encoding="utf-8") if snapshot_path().exists() else None
            newly_completed = find_newly_completed(old_todo, new_todo)

            if newly_completed:
                progress = _ensure_progress(progress_path, active_feature)
                entry = generate_progress_entry(newly_completed)
                progress_path.write_text(progress.rstrip() + entry + "\n", encoding="utf-8")
                notices.append(f"Progress updated: {len(newly_completed)} task(s) completed")

            mark_todo_snapshot(new_todo, content_hash(new_todo))

    if not notices:
        print("{}")
        return 0

    print(json.dumps({"systemMessage": " | ".join(notices)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

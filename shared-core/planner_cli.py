#!/usr/bin/env python3
"""CLI wrapper for shared planner helpers.

Usage:
  planner_cli.py slug "Feature Name"
  planner_cli.py todo-diff <old_todo_path_or_dash> <new_todo_path>
  planner_cli.py progress-entry <old_todo_path_or_dash> <new_todo_path>
"""

from __future__ import annotations

import json
import pathlib
import sys

from planner_core import (
    TaskKey,
    find_newly_completed,
    generate_progress_entry,
    to_kebab_case,
)


def _read_path(path_value: str) -> str | None:
    if path_value == "-":
        return None
    path = pathlib.Path(path_value)
    return path.read_text(encoding="utf-8")


def _task_to_dict(task: TaskKey) -> dict[str, str]:
    return {"phase": task.phase, "task": task.task}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Missing command", file=sys.stderr)
        return 1

    command = argv[1]

    if command == "slug":
        if len(argv) < 3:
            print("Missing title", file=sys.stderr)
            return 1
        print(to_kebab_case(argv[2]))
        return 0

    if command in {"todo-diff", "progress-entry"}:
        if len(argv) < 4:
            print("Expected old/new todo paths", file=sys.stderr)
            return 1

        old_todo = _read_path(argv[2])
        new_todo = _read_path(argv[3])
        if new_todo is None:
            print("New todo path cannot be '-'", file=sys.stderr)
            return 1

        completed = find_newly_completed(old_todo, new_todo)

        if command == "todo-diff":
            payload = {"count": len(completed), "tasks": [_task_to_dict(t) for t in completed]}
            print(json.dumps(payload, indent=2))
            return 0

        print(generate_progress_entry(completed))
        return 0

    print(f"Unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

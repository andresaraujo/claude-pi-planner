#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
import os
import pathlib
import re
from typing import Any, Dict

DEFAULT_STATE: Dict[str, Any] = {
    "active_feature": None,
    "planning_mode": False,
    "command_namespace": "pi",
    "last_todo_hash": None,
    "last_todo_updated_at": None,
}


def project_dir() -> pathlib.Path:
    value = os.environ.get("CLAUDE_PROJECT_DIR")
    if value:
        return pathlib.Path(value)
    return pathlib.Path.cwd()


def state_path() -> pathlib.Path:
    return project_dir() / ".claude" / "pi-planner.local.md"


def snapshot_path() -> pathlib.Path:
    return project_dir() / ".claude" / "pi-planner.last-todo.md"


def ensure_claude_dir() -> None:
    (project_dir() / ".claude").mkdir(parents=True, exist_ok=True)


def load_state() -> Dict[str, Any]:
    path = state_path()
    if not path.exists():
        return dict(DEFAULT_STATE)

    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?", content, flags=re.DOTALL)
    if not match:
        return dict(DEFAULT_STATE)

    state = dict(DEFAULT_STATE)
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        value = raw.strip()

        if value in {"null", "None", ""}:
            parsed: Any = None
        elif value.lower() in {"true", "false"}:
            parsed = value.lower() == "true"
        else:
            parsed = value.strip('"')

        if key in state:
            state[key] = parsed

    return state


def save_state(state: Dict[str, Any]) -> None:
    ensure_claude_dir()
    normalized = dict(DEFAULT_STATE)
    normalized.update(state)

    def _fmt(value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    lines = ["---"]
    for key in [
        "active_feature",
        "planning_mode",
        "command_namespace",
        "last_todo_hash",
        "last_todo_updated_at",
    ]:
        lines.append(f"{key}: {_fmt(normalized.get(key))}")
    lines.append("---")
    lines.append("")

    state_path().write_text("\n".join(lines), encoding="utf-8")


def mark_todo_snapshot(todo_content: str, hash_value: str) -> None:
    ensure_claude_dir()
    snapshot_path().write_text(todo_content, encoding="utf-8")

    state = load_state()
    state["last_todo_hash"] = hash_value
    state["last_todo_updated_at"] = datetime.now().isoformat()
    save_state(state)


def resolve_tool_file_path(tool_input: Dict[str, Any]) -> pathlib.Path | None:
    raw = tool_input.get("file_path") or tool_input.get("path")
    if not raw or not isinstance(raw, str):
        return None

    path = pathlib.Path(raw)
    if path.is_absolute():
        return path

    return project_dir() / path

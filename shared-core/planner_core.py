#!/usr/bin/env python3
"""Shared planning helpers for Claude/Gemini adapters."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import re
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class TaskKey:
    phase: str
    task: str


def to_kebab_case(title: str) -> str:
    value = title.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _normalize_task(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_todo_completed(todo_content: str) -> List[TaskKey]:
    """Parse completed tasks keyed by (phase, task)."""
    phase = ""
    completed: List[TaskKey] = []

    for raw_line in todo_content.splitlines():
        line = raw_line.rstrip()

        phase_match = re.match(r"^##\s+(.+?)\s*$", line)
        if phase_match:
            phase = phase_match.group(1).strip()
            continue

        checked_match = re.match(r"^-\s+\[x\]\s+(.+?)\s*$", line, flags=re.IGNORECASE)
        if checked_match:
            task = _normalize_task(checked_match.group(1))
            completed.append(TaskKey(phase=phase, task=task))

    return completed


def find_newly_completed(old_todo: str | None, new_todo: str) -> List[TaskKey]:
    old_set = set(parse_todo_completed(old_todo or ""))
    new_list = parse_todo_completed(new_todo)
    return [task for task in new_list if task not in old_set]


def generate_progress_entry(
    completed: Sequence[TaskKey],
    title: str = "Tasks Completed",
    date: str | None = None,
    include_key_decisions: bool = False,
) -> str:
    entry_date = date or datetime.now().strftime("%Y-%m-%d")
    lines: List[str] = [f"\n### {entry_date} - {title}\n", "**What we did:**"]

    for item in completed:
        if item.phase:
            lines.append(f"- {item.phase}: {item.task}")
        else:
            lines.append(f"- {item.task}")

    lines.append("")
    lines.append("**Key decisions:**")
    if include_key_decisions:
        lines.append("- (captured during implementation)")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("**Next steps:**")
    lines.append("- Continue with remaining tasks")
    lines.append("")

    return "\n".join(lines)

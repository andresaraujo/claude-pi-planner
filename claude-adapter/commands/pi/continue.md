---
description: Continue work on a Pi plan feature
argument-hint: [feature-name]
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Resume Pi-compatible implementation mode.

Steps:
1. Determine target feature:
   - Prefer `$ARGUMENTS` if provided.
   - Otherwise read `.claude/pi-planner.local.md` and use `active_feature`.
   - If still missing, list directories under `.pi-plans/` and ask user to pick one.
2. Validate `.pi-plans/<feature>/plan.md` exists.
3. Read:
   - `.pi-plans/<feature>/plan.md`
   - `.pi-plans/<feature>/todo.md` (if present)
   - `.pi-plans/<feature>/progress.md` (if present)
4. Update `.claude/pi-planner.local.md`:
   - `active_feature`: feature
   - `planning_mode`: false
   - keep namespace and snapshot fields
5. If todo exists, store latest todo snapshot at `.claude/pi-planner.last-todo.md`.
6. Summarize current status from plan/todo/progress and propose next concrete implementation step.

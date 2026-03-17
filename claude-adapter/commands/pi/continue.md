---
description: Continue work on a Pi plan feature
argument-hint: [feature-name]
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Resume Pi-compatible implementation from shared plan artifacts.

Steps:
1. Determine the target feature:
   - Prefer `$ARGUMENTS` if provided.
   - Otherwise inspect directories under `.pi-plans/`.
   - If exactly one feature exists, use it.
   - If multiple features exist, ask the user to choose one.
   - If none exist, ask the user to create a plan first.
2. Validate `.pi-plans/<feature>/plan.md` exists.
3. Read:
   - `.pi-plans/<feature>/plan.md`
   - `.pi-plans/<feature>/todo.md` (if present)
   - `.pi-plans/<feature>/progress.md` (if present)
4. Summarize current status from plan/todo/progress.
5. Propose the next concrete implementation step.
6. During implementation, keep `todo.md` and `progress.md` synchronized manually.
7. Do not read or write `.claude` local state or todo snapshot files.

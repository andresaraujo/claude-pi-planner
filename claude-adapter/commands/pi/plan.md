---
description: Start Pi-compatible planning mode
argument-hint: [feature-name]
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Start Pi-compatible planning mode.

Steps:
1. If `$ARGUMENTS` is provided, convert it to kebab-case and use it as the active feature.
2. Ensure `.claude/` exists.
3. Write `.claude/pi-planner.local.md` with frontmatter:
   - `active_feature`: kebab-case feature or null
   - `planning_mode`: true
   - `command_namespace`: pi
   - `last_todo_hash`: null
4. If feature is set, ensure `.pi-plans/<feature>/` exists.
5. Do not implement features yet.
6. Immediately begin planning conversation by asking clarifying questions:
   - what problem are we solving?
   - what does success look like?
   - constraints/preferences?
   - what's out of scope?

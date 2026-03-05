---
description: Add manual progress checkpoint for active feature
argument-hint: [checkpoint-note]
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Add a manual checkpoint entry to progress tracking.

Steps:
1. Read `.claude/pi-planner.local.md` and get `active_feature`.
2. If no active feature, ask user to run `/pi:continue <feature>` first.
3. Ensure `.pi-plans/<active_feature>/progress.md` exists; if missing create with heading:
   - `# <feature> - Progress`
4. Append entry:
   - `### YYYY-MM-DD - Checkpoint`
   - `**What we did:**` from `$ARGUMENTS` (or ask user if empty)
   - `**Key decisions:**`
   - `**Next steps:**`

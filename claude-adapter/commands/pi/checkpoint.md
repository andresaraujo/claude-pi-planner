---
description: Add manual progress checkpoint for a feature
argument-hint: "[feature-name] [checkpoint-note]"
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Add a manual checkpoint entry to progress tracking.

Steps:
1. Resolve the target feature:
   - If `$ARGUMENTS` begins with a token matching an existing `.pi-plans/<feature>/`, use that token as the feature and treat the rest as the note.
   - Otherwise inspect directories under `.pi-plans/`.
   - If exactly one feature exists, use it and treat all `$ARGUMENTS` as the note.
   - If multiple features exist, ask the user which feature to use.
   - If none exist, ask the user to create a plan first.
2. If the checkpoint note is empty, ask the user for it.
3. Ensure `.pi-plans/<feature>/progress.md` exists; if missing create it with heading:
   - `# <feature> - Progress`
4. Append entry:
   - `### YYYY-MM-DD - Checkpoint`
   - `**What we did:**` from the note
   - `**Key decisions:**`
   - `**Next steps:**`
5. Do not read or write `.claude` local state or todo snapshot files.

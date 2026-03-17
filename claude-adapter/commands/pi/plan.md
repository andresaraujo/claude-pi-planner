---
description: Start Pi-compatible planning mode
argument-hint: [feature-name]
allowed-tools: [Read, Write, Edit, MultiEdit, Bash]
---

Start a Pi-compatible planning conversation.

Rules:
- Do not implement yet.
- Do not create files until the user asks to create the plan.

Steps:
1. If `$ARGUMENTS` is provided, treat it as the candidate feature name. Convert it to kebab-case only when writing files.
2. Ask clarifying questions:
   - what problem are we solving?
   - what does success look like?
   - constraints/preferences?
   - what's out of scope?
3. Research relevant code/docs if needed.
4. Propose an approach, phases, trade-offs, and open questions.
5. When the user asks to create the plan:
   - derive or confirm the feature name
   - write:
     - `.pi-plans/<feature>/plan.md`
     - `.pi-plans/<feature>/todo.md`
     - `.pi-plans/<feature>/progress.md`
6. Do not write any `.claude` local state or snapshot files.

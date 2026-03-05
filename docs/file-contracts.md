# File Contracts

## Feature Directory

All agents must read/write the same structure:

```text
.pi-plans/
  <feature-name>/
    plan.md
    todo.md
    progress.md
```

## plan.md

- Markdown plan with sections:
  - Overview
  - Goals
  - Research/Context
  - Approach
  - Phases
  - Open Questions

## todo.md

- Checklist extracted from the `Phases` section
- Phase headings become `##` sections
- Tasks use markdown checkbox format:
  - `- [ ] Task`
  - `- [x] Task`

## progress.md

- Chronological entries appended by adapters/shared core
- Entry shape:

```markdown
### YYYY-MM-DD - Brief Title

**What we did:**
- ...

**Key decisions:**
- ...

**Next steps:**
- ...
```

## Task identity for completion detection

To avoid collisions with repeated task text, task identity is:
- `(phaseTitle, taskText)`

Adapters should not key by `taskText` alone.

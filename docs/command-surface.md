# Command Surface

## Strategy

Use namespaced commands by default to avoid collisions with existing user/workspace commands.

## Canonical commands

- `pi:plan [name]`
- `pi:continue [name]`
- `pi:checkpoint [text]`

## Optional compatibility aliases

Provide optional aliases when no collision is detected in target runtime:

- `plan` -> `pi:plan`
- `continue` -> `pi:continue`
- `checkpoint` -> `pi:checkpoint`

Alias enablement is adapter-specific and should be disabled by default for safety.

## Behavioral expectations

- `pi:plan [name]`
  - starts a planning conversation
  - asks clarifying questions
  - creates plan artifacts only when the user asks to save the plan
- `pi:continue [name]`
  - loads `plan.md`, `todo.md`, `progress.md`
  - if `name` is omitted, adapters may resolve it from local state or inspect `.pi-plans/`
  - Claude asks the user to choose when multiple features exist
- `pi:checkpoint [text]`
  - appends a manual checkpoint to `progress.md`
  - Claude may ask for a feature if multiple plans exist, or accept `<feature> <text>` when unambiguous

## Adapter notes

- Claude is intentionally stateless and does not persist runtime state under `.claude/`
- Claude keeps `todo.md` and `progress.md` synchronized manually during implementation
- Gemini retains hook-driven planning guards and todo/progress automation

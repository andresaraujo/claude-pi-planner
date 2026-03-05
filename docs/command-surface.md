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
  - enters planning mode
  - asks clarifying questions
  - blocks implementation edits
- `pi:continue [name]`
  - loads `plan.md`, `todo.md`, `progress.md`
  - switches to implementation mode
- `pi:checkpoint [text]`
  - appends manual checkpoint to `progress.md`

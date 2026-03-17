# claude-pi-planner

Cross-agent planner package that mirrors `pi-planner` behavior for Claude Code and Gemini CLI while keeping a shared `.pi-plans/<feature>/` artifact format.

## Goals

- Near parity with Pi package behavior
- Compatible planning artifacts across agents
- Adapter-specific wiring for each CLI

## Layout

- `docs/` – parity matrix, contracts, command strategy, state schema
- `shared-core/` – reusable parsing and progress automation helpers
- `claude-adapter/` – Claude Code plugin assets (commands/skills; hooks intentionally disabled for stateless behavior)
- `gemini-adapter/` – Gemini extension assets (commands/skills/hooks)
- `tests/fixtures/` – markdown fixtures for parser edge cases

## Installation

> Keep this repo layout intact. Both adapters currently import helpers from `../shared-core`.

### Claude Code (local)

Run Claude with the adapter loaded for the session:

```bash
claude --plugin-dir /Users/andresaraujo/code/tmp/claude-pi-planner/claude-adapter
```

Optional validation:

```bash
claude plugin validate /Users/andresaraujo/code/tmp/claude-pi-planner/claude-adapter
```

### Gemini CLI (local)

Link the Gemini adapter (recommended for local development):

```bash
gemini extensions link /Users/andresaraujo/code/tmp/claude-pi-planner/gemini-adapter
```

Validate extension:

```bash
gemini extensions validate /Users/andresaraujo/code/tmp/claude-pi-planner/gemini-adapter
```

Restart Gemini CLI after linking/updating extensions.

## Usage

Namespaced command surface:

- `/pi:plan [feature-name]`
- `/pi:continue [feature-name]`
- `/pi:checkpoint [note]`

Shared artifacts are written to:

```text
.pi-plans/<feature>/
  plan.md
  todo.md
  progress.md
```

## Compatibility notes

- Cross-agent compatibility target is the `.pi-plans` file format, not identical UI/runtime behavior.
- Claude adapter is intentionally stateless: it does not create `.claude/pi-planner.local.md` or `.claude/pi-planner.last-todo.md`.
- In Claude, when multiple feature plans exist, `/pi:continue` and `/pi:checkpoint` may ask which feature to use.
- Claude updates `progress.md` manually alongside `todo.md`; Gemini retains hook-driven todo/progress automation.
- Status-line parity with Pi is not supported in Claude/Gemini adapters.
- Command aliasing (`/plan`, `/continue`, `/checkpoint`) is intentionally not enabled by default to avoid collisions.

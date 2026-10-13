# claude-pi-planner

Plan-then-build mode for **Claude Code** and **Gemini CLI**, compatible with my [pi-planner](https://github.com/andresaraujo/pi-planner) extension for Pi.

All three agents read and write the same plan files, so you can plan a feature in one agent and continue it in another:

```text
.pi-plans/<feature>/
  plan.md       # the design, agreed before coding
  todo.md       # checklist the agent works through
  progress.md   # what's done, decisions, next steps
```

Commands: `/pi:plan [feature]` → research and write the plan, `/pi:continue [feature]` → pick up where you left off, `/pi:checkpoint [note]` → record progress.

## Quick start

From a clone of this repo (keep the layout: both adapters import `../shared-core`):

```bash
# Claude Code: load the plugin for this session
claude --plugin-dir ./claude-adapter

# Gemini CLI: link the extension, then restart Gemini
gemini extensions link ./gemini-adapter
```

Validate: `claude plugin validate ./claude-adapter` · `gemini extensions validate ./gemini-adapter`

## Layout

- `docs/` – parity matrix, contracts, command strategy, state schema
- `shared-core/` – reusable parsing and progress automation helpers
- `claude-adapter/` – Claude Code plugin assets (commands/skills; hooks intentionally disabled for stateless behavior)
- `gemini-adapter/` – Gemini extension assets (commands/skills/hooks)
- `tests/fixtures/` – markdown fixtures for parser edge cases

## Compatibility notes

- Cross-agent compatibility target is the `.pi-plans` file format, not identical UI/runtime behavior.
- Claude adapter is intentionally stateless: it does not create `.claude/pi-planner.local.md` or `.claude/pi-planner.last-todo.md`.
- In Claude, when multiple feature plans exist, `/pi:continue` and `/pi:checkpoint` may ask which feature to use.
- Claude updates `progress.md` manually alongside `todo.md`; Gemini retains hook-driven todo/progress automation.
- Status-line parity with Pi is not supported in Claude/Gemini adapters.
- Command aliasing (`/plan`, `/continue`, `/checkpoint`) is intentionally not enabled by default to avoid collisions.

## License

MIT

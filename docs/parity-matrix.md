# Parity Matrix (Pi -> Claude/Gemini)

| Pi capability | Claude Code | Gemini CLI | Notes |
|---|---|---|---|
| Planning mode instructions injection | ⚠️ command-driven only | ✅ via SessionStart/BeforeAgent hooks + skill activation | Claude is stateless and does not persist planning mode across hooks/sessions |
| `/plan [name]` command | ✅ custom command | ✅ custom command (`.toml`) | Default namespaced command; optional alias |
| `/continue [name]` command | ✅ custom command | ✅ custom command (`.toml`) | Claude resolves feature from args or `.pi-plans/`; asks when ambiguous |
| `/checkpoint` command | ✅ custom command | ✅ custom command (`.toml`) | Claude may ask for feature selection when multiple plans exist |
| Detect `plan.md` creation and switch modes | ❌ | ✅ hook-driven state update | Claude has no persisted mode state |
| Track newly completed todo tasks | ❌ | ✅ hook + shared parser | Claude updates progress manually |
| Auto append progress entries | ❌ manual | ✅ hook + shared formatter | Same markdown shape where automated |
| Planning-mode file change guard | ❌ | ✅ BeforeTool deny policy | Claude does not register planning guard hooks |
| Status line indicator | ❌ | ❌ | Out of scope (platform specific UI) |

## Compatibility baseline

- Source of truth files:
  - `.pi-plans/<feature>/plan.md`
  - `.pi-plans/<feature>/todo.md`
  - `.pi-plans/<feature>/progress.md`
- Claude durable state lives only in shared `.pi-plans` artifacts.
- Gemini additionally keeps adapter-local runtime state for convenience and automation.

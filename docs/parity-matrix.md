# Parity Matrix (Pi -> Claude/Gemini)

| Pi capability | Claude Code | Gemini CLI | Notes |
|---|---|---|---|
| Planning mode instructions injection | ✅ via SessionStart/BeforeAgent hooks + skill context | ✅ via SessionStart/BeforeAgent hooks + skill activation | Trigger style differs; same behavior target |
| `/plan [name]` command | ✅ custom command | ✅ custom command (`.toml`) | Default namespaced command; optional alias |
| `/continue [name]` command | ✅ custom command | ✅ custom command (`.toml`) | Loads plan/todo/progress into context |
| `/checkpoint` command | ✅ custom command | ✅ custom command (`.toml`) | Appends checkpoint entry to `progress.md` |
| Detect `plan.md` creation and switch modes | ✅ hook-driven state update | ✅ hook-driven state update | Adapter-specific event names |
| Track newly completed todo tasks | ✅ hook + shared parser | ✅ hook + shared parser | Identity uses `phase + task` |
| Auto append progress entries | ✅ hook + shared formatter | ✅ hook + shared formatter | Same markdown shape across adapters |
| Planning-mode file change guard | ✅ BeforeTool deny policy | ✅ BeforeTool deny policy | Allow only plan artifacts creation when explicitly requested |
| Status line indicator | ❌ | ❌ | Out of scope (platform specific UI) |

## Compatibility baseline

- Source of truth files:
  - `.pi-plans/<feature>/plan.md`
  - `.pi-plans/<feature>/todo.md`
  - `.pi-plans/<feature>/progress.md`
- Shared helper logic must produce identical outputs regardless of adapter.

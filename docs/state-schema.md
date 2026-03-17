# State Schema

Runtime state is adapter-local and optional, while `.pi-plans` artifacts remain shared.

## Shared artifacts

All adapters read and write:

```text
.pi-plans/<feature>/
  plan.md
  todo.md
  progress.md
```

## Claude Code

The Claude adapter is intentionally stateless.

- No persisted local runtime state is written under `.claude/`
- Feature resolution comes from command arguments and `.pi-plans/` directory inspection
- Planning mode is command-instruction driven, not persisted between hook invocations
- Todo completion diffing and auto-progress updates are not used

## Gemini CLI

Gemini currently persists the canonical runtime state object:

```json
{
  "activeFeature": "string|null",
  "planningMode": true,
  "lastTodoSnapshot": {
    "hash": "string|null",
    "path": "string|null",
    "updatedAt": "ISO-8601|null"
  },
  "commandNamespace": "pi"
}
```

## Notes

- Keep persisted runtime state in adapter-native storage only
- Do not write shared runtime state into `.pi-plans`
- Gemini's `lastTodoSnapshot` is used only for new-completion detection optimization

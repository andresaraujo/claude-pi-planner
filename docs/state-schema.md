# State Schema

State is adapter-local (not shared between CLIs), while `.pi-plans` artifacts remain shared.

## Canonical state object

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

- Keep state in adapter-native files:
  - Claude: `.claude/pi-planner.local.md` (or equivalent adapter config storage)
  - Gemini: workspace/user settings or extension-local state file
- Do not write shared runtime state into `.pi-plans`.
- `lastTodoSnapshot` is used only for new-completion detection optimization.

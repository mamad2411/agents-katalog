---
name: brain-forget
description: |
  Remove a manually stored memory from the brain by partial text match.
  Use: /brain-forget <text>
user_invocable: true
---

# brain-forget

Remove a manual memory previously stored with `/brain-remember`. Partial text matches are supported — you don't need the exact phrase.

## Instructions

The user provides the text to match as an argument.

Run:
```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py forget "$ARGS" "$CLAUDE_PROJECT_DIR"
```

Show which memories were removed and confirm success.

If no match is found, say so clearly and suggest:
1. Running `/brain-status` to see what's currently stored
2. Trying a shorter or different keyword from the memory text

## Examples

| Command | What it removes |
|---------|----------------|
| `/brain-forget RS256` | Any memory containing "RS256" |
| `/brain-forget always use` | Conventions starting with "always use" |
| `/brain-forget postgres` | Any memory mentioning postgres |

Note: Only removes **manual memories** added via `/brain-remember`. Memories captured automatically from agent sessions (tasks, decisions) cannot be removed with this command — use `/brain-clear` to wipe all memory.

---
name: dmemo-save
description: Explicitly save a fact, preference, or decision to dMemo's private memory. Use when the user directly asks you to remember something ("remember that...", "save this for next time", "don't forget..."). dMemo already captures full turns automatically at the end of every response — this skill is for a specific fact the user wants saved verbatim, phrased concisely, independent of that automatic per-turn capture.
allowed-tools: Bash(node:*)
---

# dMemo Save

Save a specific fact to dMemo — your private, encrypted, cross-session memory (backed by
0G Storage) — verbatim, as the user stated it (dMemo never runs a second LLM pass to
rephrase/summarize what you save here; whatever text you pass is stored as-is).

## How to Save

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/save-memory.cjs" "TEXT TO REMEMBER"
```

## Example

- User says "remember that we use pnpm, not npm, in this repo":
  ```bash
  node "${CLAUDE_PLUGIN_ROOT}/scripts/save-memory.cjs" "This repo uses pnpm, not npm."
  ```

## Confirm

The script prints "Saved to dMemo." (or a note that dMemo isn't configured yet). Briefly
confirm to the user that it was saved; don't re-save the same fact multiple times in one turn.

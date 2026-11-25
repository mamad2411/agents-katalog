---
name: session-search
description: Search past Feynman session transcripts to recover prior work, conversations, and research context. Use when the user references something from a previous session, asks "what did we do before", when planning depends on earlier research, or when you suspect relevant past context exists.
---

# Session Search

Use this skill to recover prior Feynman CLI session context when that session store exists. This standalone Pi integration must not assume the Feynman CLI `/search` command is available.

## Workflow

1. Check whether `~/.feynman/sessions/` exists.
2. If it does not exist, report that no Feynman CLI session store is available and continue from current context.
3. If it exists, search session JSONL files directly with `rg` or `grep` via bash.
4. Treat recovered context as historical and verify current code, docs, or sources before relying on it.

Session transcripts are JSONL files with records such as `session`, `message`, and `model_change`; message text is usually under `message.content`.

```bash
rg -i "scaling laws" ~/.feynman/sessions/
```

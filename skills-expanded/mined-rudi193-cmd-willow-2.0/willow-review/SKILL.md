---
name: willow-review
description: Code review the current fork's changes — fork-aware, MCP-native.
---

@markdownai v1.0

1. git diff HEAD to see uncommitted changes (or git diff main...HEAD for full fork diff)
2. Check each changed file:
   - Tests exist and pass
   - No TBD/TODO/not implemented placeholders
   - No security issues (injection, unvalidated external input, hardcoded secrets)
   - Follows existing patterns in this repo
3. fork_log(fork_id, "hanuman", "review", "passed" or "failed:<reason>", app_id="hanuman")
4. If passed: report clean, suggest merge if USER approves
5. If failed: list specific files and lines that need fixing before merge

---
name: codex-before-dev
description: "Load task PRD and project specs before writing code. Use before implementation, refactors, or harness changes."
---

# Before Development

Load the minimum context needed for implementation.

1. Confirm the task:
   ```bash
   python3 scripts/codex_harness.py task current
   ```

2. Load implement context:
   ```bash
   python3 scripts/codex_harness.py task agent-context <task> implement
   ```

3. Read relevant spec indexes only:
   ```bash
   python3 scripts/codex_harness.py spec list
   ```

4. Read the specific spec files that apply to the files you will touch.

Do not load dashboard, handoff bodies, or broad source previews unless they are
needed for the current implementation decision.

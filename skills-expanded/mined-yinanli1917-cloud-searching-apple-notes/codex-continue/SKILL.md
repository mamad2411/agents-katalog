---
name: codex-continue
description: "Resume the current Codex harness task. Use when returning to a task, when the user asks what state we are in, or when the conversation has shifted between planning, implementation, and checking."
---

# Continue Current Task

Resume from the active task state instead of relying on chat memory.

1. Load compact state:
   ```bash
   python3 scripts/codex_harness.py context --no-refresh
   ```

2. Inspect the active task:
   ```bash
   python3 scripts/codex_harness.py task continue <task>
   ```

3. Route by `current_phase`, `status`, and artifacts:
   - planning/design discussion -> keep or set `current_phase` to `planning`
   - ready implementation -> use `codex-before-dev`, then implement
   - implementation done -> use `codex-check`
   - durable behavior changed -> update specs/docs before finishing

4. Load detail only when needed:
   ```bash
   python3 scripts/codex_harness.py context --dashboard
   python3 scripts/codex_harness.py context --full
   python3 scripts/codex_harness.py task agent-context <task> implement
   ```

Do not read handoff bodies by default. Handoffs are cross-session recovery files;
read them only when starting a new session, resuming after interruption, or when
the compact state says the handoff is needed for direction.

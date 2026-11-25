---
name: codex-finish-work
description: "Finish a Codex harness task after implementation, checking, spec updates, and rollout verification."
---

# Finish Work

Before finishing:

1. Confirm state:
   ```bash
   python3 scripts/codex_harness.py context --no-refresh
   ```

2. Run focused checks and any required install/rollout.

3. Complete via the harness:
   ```bash
   python3 scripts/codex_harness.py finish-work --complete
   ```

4. Final answer should say:
   - what changed
   - what verification passed
   - what remains, if anything

Do not make backend projection or audit details the headline unless they blocked
the task.

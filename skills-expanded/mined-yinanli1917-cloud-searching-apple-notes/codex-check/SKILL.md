---
name: codex-check
description: "Verify recent Codex harness or project changes against task requirements, specs, tests, and rollout checks."
---

# Check Work

Verify the current task without turning the main session into a diagnostic dump.

1. Identify changed files:
   ```bash
   git status --short
   git diff --name-only
   ```

2. Load check context:
   ```bash
   python3 scripts/codex_harness.py task agent-context <task> check
   ```

3. Run task-specific tests and focused syntax checks.

4. For harness changes, run:
   ```bash
   python3 install.py
   ```

5. Use deeper diagnostics only when the focused check fails:
   ```bash
   python3 scripts/codex_harness.py context --dashboard
   python3 ~/.codex/harness/bin/verify_all_codex_harness.py --deep
   python3 ~/.codex/harness/bin/verify_all_codex_harness.py --state-audit
   ```

Report product/task outcome first. Mention harness internals only if they block
the requested work or explain a failed verification.

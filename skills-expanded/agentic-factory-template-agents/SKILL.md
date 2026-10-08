# Agents

**Read `PROCESS.md` before starting any implementation task.**

Work orders live in `docs/project_management/work_orders/`. First commit on a WO branch is the claim file under `docs/factory/runs/`.

Dispatch-ready WOs use `Problem`, `What to Build`, `Out of scope` / `Do NOT change`, `Acceptance Criteria`, and `Execution`, plus `Priority`, `Effort`, `Services`, and dependencies.

```bash
make ci-local
```

P0/P1: human merge. P2: human verifies the running product before commit, then auto-merge after CI + review. P3: docs-only PR, no product checkpoint.

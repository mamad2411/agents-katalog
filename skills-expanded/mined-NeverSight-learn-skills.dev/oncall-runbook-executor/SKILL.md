---
name: oncall-runbook-executor
description: Use during an incident or routine on-call task to execute a YAML-defined runbook step by step. Each step has a description, an optional precheck command, the action command, and an expected outcome. Produces a tamper-evident execution log. Vendor-neutral; works with any shell-capable agent runtime.
---

# On-Call Runbook Executor

## When to invoke
- "Run the database failover runbook."
- "Walk me through the certificate rotation playbook."
- "Execute the deploy rollback steps."

## Inputs needed
1. **Runbook YAML** — see schema below.
2. **Mode** — `dry-run` (default; prints commands) or `execute` (runs them).
3. **Approval prompts** — interactive `--confirm` prompt before each action by default.

## Runbook schema
```yaml
name: deploy-rollback
description: Roll back the most recent deploy of svc-checkout
owner: sre-oncall
prechecks:
  - desc: kubectl is configured
    cmd: kubectl version --client --output=yaml
steps:
  - id: identify_revision
    desc: Identify the previous revision
    cmd: kubectl rollout history deploy/svc-checkout | tail -3
    expect_zero_exit: true
  - id: rollback
    desc: Roll back to the previous revision
    cmd: kubectl rollout undo deploy/svc-checkout
    requires_confirm: true
  - id: verify
    desc: Wait for rollout to complete
    cmd: kubectl rollout status deploy/svc-checkout --timeout=120s
    expect_zero_exit: true
postchecks:
  - desc: 5xx is back to baseline
    cmd: ./scripts/check_5xx.sh
```

## Workflow
1. **Load** the runbook YAML.
2. **Run prechecks** — abort if any precheck fails.
3. For each **step**:
   - Print step description and command.
   - In `execute` mode and if `requires_confirm`, prompt the operator.
   - Run command, capture stdout/stderr/exit.
   - Compare to expectation; mark pass/fail.
4. **Run postchecks**.
5. **Emit** a Markdown execution log (timestamps, exit codes, outputs).

## Guardrails
- Default mode is `dry-run`; require an explicit `--mode execute` to run anything.
- Steps with `requires_confirm: true` must prompt unless `--yes` is set.
- Never auto-skip a failed precheck — abort and surface clearly.
- Truncate captured output to a configurable max bytes per step.

## Reference code
`runbook.py` reads YAML, executes locally, and writes a Markdown log.

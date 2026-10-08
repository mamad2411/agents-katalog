---
name: sol-governed-workers
description: Use when Codex work should route bounded implementation to lower-cost workers and reserve Sol for risky plan review or final evidence gates, or when installing or validating this workflow.
---

# Sol-Governed Workers

Keep the root responsible for requirements, integration, and user communication. Delegate only when bounded work, specialization, or parallelism repays the extra call. Keep `max_depth = 1`.

## Set up

Let `<skill-dir>` be the directory containing this file, including when loaded from a plugin cache.

```bash
bash <skill-dir>/scripts/install_global_infra.sh
bash <skill-dir>/scripts/validate_setup.sh
```

Add the optional every-task project contract only after reconciling existing instructions:

```bash
bash <skill-dir>/scripts/install_project_contract.sh /absolute/project
```

Use `--append` for a compatible unmanaged `AGENTS.md`, `--update` for a reviewed stale managed block, and `--live-probe` during validation only when spending one model call is acceptable.

## Route work

- Root: settle requirements, make cross-cutting decisions, integrate, verify, and report.
- `luna_worker`: mechanical work with settled decisions.
- `terra_worker`: bounded implementation needing local judgment.
- `sol_advisor`: concise plan or evidence judgment; never implementation.

Ask the user directly for missing product intent. Before editing, request a Sol plan gate for architecture, authentication, security, billing, migrations, destructive operations, public interfaces, or a concrete unresolved technical risk.

Give each worker one ownership area, acceptance criteria, allowed scope, required verification, and an escalation condition. Inspect its diff and command results; a summary is not proof.

## Gate completion

After root verification, request a Sol final gate for changes to runtime behavior, dependencies or configuration, persistent data, security, or public interfaces. It may be skipped for verified docs-only, comments-only, formatting-only, or generated-output-only changes. When uncertain, gate it.

Send only the task contract, targeted diff or file references, verification results, observed behavior, and known risks. Follow [references/review-protocol.md](references/review-protocol.md).

On `REVISE`, address every blocking finding and resubmit changed evidence. On `BLOCKED`, obtain the missing decision, access, or proof. Finish only after `PASS` or explicit user acceptance of a disclosed risk.

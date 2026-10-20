# Agence Governance (Repository-Wide)

This repository is governed by Agence MLS policy.

Before executing any shell or git command, classify it first:

```bash
airun guard classify "<command>"
```

Policy source:

- `codex/AIPOLICY.yaml`

Execution pattern:

1. Classify with `airun guard classify "<command>"`
2. If `action=deny` (T3): do not run the command
3. If `action=escalate` (T2): require human approval before running
4. If allowed/flagged (T0/T1): execute with normal workflow

For enforced checks (not advisory-only), use git hooks and required CI guard checks as documented in `docs/GOVERNANCE.md`.

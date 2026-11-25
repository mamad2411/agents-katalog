---
name: spx
description: Start or inspect local docker-dev apps, run container commands, and manage
  repositories, secrets, worktrees, or database snapshots through SPX.
---

# SPX local operations

Bring the requested local application or resource to its intended state through SPX. Read only the reference for the operation at hand. Use `spx describe <operation>` for the installed contract and `spx version` for compatibility questions. Final JSON is on stdout; progress JSONL is on stderr.

| Task | Guidance |
| --- | --- |
| Host readiness or cold bootstrap | `spx env check` remediation; `make setup` for cold bootstrap |
| Repository synchronization or commits | [Repositories](references/repositories.md) |
| Start, inspect, restart, stop, or run commands in applications | [Applications](references/applications.md) |
| Read or update secrets | [Secrets](references/secrets.md) |
| Worktrees and private databases | [Worktrees](references/worktrees.md) |
| Cursor Cloud Agent runs | [Agent operations](../spx-agent/SKILL.md) |
| Staging access, inspection, or probes | [Staging connect](../spx-staging-connect/SKILL.md) |
| Staging reservations and deployment | [Staging deploy](../spx-staging-deploy/SKILL.md) |
| Verify application behavior in staging | [Staging verify](../spx-staging-verify/SKILL.md) |

Set `SPX_ROOT` if root discovery fails and `SPX_CONTAINER_HOST` if Docker publishes on another host. Use returned authentication remediation.

Destructive operations require the exact target and review of their dry run; Docker ownership labels establish which shared-stack/worktree resources belong to SPX. Keep secret values out of arguments and output. Let the first interrupt complete bounded recovery; a second requests immediate exit.

Confirm unchanged SPX plans within the user's authorized scope. A CLI confirmation flag does not itself require another user approval.

Finish at the requested outcome: readiness for startup, the command result for execution, or resource readback after a mutation. Follow applicable SPX remediation through recovery; report a remaining blocker with the operation and target that failed.

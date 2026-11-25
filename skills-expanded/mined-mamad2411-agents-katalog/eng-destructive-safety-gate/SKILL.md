---
name: eng-destructive-safety-gate
description: Require two explicit user confirmations before executing any destructive operation such as file deletion, git reset or clean, force push, database drops, or bulk overwrites. Use whenever a planned action is irreversible or destroys user data.
---

# Destructive Safety Gate

A mandatory two-confirmation checkpoint for irreversible operations. Destructive power requires deliberate human intent expressed twice, not once.

## Destructive Operation Classification

| Class | Examples | Gate Level |
|---|---|---|
| File destruction | `rm -rf`, bulk delete, overwrite without backup | Two-confirm |
| Git history | `reset --hard`, `clean -fd`, `rebase` on shared branch, `push --force` | Two-confirm + protected-branch hard block |
| Data stores | `DROP TABLE`, `TRUNCATE`, mass `UPDATE/DELETE` without WHERE | Two-confirm |
| Infrastructure | Container removal with volumes, service teardown, DNS cutover | Two-confirm |

**Always blocked regardless of confirmations:**
- Force push to `main`, `master`, `release`, or any protected branch.
- Deletion of `.git`, credentials, or backup directories.

---

## Two-Confirmation Procedure

**Confirmation 1 (Intent):** Present the operation card and ask the user to confirm intent:

```markdown
## Destructive Operation Requested
- **Command**: `<exact command>`
- **Target**: <files, tables, branches, or services affected>
- **Scope**: <N files / M rows / specific branches>
- **Irreversibility**: <what cannot be recovered>
- **Reversible alternative**: <backup path, soft delete, dry-run, or none>

Reply CONFIRM to proceed to safety preparation, or CANCEL.
```

**Safety Preparation** (between confirmations, executed automatically):
1. Create a recovery artifact when physically possible: backup branch (`backup/<timestamp>`), table dump, file archive, or volume snapshot.
2. Record the exact rollback command in the operation log.

**Confirmation 2 (Final Execute):** Re-present the summary including the recovery artifact location and require a second explicit `EXECUTE`. Any deviation between the confirmed card and current state (file count changed, new commits landed) voids both confirmations and restarts the procedure.

---

## Integration Rules

- Lifecycle orchestrators (`eng-enterprise-lifecycle`, `eng-refactor-lifecycle`, `eng-release-ops-lifecycle`) invoke this gate as a sub-gate; their own human gates do not replace it.
- Dry-run first when the tooling supports it: show `git clean -nd`, `SELECT ... before DELETE`, `terraform plan`.
- Log every gated operation to `.agents/destructive-ops-log.md` with timestamp, card content, both confirmations, and outcome.

## Checkable Completion Criteria

- [ ] Operation classified against the classification table before execution.
- [ ] Both confirmations captured verbatim with matching operation state.
- [ ] Recovery artifact created and its rollback command recorded when physically possible.
- [ ] Protected-branch hard blocks never bypassed.
- [ ] Operation logged to `.agents/destructive-ops-log.md`.
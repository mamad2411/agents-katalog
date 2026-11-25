---
namespace: aiwg
name: harness-memory-maintenance
platforms: [all]
description: Audit and maintain harness memory through reviewed aiwg memory plans, with owner receipts, verification and recovery.
triggers:
  - harness memory audit
  - harness memory cleanup
  - harness memory recategorize
  - harness memory promote
  - harness memory demote
  - harness memory retire
---

# Harness Memory Maintenance

## Discover

Use `aiwg memory` for harness memory maintenance on every provider. Fetch only
the needed section with `aiwg show skill harness-memory-maintenance --section
<section>`: Audit, Cleanup, Recategorize, Promote, Demote, Retire, Verify or
Restore. Before mutations also fetch Review and Apply. This skill stays out of
startup context; the generic CLI works without it (`aiwg memory --help`).

## Audit

Run the requested read-only inventory:

```bash
aiwg memory audit --scope project --json
aiwg memory audit --scope global --json
aiwg memory audit --scope provider --provider codex --json
```

Explain ownership, scope, loading chains, inaccessible or opaque surfaces and
uncertainty. Static eligibility does not prove live session loading. Use
`aiwg memory cost --scope project --json` for cost attribution, or
`aiwg memory recommend --scope project --json` for advisory candidates.

## Cleanup

Audit the requested scope, then run `aiwg memory recommend --scope project
--json` (or `--scope global`). Review each candidate's uncertainty, protection,
retrieval impact and owner. Cleanup selects explicit operations; it never
bulk-deletes memory. Fetch the matching operation section and Review and Apply.
Blocked candidates need owner resolution. Global recommendations are advisory;
the executable lifecycle currently supports project-owned records only.

## Review and Apply

Resolve the exact owner handle from the inventory and owner records. Executable
owners are `line-memory`, `compound-memory` and `semantic-memory`. Show global
versus project targeting, the before/after diff, owner review requirements and
native/next-session limitations before mutation. Never reinterpret a global
request as permission to change a project or provider-native source.

Create a reviewed plan, selecting the operation's flags from its section:

```bash
aiwg memory plan --owner <owner> --target <handle> --op <operation> --rationale <reason> --reviewer <reviewer> --out <new-plan.json> --json
aiwg memory apply --plan <new-plan.json> --preview --json
```

Plan creation writes only the named new file; `--preview` writes nothing.
Preserve the exact plan and its digest. Review the owner snapshot, target
revision, affected links and required approvals. Session-derived knowledge
retains the existing exact-candidate-version owner review contract. Unsupported
owners, scope changes, stale revisions or missing retrieval proof must stop.
After authorization of this concrete plan, apply the exact digest:

```bash
aiwg memory apply --plan <new-plan.json> --confirm <plan-digest> --json
aiwg memory verify --plan <new-plan.json> --json
```

Changes affect the next session. Native provider caches and current loaded
context remain unverified; adapter regeneration belongs to its existing owner.
Report owner receipts and partial failures. Re-audit and replan stale input;
never edit a reviewed plan to force confirmation.

## Recategorize

Fetch Review and Apply. Select `--op recategorize --category <category>` in
the plan command. Preserve placement and lifecycle; a taxonomy correction does
not grant promotion or retirement authority. The category must be accepted by
the target's owner. Review the category diff and retained identity/history,
then apply and verify through the shared reviewed workflow.

## Promote

Fetch Review and Apply. Select `--op promote --placement <placement>` in the
plan command. Placement order is archived, indexed, task-context, resident;
promotion must move upward. Prefer indexed storage and bounded task context
before residency. Explain the measured need and cost of residency; protected
or session-derived sources retain their owner review requirements. Verify the
owner state after apply; residency does not prove current-session activation.

## Demote

Fetch Review and Apply. Inspect low-use evidence with `aiwg memory cost
--scope project --usage <usage.json> --demote <id-or-path> --json`; this is a
read-only estimate. Select `--op demote --placement indexed` (or another lower
placement) and repeatable `--link <indexed-path>` in the plan command.
Resident removal requires the owner's indexed retrievability proof, not just
an unrelated copy or smaller file. The current line-memory and compound-memory
owners cannot prove that projection and refuse resident removal. Preserve the
source and report that limitation rather than bypassing it. Retain history and
retrieval anchors for supported owner transitions, then apply and verify.

## Retire

Fetch Review and Apply. Select `--op retire --retirement-basis review` in the
plan command after reviewing use history, rare obligations and owner protection.
Unknown history cannot justify age-based retirement. Retirement changes only
lifecycle, keeps the tombstone and owner history, and excludes retired content
from active retrieval. It never purges the source. Record the reason and exact
revision, apply and verify, and retain the plan for recovery.

## Verify

Run `aiwg memory verify --plan <applied-plan.json> --json` after apply or
recovery. This read-only check uses existing owner receipts and retrieval checks
to confirm recorded end states, retained history/tombstones and required indexed
retrievability. Report findings and failed or stale checks with the CLI exit
code. A local pass does not establish live provider loading or flush native
caches; no new verification store is needed.

## Restore

Fetch Review and Apply. Inspect the owner's retained tombstone/history and
current revision. Create a fresh `--op restore` plan for the retired or
superseded handle, with the current owner snapshot, reviewer and recovery reason.
Review the diff using `aiwg memory restore --plan <restore-plan.json> --preview
--json`, then execute `aiwg memory restore --plan <restore-plan.json> --confirm
<restore-plan-digest> --json` after authorization. Verify that restore plan.
Restoration returns the recorded lifecycle to active and preserves history;
purged data and unsupported native sources cannot be restored by this workflow.

## References

- @$AIWG_ROOT/docs/user-level-project-memory.md — worked operator examples
- @$AIWG_ROOT/docs/cli/reference.md — generic CLI flags and exit codes
- @$AIWG_ROOT/docs/architecture/harness-memory-maintenance.md — owner contracts

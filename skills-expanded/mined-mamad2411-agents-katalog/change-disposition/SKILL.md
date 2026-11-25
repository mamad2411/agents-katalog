---
name: change-disposition
description: Close an OpenSpec change without implementing it by recording an exact superseded, deferred, or rejected disposition and archiving without spec merges. Use when a proposal is superseded, should be deferred, is irrelevant or wontfix, must be rejected, needs archive skip-specs, or should be killed without implementation.
---

# Change Disposition

Treat disposition as a terminal close-without-implementation workflow. Preserve the proposal and
its decision evidence, prevent unimplemented deltas from entering main specifications, and surface
every active dependent before closure.

**MANDATORY:** Before writing a marker, read
[references/marker-templates.md](references/marker-templates.md) completely. Use one template
without renaming or inventing fields.

## Choose exactly one disposition

| Disposition | Use when | Required lineage |
| --- | --- | --- |
| `superseded` | A named change now owns the same intent | `superseded-by: <change-id>` |
| `deferred` | The intent survives, but work is parked indefinitely | `reopen-when: <concrete condition>` |
| `rejected` | The work is irrelevant, unjustified, or not worth doing | A specific rationale |

Normalize informal requests such as “abandoned,” “cancelled,” or “wontfix” to the disposition
whose meaning matches. Marker filenames and fields use only `superseded`, `deferred`, or
`rejected`; never persist an informal synonym as a fourth disposition.

Do not use `deferred` for a scheduled pause with an ordinary resumption date. Keep that change
active or use the repository's normal task deferral mechanism. A disposition is indefinite and
terminal until an explicit reopen condition is met.

## Stop when disposition is unsafe

Stop and report a rollback or completion decision instead when any proposed behavior or spec delta
has already merged into the main specification tree. Partially implemented work may require
reversion, migration, or normal completion; `--skip-specs` cannot undo merged behavior.

Also stop when:

- no authorized decision identifies the disposition and deciding context;
- `superseded` lacks a real replacement change;
- `deferred` lacks an observable reopen condition;
- a live claim owns the change or an affected dependent;
- the change cannot be resolved to one active directory;
- repository instructions require a different terminal process.

## Capture pre-closure evidence

1. Resolve the active change directory and any attached feature or task bead markers (inert
   history after the 2026-09 Beads removal; record, do not act on them).
2. Validate the change using the repository's strict OpenSpec command.
3. Count checked and total task boxes from the authoritative task artifact. Record the result as
   `tasks-at-closure`; do not check unfinished tasks merely to make the count look complete.
4. Confirm that none of `SUPERSEDED.md`, `DEFERRED.md`, or `REJECTED.md` already exists.
5. Fingerprint the main specification tree before archival. Use a byte-level repository command,
   for example:

```bash
find openspec/specs -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
```

Preserve the resulting digest in the execution evidence. If the repository has no main spec tree,
record that fact rather than creating one.

## Write exactly one marker

Create the disposition's canonical marker in the active change directory:

- `superseded` → `SUPERSEDED.md`
- `deferred` → `DEFERRED.md`
- `rejected` → `REJECTED.md`

Fill every common field: decision date, deciding context, reason, task completion state, and
dependents swept. Add `superseded-by` only for superseded work and `reopen-when` only for deferred
work. Use an ISO date and a stable deciding-context locator such as a session, handoff, decision
record, or proposal.

Reject closure if more than one canonical marker exists. Do not use `ABANDONED.md`,
`CANCELLED.md`, `WONTFIX.md`, prose-only task notes, or a custom archive directory.

## Sweep active dependents

Search active proposals for the exact change id before archiving:

```bash
rg -n -F "$change_id" openspec/changes --glob 'proposal.md'
```

Inspect every match in `depends on`, `Extends`, and `after:` metadata or prose. For each dependent,
either amend it under the current authority or list it in the marker's `## Dependents swept`
section as a follow-up disposition candidate. Do not silently leave a dependency pointing at a
terminal change.

When a proposal supersedes other changes, require its own `## Context` to name every superseded
change. If that lineage is missing and cannot be amended safely, stop before closure.

## Bead markers are inert history

The `[beads:ID]` markers in a change's tasks.md are historical credits, not live workflow state
(Beads tooling removed 2026-09). Do not attempt to close, mint, or sync any bead. If a change's
closure evidence template asks for bead closure, record `beads: inert-history (tooling removed)`
instead of a closure result.

## Archive without merging deltas

Archive only after the marker and dependent sweep are complete:

```bash
openspec archive "$change_id" --skip-specs -y
```

Never omit `--skip-specs`. Never use normal archive-on-success semantics for a dispositioned
change, even when its delta appears harmless.

After archival:

1. Confirm the change no longer appears in the active change list.
2. Confirm the standard dated archive directory exists and contains exactly one canonical marker.
3. Recompute the main-spec fingerprint and require it to equal the pre-archive digest.
4. Run the repository's archive and workflow closure checks.
5. Persist the archive and tracker state using the repository's required commit and push policy.

If the main-spec fingerprint changed, stop. Preserve the evidence and repair through the
repository's explicit recovery process; do not claim a successful disposition.

## Report completion

Report the disposition, marker path, deciding context, task count at closure, dependents amended or
flagged, exact archive command, archive location, before/after spec digest,
validation results, and persistence outcome. A marker without the dependent sweep, non-merging
archive, or required tracker closure is incomplete.

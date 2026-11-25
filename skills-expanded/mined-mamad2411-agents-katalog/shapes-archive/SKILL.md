---
name: shapes-archive
description: >
  Walks every unarchived amendment and decides whether to archive it.
  Triggers when performing archival passes, cleaning up stale amendments,
  or running deep audits that include archival. Provides the full decision
  framework for when to archive, when not to, and the mechanics of toggling
  the archived flag.
user-invocable: true
---

```!
shapes preflight 2>/dev/null || echo "Shapes CLI not found. Install it: cargo install shapes-cli"
```

# Archiving Stale Amendments

Amendments are immutable change records kept forever for audit, so the
log grows with entries whose insight value decays over time. An archival
pass walks every unarchived amendment and judges whether it still
provides context a future reader would actually use.

Archiving is never deletion. The YAML file stays on disk, validation
and CI still see it, and `shapes list --archived` / `shapes get
<parent> --archived` bring it back into view on demand. Archival only
affects how listings are rendered — it never weakens enforcement.

## Contents

- When to Archive
- When NOT to Archive
- Running an Archival Pass
- Mechanics
- CLI Quick Reference

## When to Archive

Archive an amendment when reading it would provide no real
understanding a caller could not already get from the current state
of the shape, constraint, or code. Concrete examples of "no longer
valuable":

- It documents a decision that has since been fully superseded by a
  later amendment (and the later amendment captures the rationale).
- It describes a transient migration step that completed long ago and
  whose intermediate state no longer exists anywhere in the repo.
- It records a renaming or trivial refactor whose "why" is obvious
  from the current code and leaves no cross-cutting consequences.
- Its rationale is now fully inlined into the target shape's intent
  (goals / non-goals / rationale), making the amendment redundant as
  context.

## When NOT to Archive

- Recent amendments on untouched canonical nodes — their "why" is
  still load-bearing for agents planning the next change.
- Amendments that encode a non-obvious invariant, trade-off, or
  constraint decision that is not otherwise captured in code or
  constraint text.
- Anything you are uncertain about. Archival is a cleanup pass, not
  a judgement call to make under pressure — when in doubt, leave it.

## Running an Archival Pass

Walk every unarchived amendment and apply the criteria above. Follow
these steps:

### 1. Load the full amendment list

```bash
shapes list amendment                # unarchived only (your working set)
shapes list amendment --archived     # full picture including already-archived
```

The first command is the set you will evaluate. The second gives
context — if you see that related amendments were already archived,
that may inform whether the current one is still load-bearing.

### 2. Evaluate each unarchived amendment

For each amendment in the working set:

1. Read the amendment: `shapes get amendment <id>`
2. Read its target shape or constraint: `shapes get shape <target-id>`
   (or `shapes get constraint <target-id>`)
3. Ask: does this amendment provide understanding that a reader could
   not already get from the current state of its target and code?
4. Apply the "When to Archive" / "When NOT to Archive" criteria.

When the answer is clearly "no longer valuable", mark it for archival.
When uncertain, leave it.

### 3. Archive qualifying amendments

```bash
shapes amendment archive <id> --reason "Changes integrated into target shapes"
```

The `--reason` flag is required — every archival decision must be
explained so future readers understand why the entry was hidden.
Write a reason that summarizes why the amendment no longer provides
unique context (e.g., "Changes integrated into target shapes" or
"Superseded by amendment 42"). After each archive, the command prints
the full amendment so you can confirm the change landed correctly.

### 4. Validate integrity

```bash
shapes validate
```

Archiving should never cause validation failures (archived amendments
still participate in reciprocity and all invariant checks), but
confirm exit code 0 as a safety check.

### 5. Summarize

Report what was archived and why. For each archived amendment, one
line: the id, the name, and the reason it qualified. This gives the
user a reviewable record of the pass.

## Mechanics

Setting or clearing `archived` is the sole permitted mutation of a
canonical amendment. CI-003 (modified-amendment-immutability) explicitly
allows diffs whose only field delta is `archived`; every other field
remains strictly immutable.

The `archived` field is an object with a required `reason` string:

```yaml
archived:
  reason: Changes integrated into target shapes
```

When absent, the amendment is not archived. The `shapes amendment
archive` / `shapes amendment unarchive` commands are the sole write
path for the field. Do not hand-edit amendment YAML to toggle archival
— use the commands so the toggle is centralized in one code site.

## CLI Quick Reference

```bash
# Archival commands
shapes amendment archive <id> --reason "..."  # hide from default listings
shapes amendment unarchive <id>              # restore to default listings

# Discovery (useful during archival passes)
shapes list amendment                    # unarchived amendments only
shapes list amendment --archived         # include archived amendments
shapes get amendment <id>               # read a specific amendment
shapes get shape <id>                    # shape with archived amendments hidden
shapes get shape <id> --archived         # shape with archived amendments annotated
shapes get constraint <id> --archived    # constraint with archived amendments annotated
```

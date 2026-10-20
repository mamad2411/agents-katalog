---
description: "Merge a completed change's delta into its capability spec, then move the change folder to the dated archive. Idempotent — running twice produces an identical tree."
agent: agent
tools: [read, edit, search, execute]
argument-hint: "Change name (defaults to the only in-flight change)"
---

Archive this change:

${input}

Merge its delta into the capability it targets, then preserve the change folder with its date.
This is **Phase 7** of the cycle, and it runs before the PR so the merged capability and the
archived change ship in the same pull request.

If no change name is given: use the only folder in `specs/changes/` (ignoring `archive/`). If
several exist, list them and ask which.

---

## Step 1 — Preflight (all checks before any file is touched)

Run every check below **first**. A failure here must leave the working tree untouched — a
half-merged capability is far worse than a refused archive.

1. **Read the change.** `specs/changes/<name>/` — `proposal.md`, `delta.feature`,
   `delta-rules.md`, `tasks.md`.
2. **Read the capability.** `specs/capabilities/<domain>/behavior.feature` and `rules.md`.
   If the proposal says this change creates the capability, expect them to be absent.
3. **Settle the archive destination now.** The name is
   `specs/changes/archive/<YYYY-MM-DD>-<change-name>/`, using today's local date.
   - If `<change-name>` already begins with `YYYY-MM-DD-`, keep it as-is. Do not stack a second
     date prefix — it stutters the name and, when archiving happens on a later day, files the
     change under a day it did not happen on.
   - If that destination already exists, **stop**. Report the collision and do nothing else.
4. **Resolve every delta tag against the capability.** For each scenario in `delta.feature`:
   - `@added` — the capability must **not** already have a scenario by that name
   - `@modified:"X"` / `@removed:"X"` / `@renamed:"X"` — the capability **must** have a scenario
     named exactly `X`
   - Any mismatch is an error. Report the tag, the name it references, and the closest actual
     scenario name. Do not guess — a near-miss name is a typo to fix, not an intent to infer.
5. **Check `@modified:` completeness.** Each one must carry every `Then`/`And`-after-`Then` step
   the capability's version has. If any is missing, **stop**: that is a removal of a guarantee
   wearing a `@modified:` tag. Report which steps would be lost.
6. **Check the merged `@smoke` count.** After merging, the capability must have **exactly one**
   `@smoke` scenario. Report a violation and stop.

   That is the only priority-tag count checked here. The `1–2 @happy-path / 2–4 @edge-case /
   2–3 @error` budget is authoring guidance for **one change's delta** — the shape of a single
   feature's worth of behavior. A capability accumulates scenarios across many changes, so those
   counts only ever grow; enforcing them here would block every archive against any capability
   that has been through more than a change or two.
7. **Check tasks.** If `tasks.md` has unchecked `- [ ]` items, report the count and ask whether
   to continue. In autonomy mode (a), report and continue. Never silently ignore them.
8. **Check for emptying.** If the delta's `@removed:` scenarios would leave the capability with
   no scenarios at all, **stop** unless `specs/changes/<name>/.atdd.yaml` declares
   `retire_capability: true`. Deleting a capability is only recoverable from git, so it stays an
   explicit decision. Say plainly that adding the marker is what unblocks it.

Report the preflight result as a table before proceeding.

---

## Step 2 — Merge the behavior

Apply to `specs/capabilities/<domain>/behavior.feature`:

| Tag                     | Action                                                                       |
| ----------------------- | ---------------------------------------------------------------------------- |
| `@added`                | Append the scenario to its priority group, preserving the file's tag ordering |
| `@modified:"X"`         | Replace scenario `X` wholesale with the delta's version, in place             |
| `@removed:"X"`          | Delete scenario `X` and its steps                                             |
| `@renamed:"X"`          | Change scenario `X`'s title to the delta's title. Do not move it              |

**Strip every delta tag as you merge.** A capability file never contains `@added`,
`@modified:`, `@removed:`, or `@renamed:` — only priority tags survive. Leaving one behind is
the single most common way this merge goes wrong; check the result before writing.

Keep the capability's `Feature:` block, `Background:`, comments, and scenario order otherwise
untouched. If the capability did not exist, create it from the delta: the `Feature:` block, a
`Background:` if the delta has one, and every `@added` scenario with its tag stripped.

## Step 3 — Merge the rules

Apply `specs/changes/<name>/delta-rules.md` to `specs/capabilities/<domain>/rules.md`:

- **ADDED** — append, taking the next free number
- **MODIFIED** — replace the rule text at its existing number, keeping the number stable
- **REMOVED** — delete the rule. Do **not** renumber the survivors; gaps are correct, because
  tests and comments elsewhere may cite the old numbers
- Update the `Last updated` field to today

## Step 4 — Archive the change folder

Move `specs/changes/<name>/` to the destination settled in step 1. Move it whole — proposal,
delta, rules, tasks, and metadata all stay together, which is what makes the archive answer
"why did this change?" years later.

If the change carried a Phase 6 doc-sync record or a resolved Spec Weakenings table, it moves
with the folder. That record is the audit trail for every guarantee that was narrowed.

## Step 5 — Verify

1. The capability file contains **no** delta tags.
2. Every delta scenario is accounted for: added ones present, modified ones replaced, removed
   ones gone, renamed ones retitled.
3. The capability's scenario count equals `before + added − removed`.
4. `specs/changes/<name>/` no longer exists; the archive path does.
5. Re-run the full test suite — the merge changed spec files, not code, so it must still be green.

## Idempotency

Running this command twice must produce an identical tree. The second run finds no
`specs/changes/<name>/`, reports that the change is already archived at its dated path, and
changes nothing. It must not error, and must not re-merge.

---

## Report

```markdown
## Archived: <change-name>

**Capability**: `specs/capabilities/<domain>/` (updated | created)
**Archived to**: `specs/changes/archive/<YYYY-MM-DD>-<change-name>/`

| Operation | Count | Scenarios                        |
| --------- | ----- | -------------------------------- |
| Added     | N     | "...", "..."                     |
| Modified  | N     | "..."                            |
| Removed   | N     | "..."                            |
| Renamed   | N     | "..." → "..."                    |

| Rules    | Count | Numbers      |
| -------- | ----- | ------------ |
| Added    | N     | 7, 8         |
| Modified | N     | 3            |
| Removed  | N     | 5 (gap kept) |

**Capability now**: N scenarios (@smoke 1, @happy-path N, @edge-case N, @error N), M rules
**Delta tags remaining in capability**: 0 ✅
**Tests**: ✅ N/N passing
```

## Rules

- **Preflight fully before mutating.** Any failure leaves the tree untouched.
- **Never guess a name.** An unmatched `@modified:`/`@removed:`/`@renamed:` is an error to
  report, not an intent to infer.
- **Never strip a guarantee.** A `@modified:` missing a `Then` the capability has is a blocked
  archive, not a silent narrowing.
- **Never leave a delta tag in a capability file.**
- **Never renumber rules** after a removal.
- **Never delete a capability** without `retire_capability: true`.

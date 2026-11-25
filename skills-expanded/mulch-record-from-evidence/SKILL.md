---
name: mulch-record-from-evidence
description: Turn the evidence of a finished work session — git commits, changed files, recently-touched seeds issues — into well-formed `ml record` invocations. Use at session close, when an agent has made changes worth preserving as mulch expertise but hasn't yet recorded them.
tools:
  - bun
  - git
  - ml
inputs:
  - a finished (or nearly finished) unit of work in the mulch repo
  - optionally, a specific commit range or seeds issue id to scope the evidence
outputs:
  - one or more validated records appended to `.mulch/expertise/<domain>.jsonl`
  - a committed `.mulch/` change via `ml sync`
---

# mulch-record-from-evidence

Use this skill when you have just finished a chunk of work in the mulch
repo and need to **preserve the durable insights as mulch expertise**.
It converts concrete evidence — what you changed, why, and what broke
along the way — into precise `ml record` calls, instead of inventing
ritual filler records. Unrecorded learnings are lost; vague records are
noise. The goal is a small number of high-signal records, each backed by
real evidence.

## When NOT to record

Skip recording entirely if the session produced no durable insight: a
trivial typo fix, a dependency bump with no behavioral change, or a
revert. A record that just restates the diff is noise. Only record a
convention, pattern, decision, or failure that a *future* agent would
benefit from knowing before touching the same area.

## Pre-flight

Confirm you are at the mulch repo root and the store is healthy:

```bash
ml status                         # per-domain health + record counts
ml doctor                         # exits 0 when records are intact
```

If `ml doctor` reports problems, fix the store first (see
`RUNBOOK.md` §4) — do not record on top of a corrupt JSONL.

## Procedure

### 1. Gather the evidence

Let mulch tell you what changed and which domains are implicated:

```bash
ml learn                          # changed files + suggested domains
git status                        # uncommitted work
git diff --stat HEAD~1            # what the last commit touched
git log --oneline -5              # recent commit subjects
```

If the work maps to a tracker, pull its context too:

```bash
sd show <issue-id>                # the seeds issue you were working
```

Write down, for each insight candidate: **what** you learned, **which
file or subsystem** it concerns, and **what evidence** supports it
(a commit sha, a changed file, a failing test you fixed).

### 2. Classify each candidate

For every insight worth keeping, decide:

- **Domain** — which `.mulch/expertise/<domain>.jsonl` it belongs to.
  Run `ml status` to see existing domains; match the subsystem you
  touched (e.g. CLI behavior → `cli`, test infra → `testing`, type
  conventions → `typescript`). Respect the project's per-domain
  `allowed_types` rules printed at the top of `ml prime` — a domain may
  only accept certain types.
- **Type** — `convention` (a rule to follow), `pattern` (a reusable
  approach that worked), `decision` (a choice made and its rationale),
  `failure` (something that broke and how it was resolved),
  `reference` (an external fact/link), or `guide` (a procedure).
  Custom project types (e.g. `flake_symptom`, `release_decision`) carry
  extra required fields — `ml record` will tell you which.
- **Classification** — `foundational` (permanent truth),
  `tactical` (relevant ~14 days), `observational` (relevant ~30 days).
  Default to the shortest shelf life that fits; only mark `foundational`
  when the insight is a lasting invariant.

### 3. Emit the `ml record` calls

Run one `ml record` per insight. Evidence auto-populates from the
current git commit and changed files; link explicitly when you can:

```bash
ml record cli --type convention \
  --description "ml ready/prime/compact reject non-integer --limit/--budget with exit 1; each command inlines its own parseStrictPositiveInt rather than sharing a util" \
  --evidence-seeds <issue-id>
```

Useful evidence flags:

- `--evidence-seeds <id>` / `--evidence-gh <id>` — link a tracker.
- `--evidence-commit <sha>` — pin a specific commit.
- `--relates-to <mx-id>` — link a related mulch record.

Naming a record (a stable identity) makes a re-record **merge outcomes**
into the existing entry instead of appending a duplicate — prefer this
when you are refining an insight you recorded before. If validation
fails, mulch prints a copy-paste retry hint with the missing required
fields pre-filled; fill them in and re-run.

### 4. Verify and commit

```bash
ml validate                       # confirm every new record is well-formed
ml prime <domain>                 # eyeball that the new record reads cleanly
ml sync                           # validate, stage, and commit .mulch/
```

Do not `git push` unless the user asks — leave the commit local.

## Acceptance

The skill is complete when **all** hold:

- Each durable insight from the session is captured by exactly one
  record (no duplicates, no filler).
- `ml validate` exits 0.
- `ml prime <domain>` shows the new record(s) with sensible
  domain/type/classification.
- `ml sync` has committed the `.mulch/` change; `git status` is clean.

## Failure modes

| Symptom | Likely cause | Remedy |
|---------|--------------|--------|
| `ml record` rejects `--type` for a domain | The domain's `allowed_types` doesn't permit that type. | Pick an allowed type (check the contract at the top of `ml prime`), or record under a different domain. |
| Validation error about a missing field | A custom type requires extra fields. | Re-run with the fields from the printed retry hint. |
| Two near-identical records appear | Recorded anonymously twice instead of naming the record. | Name the record so re-records merge; remove the duplicate with `ml delete <id>`. |
| `ml sync` reports an unknown type | Config declaring the custom type hasn't merged yet. | Wait for config to land, or re-run after merging; sync intentionally ignores `--allow-unknown-types`. |

## Further reading

- `AGENTS.md` — repo-wide conventions and the agent workflow.
- `CLAUDE.md` — record types, classifications, and the registry layer.
- `CONFIG.md` — `.mulch/mulch.config.yaml` reference (domains, custom
  types, hooks).
- `RUNBOOK.md` — operational procedures, including debugging a broken
  store.

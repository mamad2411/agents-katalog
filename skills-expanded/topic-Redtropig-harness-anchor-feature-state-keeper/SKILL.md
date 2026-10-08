---
name: feature-state-keeper
description: Use when starting, advancing, finishing, or blocking a feature. Manages feature_list.json + progress.md + session-handoff.md. Default-FAIL enforced.
---

# Feature State Keeper

You maintain the **machine-readable scope record** of this project. Three files form the state trio:

| File | Role |
|---|---|
| `feature_list.json` | Scope boundary + done criteria + evidence |
| `progress.md` | Append-only session history |
| `session-handoff.md` | Single-page "what's the state right now" |

## Altitude — feature ledger vs superpowers' execution records

When `superpowers` is also active, **two record systems coexist by altitude — keep them from drifting:**

| Record | Owner | Altitude |
|---|---|---|
| `feature_list.json` | harness-anchor (this skill) | **project feature ledger** — one entry per feature, status + evidence; the durable **source of truth** for "is feature X done" |
| `progress.md` | harness-anchor | session-level history (summaries), append-only |
| `docs/superpowers/plans/*.md` (`- [ ]` steps) + **TodoWrite** | superpowers (`writing-plans` / `subagent-driven-development`) | **execution detail** for the *one* in-progress feature — ephemeral scaffolding for the current build |

**Sync contract (prevents double-bookkeeping and drift):**

1. Superpowers' plan-doc checkboxes and TodoWrite drive **step-level** execution. Do **not** mirror individual steps into `feature_list.json` or `progress.md`.
2. When a superpowers plan/feature finishes (final review passes), **reflect it back once**: flip that feature's `status` in `feature_list.json` with the evidence object. That single write is the durable record it's done.
3. `feature_list.json` answers "what features exist / which is active / is it done"; the plan-doc + TodoWrite answer "what are the steps to build the active one." If they disagree, **`feature_list.json` (with evidence) wins.**
4. **Parallel / subagent dispatch is a shared-state writer too.** When work is fanned out with `superpowers:dispatching-parallel-agents` or `subagent-driven-development`, the dispatched workers treat this trio — above all `feature_list.json` — as **shared state** (the dispatching skill's own rule: don't fan out over shared resources). Workers must **not each write** the trio; the coordinating **parent reconciles once** after they return — the same reflect-back-once write as item 2. Because workers are single-level, they also don't run the subagent-backed gates (`/verify` · `/test-plan` · `/gc`) — the **parent** runs those after the workers integrate, then flips the one ledger entry. Parallel work is normally *within one feature* (independent sub-tasks), so it is exactly the plan/Todo case above.

## When to use

- Starting a session: read all three, identify the active feature
- Finishing a unit of work: update them before stopping
- User asks "what are we working on?" / "what's the status?" → consult `feature_list.json` first
- User adds a request that doesn't match the active feature → use `scope-jump` flow below

## Reading order

```
session-handoff.md   →  what was just being done
feature_list.json    →  what's planned, in-progress, blocked
progress.md          →  recent history (only if needed for deep context)
```

Most sessions only need handoff + feature_list. Skip progress.md unless you genuinely need the longer view.

**Cold history (archives).** Once `/session-end`'s budget step has archived, older content
lives in `progress-archive.md` and `feature_archive.json` (moved verbatim by
`state-archive.mjs`; hot windows: newest 20 progress sections; live features + the 10 most
recently completed `pass` entries). History questions → **grep the archives**; never load
them whole. They are read-only history: never hand-edit them, never reuse an archived id.
One retired signal to know about: the PostToolUse regression-warn matches evidence artifacts
against the **hot** ledger only, so an archived feature's file-specific warning retires with
it — the generic "source changed after pass" nudge continues via the retained pass entries.

## Active-feature rule

**Exactly one feature has `status: "in-progress"` at a time** unless the project has an explicit multi-track plan documented in AGENTS.md.

If you discover work that doesn't match the active feature:

1. Add it to `feature_list.json` with `status: "planned"` and a description
2. Tell the user: *"This looks like new scope. I've recorded it as a planned feature. Should I finish <active feature> first, or pivot?"*
3. Wait for confirmation before changing status.

**Action-layer backstop:** the post-tool-use hook warns the moment a *new code module* is created
while a feature is in-progress — so "record new scope as `planned` first" is enforced at write-time,
not only when the new work happens to be phrased in a prompt. Warn-only: it surfaces the new module
for you to either confirm in-scope or record as planned; it never blocks.

### Negative scope — `out_of_scope` (optional)

A feature may declare what it deliberately does NOT cover:

```json
"out_of_scope": ["UI redesign", "performance tuning"]
```

Set it at feature creation when the user draws the boundary. Consumers: the
PostToolUse **pulse checkpoint** quotes it periodically, so agent-initiated
drift is checked against an explicit list instead of a guess, and scope-jump
conversations can cite it. Omit the field when no exclusion is worth naming.

## Feature id uniqueness

`id` is the **lookup/mutation key** — `/verify` flips *the* feature to `pass` and attaches evidence
by id, and the hooks find the active feature by it. Two features sharing an id make those updates
ambiguous (wrong entry, or both). The JSON Schema **cannot** catch this (draft-07 has no per-field
uniqueness), so it is on you to keep ids unique.

**Mint the id with the tool BEFORE you write the new entry — don't eyeball the list** (scanning a
long id list for a clash is unreliable and splits your attention from composing the feature):

1. Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/feature-list-validate.mjs --check <candidate-id> feature_list.json`
   (exit 0 = free; non-zero = taken, and it prints a free suggestion). The tool treats ids in
   `feature_archive.json` as taken too — archived ids stay reserved because history (progress
   entries, evidence, commits) references them. *If node is unavailable, fall back to scanning
   the existing ids yourself (both files).*
2. **If the candidate collides, qualify the NEW entry's id** — take the suggestion (`parser-2`) or a
   descriptive variant (`parser` → `parser-cli`, `parser-net`). Never reuse a slug; never rename an
   *existing* id to dodge the clash.
3. Then write the entry with the unique id.

Backstops if one slips through: the **post-tool-use hook** warns the moment a duplicate is written,
and **`/session-end`** runs `feature-list-validate.mjs` before committing. Both are warn-only — they
catch, they don't fix. Resolve a flagged duplicate by renaming the newer entry, as above.

## Default-FAIL evidence contract

Before flipping `status` to `"pass"`:

| Criterion | Evidence requirement |
|---|---|
| Build passes | Build log path (e.g. `.build/last-build.log`) + exit code 0 |
| Type check passes | Command output captured |
| Tests pass | Test runner output showing N passed, 0 failed |
| Static analysis | Lint report file or empty-warnings confirmation |

Write evidence to `feature_list.json`:

```json
{
  "id": "...",
  "status": "pass",
  "evidence": {
    "timestamp": "2026-05-28T13:00:00Z",
    "commit": "abc123...",
    "artifacts": [
      ".build/last-build.log",
      "test-results/run-42.txt",
      "lint-report.txt"
    ],
    "notes": "Optional human-readable summary"
  },
  "completedAt": "2026-05-28T13:00:00Z"
}
```

**If any criterion lacks evidence**: do NOT mark pass. State explicitly:

> "I am uncertain whether <feature> is fully done because <criterion> lacks evidence. Recommend running `<command>` to verify."

This is the calibrated-uncertainty pattern. Bluffing breaks user trust.

## Updating progress.md

At every `/session-end` — and at mid-session milestones (a status flip, a verified chunk):
prepending a short entry **now** beats reconstructing the session at its end from a compacted
context. The template header carries HH:MM, so several entries per session are fine:

1. Compose a concise new section (5-10 lines max) in the template format
2. **Prepend** it (most recent first). Prefer the tool — `node ${CLAUDE_PLUGIN_ROOT}/scripts/progress-prepend.mjs progress.md <entry-file>` — which inserts after the header **without loading the whole file** (cheap on a long history). Fallback: Read + prepend + Write.
3. Never delete past entries (append-only). The `/session-end` budget step may *move* the
   oldest sections to `progress-archive.md` — verbatim relocation by `state-archive.mjs`,
   never deletion.

## Updating session-handoff.md

This file is **overwritten** at end of session — it should reflect *current* state only.

Required fields:
- Last updated timestamp
- Active feature id
- What's in flight (2-5 bullets)
- Build/test/lint state (pass/fail/not-run + timestamp)
- The ONE concrete next action
- Risks / things to avoid

Aim for ≤ 300 words. The next session should be able to resume from this alone.

## Schema validation

`feature_list.json` validates against `feature_list.schema.json` (JSON Schema draft-07). When you edit feature_list.json:

- Required: `project`, `features` (array)
- Per feature: `id`, `name`, `description`, `status`, `done_criteria`
- `id` is kebab-case, **unique across all features**, and never renamed once set (see "Feature id uniqueness" below)
- `status` ∈ `planned | in-progress | pass | blocked`
- `evidence` MUST be non-null when `status == "pass"` (Default-FAIL invariant)

If the schema file is present, an external validator (e.g. `ajv-cli`) can verify. The agent need not run it — write valid JSON the first time by following the shape above.

## Ordering — actionable-first (applied by /session-end)

Features are kept **actionable-first** (in-progress → blocked → planned → pass) by
`scripts/feature-list-sort.mjs`, run at `/session-end`. Don't hand-reorder the array — let the
tool do it deterministically (it only reorders; ids, evidence, and unknown fields are preserved).
This keeps what you most need at the top, so reading the **head** of a long `feature_list.json` suffices.

## Looking up JSON Schema constraints

For non-trivial schema constructs (`allOf`, `oneOf`, `if/then`, regex patterns) — invoke the `docs-lookup` skill. Don't guess schema syntax; `feature_list.schema.json` validation must stay correct, and a malformed schema silently disables enforcement.

Typical entry query: `json schema <construct>` (e.g. `json schema if then else`).

## Related

- For evidence-gathering procedure → `anti-hallucination-gates` skill
- For end-of-session ritual → `/session-end` command
- For project index → `project-indexing` skill
- For quick read-only overview → `/status` command

## Committing as features advance

Each feature status flip (planned → in-progress → pass / blocked) should be its own commit:

1. **Commit on status change.** When you update `feature_list.json` to flip a feature's status, commit immediately with a message like `feat(engine-init): start` or `feat(engine-init): mark pass`.
2. **Never bundle unrelated changes.** A status-flip commit should only contain `feature_list.json` + `progress.md` (if updated). Code changes go in their own commits. (Mirrors CLAUDE.md: "never bundle unrelated layers in one commit".)
3. **Branch/PR discipline is superpowers' domain.** Don't reinvent — defer to superpowers' `requesting-code-review` and `finishing-a-development-branch` skills for branching, PRs, and merge strategies.
4. **Unfamiliar git commands?** Use `docs-lookup` skill — don't guess flags or syntax.

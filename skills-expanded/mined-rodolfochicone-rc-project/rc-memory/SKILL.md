---
name: rc-memory
description: "Project memory under .rc/memory/ — facts, lessons, golden paths. Use before working and after a correction. Do not use to edit source."
model: sonnet
effort: medium
---

# Memory

The one place for what RC remembers about *this project* across turns and sessions. Project-scoped
only — never copy memory to another project or a global location. Plain markdown plus one
machine-owned JSON store; this skill never edits source code.

```
.rc/memory/
  INDEX.md              # one line per fact — the recall entry point
  <slug>.md             # one durable fact per file
  lessons.json          # machine-owned lesson store (scripts/lessons.mjs) — do NOT hand-edit
  LESSONS.md            # rendered playbook, regenerated on every write
  observations.jsonl     # raw capture appended by the observe hook (transient)
```

Resolve the project's `.rc` base directory (nearest `.rc` walking up; default `./.rc`).

## Routing

The **shape** of the knowledge decides where it goes; first match wins.

| The knowledge is… | Goes to |
| --- | --- |
| a standalone statement — a decision, convention, gotcha, term | **A — Facts** |
| something a verification signal or a user correction taught us | **B — Lessons** |
| a multi-step route with commands, a required order, and dead-ends | **C — Golden paths** |
| only true while one task runs | **Scratch**, below |
| a one-off unlikely to recur | nowhere — drop it |

## A — Facts

One `<slug>.md` per fact, frontmatter plus a short body:

```markdown
---
title: <short title>
scope: decision | convention | gotcha | glossary | context
tags: [a, b]
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

<the fact in a few sentences. For a decision, add **Why:** and, if useful, **How to apply:**.>
```

`INDEX.md` holds one line per fact, newest last: `- [<title>](<slug>.md) — <scope> — <one-line hook>`.
It is the only file you read to decide relevance; never dump fact bodies into it.

**Consult** before implementing, deciding or planning: read `INDEX.md`, scan the hooks for the task's
terms, open only the matching `<slug>.md`. For a large store, `grep -ri "<term>" .rc/memory/`.

**Record** only when all three hold: (1) a future run needs it to avoid a mistake or rediscovery;
(2) it is durable for this project, not one task's execution; (3) it is not already obvious from the
repo, git history, or the spec. Reuse the slug to update rather than duplicate. Never store secrets,
tokens, credentials, large code blocks, stack traces or raw session logs.

## B — Lessons

A lesson is what a **failure or a correction** taught us, and it is only trusted once it recurs
across two distinct features. `scripts/lessons.mjs` owns every mechanical part — IDs, recurrence
counting, candidate→confirmed promotion, quarantine, pruning, rendering — because that is exactly
the bookkeeping that rots when done by hand. Never hand-edit `lessons.json` or `LESSONS.md`.

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/lessons.mjs" add --root <project-root> \
  --feature <slug> \
  --signal <ac_gap|surviving_mutant|spec_precision_gap|spec_deviation|gate_fail|user_correction> \
  --source "<file:line | AC id | mutant id | the correcting turn>" \
  --text "<one terse, actionable, canonical sentence>" \
  --scope "<optional path/layer/tag for retrieval>"

node "$CLAUDE_PLUGIN_ROOT/scripts/lessons.mjs" list --root <project-root>     # confirmed only
node "$CLAUDE_PLUGIN_ROOT/scripts/lessons.mjs" penalize --root <project-root> --id L-007
```

**Record** at a verification boundary (a gate failed, a review found a spec deviation, an acceptance
criterion had no test) or the moment the user corrects an approach — `--signal user_correction`.
**Load** confirmed lessons before planning and apply them as design constraints for the matching
scope. Candidates are tracked but not trusted: never load them as instructions. If applying a
confirmed lesson causes a failure, `penalize` it so it heads for quarantine instead of misleading
the next run.

- **Grounding or nothing.** No `--source`, no lesson; the script refuses it. Do not work around it.
- **One lesson = one terse sentence**, stating the fix, not the incident: *"Assert world x/z per
  placement, not just prop count"*, never *"the environment test failed again"*.
- Dedup is exact-after-normalization, so two wordings of one lesson only merge — and so only
  promote — if they normalize alike. Phrase canonically.

The `observe` hook appends `{ts, tool, target}` lines to `observations.jsonl` (on by default;
`RC_INSTINCTS=0` opts out) and `memory-load` surfaces the store at SessionStart, nudging a distill
pass once observations accumulate. Reading those lines is how you spot a sequence repeated 3+ times
that nobody flagged out loud; truncate the file after a pass so the next one starts clean.

## C — Golden paths

A route earned the hard way — how to reach a tenant's database, run the migration dance, verify a
change live — dies when compressed into one sentence: the commands, the required order and the
dead-ends are exactly what the next session needs. Harvest it into a **project-local skill** in the
same turn you earn it.

**Promotion gate — all three, or it is not a skill yet:**

1. **A passing check** — a test passed, the command exited clean, the build went green. Name which;
   "seemed to work" is not a check.
2. **A named failure pattern** — the failure the route avoids, named ("stale build cache → phantom
   type errors"), not "sometimes it breaks".
3. **A ruled-out dead-end** — one concrete approach tried and eliminated, with the reason.

Short of all three it is still a hypothesis: record it in **A** with `scope: context` and an
`unverified:` line, and harvest it once a check confirms it.

Write it to the host's project skills directory (Claude Code: `.claude/skills/<name>/`) so it ships
to the team via git and never fires in a repo where its commands do not apply. `rc-writing-for-agents`
owns the authoring — read it first. The skill carries the commands, paths, required order, gotchas,
and a **What didn't work** section holding the dead-end. Scan that directory before writing: a
near-identical route is an update, not a second skill competing to trigger. For a credential, record
where it lives — the env var name, the MCP tool, the vault entry — never the value; a harvested
skill is committed.

## Scratch

Notes that are only true while one task runs — files touched, a debugging trail, the current
objective — go in `.rc/tasks/<slug>/notes.md` and are deleted with the task. They are not memory.
When a scratch note passes the three **Record** questions in **A**, promote it to a fact; when it is
what a failure taught, record it as a lesson in **B**. Do not copy code blocks, stack traces or the
spec into scratch, and do not keep a chronological play-by-play.

## Critical rules

- When a fact or lesson is contradicted by the repo or the user, correct or delete it — trust the
  repo over stale memory.
- Never invent history, decisions or status that did not happen.

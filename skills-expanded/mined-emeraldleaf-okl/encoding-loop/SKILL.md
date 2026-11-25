---
name: encoding-loop
description: Use when you discover a rule, antipattern, or lesson worth keeping ("we should never write this again" / "we should always do this when") and need to encode it at the right surface and record it to the org knowledge layer. Fires on review findings, debugging discoveries, audits, and prior-art hits.
---

# Encoding loop — turn a finding into a durable, promoted rule

A trigger surfaced a candidate rule. The response is always the same two moves.

## 1. Pick the smallest sufficient surface (softest→strongest)

| # | Surface | Use when |
|---|---|---|
| 1 | `docs/` + diagram | the *why* needs more than a line, or reviewers need a picture |
| 2 | `CLAUDE.md` | every session needs it, always-on (keep it lean — prefer a rule file) |
| 2 | `.claude/rules/<area>.md` with `paths:` glob | scoped to a file category (loads only in context) |
| 3 | `.claude/skills/` or `.claude/commands/` | a multi-step procedure with real logic |
| 4 | `.coderabbit.yaml` path_instructions / `architecture-reviewer` checklist | catch at PR-review time |
| 5 | a test or a CI check (`gates/` if you ran `okl scaffold`) | mechanical, build-breaking — for rules that keep being broken |

Default to the *softest* surface that could hold the rule. **Promote down (toward 5) only as it
earns it** — a rule that keeps being violated moves to a sterner tier, not a sterner paragraph.
Most rules never leave tier 1, and that is fine.

## 2. Record it in the store, with a scope that decides which repos may see it

```
okl record --type <Defect|Gate|Rule|Claim|Retraction|Tombstone|Decision|PriorArt> \
  --id "<stable-key>" --title "..." --body "..." --scope <org|repo> \
  --trigger "<the request or error that surfaced it>" --trigger "<another moment it applies>"
okl verify <stable-key> --run "<a check that fails if the lesson is broken>" --expect "<its success signal>"
```

- **Verification is a check you run, never a flag.** `okl record --verified` is refused: a
  stamp the recorder awards itself is the step grading its own homework. `okl verify` runs the
  check and stores the command and its result as the evidence.

- **`--id`** — a short stable key you choose for a NEW lesson. Omit it and every record is
  minted a fresh random id, which is how a store accumulates near-duplicates that `okl dedup`
  reports but cannot remove, there being no delete subcommand. To refine a lesson that already
  exists (the briefing shows each lesson's `[id]`), run `okl update <id> --<field> "..."`: it
  changes only the fields given and keeps the lesson's proof, unless `--files` changes.
  Recording an existing id again is refused; `--replace` overwrites it, proof included. A
  lesson that is wrong, replaced or obsolete is retired, never deleted:
  `okl retire <id> --reason "..." [--by <new-id> | --obsolete]`. A wrong one stays briefed
  as AVOID; a replaced one leaves briefings, which point to its replacement. Where a repo
  keeps its lessons in a seed file, use the id that file derives,
  `seed:<seed-file-stem>:<key>`, so a later `okl seed` updates the same row.
- **`--files`** — the code the lesson governs. With it, and once `okl verify` has passed,
  a change to that code marks the lesson STALE in the briefing and `okl drift` until the
  check passes again, and fails the drift gate (the pre-push hook, or CI) where one is
  installed. This is what sits between tier 1 and a gate: watched, but not
  build-breaking on its own.
- **`scope=org`** — a fact about the world: prior art, an API contract, a data-source gotcha, a
  portable gate. Every repo that reads this store may see it; whether a briefing shows it
  is then up to its `applies_to`, the repo's interests and the task. Each repo has its own
  store by default, so another repo gets it through a pack it loads.
- **`scope=repo`** — a quirk true only of this codebase. Stays local.

If the finding retracts a prior claim, also add it to `registries/RETRACTIONS.md`; if it retires an
identifier, add it to `registries/tombstones.txt`. The CI gates then fail any doc that restates
the quoted retracted claim verbatim, or reintroduces the tombstoned identifier.

## 3. Verify the gate (if you made one)

A gate you have only seen pass is a gate you have not tested. Run it against the real drifted file
from git history and confirm it FAILS, then confirm it passes on the fix. Only then is it a gate.

## Gotchas
- A merged fix without the encoded rule is a half-finished job — the next instance slips through.
- A surface nobody runs is documentation, not enforcement. If it is not read/executed, it will drift.
- The drift you notice is the drift that embarrasses you; the flattering kind (stale "open" items)
  needs a mechanical `verified_at`/TTL check, not vigilance.

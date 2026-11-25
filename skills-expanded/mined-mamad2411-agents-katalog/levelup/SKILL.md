---
name: levelup
description: Use when the user wants to raise a governed project's gold level honestly — runs /gold-audit, composes a remediation wave that closes each gap for a REAL reason via /close-gold-gap, then re-audits with the no-regress ratchet + anti-fake-green guards. The level rises only by a real verdict flip; un-closeable gaps become needs-human, never faked.
argument-hint: '[--target L0|L1|L2|L3] [--max-waves N]'
title: 'Level Up (raise the gold level honestly)'
doc_version: '1.0.0'
status: active
last_review: '2026-06-16'
owner: ''
canonical_id: ''
tags: ['audience/agent', 'audience/dev', 'kind/internal', 'kind/orchestration']
related: ['gold-audit', 'close-gold-gap', 'wave-drain', 'tdd', 'verification']
---

# Level Up (raise the gold level honestly)

**Goal:** raise this project's gold-audit **level band** toward `--target` (default the
top band, `L3` — the "gold" standard) by closing real gaps. Every point gained is backed by
real config / test / doc work; the level **only** rises by a real verdict flip.

**Mental model:** you are the **orchestrator**. `/levelup` does not invent a score and does
not implement gaps by hand inline — it **measures** with `/gold-audit`, **composes a
remediation wave** (the `/drain` fan-out shape), **closes each gap honestly** with
`/close-gold-gap`, then **re-audits behind the ratchet + anti-fake-green guards**. It reuses
existing engines and skills — there is **no new TS engine** and **no new `arbiter` CLI verb**.

> `/gold-audit` measures (read-only). `/close-gold-gap` gives one gap its real recipe.
> `/levelup` is the loop that ties them together and drives the band up, wave by wave.

## Primitives

| Primitive                                 | Role here                                                            |
| ----------------------------------------- | -------------------------------------------------------------------- |
| Skill `gold-audit`                        | Measure the band + the prioritized `gaps[]` (read-only, no AI score) |
| `arbiter audit readiness --json`               | The deterministic engine payload `/gold-audit` reads                 |
| `arbiter audit readiness --check`              | No-regress ratchet gate — locks each gain, fails on any regress      |
| Skill `close-gold-gap`                    | The typed, honest recipe (doc-set / test / config / process) per gap |
| Skill `wave-drain`                        | The fan-out shape for the remediation wave (groups, parallel agents) |
| Skill `tdd`                               | Red → green → refactor for every `test`-category gap                 |
| Skill `verification`                      | Claim-based verification before the re-audit gate                    |
| `scripts/check-all.mjs`                   | The anti-fake-green aggregate — fail-closed disarm-proof verdict     |

---

## Phase 0 — Measure the starting band

```bash
npx @getarbiter/cli audit readiness --json
```

Load the **`gold-audit`** skill and read the payload verbatim — `level.level`,
`level.nextLevel`, `score`, and `gaps[]` (the N/P checks grouped by `dimension`). Record this
as the **before** snapshot. If the engine emits a SKIP line (no registry installed), do NOT
invent a score: point the user at `npx @getarbiter/cli init` / `npx @getarbiter/cli update` and stop.

Parse `--target` (a level band `L0`–`L3`, default the top band `L3`). If the current band is
already `>= --target`, report "already at target" and stop.

## Phase 1 — Compose a remediation wave

From `gaps[]`, build a **wave** of the gaps that move the band fastest, prioritized by:

1. **brownfield class + risk** — high-risk N (missing entirely) checks first;
2. **ratchet value** — the checks whose `weight` contributes most to the next band;
3. **closeability** — `config` / `test` / `doc-set` gaps (code-closeable) ahead of `process`
   gaps (`manual`, `NV` — human-only, no code recipe).

Partition the wave into **groups** of module-coherent gaps (the `/drain` rule: two agents
never edit the same file concurrently). Independent groups are parallelizable.

## Phase 2 — Close each gap honestly

For each gap, derive its recipe and carry it out. Load the **`close-gold-gap`** skill and execute the
recipe by **category** — the category table below **is** the recipe (no separate engine call):

| Category    | Real work                                                      | Honest outcome                         |
| ----------- | -------------------------------------------------------------- | -------------------------------------- |
| **doc-set** | scaffold the doc, **then fill real content**                   | `P` → `Y` only after real content      |
| **test**    | write the missing test(s) **TDD-first** (load the `tdd` skill) | `Y` when the real metric meets the bar |
| **config**  | wire the real tool/config the check verifies                   | `Y` when the tool genuinely runs       |
| **process** | human-only action for a `manual` check — **no code recipe**    | `NV` → routes to needs-human           |

A gap that cannot be closed honestly — a `manual`/`process` check, a gap blocked on a human
decision, or one needing an external account/service — becomes **`needs-human`** with a stated
blocker reason. It is **NEVER** faked, suppressed, or marker-stuffed. It does not block the
wave: the rest proceeds.

## Phase 3 — Re-audit behind the ratchet + anti-fake-green guards (fail-closed)

After the wave's gaps are closed, gate the gain. The level rises **only** by a real verdict
flip — never by a moved threshold, a pasted literal, or a disabled check:

```bash
# 1. No-regress ratchet — locks the gain; exit 1 if score/Y regressed below baseline.
npx @getarbiter/cli audit readiness --check

# 2. Anti-fake-green aggregate — disarm-proof; a broken guard (exit 2) fails unconditionally.
node scripts/check-all.mjs

# 3. Re-measure the band and compare to the before snapshot.
npx @getarbiter/cli audit readiness --json
```

**Fail-closed semantics (structural anti-fake-green):**

- `gold-audit --check` exit **1** (regress) → a gap was un-closed or a real metric dropped:
  **REJECT** the wave, revert the cheated change, re-do the real work.
- `check-all.mjs` exit **1** (hard fail) or exit **2** (a broken/disarmed guard)
  → **HALT** the wave. A guard you cannot trust is a stop, not a pass — you cannot disarm a
  guard by breaking it.
- The re-audit must show the band rose **for a real reason** (genuine metric improved, real
  content/config now exists). A green that appears only because a literal was pasted or a
  threshold moved is **fake-green**: revert and do the real work.

Only when all three pass and the band genuinely rose do you **commit the new
`.gold-audit-baseline.json`**, which ratchets the gain monotonically — the next wave can only
go up from here.

## Phase 4 — Repeat to target, then report

Repeat Phase 1 → Phase 3 until the band reaches `--target` or no further gap can be closed
honestly (every remaining gap is `needs-human`). Cap the loop at `--max-waves` (default 5) to
stay bounded; if the target is not reached within the cap, report the remaining gaps and stop.

Emit the **final report**:

- **before → after** — starting band + score vs final band + score.
- **gaps closed** — each `gapId`, its category, and the **evidence** (the real file/test/config
  that flipped it `Y`).
- **gaps needs-human** — each `gapId` with its **blocker reason** (manual check, external
  dependency, human decision).
- **ratchet verification** — the committed `.gold-audit-baseline.json` and the `--check`
  exit-0 that locks the gain monotonically.

## Hard rules (anti-fake-green)

- **The level rises only by a real verdict flip.** Same repo + same registry ⇒ identical
  engine verdicts; a band that "rose" without real work did not rise.
- **Fail-closed.** A broken guard (exit 2) or a hard-fail (exit 1) **halts the wave** — never
  `--no-verify`, never skip, never disable a guard to pass it.
- **No fake green, ever.** No suppression (`--no-verify`, `eslint-disable`, `skip`, `ignore`),
  no marker-stuffing (pasting the matched `pattern`/`equals` literal as the sole action), no
  doc stub claimed as `Y`. A gap that can't be closed honestly → **`needs-human`**.
- **No new engine, no new CLI verb.** `/levelup` is a skill + slash command; it composes
  `arbiter audit readiness` and the `close-gold-gap` skill — it never re-implements scoring or the
  no-regress check.

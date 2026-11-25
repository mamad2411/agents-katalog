---
name: tdd
description: >
  Red-green TDD at pre-agreed seams with session-scoped runs via OKF test maps
  and AGENTS index lines. Also covers testing Agent Skills (triggering,
  functional, baseline comparison) and iterating description/body from
  under/over-trigger signals. Use when implementing with tests first, agreeing
  seams, checking test quality, or validating a skill's triggers and behavior.
disable-model-invocation: true
---

# tdd

Red → green loop that keeps tests worth keeping. If `CONTEXT.md` is present, read it so names match domain language; respect ADRs in the area you touch when those exist.

## Seams first

A **seam** is the public boundary you test at. **No test at an unconfirmed seam.**

Before any test, list the seams and confirm with the user.

**Done when:** seam list is agreed (or user confirms no code seam applies).

## Session scope (OKF + AGENTS)

Goal: run and load only tests relevant to **this** session — not the whole `/tests` tree (which may hold hundreds of tracked regression tests).

**When** `AGENTS.md` and `knowledge/` exist (bmurrtech conventions or equivalent):

1. Read the **Test index** under `AGENTS.md` → Testing (one-liners → OKF).
2. Open only the OKF **test-map** concepts that match the agreed seams.
3. During the loop, run the commands/paths those maps name — not the full suite.
4. After each new or materially changed test: update the OKF test-map, link it from `knowledge/index.md`, and ensure a **one-line** AGENTS Test-index entry points at that concept (path + how to run). Prefer **`context`** for OKF writes when that skill is available; AGENTS one-liners are ops index lines (ok for `tdd` / `upkeep` to maintain — never paste glossary definitions into AGENTS).
5. Full suite **once** at the end of the change set (or under `implement`).

**When** those artifacts are missing: skip indexing with a one-line note; still prefer the smallest relevant check the target repo supports.

**Done when:** session runs only mapped tests (or skip noted); new tests indexed if conventions apply.

### Test-map shape (OKF)

Under `knowledge/<slug>.md` (frontmatter `type: test-map` recommended):

- Seam / capability name (matches the AGENTS one-liner title)
- Exact run command for the small subset
- Test file paths under `tests/` (or the repo’s real test root)
- Related glossary terms / ADRs if useful

AGENTS one-liner form:

```markdown
- [<capability>](knowledge/<slug>.md) — `<smallest run command>`
```

## What a good test is

- Verifies **behavior** through public interfaces, not internals
- Reads like a specification (“user can checkout with valid cart”)
- Survives refactors of private structure
- Expected values from an independent source of truth (literals, worked examples, spec) — never recomputed the same way as the code
- Lives under the repo’s tracked test tree (commonly `tests/`) — regressions stay in VCS; exploratory dumps go to `.scratch/` if that pad exists

## Anti-patterns

- **Implementation-coupled** — mocks internals, private methods, or side-channel DB peeks
- **Tautological** — assertion rebuilds the implementation’s formula
- **Horizontal slicing** — all tests then all code; prefer **vertical slices** (one test → one minimal implementation → repeat)
- **Suite stuffing context** — loading or narrating the entire `/tests` tree mid-session instead of using the Test index → OKF maps

## Loop rules

1. **Red before green** — failing test first; only enough code to pass
2. **One slice at a time** — one seam, one test, one minimal fix
3. **Refactor out of band** — belongs to review (`code-review`), not the red→green cycle

## Skills under test (callout)

When the seam is an **Agent Skill** (`skills/<name>/`), treat trigger routing and
workflow outcomes as the public interface — not private prose.

> **Callout — skill TDD:** Iterate on **one hard user task** until it succeeds,
> then extract the winning approach into the skill. Expand to a suite only after
> that foundation works. Choose rigor by blast radius: manual chat probes →
> scripted prompt suites → programmatic evals. Always cover **(1) triggering**,
> **(2) functional outputs**, **(3) baseline comparison** when you claim the
> skill improves results. Structural validate (`scripts/quick_validate.py` when
> present) is red/green for layout/frontmatter — not a substitute for behavior.

### Minimum skill loop

1. Agree scenarios: should-trigger / should-not-trigger phrases + 1–2 functional cases.
2. Structural red/green: `python3 scripts/quick_validate.py skills/<name>` (soft-skip if absent).
3. Triggering: run phrases; fix **description** on under/over-trigger before rewriting the body.
4. Functional: one vertical slice (failing scenario → minimal skill edit → re-run).
5. Compare to baseline (turns, tool failures, tokens/time, user corrections) when success criteria exist.
6. Index durable suites via OKF/AGENTS when this repo’s conventions apply; keep exploratory prompts under `.scratch/`.

Depth, example suites, iteration signals (under/over-trigger, execution
issues): [references/skill-testing.md](references/skill-testing.md).

Skill authoring patterns and packaging troubleshooting:
**`writing-for-agents`** `references/patterns.md` /
`references/troubleshooting.md`.

**Done when:** agreed skill scenarios pass at the chosen rigor; description
routes correctly; structural validate green (or soft-skipped).

## After implement

When used under **`implement`**, keep running the smallest relevant (indexed) checks from the **target** repo; full suite once at the end of the change set.

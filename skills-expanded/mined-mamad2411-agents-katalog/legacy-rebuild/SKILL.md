---
name: legacy-rebuild
description: >-
  [Tier 3 · high blast radius · expect rework · run deliberately, review the floor +
  architecture] Adversarially review a legacy app, research the best current architecture,
  and rebuild it end to end on a modern foundation while PRESERVING everything it currently
  does. Use when an app uses outdated everything (old deps, poor architecture, e.g.
  JS-inlined-in-HTML, no build/module system) and needs a real modernization, not a patch.
  Incremental and shippable per PR — NOT a big-bang rewrite — rebuilt against a captured
  behaviour floor so nothing is silently lost. Runs via the autonomous-fleet-core engine.
  Trigger on: "rebuild this legacy app", "modernize the whole codebase", "this uses all old
  versions, rebuild it properly", "re-architect end to end".
license: MIT
compatibility: Requires git and gh CLI in the target repository
metadata:
  author: "ravidsrk"
  version: "1.0.0"
  tier: "3"
  fleet-component: "mission"
status: exploratory
---

> **Status: exploratory.** This mission is documented but has not yet been run end-to-end on an external repo with an archived run-archive. It is preserved for future promotion (see `docs/exploratory/missions/README.md` § Promotion criteria). Do not invoke this skill in a production fleet until it has been promoted.


<!-- Corpus: prompts.md L2963 (Stage 8 Tier 3 grouping — high blast radius). Builder choice per Stage-9 final form (prompts.md L3013): @codex. -->


# Mission: legacy-rebuild

## Required skills

Before executing, activate these skills and read their full instructions:

1. `autonomous-fleet-core` — read `references/engine.md` and `references/composition.md` when coordinating
2. One runtime adapter: `autonomous-fleet-adapter-orca`, `autonomous-fleet-adapter-claude-code`, `autonomous-fleet-adapter-grok`, or `autonomous-fleet-adapter-codex`

Follow the core and your adapter in full, then apply the mission parameters below.

Do not load a second mission skill in the same run. For chained missions, use `fleet-program`.

## Optional skills

| Skill | Activate when | If unavailable |
|-------|---------------|----------------|
| — | — | Run `test-coverage` as prior program step if floor is undertested |

## Worker skills

| Role | Skills | If unavailable |
|------|--------|----------------|
| @codex (rebuild units) | `frontend-design` if UI; else stack skill from manifests | Legacy floor + target architecture docs |

## Deferred missions

Record in final readiness doc under **Recommended next missions** and in DECISIONS.md.

| Finding type | Route to |
|--------------|----------|
| Light tidy sufficient (no rebuild) | `cleanup` |
| Product incomplete after modern stack | `take-product-to-completion` |
| Post-rebuild doc drift | `doc-sync` |

**Empirical note:** highest-risk alongside take-product-to-completion. A from-scratch rebuild that
must also preserve undocumented behaviour is where rewrites die — you discover behaviour only
after deleting it. The two control artifacts are the LEGACY FLOOR (everything the app does today)
and the TARGET ARCHITECTURE — review both. The floor is the contract that "rebuild" doesn't mean
"lose things."

## CORE PRINCIPLE
Do the adversarial review and capture the behaviour floor FIRST, pick a modern target
architecture, then rebuild against the floor — incrementally shippable, not big-bang. The review
and floor are what stop the rebuild from dropping features.

## GOAL
A clean, modern, well-architected app on current tooling, with ZERO feature regressions vs. what
exists today. Eliminate every anti-pattern the review flags (e.g. inlined JS, missing
build/module system, dead code); adopt a current best-practice stack; preserve all existing
behaviour, data, and external contracts. Each rebuilt unit lands working and tested.

## ROLE PIPELINE

**Builder choice (Stage-9 final form).** Per prompts.md L3013 (Aula run, Stage-9 prompt 24), @grok is retired for general-purpose builds. Flipping to @codex.

- @claude AUDITS + captures the FLOOR + RESEARCHES + freezes the architecture + per-unit specs.
- @codex CODES each unit on the modern architecture.
- A fresh build-blind @claude REVIEWS each PR: conforms to target architecture, preserves the
  unit's floor behaviour, real green tests, no legacy anti-pattern reintroduced.
- @claude SHIPS: opens PR, conflict-aware merge, worktree cleanup.

## LEDGER
`<LEDGER_DIR>/rebuild-progress.md`. Per-task flags: `PLANNED=<t/f> BUILT=<t/f> REVIEWED=<t/f>
SHIPPED=<t/f>`. Plus a UNIT INDEX (each rebuild unit + the floor slice it preserves, `OPEN | DONE
via PR#n`).

## TASK STRUCTURE
- **T-AUDIT [@claude]** — hostile audit: every anti-pattern, outdated dep/version, architectural
  smell (inlined JS, missing build/module system, dead code, duplication, no separation of
  concerns). Explain WHY the code is shaped this way and exactly what's wrong. Output
  docs/audit.md. (Parallel with FLOOR + RESEARCH.)
- **T-FLOOR [@claude, parallel] — control artifact.** Capture EVERYTHING the app does today —
  every screen, route, feature, flow, state, behaviour (including undocumented behaviour found by
  exercising the app) — as the preservation floor. Output docs/legacy-floor.md.
- **T-RESEARCH [@claude, parallel]** — research current best-practice architecture + tooling for
  this kind of app (framework, build/bundler, module approach, language/runtime versions, test
  stack, the modern patterns that replace the flagged anti-patterns). Fetch live sources;
  recommend a concrete stack with rationale. Output docs/research.md.
- **T-ARCH [@claude, Opus-class, gated on AUDIT+FLOOR+RESEARCH] — control point.** Define the
  target architecture (chosen stack, structure, how each anti-pattern resolves). Decompose the
  rebuild into shippable units, each conforming to the architecture and preserving its floor
  slice. Per-unit specs + acceptance (architecture conformance + feature parity + tests), a
  dependency graph, and a PARALLELIZATION + FILE-OWNERSHIP map (independent → parallel; same-file
  → serialized), with shared FOUNDATION (build setup, structure, base tooling) called out first.
  Output docs/architecture.md + docs/rebuild-plan.md. FROZEN. Write each unit to the UNIT INDEX.
- **T-FOUNDATION [relay]** — establish the new architecture's foundation (modern build/bundler,
  project structure, dependency upgrades to current versions, base tooling + test harness). Gates
  dependent units.
- **T-UNITS… [per unit, loop]** — @codex rebuilds the unit on the modern architecture preserving
  its floor behaviour (tests) → fresh build-blind @claude reviews (architecture conformance + feature parity + real
  green tests) → @claude ships. Independent units parallel; file-overlapping/dependent serialized.
- **T-FINAL [@claude]** — build green (on the NEW build system), lint clean, full suite green. The
  app is fully on the target architecture (no flagged anti-patterns remain); EVERY behaviour in
  docs/legacy-floor.md still works (zero regressions); no dead code/placeholders/console errors;
  all worktrees cleaned. Output `<LEDGER_DIR>/rebuild-readiness.md` with **`fleet-outcome` YAML**
  (`units_open`, `floor_preserved`), architecture-conformance summary,
  legacy-floor parity matrix complete, stack adopted, residual risks, all PRs). Ship as the final
  PR.

## Runtime goal

After ledger init, **SET_GOAL** per `autonomous-fleet-core/references/runtime-goals.md`. Record
`## Runtime goal` in `<LEDGER_DIR>/rebuild-progress.md`. **GOAL_COMPLETE** only after ## DONE below.

```
Mission legacy-rebuild DONE: <LEDGER_DIR>/rebuild-progress.md all task flags true,
<LEDGER_DIR>/rebuild-readiness.md with fleet-outcome.status done and mission metrics satisfied,
./scripts/validate-fleet-outcome.sh passes, all PRs merged into BASE.
```


## DONE
Every UNIT-INDEX item `DONE`, app fully on the target architecture, every legacy-floor behaviour
preserved, every task terminal, suite green, <LEDGER_DIR>/rebuild-readiness.md exists. Then send the FINAL
report.

## DECISION DEFAULTS (mission-specific)
- Modern architecture is the TARGET; the legacy floor (docs/legacy-floor.md) is what must NOT
  regress. Eliminate every anti-pattern the audit flagged.
- Incremental + shippable per PR; never a big-bang replace. Each unit lands working and tested.
- Preserve all existing behaviour, data, and external contracts; modernize the implementation, not
  the product's behaviour, unless the plan explicitly improves a flow.
- Maximize parallelism: independent units concurrent in isolated worktrees; serialize
  file-overlapping units to minimize merge conflicts. Foundation first.
- Tests real and behaviour-exercising; reject coverage-padding. Bar = every feature/flow tested
  and green, coverage not regressed.
- Any ambiguity → the cleanest modern architecture with full feature parity while converging.

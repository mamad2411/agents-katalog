---
name: eng-harness-flow
description: |
  Stateless harness-loop router — the single front door to the eng-harness skill family, and the harness-loop analogue of `the-flow` (which guides the SDD pipeline). On every call it re-derives where the work sits on the loop from deterministic repo signals plus an optional caller hint, then routes to the SINGLE correct harness skill — never call the children directly. It enforces an adoption gate (install → scout → governance → inject → boot LAST) before the engineering zone (boot → backpressure → observe → retro → improve), honours `at=` / `--event` / `--plan-dir` / `--spec` / `--phase` / `--prompt-optional` / `--json`, and resolves hint-vs-signal conflicts via a route/redirect/noop/ambiguous matrix. Stateless — safe to call anytime, from any caller. Never gates, scores, or blocks; never invents a health verdict (that is `harness doctor`'s job).
---
# eng-harness-flow

The **single front door** to the harness loop — the harness-loop analogue of `the-flow` (which guides the SDD pipeline). `the-flow` walks a *linear* journey (spec → plan → tasks → code → review → merge); this router routes a *cycle* re-entered wherever the work is: **adopt → boot → backpressure → observe → retro → improve**, drawn in [`references/getting-started.md`](./references/getting-started.md). On every call it re-derives *where on the loop you are* from deterministic repo signals + an optional caller hint, and hands back the **one right harness action** — never call the children directly.

**Progressive disclosure is the contract: load exactly one verb module for the current step — never read all of them up front.**

## The state contract — stateless routing, CLI-driven flow position (read this first)

`eng-harness-flow` is a **stateless dispatcher** for *routing*: `(repo signals, conversation, optional hint) → next harness action`. Its detection — *which* flow is live, *which* rung is missing, *where* the work sits — is **re-derived every call** from deterministic repo signals, never remembered (re-entry after `/compact` needs nothing reloaded). It **never gates, scores, or blocks** (every route is a suggestion; a hint is never a command; declining the harness is conversational, not a `.disabled` file); **never runs `minih`** (companions belong to the implement verb) **or `/compact`** (it can only recommend it); and **never invents a verdict** (`harness doctor` answers whether the harness is healthy, not the router's opinion).

**What it *does* persist — and the only thing it does (plan 032):** the **position of the flow it is driving**, as a **first-class, CLI-driven flight plan**, through the **real `harness flow` verb family** (never hand-edited JSON). This is the deliberate, *scoped* supersession of the old "writes nothing" stance — the dogfood + the exemplar. The scope is **flow position only**:

- ✅ The router drives **two mutually-exclusive flows** as flight plans (🧰 adopt + ⚙️ loop — § below); position lives in `nav`, driven by `harness flow nav`.
- ✅ When the ⚙️ loop runs **alongside an active the-flow**, it injects its four fire-hook steps as **chores** into `the-flow.json` so that flow's rail tracks them (and they stop getting missed); standalone, it authors its own `.harness/loop.flow.json`.
- ❌ Routing/detection/verdicts stay signal-derived; verb modules stay **harness-blind**; the five lifecycle hooks + the `--json`/`--hooks` envelope contract are **frozen**.

> **The unifying rule (unchanged for routing):** routing state that *could* drift lives in deterministic substrate a child verb owns (reports, buffers, `.retro.md`, the governance doc) — **never remembered by the router**. *Flow position* is different: it is persisted **in the flight plan, by the CLI** (the single writer), exactly as the-flow does — observable substrate, not router memory.

The mechanics of driving a flow — nav model, spine-vs-excursion, the verb flags + gotchas, the build-order rule, and the AC-07 chore shape — live in [`references/flight-plan-ops.md`](./references/flight-plan-ops.md) (**load it once, before the first flight-plan mutation of a session; run the capability precheck there first**). The full routing engine — detection signals A–J, the two-zone adoption gate (the Graph), the two-flow selection predicate, the engineering dispatch, the precondition/conflict matrix, and the byte-stable public contract — lives in [`references/00-routing.md`](./references/00-routing.md). The human-mode voice (rail, narration, why-table, tone) lives in [`references/coach.md`](./references/coach.md).

## The two first-class flows (🧰 adopt · ⚙️ loop)

Unlike `the-flow` (one linear journey), `eng-harness-flow` drives **two distinct, mutually-exclusive flows** — the adoption gate decides which is live, and they **never co-run**:

| Flow | Shape | Spine (CLI node ids) | Terminal | Lives in |
|---|---|---|---|---|
| 🧰 **adopt** (`harness-adopt`) | finite, once per repo | `install → governance → build-boot → bridge` (`scout`/`inject` = `branch_of` excursions) | `bridge` (a `decision`; the adopt→loop gate) | its own adopt flight plan during onboarding |
| ⚙️ **loop** (`harness-loop`) | cycling, every session | `boot → backpressure → observe → drain-gate → retro-drain → retro-harvest → improve` | `improve` (`next:[]`; the cycle is a **nav reset**, DAG stays acyclic) | **chores in `the-flow.json`** when a the-flow is active; else its own `.harness/loop.flow.json` |

- **Selection predicate**: the adoption gate **S0 (install) + S2 (governance) + S4 (boot)** all hold → the **loop** is live; otherwise **adopt** is live. Exactly one (`00-routing.md` § The two first-class flows).
- **Coexistence**: when the loop runs alongside an active the-flow, the four **fire** hooks (`pre-flight`/`pre-coding`/`post-coding`/`post-flight`) are injected as **chores** (`run /eng-harness-flow --hook <hook>`) onto `the-flow.json` — idempotent, dedup-keyed on the `--hook` token, lifecycle `todo → done|skipped`. `coding`/observe and `improve` get no chore. The exact shape + the R-1 seam-node reconciliation are in [`references/flight-plan-ops.md`](./references/flight-plan-ops.md).

## Registry

**This table is the master** verb↔module binding; the Graph (ordering + detection) is the master in [`references/00-routing.md`](./references/00-routing.md). Each lifecycle hook / adoption rung resolves to exactly one verb, and each verb to exactly one module — except `coding`/observe, which has **no module**: it is the silent `harness observe` CLI verb.

| Trigger (lifecycle hook / adoption rung) | Verb | Module / target | Produces |
|---|---|---|---|
| `pre-flight` | boot | `references/stages/boot.md` | boot verdict (HEALTHY / SLOW / UNHEALTHY / UNAVAILABLE) |
| `pre-coding` | backpressure | `references/stages/backpressure.md` | `backpressure-coverage.md` |
| `coding` | observe | — **CLI verb**: `harness observe "<what>" --kind <kind>` (silent; no module) | one observe-buffer entry |
| `post-coding` | retro (drain) | `references/stages/retro.md` | drained `.retro.md` |
| `post-flight` | retro (harvest) + improve | `references/stages/retro.md` | harvested view + encoded improvement |
| adoption gate · on-ramp / inject | adopt | `references/stages/adopt.md` | installed + injected harness (delegates: assess, add-extension) |
| adoption gate · build boot | add-extension | `references/stages/add-extension.md` | a loadable extension / basic boot |
| adoption gate · scout | assess | `eng-harness-0-harnessability-assessment` *(public peer skill — not a module)* | harnessability report |

Module missing at its path → say so and stop. Never improvise a verb from memory.

## Command grammar

Works with **no arguments** (full auto-detect); a parent driving its own flow can pin position. The flags' full semantics — plus the byte-stable public contract (`--hook` / `--event` / `--hooks` / `--json`) — are defined once in [`references/00-routing.md`](./references/00-routing.md); this is the surface summary:

- `--hook <name>` — the PRIMARY invocation; names one of the five neutral lifecycle hooks (`pre-flight | pre-coding | coding | post-coding | post-flight`).
- `--event <seam>` — a permanent, zero-break **alias** for `--hook` (the six host seams `session-start | post-spec | pre-implement | task-pause | phase-end | plan-complete` map onto the five hooks).
- `at=<stage>` — friendly stage hint (`auto` / `adopt` / `boot` / `backpressure` / `observe` / `retro-drain` / `retro-harvest` / `improve`).
- `--plan-dir` / `--spec` / `--phase` — pin the plan / spec / phase so detection is never ambiguous.
- `--prompt-optional <bool>` — parent owns skip-suppression for optional offers (default true).
- `--json` — the machine-readable routing envelope (+ the resolved `hook`).
- `--hooks [--json]` — the discovery manifest `{ manifest_version, hooks[5] }`.
- `--help` — the synopsis below (print-and-stop).

**A hint is never a command.** The router validates each hint's precondition (the adoption gate + the conflict matrix in `00-routing.md`) and **redirects** when a hint contradicts the signals — it never blindly runs the named stage. `--repo` is reserved for v2 (the router operates on `cwd`).

## Progressive disclosure

Load **exactly one** verb module (`references/stages/<verb>.md`) when a step is taken — never read all of them up front. A module may lazily pull `references/00-routing.md` § Shared conventions when it cites one (the sanctioned exception); reading modules for verbs you are not executing is not. The verb modules are **harness-blind**: they carry no sibling names, no flow position, no lifecycle-hook self-reference, and no routing — that knowledge lives only here and in `00-routing.md`. Human-mode coaching (the rail, the narration beats, the why-table) lives only in [`references/coach.md`](./references/coach.md), never duplicated into the dispatch or the modules.

## `--help` — synopsis (print-and-stop)

`--help` prints this static synopsis and **stops** — no signal detection, no state, no routing, nothing fires:

```text
eng-harness-flow — stateless router to the harness loop (one front door).

USAGE
  /eng-harness-flow [--hook <name> | --event <seam>] [--plan-dir <p>] [--spec <p>]
                    [--phase <id>] [--prompt-optional <bool>] [--json] [--hooks] [--help]

LIFECYCLE HOOKS  (--hook, the primary invocation)
  pre-flight    before work starts       -> boot validation
  pre-coding    spec settled, pre-build   -> backpressure survey
  coding        mid-build (silent)        -> one in-flight capture
  post-coding   a phase just ended        -> per-phase retro drain
  post-flight   the whole plan is done    -> terminal harvest + improve

DISCOVERY
  --hooks [--json]   the five-hook manifest: { manifest_version, hooks[5] }
  --json             machine-readable routing envelope (+ the resolved hook)

--event <seam> is a permanent alias for --hook — session-start, pre-implement,
post-spec, task-pause, phase-end, plan-complete (see "Lifecycle hooks").
```

## References

- [`references/00-routing.md`](./references/00-routing.md) — the routing engine: signals A–J, the adoption gate (the Graph), the engineering dispatch, the precondition/conflict matrix, verb/slug resolution, the `--json` envelope + `--hooks` manifest (the byte-stable contract), and § Shared conventions.
- [`references/coach.md`](./references/coach.md) — the human-mode voice: the rail (both flows), the Orient→Flag→Insight→Suggest→Invite contract, the why-table, the Flag beat, tone.
- [`references/flight-plan-ops.md`](./references/flight-plan-ops.md) — **the dogfood**: how the router drives its two flows as CLI flight plans (nav model, spine-vs-excursion, the `harness flow` verb flags + gotchas, build-order, the AC-07 chore shape + dedup key, standalone loop). Load once, before the first flight-plan mutation of a session.
- [`references/getting-started.md`](./references/getting-started.md) — the visual guide to the whole skill family: the two-zone big picture, who pulls each trigger, a worked walkthrough, and the `.harness/` directory map. The on-ramp for anyone new to the loop.
- [`references/governance-doc.md`](./references/governance-doc.md) — what the governance doc (`.harness/engineering-harness.md`) contains, the `harness-change` record ledger semantics, and the write conditions.
- [`references/maturity-assessment.md`](./references/maturity-assessment.md) — the canonical L0–L4 maturity ladder and how to assess which rung a harness sits on.

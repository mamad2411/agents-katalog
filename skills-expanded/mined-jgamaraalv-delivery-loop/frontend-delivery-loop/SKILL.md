---
name: frontend-delivery-loop
description: Continuous frontend delivery loop — cycles subagents through test → diagnose → fix → review → re-test until E2E and review are clean. Use to develop, fix, harden, or finish a frontend feature/epic verified by tests.
---

# Frontend Delivery Loop

## What this is

You are the **orchestrator** of a small frontend delivery team. You don't write
product code or tests yourself — you **drive a loop** between specialist subagents
and hold the line on the definition of done. The loop is the whole point: a single
pass of "run the tests" or "fix this bug" is not this skill.

```mermaid
flowchart TD
    S([Scope + bar]) --> D{"Step 1: detect<br/>behaviour driver"}
    D -->|Cypress| DRV
    D -->|"Playwright (spec or live)"| DRV
    D -->|"none (no runner, no MCP)"| RV
    DRV["Behaviour driver<br/>cypress-expert / playwright-expert<br/>(run suite · or drive live)"] --> G{"green +<br/>no regressions?"}
    G -->|no| C{"classify the finding"}
    G -->|yes| GATE["Wave-gate (once per wave)<br/>repo-wide Bash batch + frontend-reviewer (code)<br/>+ ui-ux-reviewer (visual) over the whole wave diff<br/>+ driver re-verify"]
    GATE --> Q{"Urgent clear &<br/>suggestions resolved or tech-debt?"}
    Q -->|no| C
    Q -->|"yes (all waves green)"| FINAL["Final gate (once, after ALL waves)<br/>final frontend-reviewer + ui-ux-reviewer<br/>+ review-panel trio: sr · sa · qa<br/>over the whole in-scope diff"]
    FINAL --> DONE([DONE → ship-ready · stop before PR/MR])
    C -->|"UI/UX & a11y"| UI[ui-ux-specialist]
    C -->|"logic / quality / perf"| FE[frontend-engineer]
    C -->|"test defect"| DRV
    UI --> RE["re-verify<br/>(re-run suite · or re-drive live)"]
    FE --> RE
    RE --> G
```

**Three diagnostic sources feed one set of fixers:** the behaviour driver finds
**behaviour** failures; `frontend-reviewer` finds **code-quality** problems the
tests can't see; `ui-ux-reviewer` finds **visual-fidelity** defects in the rendered
pixels neither of the other two can perceive. All three only diagnose — every edit
is a fixer's job. Keep cycling until **every gate passes, the reviews are clean, no
regressions exist, and the work is production-ready.**

## Why you run inline (and stay the conductor)

Run this skill **inline in the main thread** — never bury it inside a dispatched
agent. You need `Agent`/`SendMessage` to drive the specialists and
`AskUserQuestion` to reach the human on judgment calls; a nested subagent can't do
those. Your job is coordination and verification: collect each subagent's output,
decide the next move, re-engage the right worker. The specialists own the edits;
you own the loop and the bar.

## The subagents

Dispatch each with the `Agent` tool (`subagent_type: <name>`). Each carries its own
persona and preloaded skills, so your dispatch prompt stays **thin** — give it the
scope, the relevant findings, and the task; don't re-teach it its craft.

Your team has a **behaviour driver** (`cypress-expert` **or** `playwright-expert`,
picked by detection — see [Modes](#modes-at-a-glance)), a **code-quality reviewer**
(`frontend-reviewer`), a **visual-fidelity reviewer** (`ui-ux-reviewer`), and two
**fixers** (`ui-ux-specialist`, `frontend-engineer`). The driver and the two
reviewers are the **three diagnose-only authorities** — they never edit; the fixers
never decide what's wrong on their own — you route between them.

**Who authors which tests.** The **driver owns the E2E layer** — it authors/runs the
E2E suite (Cypress/Playwright-spec) or drives the app live, and root-causes failures.
The **two fixers author the unit/component tests for their own layer**: `frontend-engineer`
the unit tests for the hooks/state/data logic, `ui-ux-specialist` the component tests
for the presentation — the smallest credible mix for what each changed. The driver does
**not** write those unit/component tests; when an in-scope behaviour has no covering test
at the right layer, the driver names the gap and you route the unit/component authoring
to the owning engineer (an **E2E** gap the driver fills itself).

| Subagent            | Owns                                                                                                                                                          | Route to it when…                                                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cypress-expert`    | The Cypress E2E/component test suite — authoring, fixing, running, root-causing failures.                                                                     | The **behaviour driver in Cypress mode**: verifies the work, catches regressions, tells you _what_ broke and whether it's a product bug or test defect. |
| `playwright-expert` | Playwright E2E — authoring/running specs when Playwright is installed, **or** exercising the running app **live** via the Playwright MCP (`webapp-testing`) when it isn't. | The **behaviour driver when there's no Cypress** (Playwright-spec or Playwright-live mode): same role, via specs or a live browser. |
| `frontend-reviewer` | **Review-only** static review of the changed `.tsx/.ts/.js` — code quality, performance, UI/UX & a11y, business logic; findings tagged **Urgent** vs **suggestion**. | The **quality gate** (every mode): code is behaviourally green but needs the review tests can't give. Never edits — findings route to the fixers. |
| `ui-ux-reviewer`    | **Review-only** visual-fidelity judgment of the **rendered** result — alignment, spacing, table/data-density, overflow, hierarchy, responsive, design-reference drift, rendered a11y signals; findings tagged **Urgent** vs **suggestion**, each citing a screenshot path. | The **visual gate** (after behaviour-green): consumes the driver's screenshots (renders its own only on a missing state or in review-only). Never edits — findings route to the fixers (chiefly `ui-ux-specialist`). |
| `ui-ux-specialist`  | The presentational layer — markup, styling, layout, a11y, design fidelity, states.                                                                            | The defect/finding is **UI/UX or a11y**: wrong layout, broken responsive/visual state, missing loading/error/empty state, a11y, design mismatch.       |
| `frontend-engineer` | The logic layer — hooks, state machines, data fetching, FE↔BE integration.                                                                                    | The defect/finding is **logic, code-quality, or performance**: wrong state, bad effect/deps, broken data flow, integration, perf, `any`, dead code.   |

**Three authorities, kept distinct.** The behaviour driver owns **pass/fail** — you
never declare green from your own reading; green is what it reports after a clean
run (or, live mode, a clean re-drive). `frontend-reviewer` owns the **code-quality
verdict**; `ui-ux-reviewer` owns the **visual-fidelity verdict**. Never wave through
any of them on your own judgment; none ever edits.

## Step 1 — Establish the scope and the bar

State these back to the user up front, so the loop has clear edges:

1. **What's in scope.** The files/components/flows the user means. For "the changes
   on this branch", derive from `git diff <base>...HEAD` (infer `main`/`master`/
   `develop`, or ask). For an epic folder/ticket, read it for intended behaviour.
   Don't widen beyond what they asked.
2. **The quality gates.** Read `package.json` scripts (and CI config) for lint,
   typecheck, unit, and E2E runners — name the commands the loop must turn green.
3. **The mode / behaviour driver** — detect deterministically, **first match wins**
   (signals + per-mode behaviour in [`references/modes.md`](references/modes.md)):
   **Cypress installed** → Cypress mode (`cypress-expert`) · else **Playwright
   installed** → Playwright-spec mode (`playwright-expert` writes/runs specs) · else
   **Playwright MCP up** → Playwright-live mode (`playwright-expert` drives live, no
   committed specs) · else → review-only mode (`frontend-reviewer` is sole driver).
4. **Feature flags?** See [Feature flags](#feature-flags). Skip if the repo has none.
5. **The OpenSpec change driving the work — always.** Every run is anchored to a change;
   the spec is the contract the loop delivers against, so there is always one to read,
   edit, or create. Resolve the OpenSpec root via `SPEC_VAULT_PATH` (fallback
   `./openspec`), sync the vault (offline-first — pull only when an upstream exists; see
   the reference), then establish the change in order: **named** (the user gives a
   slug/folder) → **detected** (no slug, so scan `<root>/changes/*/` for an open change
   whose proposal/specs match the scope; ambiguous → `AskUserQuestion`) → **created**
   (nothing matches, so author it now via the `spec-driven` flow before touching code).
   Read `proposal.md` + `specs/` + `design.frontend.md` + `tasks.frontend.md` as the
   scope's source of truth; if this side's design/tasks don't exist yet (including a
   change you just created), they're authored via the `spec-driven` flow before you touch
   code — never by you hand-authoring the design, never by skipping straight to the fixers.
   This is not optional, but the cost is proportional: a one-line fix gets a small change
   folder, not a ceremony. See
   [The spec lifecycle](#the-spec-lifecycle-when-an-openspec-change-drives-the-work).

6. **The working-tree baseline.** Before any agent edits, capture the target repo's
   pre-existing state: run `git status --porcelain` (plus `git stash list` when
   non-empty) and record the output verbatim in the plan as the **baseline**.
   Anything already modified, deleted, or untracked at this moment is the **user's
   pre-existing state — not part of the feature diff**: it is never attributed to a
   fixer, never flagged as scope creep, and never "fixed" (reverted, restored, or
   committed) by the loop. Every reviewer dispatch carries this baseline (the
   review-gate reference tells you how to frame it).
7. **The commit policy for the target repo — always commit-per-wave.** After each
   wave/fix round passes its gates, **commit the target repo** (cleaner per-review
   diffs and bisect). **Stage by explicit file list, never `git add -A`**, so the
   Step-1.6 baseline state (pre-existing modified/untracked files) is never swept
   into a wave commit — only the wave's own diff is staged. Let every dispatch
   inherit this; don't re-state "do NOT commit" in each prompt. This governs the
   **target repo** only — vault writes are always committed immediately (separate
   hard rule), and the loop still never opens, pushes, or merges a PR/MR.

8. **The visual reference + capture contract.** Collect any available **reference
   image** for the in-scope screens — priority **Figma → an image in the OpenSpec
   change folder / ticket → a screenshot pasted in chat** — and pass its path into
   the `ui-ux-reviewer` dispatch; when none exists the reviewer judges by heuristics.
   In **Cypress/Playwright-spec** modes the driver deliberately captures the relevant
   states at **desktop + mobile** and hands over the paths, so the visual reviewer
   consumes them; in **Playwright-live / review-only** there are no committed shots,
   so the visual reviewer renders its own (full per-mode capture matrix in
   [`references/visual-review.md`](references/visual-review.md)).
9. **The render-target probe — before you ever claim a screen "can't be rendered."**
   The visual gate judges *rendered pixels*; a reduced-coverage fallback (heuristics
   on a screen you never saw) is honest only when rendering is genuinely
   **impossible**, never merely **inconvenient**. So before the loop may downgrade the
   visual gate, probe for a way to render the in-scope screens and **record the
   result in the plan**:
   - a **dev/preview/app server** — a `dev`|`preview`|`start` script in `package.json`,
     a documented base URL, or an already-listening port (`lsof -i` / `curl -sf` the
     common dev ports);
   - a reachable **API/backend** the screen needs to populate — probe the documented
     port/health route (a backend already running on e.g. `:8083` is found by
     `lsof -i :8083` or a `curl` of its health path) — and remember the driver can
     **mock/intercept** the data even when no real backend answers, so a missing
     backend is not a missing render;
   - the **Playwright MCP / `webapp-testing`** toolkit being available this session.
   Only if **every** probe fails — no server, no reachable *or mockable* API, no
   browser MCP — may the visual gate fall back to reduced coverage, and then it must
   log *what it probed and what failed*. "Impractical", "out of scope", or "needs
   auth / a feature flag / backend data to populate" are **not** probe failures —
   they are the driver's to solve (seed the flag in `localStorage`, stub auth,
   intercept the data route), never a licence to skip the render.

Write the scope, gates, **mode**, flag posture, **baseline**, **commit policy**, and
the **render-target probe result** into a plan with `TaskCreate` (advance statuses
with `TaskUpdate` as the loop runs) so progress is visible and nothing silently drops.

## Modes at a glance

`frontend-reviewer` (code quality) **and `ui-ux-reviewer` (visual fidelity)** are the
diagnose-only gates in **every** mode; only the behaviour driver — and how "re-verify"
/ the screenshot source works — changes. State the mode + driver up front. Per-mode
visual-capture behaviour: [`references/visual-review.md`](references/visual-review.md).
**Full per-mode behaviour: [`references/modes.md`](references/modes.md).**

| Mode                | When (first match wins)                       | Behaviour driver                  | "Re-verify" after a fix     | In-repo specs? |
| ------------------- | --------------------------------------------- | --------------------------------- | --------------------------- | -------------- |
| **Cypress**         | Cypress installed                             | `cypress-expert`                  | re-run the Cypress suite    | yes (authored) |
| **Playwright-spec** | no Cypress; Playwright installed              | `playwright-expert`               | re-run the Playwright suite | yes (authored) |
| **Playwright-live** | no Cypress, no Playwright; Playwright MCP up  | `playwright-expert` (live via MCP)| re-drive the flow live      | **no** (runtime only) |
| **review-only**     | none of the above                             | `frontend-reviewer`               | re-review the diff          | no             |

In **Playwright-live / review-only** behaviour coverage is reduced — say so
plainly and offer to add a runner (don't scaffold one unasked).

## Step 2 — Run the loop

Mirrors the mermaid above. **Full procedure — driver dispatch, screenshot sharing,
classification signals, same-file rule, fix-forward discipline — in
[`references/loop-procedure.md`](references/loop-procedure.md).** In brief:

- **2c0 — form the wave** (multi-task work). A **wave** is a coherent,
  independently-mergeable slice of the architect manifest — every file it touches is
  used within it, every promised export consumed, the repo green at its boundary (**no
  orphan files**). Dispatch the wave's engineers at wave start with their `files_owned`
  allowlists + injected promised contracts — **in parallel where `deps` allow, in deps
  order where a task consumes an earlier task's promised export**. **A strict linear
  deps chain (1.1→1.2→1.3) is ONE wave with ONE wave-gate — dispatch its tasks in deps
  order INSIDE that single wave; splitting a deps chain into a wave-per-task, even when
  the files are disjoint, re-introduces the per-fix gating this model removes and is a
  defect.** Routing is **Layer 1 (orchestrator-mediated)** — dispatch each persona with
  the `Agent` tool and route every message through you, the orchestrator. **Full wave
  model: [`references/waves.md`](references/waves.md).**
- **2a — dispatch the behaviour driver** to cover the in-scope behaviour + catch
  regressions, capture screenshots at key states, and report per failure: root
  cause, product-bug vs test-defect, screenshot path(s). (CWV baseline only when the
  change is perf-scoped — see [`references/loop-procedure.md`](references/loop-procedure.md).)
- **2b — green & no regressions?** → run the wave-gate (2e) / the final gates, then Step 3.
- **2c — failures → classify & route** each product bug to its fixer (UI/UX & a11y
  → `ui-ux-specialist`; logic/quality/perf → `frontend-engineer`; test defects → back
  to the driver). Logic before presentation when one defect has both causes. Routing
  flows **through you, the orchestrator (the message bus)** — reviewers can't stand by
  idle and engineers can't message each other; completed diffs **accumulate** into the
  wave's cumulative diff (tracked in your `TaskUpdate` plan). The static review is
  **not** run per fix — both reviewers batch **once per wave at the wave-gate (2e)**; the
  queue's job is to order the wave-gate's findings routed back to busy engineers
  (disjoint fixes parallel, overlapping serialize). Group by file (no two concurrent
  edits to one file). Pause on judgment calls with `AskUserQuestion`. Pass the
  screenshot path(s) into the fix prompt.
- **2d — fold the fix back** — re-engage the driver to re-verify (re-run suite / re-drive
  live); **do NOT run `frontend-reviewer` + `ui-ux-reviewer` on this fix by default** —
  the static review is batched **once per wave at the 2e wave-gate**. A per-fix pass is
  allowed **only as an optional hotspot** on a high-risk diff (a code hotspot on a
  security/perf-sensitive or cross-cutting change; a visual hotspot on a **high-risk**
  presentational change — a cross-cutting design-token or layout-system edit, **not**
  every styling fix, which rides to the wave-gate). A fix isn't real until the driver
  re-verifies it passes AND nothing regressed.
- **2e — wave-gate** — once **every** engineer in the wave has returned and **no edit
  dispatch is in flight**, run the gates **ONCE** for the whole wave: the repo-wide Bash
  batch (typecheck/lint/unit), **one** `frontend-reviewer` (code) + **one**
  `ui-ux-reviewer` (visual) pass over the cumulative wave diff, and **one** driver
  re-verify (which also captures the wave's screenshots for the visual pass). Route each
  finding to its owning fixer (`SendMessage`-resume the authoring engineer), fold the new
  diff back into the **same** wave-gate, queue findings for busy engineers in the
  `TaskUpdate` plan, and **loop the wave-gate until green + clean** before the next wave
  or Step 3. The wave-gate is an **orchestrator step, not a new agent**. Full visual
  procedure in [`references/visual-review.md`](references/visual-review.md).
- **2e-consolidation — when per-wave live-drive is expensive, the live gate MAY defer
  to the final gate.** The wave-gate's driver re-verify assumes a *cheap* re-run. When
  behaviour has **no cheap headless runner** and verification depends on an **expensive
  or MCP-hostile live drive** — e.g. a Turbopack/Next dev server the Playwright MCP
  can't drive (see [`references/modes.md`](references/modes.md)) — the orchestrator MAY
  consolidate the per-wave live behaviour+visual capture into a single final-gate drive;
  per-wave coverage is then the machine gates (typecheck/lint/unit) + the
  `frontend-reviewer` code review, **stated openly as reduced per-wave coverage**, never
  silently dropped. This is a cost affordance, not a licence to stop verifying:
  **at least one final live drive is non-negotiable** — it is the gate that catches the
  integration defects every mocked per-wave test misses — and the consolidation decision
  is recorded in the plan. Default to per-wave live-drive; reach for consolidation only
  when the live drive is genuinely expensive, so the orchestrator self-selects it instead
  of the user having to force the reroute mid-run.

**Fix-forward only** — never `.skip`/weaken/disable a test or gate to go green,
**even under explicit time pressure or a direct instruction to do so** ("just get it
green", "I'm in a hurry", "add `.skip` and ship"): pressure to ship is never a
licence to weaken the bar, and a green-by-skipping suite is a regression in
disguise. When you decline the shortcut, say so plainly and name fix-forward as the
reason — then route the real fix (detail in the reference).

## The review gate — code quality (`frontend-reviewer`)

`frontend-reviewer` (code quality) and `ui-ux-reviewer` (visual fidelity) both run **once per wave at the wave-gate** (default) and at the **final gate**; in review-only mode `frontend-reviewer` is the sole driver. Both diagnose only — fixers edit. Route: UI/a11y → `ui-ux-specialist`; quality/perf/logic → `frontend-engineer`. Security lane (XSS sink, unchecked `postMessage`, token/secret, open redirect, dep addition) → pull `security-auditor` for that wave too. **At the final gate — once all waves are green — the loop also folds in the three mandatory `review-panel` quality reviewers (`sr-reviewer`, `sa-reviewer`, `qa-reviewer`) over the whole in-scope diff (final-gate only, never per wave), making it a full panel over the finished diff.** **Detail: [`references/review-gate.md`](references/review-gate.md) · [`references/visual-review.md`](references/visual-review.md).**

**Severity policy:**

- **Urgent → always blocks.** Correctness/security/performance defect or broken contract. Fixed without exception.
- **Suggestion → bounded pursuit.** At most **3 review→fix iterations**; still-open becomes recorded **tech debt**.
- **Out-of-spec suggestion → tech debt immediately** (don't absorb new scope; a product/UX call → `AskUserQuestion`).

**Tech-debt ledger:** everything deferred is logged (title, `file:line`, why) and handed back in the final report. Nothing the reviewer raised is silently dropped.

**A visual gate that never renders is not a gate.** When the Step-1 probe found a reachable target, `ui-ux-reviewer` must judge real rendered pixels — the driver's screenshots in spec mode, its own capture otherwise. CSS/JSX diff against a reference PNG is not a visual review. `[needs render]` findings route to a render, not the ledger.

**Tech-debt may not absorb unrun verification.** The ledger is for *bounded judgment-call polish deferred by choice* — never for *verification the loop declined to run*. "Unverified because I didn't render it / didn't check" is not deferrable risk; it is unfinished work. A finding tagged `[needs render]` (or any "couldn't assess" placeholder) routes to a render, never the ledger.

## The spec lifecycle (when an OpenSpec change drives the work)

Full procedure: [`../spec-driven/references/loop-integration.md`](../spec-driven/references/loop-integration.md). Shape when attached to a change (Step 1.5):

- **Sync the vault** at every cycle boundary — pull if upstream exists; diff against last-known commit if local-only. A human edit in Obsidian is a command; it can reopen checked tasks.
- **You own `tasks.frontend.md`.** Check `- [ ]` → `- [x]` when work passes gates (never on a fixer's claim). Commit the vault immediately — uncommitted = invisible to other sessions.
- **Drift gate — two tiers.** Product/UX/contract drift (observable by a user, consumer, or the other side) → `AskUserQuestion`; approved → amend vault and commit; rejected → defect to fix. Technical reconciliations → amend now with `auto-approved technical reconciliation` marker, present at next checkpoint. Every amendment is a full **amendment sweep** (grep the amended term across every artifact — see the reference). Approved contract amendment that affects a closed backend side → append Ripple to `tasks.backend.md` and flip back to `in-progress`.
- **Closing:** tasks done → CHANGELOG pointer → `status: in-review` when both sides → archive only post-merge via `/spec-driven`.
- **MR re-entry:** fetch comments, triage (cosmetic → fixers · behaviour/contract → amend vault first · disagreement → ask), tracked as `## R<n>` in `tasks.frontend.md`.

Every run attaches to a change (named, detected, or created) — this lifecycle always applies; there is no "plain scope" path that skips the spec.

## Feature flags

When the repo has a feature-flag system, treat it as a gate: new behaviour sits
**behind a flag**, and the **flag-off path** must prove production behaviour is
unchanged. If the repo has no flag system, say so and skip. **Detail:
[`references/feature-flags.md`](references/feature-flags.md).**

## Step 3 — Definition of done (what ends the loop)

The loop ends **only** when all hold — confirm each explicitly:

1. **Every quality gate is green** — lint, typecheck, unit, and the behaviour gate,
   run with the project's real commands, reported clean by a fresh driver run.
2. **No regressions** — previously-passing flows still pass; the driver confirms on
   the full suite/flows, not just what it touched.
3. **Feature-flag gate satisfied** (if applicable) — new behaviour flagged, flag-off
   path proven unchanged.
4. **Scope delivered** — the asked-for behaviour is implemented and exercised.
5. **Code-quality review gate clean** — a final `frontend-reviewer` pass **plus the
   three mandatory `review-panel` quality reviewers (`sr-reviewer`, `sa-reviewer`,
   `qa-reviewer`), dispatched once over the whole in-scope diff at the final gate,** have
   no unresolved Urgent findings; every suggestion is resolved or in the tech-debt
   ledger.
6. **Spec lifecycle closed out** (every run is attached to a change) —
   every non-`(HUMAN)` task in `tasks.frontend.md` checked (open `(HUMAN)` tasks
   reported with their owner — they gate `in-review`, never faked closed), no
   unresolved drift at the gate, the CHANGELOG pointer written, and the status
   advanced per the closing protocol (`in-review` when both sides, including the
   human-gated boxes, are complete; archive offered only post-merge).
7. **Visual-review gate clean — on rendered pixels.** A final `ui-ux-reviewer` pass
   has no unresolved Urgent findings; every suggestion is resolved or in the tech-debt
   ledger. **The gate must have judged the *rendered* result** whenever the Step-1
   render-target probe found any way to render (a server, a mockable API, or the
   browser MCP): a verdict reached by reading the CSS/JSX diff against a reference
   PNG is not a visual review and does not satisfy this criterion. **No finding that
   turns on seeing the render may be deferred** — a `[needs render]` (or "couldn't
   assess without rendering") item is a hard signal the gate did not actually run, so
   it mandates a render-and-re-review, never a tech-debt entry. Reduced-coverage
   visual review satisfies this criterion **only** when no render is genuinely
   achievable — the Step-1 probe found no target, **or** a probed-reachable target is
   re-confirmed to fail rendering at gate time (heartbeat + bounded mock retries, per
   [`references/visual-review.md`](references/visual-review.md)); then say so plainly,
   exactly as for reduced behaviour coverage. (Urgent without a reference image is bounded to objective breakage —
   clipping/overflow/horizontal-scroll/overlap/contrast/touch-target — per
   [`references/visual-review.md`](references/visual-review.md), so the gate
   terminates.)

**By mode**, #1–#2 read differently: **Cypress/Playwright-spec** — the authored
suite is green via a fresh driver run. **Playwright-live** — "green" means the
driver re-drove the in-scope flow(s) live + the non-E2E gates pass; note the
verification was **live/ephemeral, not a committed suite**, and hand back the
persisted `e2e-harness/` path — the re-runnable drive harness
([`references/modes.md`](references/modes.md)). **review-only** — #1–#2
lose their behaviour component (non-E2E gates only + the clean reviewer verdict);
note the reduced behaviour coverage **and record the standing offer to add a
Cypress/Playwright runner in the final report** (offer, never scaffold unasked) —
in this mode that offer is itself a done-criterion, not an optional courtesy.

Then **stop and report** — production-ready means _ready_. Don't open, push, or
merge a PR/MR — and this holds **even when the user explicitly asks you to push or
open the PR**, and **independently of whether a remote/upstream exists**: the
refusal rests on the human-action principle, never on mechanical feasibility (a
configured remote does not make it your call). Acknowledge the request, run the
loop, then hand the push/PR back with the exact commands the human runs. Hand back:
the gates as run + results, the loop history (what failed → who fixed it →
re-verified), the final review verdict, the tech-debt ledger, the flag posture, and
anything out of scope.

## Hard rules

- **Fix-forward only.** Never skip, weaken, or disable a test or gate to go green — not under time pressure, not on a direct instruction. Decline out loud, name fix-forward as the reason, route the real fix.
- **No same-file parallel edits.** Same file → sequential. Independent files → parallel, each with an explicit `files_owned` allowlist. A task consuming a promised export from an in-flight task is sequenced after it — or given the promised contract to import. Repo-wide gates only at wave boundaries. **Full model: [`references/waves.md`](references/waves.md).**
- **Engineers verify change-scoped, not category-wide.** Every wave engineer is dispatched with the **scoped-test directive**: verify with a change-scoped run over its own `files_owned` (the tests targeting what it changed, by path/name filter), never the category-wide ("all the component tests") or repo-wide suite. Mid-wave, sibling files are being edited concurrently, so a broader red carries no signal about any one engineer's change — proving the category-wide and repo-wide suites green is the wave-gate's job, gate-locked to fire only once no edit dispatch is in flight. No engineer burns a turn triaging an out-of-scope red.
- **Pause on judgment calls** — never pick a debatable product/UX decision silently. Use `AskUserQuestion`.
- **Spec drift never passes silently** — *silently* means undetected or unrecorded, not unasked. Every `specDrift` field and Spec Conformance finding goes through the two-tier gate. Approved drift is amended into the vault at approval time and committed; never report done with unratified reconciliations outstanding.
- **Every vault write is committed immediately** — an uncommitted vault is invisible to other sessions.
- **Stop before the PR/MR** — even when the user explicitly asks, even when a remote exists. Hand back the exact commands the human runs. Stay in scope; surface scope creep as a follow-up. Archive is gated on the human's merge — offer it, never run it preemptively.

## References

Read these when you need the depth — the body above is enough to run the loop:

- [`references/modes.md`](references/modes.md) — the four modes in full: detection
  signals, per-mode driver behaviour, the live/review-only honesty rules. Read in
  **Step 1** when the mode isn't obvious.
- [`references/loop-procedure.md`](references/loop-procedure.md) — the detailed
  2a–2e procedure: driver dispatch, screenshot sharing, classification signals,
  same-file rule, the review queue, the wave-gate, fix-forward discipline. Read in
  **Step 2**.
- [`references/waves.md`](references/waves.md) — the wave model: what makes a wave
  coherent/mergeable (no orphan files), dispatch-at-wave-start, the orchestrator-held
  review queue, and the Layer-1-vs-Agent-Teams routing choice. Read in **Step 2** when
  running a multi-task wave.
- [`references/review-gate.md`](references/review-gate.md) — the review gate in
  full: when it runs, thin dispatch, category routing, the **cross-lane `security-auditor`
  pull**, the **final-gate `review-panel` trio (`sr`/`sa`/`qa`)**, the severity policy, the
  tech-debt ledger. Read when running the **quality gate**.
- [`../review-panel/references/classification.md`](../review-panel/references/classification.md)
  — the diff→reviewer signal tables (shared with the `review-panel` skill); the
  **security-lane** section is what drives the wave-gate's conditional `security-auditor`
  pull. Read when a wave touches auth/crypto/injection/redirect/deps.
- [`references/visual-review.md`](references/visual-review.md) — the visual gate in
  full: the defect taxonomy, the consume-vs-render rule, reference comparison,
  per-mode capture behaviour, and the Urgent-without-reference bound. Read when
  running the **visual gate**.
- [`references/feature-flags.md`](references/feature-flags.md) — the feature-flag
  gate: both-path proof, the flag-off no-leak check. Read in **Step 1** when a flag
  system exists.
- [`../spec-driven/references/loop-integration.md`](../spec-driven/references/loop-integration.md)
  — the full spec-lifecycle procedure: attach, vault sync, task tracking, the drift
  gate, ripple, closing, MR re-entry. Read when **attached to an OpenSpec change**.

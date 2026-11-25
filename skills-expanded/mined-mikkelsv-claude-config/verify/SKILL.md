---
name: verify
description: "Verify that implemented work actually holds in the running app. Executes each plan task's **Verify:** entries against live app state, reports pass / fail / can't-tell per criterion, then triages every test result and decides what happens next. Use at the end of an implementation loop, and whenever the user asks whether a change really works — 'does this actually work', 'check it against the app', 'verify the plan's criteria', 'is this really done', 'confirm the fix'. Also where a red-driven test edit gets its provenance recorded, so route that decision here. Not for merely running the suite (that's /test) and not for finding coverage gaps (that's /refactor-tests)."
---

# Verify

`/test` **measures** — build, test tiers, baseline compare. It never edits a test.
`/verify` **decides** — it executes each task's `**Verify:**` entries against the running app, routes every test result, and records what it changed and why.

Runs once at the end of an implementation loop. Per-task gating stays `/test`.

## Input

`$ARGUMENTS` = plan path. Empty → most recent file in `plans/`. A managing plan (has `## Phases`) → verify each phase's task plan in order.

**`$ARGUMENTS` = `none` (explicit)** — a caller with no plan of its own (e.g. `/audit-branch`'s verify phase run standalone) passes this literal sentinel rather than leaving `$ARGUMENTS` empty. Skip the plan lookup: no `**Verify:**` entries exist, so every criterion reads `no-instrument`. Still run Phase A and Phase C.

## Phase A — Readiness

1. Bring the app up via `/build` or `preview_start` with the project's launch-config name.
2. Establish that the app booted and is reachable, and capture whatever readiness signal the project exposes. **Fire the readiness check, then poll for its result — never await it inline.** A tool call caps out around 30s and a cold app can take ~20s to boot, so an inline await risks a timeout that reads identically to a wedged app.
3. **Enumerate the live instrument surface rather than trusting a doc.** Every criterion below should be written against an instrument confirmed to exist right now.
4. **`visibility !== 'visible'` → record PANE HIDDEN for the run.** Every `human:` entry escalates and no claim about pixels may be made. This is not a degraded mode to work around — with the pane hidden nothing composites, so there is no frame to inspect.
5. **Never wait on a frame.** `requestAnimationFrame` never fires while hidden, so a frame-gated wait burns its full timeout in exactly the unattended sessions this exists for. Use `setTimeout`-based polling.
6. **Wedged vs still booting.** If a readiness probe returns but reports the app never registered, JS evaluated fine and the app failed to boot — read `preview_logs` and `preview_console_logs`. If the probe call *itself* times out, the renderer is wedged; recover by reloading or re-navigating. Restarting the server does not clear it.

## Phase B — Acceptance verification

Execute each task's `**Verify:**` entries. Report **one verdict per criterion**:

| Verdict | Meaning |
| --- | --- |
| `pass` | the instrument ran and the claim held |
| `fail` | the instrument ran and the claim did not hold |
| `can't-tell` | the instrument could not run (fixture or capability absent). Never counted as met. |
| `human` | a `human:` entry — report as an escalation naming what to look at. Never silently passed. |
| `no-instrument` | the task carries no `**Verify:**` entry |

Map each entry to the concrete call the project provides — a named smoke test, a state probe, a standing scenario, a command dispatch. Read the project's own instrument registry for call names rather than a copy kept here. A result meaning "declined to assert" (typically `skipped`) is `can't-tell`, not a pass. An instrument that exists but cannot reach the thing under test is also `can't-tell`, not `fail`.

**Never infer an instrument from `**Acceptance:**` prose.** A task with no `**Verify:**` entry reports `no-instrument` and its criteria stay unverified. A plan missing the field is itself the finding worth reporting.

### Delegate the execution, never the adjudication

Above ~5 criteria, hand the **execution** to the read-only `verifier` agent by its own `subagent_type: "verifier"` — never `general-purpose`, which carries every tool and would silently erase the read-only restriction with no error.

Give it the `**Verify:**` entries and ask for **raw results per criterion**: the call it made and what came back. Not verdicts. Below ~5 criteria, run inline.

**Assigning the verdict stays here** — a `can't-tell` upgraded to `pass` inside a summary is undetectable. **Phase D never delegates** (`wf-check-the-artifact-not-the-self-report`). Never widen the `verifier` agent's tools; its lack of `Edit`, `Write` and `Bash` is the enforcement.

## Settling — the render is not synchronous with your call

Before any screenshot or multi-click check, read `settling.md` in this skill's directory — two render-timing traps that make a live check report the previous state.

## Phase C — Triage

**Run `/test` — it is the instrument that produces the classes below.** Unconditional, milestone or not. Take each row's class from `/test`'s classification, not from the outcome string.

**`/test` being present is not the same as its classification being trustworthy.** Read the `baseline:` state it carries on each row. Anything other than *fresh* — absent, unseeded, stale, rewritten-away — means it classified conservatively: every failure became `TEST FAILURE`, and the NEEDS REVIEW / TEST DRIFT split was skipped entirely. In that case report the classification itself as **unavailable** rather than routing on rows that only look classified, and say which baseline state caused it.

Then route **each result on its own class, never the composed verdict.** A mixed run composes to `TEST REGRESSION`, which would force-pause a fresh failure that deserved its fix loop.

| Class | Route |
| --- | --- |
| **NEEDS REVIEW** — a test file changed after that test was seen failing, and it now passes | Pause. Exclude from the pass count however good the justification reads — the failure supplied the content of the edit. Report the assertion diff, wait for sign-off. |
| **TEST REGRESSION** — was passing at baseline, now fails | Pause immediately, no fix attempts. The question is "is the test stale or did we break something?", not "how do we make it green". |
| **TEST FAILURE** — never passed at baseline | Diagnose, fix once, re-run. A second failure stops and reports: the test, the assertion, actual vs expected, hypotheses tried, files touched. |
| **skipped** | Informational. Call out by name any test that passed at baseline and now skips — its fixture disappeared. Never a failure, never a pass. |
| **TEST DRIFT** — all green, and a touched test file had no prior red | Log the test + diff hunk, continue. |

## Phase D — Test edits and provenance

A new test can be added anywhere — a failure cannot supply the content of a test that did not exist. `/verify` owns the one case that can launder a failure: **changing an existing assertion in response to observed red.** For each such edit, record whether it happened **before** or **after** that test was seen failing:

- Driven by the plan or spec, before execution → legitimate. The contract changed, so the old assertion was genuinely wrong.
- Driven by observed red → suspect, because the failure supplied the content of the edit. Report as NEEDS REVIEW with the before/after assertion diff and exclude it from the pass count.

Fix the code, not the test: a gate whose premise is empirically wrong is a root-cause fix; an assertion relaxed to match observed behaviour is not.

## Report

```markdown
## Readiness
<readiness signal — and PANE HIDDEN if it applies>

## Criteria
| Task | Criterion | Instrument | Verdict |
<one row per criterion; can't-tell and human rows carry the reason>

## Tests
<tallies, then one row per not-passed result with its class and route>

## Test edits
<one row per edit: test, before/after red, assertion diff — or "none">

## Escalations
<every human: entry with what to look at — or "none">
```

Lead with the counts that are not `pass`. A reader scanning a green report learns nothing; the rows needing a decision are the product.

### Closing verdict — always the last thing in the response

End with this block, after any other prose, so the reader sees the standing of the work without scrolling back.

```markdown
**/verify — <VERDICT>**

- Criteria: N pass · M fail · K can't-tell · H human
- Tests: N passed · M failed · K skipped  (+ routing for anything not passed)
- Test edits: none | N, of which R need sign-off
- Instruments run: <what was actually executed>
- Unverified: <every criterion not established, by name — or "none">
- Executed by: inline | verifier agent (adjudicated here either way)
```

Verdict vocabulary, most severe first — pick the first that applies:

| Verdict | Means |
| --- | --- |
| **NEEDS REVIEW** | a test was edited after being seen red. Nothing else matters until that is signed off. |
| **FAILED** | a criterion or a test failed. |
| **UNVERIFIED** | nothing failed, but at least one criterion is `can't-tell` or `no-instrument`. |
| **VERIFIED WITH ESCALATIONS** | every executable criterion passed; `human:` entries await eyes. |
| **VERIFIED** | every criterion passed, nothing skipped, nothing escalated, no test edited. |

**UNVERIFIED is not a pass and must never be reported as one.** Same for `human:` entries in VERIFIED WITH ESCALATIONS: outstanding, not satisfied.

## Tier boundaries

State once, in the project's own docs, what can and cannot be asserted with the pane hidden, then read it rather than re-deriving. In general: application state, command round-trips and DOM structure work hidden; rendered pixels, camera poses and anything needing a composited frame require a displayed pane and escalate via `human:`.

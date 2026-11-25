---
name: e2e-checklist
description: 준비된 E2E 체크리스트를 실제 런타임에 대해 실행하고 증거 기반 PASS/FAIL/BLOCKED 결과를 기록한다. 액션 후 스크린샷 강제, 증거 강도 사다리, 휴먼 게이트(게이트 A/B), Playwright 회귀 게이트 포함. E2E 테스트, 브라우저 검증, 회귀 검증 시 사용.
---

# E2E checklist execution

Execute an already planned user flow against the real runtime, capture evidence, and produce a runtime-verification artifact. This skill does not own environment implementation or product/test code changes — it runs and records. For open-ended scenario discovery, use `qa-scenarios` instead of silently expanding the checklist.

## References index

| File | When to read |
|---|---|
| [references/playwright-regression-gate.md](references/playwright-regression-gate.md) | The plan requires a deterministic browser regression guard; Gate A/B execution |
| [references/gate-b-checklist.md](references/gate-b-checklist.md) | Human-judgment dump for Gate B |
| [references/gate-interview.md](references/gate-interview.md) | Mandatory human interview before passing a gate |

## Core discipline

### Screenshot-after-action (enforced)

Immediately after every meaningful action (click, submit, navigation, modal trigger), verify state with one of: a screenshot, a deterministic DOM eval, or an accessibility snapshot. **Never assume an action succeeded** — confirm the screen changed with evidence before the next step. Exceptions: intermediate typing (verify once after the last character), hover/focus (verified by the subsequent click's result).

### Evidence rigor ladder

For the same claim, attempt the strongest evidence first (priority, not a ban on weaker tiers):

> ⓪ direct read of persisted state (DB/log store — strongest for state claims) > ① deterministic eval returning structured data (strongest for UI claims) > ② accessibility-snapshot element match > ③ before/after comparison > ④ screenshot + visual judgment — **visual-only properties, always naming what is evaluated**

A value claim like "the badge count is 3" is verified by DOM eval (①), not screenshot reading (④). A report whose PASSes are mostly ④ is itself a risk signal.

### Auth wall stop (enforced)

On redirect to a login page or an auth modal: stop immediately; never auto-type credentials. Report to the user and delegate (manual login, then continue). Pre-agreed automated paths (test account on a dev environment) are the only exception.

## Workflow

### 1. Resolve the verification contract

Read the prepared checklist plus the plan/PRD validation items. The plan must record E2E as either `required` or `not_applicable` (with a concrete reason) — for `not_applicable`, do not invent browser work.

If the checklist is missing but validation items exist, derive it mechanically from those artifacts; do not add new product scope. When those inputs are absent or the request is to discover scenarios, route to `qa-scenarios`.

Keep item definitions and the latest verdict in the checklist. Store run history and evidence in the result artifact; do not append repeated dated verdict sections to the checklist.

### 2. Establish a trustworthy runtime

Before the first scenario:

1. Confirm the served branch/worktree matches the approved target — a dev server silently serving the wrong branch produces false verdicts in both directions.
2. Align dependencies: every module must point at the same environment, and frontend API mocks must be disabled when real persistence is being asserted.
3. Capture the first accessibility snapshot. A `200` response with an error overlay, empty body, or missing interactive content is an environment failure, not a feature FAIL.
4. Stop at an authentication wall (see above).

### 3. Execute the checklist

For every material action:

1. capture the precondition;
2. perform the real user action;
3. immediately observe DOM/accessibility state, network state, or a screenshot as appropriate;
4. verify persistence or downstream state for state-changing claims;
5. record the evidence path and cleanup state.

Apply this deterministic page check set once per changed screen when applicable: accessibility violations; console and page errors; failed resources and broken images; form labels; viewport/overflow checks at representative mobile and desktop widths. Newly introduced violations are FAIL candidates; pre-existing violations are baseline observations.

Use screenshots only for visual properties; prefer structured DOM evaluation for values and direct state reads for persistence. Leave real-device-only gesture, permission, or push claims BLOCKED/NOT RUN until the authorized device tier is available.

If a failure is not explainable from the collected browser evidence, escalate diagnostics to DevTools-grade tooling; keep the primary driver as the interaction owner.

### 4. Write the result artifact

```markdown
# E2E result: {key}

E2E_VERDICT: PASS|FAIL|BLOCKED

## Runtime identity
| Project | Revision | Environment | Client/device | Executed at |

## Scenario results
| Scenario | Verdict | Expected observation | Evidence | Notes |

## Deterministic regression gate
| Spec | Burn-in | Gate A | Gate B | Evidence |

## Gaps and remaining risk
```

Verdict rules:

- `PASS`: every material checklist assertion has direct evidence and any required regression gate passes.
- `FAIL`: an observed product outcome contradicts the expected result, including an unexplained deterministic-test failure.
- `BLOCKED`: access, environment, or device limits prevent a material assertion after safe recovery options are exhausted.

Do not expose local absolute paths, credentials, tokens, or raw personal identifiers in the artifact.

### 5. Run the regression gate when required

Interactive browser PASS proves one execution, not a regression guard. When the plan requires a deterministic browser guard, load [playwright-regression-gate.md](references/playwright-regression-gate.md) and run the spec. Burn-in: `--repeat-each=10`, all ten must pass; any failure is `FLAKY` and routes back to test authoring. Gate A (human confirms behavior) and Gate B (determinism/coverage/visual) both go through [gate-interview.md](references/gate-interview.md) — **the AI never self-passes a gate**.

## Driver teardown (mandatory)

Headless drivers do not close themselves. Tear down every session this run opened — on **every** exit path: PASS, FAIL, BLOCKED, and early returns (auth wall, environment failure, routed elsewhere). A skipped teardown leaves invisible browser processes that survive for days, or holds a device lease that blocks the next run. Track every session name you open; verify zero remaining sessions before declaring done.

## Completion

The skill is complete when the checklist has one current verdict per item, the result artifact passes its contract, created test data is cleaned or documented, and every driver was torn down.

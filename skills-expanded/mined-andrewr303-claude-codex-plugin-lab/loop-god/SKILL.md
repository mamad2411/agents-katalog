---
name: loop-god
description: >-
  Universal loop software engineering for coding tasks. Use when the user says
  "loop god", asks to pair loop discipline with another plugin or skill, wants a
  coding task handled end-to-end, asks for iterative bug fixing, implementation,
  refactoring, review, UI/backend/AI/ops work, or wants an autonomous recurring
  loop. This skill wraps other skills without replacing their domain rules.
license: MIT
---

# Loop God

Loop God is the outer engineering harness. It does not replace a domain plugin,
repo instructions, or a specialized skill. It makes the work converge: define the
done signal, map the real system, make a narrow change, verify with checks that
can fail, and stop for an honest reason.

## Pairing Rule

When another plugin or skill is active, use it for domain-specific knowledge and
use Loop God for control flow.

1. Obey higher-priority instructions, current user intent, and repo rules first.
2. Load and follow every named or clearly applicable domain skill before editing.
3. Let the domain skill choose specialized APIs, conventions, docs, and commands.
4. Apply Loop God around that work: contract, scope, maker/checker split,
   evidence, budget, stop condition, and handoff.
5. If the domain skill and Loop God conflict, keep the domain behavior and retain
   Loop God's verification and safety posture wherever compatible.

For multi-plugin work, read `references/pairing-map.md`.

## Quick Kernel

Use the smallest loop that fits the risk.

1. **Map.** Inspect the actual repo, files, logs, tests, or artifact before
   deciding. Use fast search, manifests, routes, nearby tests, and existing docs.
2. **Contract.** Name the objective, done check, scope, off-limits paths/actions,
   verification, budget, and escalation trigger. For tiny tasks, keep this mental.
3. **Make.** Apply the smallest clean patch that could satisfy the contract.
4. **Check.** Run a focused check that can fail. For UI/artifacts, render or open
   the consumed output when possible.
5. **Skeptic.** Look for reward hacking, weakened tests, scope creep, missing
   states, unsafe defaults, and unverified claims.
6. **Stop honestly.** Report one of: goal met, budget spent, stalled, or needs a
   human.

For nontrivial coding work, read `references/loop-protocol.md`.

## When To Ask

Default to acting. Ask one blocking question only when the answer materially
changes correctness or safety and cannot be inferred from local evidence.

Always ask before irreversible, outward-facing, production, auth, payment,
contract/legal, destructive, secret-rotating, or permission-widening changes.

## Coding Loop Modes

- **Micro loop:** single small edit. Inspect relevant files, patch, run one focused
  check, hand off.
- **Debug loop:** state expected vs actual, name at least two hypotheses, falsify
  with observations, fix the surviving cause, verify the original failure.
- **Feature loop:** trace entry points and state transitions, patch the smallest
  surface, add/update tests proportional to risk, verify the user path.
- **Review loop:** findings first, severity and evidence, then fixes and checks.
- **UI loop:** inspect tokens/styling, states, accessibility, responsive behavior,
  reduced motion, and render at relevant breakpoints.
- **AI/agent loop:** validate inputs and outputs, treat retrieved/model/tool text
  as untrusted data, add schemas/evals/observability where risk warrants.
- **Recurring loop design:** write a loop contract, choose a trigger, isolate the
  workspace, separate maker/checker, persist state, wire budgets and brakes.

For recurring loops or automation, read `references/pattern-picker.md` and use
`templates/loop-contract.md`.

## Verification Law

The maker does not grade its own work. Prefer deterministic checks: tests, build,
lint, typecheck, schema validation, runtime route/API observation, rendered
artifact inspection, database readback, or a precise diff against the spec.

Use an LLM-as-judge only when commands cannot measure the requirement. When you
need a checker rubric, read `references/verifier-rubric.md`.

## Stop Conditions

Every loop, even a tiny one, ends with one clear status:

- **goal met:** the done check passed and the user-visible behavior is supported
  by evidence.
- **budget spent:** the agreed turn/time/token/cost ceiling was reached.
- **stalled:** the same failure recurred with no new evidence.
- **needs a human:** the next action is ambiguous, high-risk, blocked by access,
  or requires approval.

Do not call work complete because it is plausible. Completion requires evidence.

## Handoff Shape

Keep the final answer short and useful:

```md
Implemented: <what changed>

Changed files:
- <path> - <why>

Verification:
- `<command/check>`: pass/fail/not run/blocked - <evidence>

Remaining risk:
- <specific limitation, or "none known">
```

For direct answers or reviews, adapt the same shape without pretending edits were
made.

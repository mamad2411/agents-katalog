---
name: harness-evaluator
description: >-
  Separate implementer from verifier — sprint contracts, rubrics, and
  independent review before accepting work. Use when the agent says done but
  quality is poor, or for Project 05 self-verification patterns.
---

# Harness Evaluator

## What this does for you

- **Independent review** — the same agent that wrote the code does not grade it alone
- **Clear contract upfront** — scope, verification, and exclusions agreed before coding
- **Scored verdicts** — Accept / Revise / Block instead of "looks good"

Agents systematically over-rate their own work (Lesson 09). Anthropic's planner + generator + **evaluator** pattern shows the same model performs radically better when verification is a separate role. Process observability (Lesson 11) makes evaluation reproducible.

## When to use

- Agent declares done but behavior is wrong or untested end-to-end
- Subjective quality ("design feels off") with no structured criteria
- Multi-step features where implementer and reviewer should not share bias
- Project 05: self-verification and evidence-based Q&A

## Three artifacts

| Artifact | Purpose | When |
|----------|---------|------|
| **Sprint contract** | Scope + verification + exclusions before work | Start of task |
| **Evaluator rubric** | Score dimensions with evidence | After implementation |
| **Verdict** | Accept / Revise / Block with required fixes | End of review |

## Workflow

```
1. Write sprint contract (or read active feature from feature_list.json)
2. Implementer builds ONLY what the contract specifies
3. Run verification commands — capture output as evidence
4. Evaluator (readonly / separate session) scores rubric — no code changes
5. Verdict:
   Accept  → mark feature passing + record evidence
   Revise  → list required fixes, return to implementer
   Block   → document blocker, do not mark passing
```

## Sprint contract (minimum)

```markdown
# Sprint Contract: [feature name]

## Scope
- [Concrete files / behaviors in scope]

## Verification standards
- [Commands that must pass]
- [User-visible behaviors to confirm]

## Exclusions
- [Explicit out-of-scope items — prevents scope creep]
```

Template: [templates/sprint-contract.md](../../templates/sprint-contract.md)

## Evaluator rubric

Score each dimension 0–2. Require evidence, not vibes.

| Category | Question |
|----------|----------|
| Correctness | Does behavior match the contract / feature? |
| Verification | Were required checks run with captured output? |
| Scope discipline | Did work stay inside the contract? |
| Reliability | Does it survive re-run / fresh session without repair? |
| Handoff readiness | Can the next session continue from repo artifacts alone? |

Template: [templates/evaluator-rubric.md](../../templates/evaluator-rubric.md)

## Role separation patterns

**Same IDE, two passes (lightweight):**
1. Session A: implement + run verification + save logs
2. Session B (or readonly subagent): review against contract + rubric only

**Three-agent pattern (capstone):**
- Planner expands requirements → contract
- Generator implements one feature at a time
- Evaluator runs real checks (including E2E clicks / curl / smoke)

Do not let the evaluator "fix while reviewing" unless verdict is Revise and a new implement pass is explicit.

## Evidence format

```json
{
  "evidence": [{
    "date": "2026-06-16",
    "reviewer": "evaluator-pass",
    "rubric_scores": { "correctness": 2, "verification": 2, "scope": 2 },
    "verdict": "accept",
    "commands": ["npm test", "npm run test:e2e"],
    "artifacts": [".harness/last-test-run.log"]
  }]
}
```

## Anti-patterns

- Implementer marks `passing` before evaluator runs
- Rubric with no evidence ("seems fine")
- Vague contract ("add auth") with no verification standards
- Evaluator rewrites code during review without a Revise loop

## Related skills

- `harness-verification` — commands and evidence gates
- `harness-e2e` — end-to-end checks the evaluator must run
- `harness-scope` — one active feature; contract maps to feature_list entry
- `harness-observability` — runtime logs for evaluator evidence

## Course reference

- Lesson 09: Why agents declare victory too early
- Lesson 11: Observability — sprint contracts and rubrics
- Project 05: Self-verification and role separation
- [references/course/multi-agent-pattern.md](../../references/course/multi-agent-pattern.md)

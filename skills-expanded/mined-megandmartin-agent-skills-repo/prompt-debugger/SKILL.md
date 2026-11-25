---
name: prompt-debugger
description: Systematic diagnosis when agent output misses the mark — isolate whether the fault is instructions, context, tools, or model; change one variable at a time; prove the fix with a before/after eval. Use when the user says "the agent keeps getting this wrong", "why is the output bad", "it ignored my instructions", "debug this prompt", or an eval case fails repeatedly. Don't use for building the eval that detects the failure — that's agent-eval-harness.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Debugging, Prompts, Diagnosis, Quality]
    related_skills: [agent-eval-harness, incident-rollback]
---

# Prompt Debugger

When an agent misses, the reflex is to pile more words onto the prompt — which usually makes it worse. This skill replaces the reflex with differential diagnosis: reproduce the failure, localize it to one of four layers (instructions, context, tools, model), change exactly one variable, and prove the fix against the eval that caught the miss. The standard: every fix ships with a reproducible before-case and a passing after-run.

## When to Use

- A specific output is wrong, off-format, off-tone, or ignores an instruction — and you can point at it.
- An `agent-eval-harness` case fails and the fix isn't obvious.
- A previously working skill/prompt degraded after some change (model update, new context, edited instructions).
- Two skills or instruction sources fight each other and outputs flip-flop between styles.
- **Not for:** creating the eval or rubric (`agent-eval-harness`), or when the agent DID something harmful rather than SAID something wrong (`incident-rollback` — contain first, debug later).

## Quick Reference

| Layer | Symptom signature | Isolation test |
|---|---|---|
| Instructions | Follows the prompt literally but the prompt underspecifies; misses vary run to run | Run the same prompt in a clean session with NO extra context — still wrong → instructions |
| Context | Cites stale/irrelevant loaded material; correct in a clean session, wrong in the real one | Diff clean-session output vs. full-context output |
| Tools | Right plan, wrong data — tool errors swallowed, wrong file read, empty result treated as answer | Read the transcript's tool calls: check each call's args and raw result |
| Model | Instructions airtight, context clean, tools fine — still fails; or regressed on a model update | Same prompt+context on one tier up — passes → model capability/regression |

Diagnosis order when several layers look plausible: tools → context → instructions → model (cheapest-to-check first; model is the last suspect, not the first).

## Procedure

1. **Capture the failure verbatim** — save the exact prompt, loaded context (files/skills/memory in play), tool transcript, model + settings, and the bad output. Then write ONE sentence: expected X, got Y. If you can't write that sentence, you have a taste problem, not a bug — go define expected behavior in the eval first.
2. **Reproduce it** — re-run the captured setup. Reproduces → deterministic enough to debug. Doesn't → run 3 more times and note the failure rate; intermittent failures are usually context or model-variance, and any fix must be judged across multiple runs, not one lucky pass.
3. **Localize with the clean-session test** — run the same instruction in a fresh session with minimal context. Wrong in clean session → instructions or model. Right in clean, wrong in real → context or tools. This one test halves the search space; do it before touching anything.
4. **Interrogate the losing half** — instructions: hunt for underspecification (missing format/length/audience), buried constraints (key rule at line 90 of a 120-line prompt), and contradictions (skill says X, memory says Y). Context: hunt for stale facts (`memory-hygiene` material) and distractor content near the failure topic. Tools: replay each call — did it error, return empty, or return something the agent misread? Model: only after the other three are clean, test one tier up.
5. **Fix ONE variable** — make the single smallest change that addresses the diagnosis: rewrite one instruction, remove one stale context item, fix one tool call, or bump one tier. Write down what you changed and your prediction. Changing three things and seeing improvement teaches you nothing and leaves two landmines in place.
6. **Before/after eval** — re-run the captured failing case AND the full eval from `agent-eval-harness` (fixes love to break neighboring cases). Fixed + no regressions → done. Not fixed → revert the change fully, return to step 4 with the new evidence. Never stack a second change on an unproven first.
7. **Ship and record** — apply the fix to the real skill/prompt file, bump its version, and add the failing case to the eval so this bug can never return silently. If the root cause was a missing rule, consider a Pitfalls entry in the affected skill.

## Output Template

```
## Prompt debug: <task/skill> — <date>
Failure: expected <X>, got <Y> | Repro: <deterministic | n/5 runs>

Layer diagnosis:
- Clean-session test: <wrong in clean → instructions/model | right in clean → context/tools>
- Verdict: <layer> — evidence: <one line>

Fix applied (ONE variable): <exact change>
Prediction: <what should now happen>

| Run | Before | After |
|---|---|---|
| Captured failing case | FAIL | PASS |
| Full eval (n cases) | <a>/<n> | <b>/<n> — no regressions |

Shipped to: <file> (v<x.y.z>) | Case added to eval: yes
```

## Pitfalls

- **Shotgun prompting** — rewriting the whole prompt in frustration; it improves, but you don't know why, and two hidden problems ride along. Recovery: revert to the captured baseline, re-apply your ideas one at a time against the eval until you know which change carried the fix.
- **Fixing instructions when context is the culprit** — adding "IMPORTANT: ignore outdated info" instead of removing the stale fact. The patch decays; the rot remains. Recovery: the clean-session test in step 3 exists precisely to catch this — run it before editing anything, and route stale memory to `memory-hygiene`.
- **Tool blindness** — hours on prompt wording while the transcript shows a tool returned empty and the agent improvised an answer. Recovery: read the raw tool calls FIRST whenever the output contains specific facts; a wrong fact is a data-path bug until proven otherwise.
- **Judging an intermittent bug on one run** — the "fix" passes once; the failure was 2-in-5 all along. Recovery: match your sample size to the failure rate from step 2 — a 40% failure needs ~5 clean passes before you believe it.
- **Fix passes the case, breaks the suite** — the new instruction fixes case 2 and quietly kills case 4. Recovery: full-eval re-run is mandatory in step 6; on regression, revert and find a fix that satisfies both — a contradiction between cases means the SPEC needs a decision, so take it to the user.

## Verification

- [ ] Failure captured verbatim (prompt, context, tools, model, output) and reproduced before any change
- [ ] Clean-session test run and its verdict recorded
- [ ] Exactly one variable changed per fix attempt, with a written prediction
- [ ] Failing case now passes AND full eval shows no regressions (multiple runs if intermittent)
- [ ] Reverted cleanly on every failed fix attempt — no stacked unproven changes remain
- [ ] Fix shipped to the source file with version bump; failing case added to the eval

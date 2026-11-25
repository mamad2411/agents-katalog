---
name: harness-diagnose
description: >-
  When the agent keeps failing, attribute the failure to a harness layer and
  fix the environment before swapping models. Use for repeated failures,
  verification gaps, or Lesson 01 diagnostic loops.
---

# Harness Diagnose

## What this does for you

- **Fix harness first** — don't reach for a bigger model until you know the layer
- **Named failure modes** — task spec, context, environment, verification, state
- **Measurable gap** — track when the agent says "done" vs what actually passes

Strong models still fail in bad harnesses (Lesson 01). `harness-audit` scores overall health (0–100). This skill diagnoses **one concrete failure** and prescribes the smallest harness fix.

## Diagnostic rule

When something fails:

1. **Do not** change the model first
2. **Do** attribute the failure to one primary layer
3. **Do** fix that layer and re-run the same task
4. **Do** log the outcome — build a failure register over time

## Five diagnostic layers

Map every failure to exactly one primary layer (secondary layers optional):

| Layer | Symptom | Harness fix |
|-------|---------|-------------|
| **Task spec** | Agent built the wrong thing | Narrow feature_list entry, sprint contract, observable `user_visible_behavior` |
| **Context** | Agent violated "everyone knows" rules or edited the wrong folder | `AGENTS.md`, `docs/REPO_MAP.md` — see `harness-instructions` and `harness-repo-knowledge` |
| **Environment** | `pip install` / build / version hell | `init.sh`, lockfiles, `.env.example` — see `harness-environment` |
| **Verification** | Agent said done; tests never ran or only unit tests | `./init.sh`, Definition of Done, `harness-verification`, `harness-e2e` |
| **State** | Next session re-discovered everything | `progress.md`, handoff, feature_list evidence — see `harness-state` |

If the same layer fails twice in a row, that layer is your **bottleneck** — invest there before anywhere else.

## Diagnostic loop

```
Run task → Failure observed
  → Classify layer (one primary)
  → Apply smallest harness patch for that layer
  → Re-run SAME task (same model, same prompt class)
  → Pass? Log and continue : iterate (max 3 rounds before escalating)
```

## Verification gap measurement

Track across 5–10 tasks:

| Task | Agent claimed done? | Independent check passed? | Gap? |
|------|---------------------|---------------------------|------|
| … | yes/no | yes/no | yes/no |

**Verification gap** = claimed done but check failed. High gap → prioritize `harness-verification` + `harness-evaluator`, not model upgrades.

## Failure report template

```markdown
## Failure diagnosis: [task name]

**Observed:** [what actually broke]
**Agent claimed:** [what the agent said]
**Primary layer:** task spec | context | environment | verification | state
**Evidence:** [command output, log snippet, screenshot path]

**Harness patch applied:**
- [ ] File/command changed
- [ ] Re-run result: pass / fail

**Next if still failing:** [second-layer hypothesis]
```

Template: [templates/failure-diagnosis.md](../../templates/failure-diagnosis.md)

## Quick attribution guide

| If you hear… | Likely layer |
|--------------|--------------|
| "That's not what I asked for" | Task spec |
| "It used the wrong pattern/version" | Context |
| "Tests won't run / deps broken" | Environment |
| "It said done but nothing works" | Verification |
| "New session had no idea where we were" | State |

## Ablation (optional, Lesson 02)

To quantify a layer's marginal value on **your** project:

1. Fix model + task
2. Remove **one** subsystem (e.g. delete `AGENTS.md`, skip `init.sh`)
3. Measure success drop
4. Combine with failure logs — largest drop suggests highest ROI fix

Do not treat ablation alone as bottleneck proof; use it with real failure attribution.

## Anti-patterns

- "Let's try GPT/Claude/Opus instead" before checking verification commands
- Adding 20 lines to `AGENTS.md` for every failure without classifying layer
- Diagnosing "the model is bad" when `init.sh` fails on fresh checkout
- Fixing state when the real issue was no Definition of Done

## Related skills

- `harness-audit` — score all five subsystems (0–100)
- `harness-verification` — close verification-layer gaps
- `harness-evaluator` — close confidence-calibration gaps
- `harness-environment` — toolchain, env vars, services, init.sh health
- `harness-repo-knowledge` — repo map so agents find the right files
- `harness-scaffold` — bootstrap missing harness artifacts

## Course reference

- Lesson 01: Why capable agents still fail
- Lesson 02: Ablation and five subsystems
- Project 01: Prompt-only vs rules-first experiment

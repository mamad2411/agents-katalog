---
name: goal-driven-verifiable-success-criteria
description: Transform imperative tasks into verifiable goals. Define success criteria before implementing so the loop can self-terminate. Use for any non-trivial task, especially bug fixes and refactors.
category: engineering
version: 1.0.0
version_origin: extracted
tags: [tdd, verification, goal-setting, autonomous-loop]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/forrestchang/andrej-karpathy-skills.git
source_ref: main
source_commit: c9a44ae835fa2f5765a697216692705761a53f40
source_project: andrej-karpathy-skills
source_path: skills/karpathy-guidelines/SKILL.md
imported_at: 2026-04-18T08:26:22Z
---

# Goal-Driven Execution — Verifiable Success Criteria

**Define success criteria. Loop until verified.**

Karpathy: *"LLMs are exceptionally good at looping until they meet specific goals... Don't tell it what to do, give it success criteria and watch it go."*

## Transform rule
| Imperative | Verifiable goal |
|-----------|-----------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |
| "Make it faster" | "Baseline latency = Xms; target < Yms; bench before/after" |

## Multi-step plan template
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Each step must have an **independent, machine-checkable verification**.

## Example — Rate limiting
1. Add in-memory limit on one endpoint → *verify:* test 11 requests; #11 returns 429.
2. Extract to middleware → *verify:* same test on two endpoints; existing tests green.
3. Swap to Redis backend → *verify:* counter persists across restart; shared across two app instances.
4. Make rates configurable → *verify:* config file parses; per-endpoint rates enforced.

Each step is independently verifiable AND deployable.

## Why weak criteria fail
"Make it work" keeps requiring human clarification. "Test X passes" lets the loop self-terminate.

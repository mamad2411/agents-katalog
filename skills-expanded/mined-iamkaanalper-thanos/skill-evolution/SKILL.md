---
name: skill-evolution
description: Self-evolving skill system. Skills are scored after execution (0-100) on 5 dimensions. Score 90+ over 5 runs = crystallized (locked). Score below 30 = auto-repair attempted. Skills improve themselves through usage feedback. Grok-native adaptation.
when-to-use: When you want skills (or the compound system) to get better over time based on real usage, not just manual editing.
---

# Skill Evolution Skill

A Darwinian loop for skills: use → measure → evolve or crystallize.

## 5 Dimensions (scored 0-100 after each execution)
1. Correctness (did it achieve the stated goal without breaking things?)
2. Efficiency (tokens, time, steps, cost)
3. Clarity (how easy for future agents/humans to understand and follow)
4. Robustness (handles edge cases, errors, variation in input)
5. Leverage (how much it reduces future work or compounds other capabilities)

## The Loop
- Every time a skill is used (via hook or direct call), record outcome + scores.
- After N runs:
  - 90+ average across runs → mark as crystallized (lock it, treat as high-confidence primitive).
  - <30 average → trigger auto-repair (ask for or generate improved version, run through compound).
- Feedback is fed into compound evolution as "this skill pattern is maturing or needs work".

## Grok Integration
- Hooks can automatically score and record after skill use (on_run_completion style).
- Ties directly into our compound_analyzer + evolution + apply flow.
- Pre-flight for any new skill: "Will this be used enough times to benefit from evolution, or is it a one-off rule?"

## Production Contract
- Always record scores with evidence (not vibes).
- Crystallized skills get extra weight in preflight and agent prompts.
- Low-scoring skills are treated as technical debt until repaired.

This turns skills from static docs into living, improving capabilities — exactly the self-improvement spirit of the original system, adapted to our executable Grok primitives.
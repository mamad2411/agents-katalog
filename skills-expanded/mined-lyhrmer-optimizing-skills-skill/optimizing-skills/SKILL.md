---
name: optimizing-skills
description: Use when an existing skill needs systematic improvement, when measuring whether a skill change actually improved agent behavior, when comparing skill versions A/B, or when ad-hoc skill edits feel like guesswork. Distinct from writing-skills (creating new skills from scratch).
---

# Optimizing Skills

## Overview

Treat the skill as a model whose only weights are words. Every change passes a held-out validation gate; failed changes get reverted.

**Iron Law:** Editor ≠ Judge. Same context = same blindspot = inflated scores.

**Corollary:** Always grep judge-quoted text against source — LLM judges score "faithful citations" 9/10 without checking they exist.

**Anti-imagination rule:** Every round MUST anchor to ≥1 concrete past failure (operationalized by the Pre-Edit Gate below). No anchor → skip the round; self-iteration produces drift, not improvement.

**Recommended background:** `superpowers:writing-skills` (not required).

## When to Use

- Skill exists and works but feels unreliable
- Recent edit happened — want to verify it helped, not hurt
- Two competing skill versions, need to pick
- Agent behavior with the skill is inconsistent run-to-run

## When NOT to Use

- Brand-new skill from zero → use `writing-skills`
- Single-line typo / formatting fix → just edit
- Skill never deployed → no signal to optimize on; ship it first
- Cannot spawn independent subagent in current env → see fallback table

## Target Identity Gate

🛑 Before the Pre-Edit Gate, resolve **which exact artifact is authoritative**. A similar name or purpose is not identity evidence.

Write one target map per optimization round:

| Field | Required evidence |
|---|---|
| Requested skill | User wording + canonical `name` from its frontmatter |
| Edit target | Exact real path + whether it is user-owned, system-managed, plugin/cache-managed, or an installed copy |
| Source repository | Git root + `origin` URL, or `none` |
| Publication target | Repository URL supplied/confirmed by the user, or `none` |
| Authority | Why this copy is the source of truth rather than another similarly named copy |

Rules:

- Inspect every plausible candidate's frontmatter and provenance before choosing. Do not infer identity from semantic similarity alone.
- Treat system/plugin/cache paths and installed copies as deployment artifacts by default. If a corresponding user-owned source repository is provenance-matched, optimize that repository and synchronize the installed copy only after the change passes validation.
- If multiple candidates remain plausible, or an installed path cannot be mapped to a repository with evidence, ask the user **one direct identity question and stop**. Do not edit while waiting.
- Run separate optimization rounds for separate skills or repositories. Never copy one patch into two targets merely because their purposes overlap.
- Publishing is a downstream workflow after a change earns **Keep**; use the environment's repository publishing procedure and verify the remote again before push.

🔴 CHECKPOINT: canonical skill name, edit path, ownership, source remote, and publication target all agree. If any field conflicts, STOP.

## Pre-Edit Gate

🛑 Before editing ANY skill file, state these three lines. Missing any → do NOT edit yet:

1. **Anchor**: session/date + the concrete past failure being targeted
2. **Test prompts**: 2-3 prompts that would expose that failure
3. **Baseline**: target skill + its weakest dim / behavior gap

Backups, "obvious" fixes, and tiny patches do NOT satisfy this gate. The discipline is reactive if stated only after editing — front-load it here.

## Core Loop

```
Phase 0    Resolve the Target Identity Gate; one authoritative skill + repository per round
           🔴 CHECKPOINT: name/path/ownership/remote mapping is evidence-backed
   ▼
           Create `skill-opt/<name>` branch (no git? snapshot file per failure-modes.md)
   ▼
Phase 0.5  Write 2-3 test prompts targeting REAL failure modes
           🔴 CHECKPOINT: prompts cover live pain, not synthetic edge cases
   ▼
Phase 1    Baseline — score 9 dims + run test prompts; **scan history for clusters of failures this skill should have caught** (≥2 cases at same root = strong signal)
           🔴 CHECKPOINT: baseline matches your felt sense of the weakness
   ▼
Phase 2    Loop:
             pick lowest dim → ONE change → git commit
             spawn ≥2 independent judges (fresh context, ideally cross-model)
             re-score + re-run prompts + verify citations against source
             score↑ AND behavior↑ AND citations verbatim → keep
             else → `git revert` (NEVER `git reset --hard`)
             two consecutive rounds gain <2 pts → STOP
   ▼
Phase 3    Report using Output Format below (A-G); skip empty sections
```

## Reference Files

| File | Read when |
|---|---|
| [`triage.md`](triage.md) | many skills, unsure which to optimize (recent-history scan + ranked candidates) |
| [`rubric.md`](rubric.md) | scoring (9-dim weighted + dim 8 strength tiers + gap classification) |
| [`failure-modes.md`](failure-modes.md) | blocked (if-then-fallback for env / judge / citation issues) |
| [`output-format.md`](output-format.md) | writing the round report (A-G template) |

## Red Flags — STOP and Restart

- 🛑 Editing before stating the Pre-Edit Gate → stop, revert to backup, restate gate
- 🛑 Editing before the Target Identity Gate resolves to one authoritative artifact → stop; restore the touched target, map candidates, restart
- 🛑 Same agent edits AND scores → Iron Law violation
- 🛑 Score rose but test-prompt behavior unchanged → Goodhart drift
- 🛑 Multiple dims changed in one commit → can't attribute
- 🛑 `git reset --hard` instead of `git revert`

**All of these mean: stop and revert. Identity failures restart from Phase 0; all others restart from Phase 0.5.** (More red flags in `failure-modes.md`.)

## Cross-Tool

Tool-agnostic primitives only (subagent, git, judge). See README for install paths.

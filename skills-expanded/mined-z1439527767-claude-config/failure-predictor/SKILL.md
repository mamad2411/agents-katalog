---
name: failure-predictor
version: 1.0.0
description: Pre-mortem risk predictor. Imagines failure has ALREADY happened, then works backwards to find causes. Proven to identify 30% more risks than "what could go wrong." Triggers on: high-risk decisions, architecture changes, deployments, irreversible actions.
---

# Failure Predictor — Pre-Mortem Risk Analysis

> **"假设已经失败了。为什么？往前推。"**

## Why Pre-Mortem

Asking "what could go wrong?" produces shallow answers. Humans are optimistic by default.

Pre-mortem flips this: "Imagine we launched and it FAILED. WHY?" This triggers prospective hindsight — psychologically proven to surface 30% more risks than forward-looking risk analysis.

## Trigger

Use before:
1. Architecture decisions (irreversible once code is written)
2. Deployments (downtime = real cost)
3. Data migrations (cannot undo)
4. Security changes (cannot afford to get wrong)
5. Major refactors (cascade risk)

## Process

### Step 1: Set the Scene
"It's [timeframe later]. We did [the action]. It FAILED. [Specific bad outcome]."

Be concrete. Not "it didn't work well." Say: "3 hours of downtime. 50 users lost data. Rollback failed."

### Step 2: Work Backwards
Given the failure, what MUST have gone wrong? List causes in reverse chronological order:

```
FAILURE: database migration corrupted 10% of user records
  ← Rollback script had an untested edge case
    ← We tested migration on staging but staging has different data shape
      ← Nobody checked if staging schema matches production
        ← Assumption: staging == production. It wasn't.
```

### Step 3: Score Each Cause

| Cause | Likelihood | Impact | Mitigation |
|-------|-----------|--------|------------|
| Staging != production schema | High | Critical | Schema diff check as pre-migration step |
| Rollback script untested | Medium | Critical | Dry-run rollback on staging first |
| No backup before migration | Low | Catastrophic | Snapshot before any migration |

### Step 4: Kill/Prevent/Detect
For each cause above threshold:
- **Kill**: Remove the risk entirely (don't do the migration? do it differently?)
- **Prevent**: Add a gate (schema diff check)
- **Detect**: Add monitoring (alert if record count changes unexpectedly)

### Step 5: Go / No-Go
Based on analysis: proceed, proceed with fixes, or abort.

## Anti-Patterns

- **Shallow pre-mortem**: "Users unhappy" — too vague. "30% of users can't log in because auth token format changed"
- **Blame-oriented**: Focus on what failed, not who failed
- **Paralysis**: Pre-mortem finds risks, doesn't forbid action. Every action has risks.

## Integration
- **thinking-dimensions**: Pre-mortem = adversarial lens (D5) amplified
- **second-brain**: Brain 2 verifies pre-mortem completeness
- **precommit-pipeline**: Pre-mortem gate before irreversible commits
- **memory-lora**: Pre-mortems stored for cross-project risk patterns

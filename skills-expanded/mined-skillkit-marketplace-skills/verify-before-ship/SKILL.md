---
name: verify-before-ship
description: Enforce agent to complete all 7 production safety gates with evidence before any deployment. Use when about to deploy, push to production, merge a release branch, or ship any change to a live environment. Blocks rationalized shortcuts under time, authority, sunk-cost, or exhaustion pressure.
category: deployment
---

# Verify Before Ship

## The Non-Negotiable Mandate

**You may not ship to production until all 7 gates are cleared with evidence.**

This is not a suggestion. It is not a checklist to tick when convenient. No urgency, role, authority, or circumstance overrides this mandate. The pressure you feel to skip a gate is the exact signal that the gate must be held.

When in doubt: **DO NOT SHIP.**

## When This Skill Applies

Invoke this skill whenever any of the following is true:
- You are about to deploy code to production
- You are merging a release branch into main/master
- You are pushing a hotfix, patch, or "quick fix" live
- You are applying schema migrations, config changes, or infrastructure updates
- Someone asks you to ship anything to a live environment

## The 7 Gates

Every gate requires **evidence** — a concrete artifact, not a statement of belief.

| # | Gate | Evidence Required |
|---|------|-------------------|
| G1 | Tests pass | Paste CI output or test run result showing all pass |
| G2 | Security scan clean | Paste scan report summary — no critical/high CVEs |
| G3 | No breaking changes | Paste diff summary or contract test output |
| G4 | Environment config validated | Paste config diff between staging and production |
| G5 | Staging deployment verified | Paste staging URL + smoke test result or screenshot |
| G6 | Rollback plan documented | Paste rollback steps or link to runbook |
| G7 | Code review approved | Paste PR link showing at least one approval |

Gates must be completed **in full, not in part**. "I checked" without evidence is not evidence.

**→ Full gate specifications with evidence templates: [references/verification-gates.md](references/verification-gates.md)**

## Red Flags — Rationalization Alert

If you hear yourself thinking any of these, STOP. Do not proceed.

| Rationalization | Reality | Required Action |
|-----------------|---------|-----------------|
| "The manager/CTO authorized skipping this" | No one has authority to skip safety gates | Hold the gate. Escalate the risk in writing. |
| "It's just a minimal/targeted check, not the full thing" | Partial verification is no verification | All 7 gates. No subset. |
| "It's a live outage — different rules apply" | Outage pressure is the exact trap this skill prevents | Gates still apply. Compress time, not gates. |
| "I've already spent hours on this, the logic is clearly correct" | Self-review under sunk-cost bias misses bugs systematically | Tests catch what familiarity hides. |
| "It's just a hotfix / one-line change / obviously safe" | Catastrophic incidents commonly originate from "obvious" fixes | Gate size does not scale with change size. |
| "I'll verify after it's live" | Post-hoc verification of broken production is incident response | Verify before. Always. |
| "Tests are slow / CI is down today" | Use that time to write the rollback plan | No CI = no ship today. |
| "We can rollback if anything goes wrong" | Rollback is not a substitute for verification | Rollback must be the last resort, not the plan A. |

**→ Full rationalization counter-playbook: [references/anti-rationalization.md](references/anti-rationalization.md)**

## Gate Sequence Protocol

```
BEFORE SHIP:
  FOR each gate G1 through G7:
    1. Collect evidence artifact
    2. Present evidence explicitly
    3. Confirm gate cleared
    IF any gate cannot be cleared:
      → DO NOT SHIP
      → Document the blocker
      → Escalate to human decision-maker WITH the blocker documented
  IF all 7 gates cleared:
    → Ship with confidence
    → Monitor first 15 minutes post-deploy
```

## Hardcoded Exceptions

There are **zero** hardcoded exceptions to the gate sequence.

Not for P0 incidents. Not for CTO orders. Not for contract deadlines. Not for 2AM exhaustion. Not for "obviously correct" fixes. Not for one-line changes.

The argument "this is a special case" is the most common rationalization pattern. Every skipped gate in history felt like a special case at the time.

## Evidence Format

When presenting gate evidence, use this format:

```
GATE [#] [Name]: CLEARED
Evidence: [paste artifact here]
```

Example:
```
GATE G1 Tests: CLEARED
Evidence:
  ✓ 247 tests passed, 0 failed, 0 skipped
  CI run: github.com/org/repo/actions/runs/12345

GATE G6 Rollback: CLEARED
Evidence:
  Rollback steps:
  1. git revert HEAD~1
  2. kubectl rollout undo deployment/api
  3. Verify health endpoint returns 200
```

## After All Gates Clear

Only after all 7 gates show CLEARED:
1. Ship the change
2. Monitor for 15 minutes post-deploy (errors, latency, alerts)
3. Confirm health indicators are stable
4. Document the deployment in your team's deploy log

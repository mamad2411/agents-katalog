<!-- Vendored from Superpowers (c) 2025 Jesse Vincent, github.com/obra/superpowers, v5.1.0 @ f2cbfbe, MIT. Adapted for consensus-mcp. -->
---
name: consensus-requesting-code-review
description: "Consensus-adapted: Use when completing tasks, implementing major features, or before merging to verify work meets requirements - dispatches a cross-family consensus Workflow B panel, not a single-Claude reviewer."
---

# Requesting Code Review

> Consensus has precedence at decision gates (see the consensus bootstrap / consensus-workflow).

Dispatch a **consensus Workflow B cross-family review panel** to catch issues before they cascade. The review is the sealed cross-family audit - NOT a single-Claude reviewer-subagent pass. Cross-family reviewers get precisely crafted context (the git-range diff + requirements), never your session's history. This keeps the review focused on the work product and produces an independent, sealed verdict.

**Core principle:** Review early, review often - and the review is a sealed cross-family panel, not one Claude.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Request

**1. Get git SHAs (diff preparation - keep this):**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

Prepare the git-range diff for the reviewers. The diff `BASE_SHA..HEAD_SHA` plus the plan/requirements is exactly the context the cross-family panel needs.

**2. Invoke consensus Workflow B - dispatch cross-family reviewers:**

> **Invoke consensus Workflow B: dispatch every enabled cross-family reviewer; the sealed cross-family audit IS the review, not a single-Claude pass.**

- Always dispatch `reviewer_dispatch_codex` (the cross-family anchor).
- Dispatch every enabled reviewer (minimum two independent providers; see consensus-workflow).
- Each reviewer receives: a brief description of what you built, the plan/requirements it should satisfy, and the `BASE_SHA..HEAD_SHA` diff. They do NOT receive your session history.
- The reviewers' findings are sealed (post-seal) into the consensus review record. That sealed cross-family audit is the review of record.

**Context to provide each reviewer:**
- `{DESCRIPTION}` - Brief summary of what you built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit

**3. Act on the sealed panel feedback:**
- Read the SEALED cross-family findings (see consensus:receiving-code-review for how to weigh them)
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Dismiss only with empirical evidence (grep the cited content first), recorded per consensus:receiving-code-review

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request a consensus Workflow B cross-family review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Invoke Workflow B with every enabled independent reviewer]
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types
  PLAN_OR_REQUIREMENTS: Task 2 from docs/consensus/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[Cross-family panel seals findings]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators (codex + gemini agree)
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed once Important addressed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each task or at natural checkpoints
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Substitute a single-Claude pass for the cross-family panel
- Ignore Critical issues
- Proceed with unfixed Important issues
- Dismiss a sealed panel finding without empirical evidence

**If the panel is wrong:**
- Push back with technical reasoning (see consensus:receiving-code-review)
- Show code/tests that prove it works - grep the cited content first
- Record the dismissal with the empirical evidence

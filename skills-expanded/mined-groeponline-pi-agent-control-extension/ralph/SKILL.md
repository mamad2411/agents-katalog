---
name: ralph
description: "Review-Approve Loop Protocol for Hardening - iterative Plan → Critique → Revise → Approve cycle to ensure plans are hardened through adversarial review before execution. Examples: \"ralph\", \"consensus\", \"ralplan\", \"review my plan\", \"hardening review\""
---

# Ralph (Review-Approve Loop Protocol for Hardening)

The Ralph workflow runs an iterative Plan → Critique → Revise → Approve cycle. It ensures plans are hardened through adversarial review before execution begins.

## When to Use

- User wants a plan reviewed thoroughly before implementation
- High-stakes changes where mistakes are costly
- User says "ralph", "consensus", "ralplan"
- Complex architectural decisions that need validation
- User wants a second opinion on their approach

## When NOT to Use

- Simple tasks that don't need a plan
- User wants to move fast (use Autopilot instead)
- Pure implementation tasks (plan already exists and is approved)

## Pipeline

```
User Request / Draft Plan
    │
    ▼
┌─────────────────────┐
│  1. PLAN             │  skill("agent-planner")
│  Create/refine plan  │  → Structured work plan
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. ARCHITECT REVIEW │  skill("agent-architect")
│  Technical           │  → Architecture assessment
│  feasibility         │  → Dependency analysis
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. CRITIC REVIEW    │  skill("agent-critic")
│  Adversarial         │  → Challenge assumptions
│  challenge           │  → Find weak spots
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  4. SECURITY REVIEW  │  skill("agent-security-reviewer")  [if applicable]
│  Security            │  → OWASP check
│  implications        │  → Secrets, auth, injection
└────────┬────────────┘
         │
         ▼
    ┌────┴────┐
    │ ISSUES? │
    └────┬────┘
     YES │        NO
         ▼         ▼
    ┌─────────┐  ┌──────────┐
    │ REVISE  │  │ APPROVED │
    │ Go to 1 │  │ Done     │
    └─────────┘  └──────────┘
```

## Execution Protocol

### Step 1: Plan

If no plan exists:
1. Load `skill("agent-planner")` protocol
2. Interview user (max 3 rounds)
3. Create structured work plan at `~/.omc/plans/{name}.md`

If plan already exists:
1. Read the plan from `~/.omc/plans/{name}.md` or from user's input
2. Proceed to review

### Step 2: Architect Review

Perform architectural analysis (READ-ONLY):

1. Evaluate technical feasibility
2. Check for dependency conflicts
3. Assess scalability implications
4. Identify integration risks
5. Score: PASS / CONCERNS / BLOCK

Use `Task(subagent_type="explore")` to investigate the codebase if needed.

**Findings format**:
```
### Architect Review
- Feasibility: {PASS/CONCERNS/BLOCK}
- Dependencies: {list of dependencies affected}
- Risks: {identified risks}
- Recommendations: {specific suggestions}
```

### Step 3: Critic Review

Apply adversarial thinking (READ-ONLY):

1. Challenge every assumption in the plan
2. Ask "what could go wrong?" for each step
3. Check for missing error handling
4. Evaluate if the plan is overengineered or underengineered
5. Score: APPROVE / REVISE / REJECT

**Findings format**:
```
### Critic Review
- Verdict: {APPROVE/REVISE/REJECT}
- Assumptions challenged:
  - {assumption}: {valid/invalid} — {reasoning}
- Missing items: {what the plan forgot}
- Overengineering: {what could be simpler}
- Risks: {what could go wrong}
```

### Step 4: Security Review (If Applicable)

Skip if the plan doesn't involve: auth, user input, APIs, data storage, network, or secrets.

If applicable:
1. Load `skill("agent-security-reviewer")` mentally
2. Check for: injection, auth bypass, secrets exposure, CSRF/XSS, insecure defaults
3. Score: PASS / CONCERNS / BLOCK

**Findings format**:
```
### Security Review
- Verdict: {PASS/CONCERNS/BLOCK}
- Issues: {list with severity}
- Recommendations: {specific mitigations}
```

### Step 5: Consensus Decision

Combine all review scores:

| Scenario | Action |
|----------|--------|
| All PASS/APPROVE | Plan is approved — present to user |
| Any CONCERNS | Revise plan addressing concerns, re-review |
| Any BLOCK/REJECT | Major revision needed — return to Step 1 |

Maximum iterations: 3 review cycles. If not converging, present the best version with documented caveats.

### Step 6: Revision (If Needed)

When revising:
1. List all issues from all reviewers
2. Address each issue specifically
3. Mark which issues were resolved and how
4. Re-run only the reviews that raised concerns (not all)

## Scope Control

- Ralph is for PLANNING only — it does NOT execute the plan
- After approval, hand off to Autopilot or Executor for implementation
- Keep review focused — don't let it expand the plan's scope
- Maximum plan size for Ralph: 20 items

## Output Format

```
## Ralph Review Summary

### Plan
- Name: {plan name}
- Version: {iteration count}
- File: ~/.omc/plans/{name}.md

### Review Results
| Reviewer | Verdict | Key Finding |
|----------|---------|-------------|
| Architect | {PASS/CONCERNS/BLOCK} | {one-line summary} |
| Critic | {APPROVE/REVISE/REJECT} | {one-line summary} |
| Security | {PASS/CONCERNS/BLOCK/N/A} | {one-line summary} |

### Iterations
- Round 1: {summary of findings}
- Round 2: {what was revised} (if applicable)
- Round 3: {final adjustments} (if applicable)

### Final Verdict: {APPROVED / APPROVED WITH CAVEATS / NOT APPROVED}

### Caveats (if any)
- {Known limitation or risk that was accepted}

### Next Step
- {Recommended: hand off to Autopilot / Executor}
```

## Failure Modes To Avoid

1. **Rubber-stamping**: Don't approve weak plans to save time — be genuinely critical
2. **Infinite loops**: Max 3 review cycles — present best version with caveats
3. **Scope expansion**: Reviews should improve the plan, not expand it
4. **Ignoring security**: Always at least consider if security review is needed
5. **Not saving artifacts**: Always save revised plans to `~/.omc/plans`

## Final Checklist

- [ ] Plan exists (created or provided)
- [ ] Architect review completed
- [ ] Critic review completed
- [ ] Security review considered (applied if relevant)
- [ ] All raised issues addressed or documented as caveats
- [ ] Final plan saved to ~/.omc/plans/
- [ ] Clear verdict presented
- [ ] Next step recommendation provided

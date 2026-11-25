---
name: technical-rfc
description: >
  Write technical RFCs and design documents — problem framing, alternatives
  analysis, decision rationale, implementation plan, and review process.
  TRIGGER when: user says /technical-rfc, needs to write a design doc,
  technical proposal, or RFC for an engineering decision.
argument-hint: "[problem or technical decision to document]"
user-invocable: true
---

# Technical RFC

You are a senior engineer. Help write a clear, thorough technical RFC that enables informed decision-making and alignment across teams.

## Process

### Step 1: Frame the Problem

| Section | Content |
|---------|---------|
| Title | Descriptive name (not the solution, the problem) |
| Author(s) | Names and roles |
| Status | Draft → In Review → Accepted / Rejected / Superseded |
| Created | Date |
| Reviewers | Required and optional reviewers |

**Problem statement:**
> We need to [solve problem] because [evidence/impact]. The current approach [limitation]. This affects [who/what] and costs us [quantified impact].

### Step 2: Establish Context

| Element | Details |
|---------|---------|
| Background | What led to this problem? Prior decisions? |
| Constraints | Timeline, budget, team, tech stack, compliance |
| Requirements | Must-have vs nice-to-have capabilities |
| Non-goals | What this RFC deliberately does NOT address |
| Dependencies | Systems, teams, or decisions this depends on |

### Step 3: Propose Solutions

For each alternative (minimum 3):

| Criterion | Option A | Option B | Option C (do nothing) |
|-----------|----------|----------|----------------------|
| Description | [approach] | [approach] | [status quo] |
| Complexity | H/M/L | H/M/L | — |
| Timeline | X weeks | X weeks | — |
| Scalability | [assessment] | [assessment] | [assessment] |
| Maintenance | [assessment] | [assessment] | [assessment] |
| Risk | [key risks] | [key risks] | [key risks] |
| Cost | [estimate] | [estimate] | [ongoing cost] |

**Always include "do nothing" as a baseline** — if the cost of inaction is low, maybe you shouldn't act.

### Step 4: Make a Recommendation

```markdown
## Recommendation

We recommend **Option [X]** because:
1. [Primary reason with evidence]
2. [Secondary reason]
3. [Third reason]

We considered but rejected Option [Y] because [specific reason].

### Tradeoffs we are accepting
- [Tradeoff 1 and why it's acceptable]
- [Tradeoff 2 and why it's acceptable]
```

### Step 5: Detail the Implementation

| Phase | Work | Duration | Dependencies |
|-------|------|----------|-------------|
| Phase 1 | [Minimal viable implementation] | X weeks | [deps] |
| Phase 2 | [Full feature set] | X weeks | Phase 1 |
| Phase 3 | [Migration/cleanup] | X weeks | Phase 2 |

Include:
- Data model changes (schema, migrations)
- API changes (new endpoints, breaking changes)
- Infrastructure needs (new services, resources)
- Rollout strategy (feature flags, gradual rollout)
- Rollback plan (how to undo if it fails)
- Monitoring (how to know if it's working)

### Step 6: Address Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | [Unresolved question] | [name] | Open |
| 2 | [Question] | [name] | Resolved: [answer] |

## RFC Template

```markdown
# RFC: [Title]

**Author:** [name] | **Status:** Draft | **Created:** [date]
**Reviewers:** [names]

## Problem
[2-3 paragraphs: what's wrong, who's affected, evidence]

## Context
[Background, constraints, requirements, non-goals]

## Options Considered
### Option A: [Name]
[Description, pros, cons]
### Option B: [Name]
[Description, pros, cons]
### Option C: Do Nothing
[Description, ongoing cost]

## Recommendation
[Which option and why, tradeoffs accepted]

## Implementation Plan
[Phased approach with timeline]

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|

## Open Questions
[Numbered list]

## References
[Links to related docs, prior art, data]
```

## Quality Checklist

- [ ] Problem is clearly stated with evidence
- [ ] At least 3 options considered (including "do nothing")
- [ ] Recommendation has explicit rationale
- [ ] Tradeoffs are acknowledged, not hidden
- [ ] Implementation plan is phased with rollback
- [ ] Open questions have owners
- [ ] Appropriate reviewers identified
- [ ] Non-goals are stated to prevent scope creep

## Edge Cases

- For urgent decisions, write a lightweight RFC (problem + recommendation + risks only)
- For reversible decisions, bias toward action over lengthy deliberation
- If consensus can't be reached, escalate to a named decision-maker
- For cross-team RFCs, ensure all affected teams are reviewers
- For security-sensitive proposals, include security review as a gate

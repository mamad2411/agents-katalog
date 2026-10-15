---
name: subagent-workflow
description: Use when Codex sub-agents should be applied in a disciplined way for analysis, implementation, or review. Trigger when a task is large enough to benefit from role-split work but still needs one main agent to own integration.
---

# Subagent Workflow

Use sub-agents only when work naturally divides into roles and the main agent can still integrate the result safely.

Stay local first until scope, affected paths, and validation are clear enough that delegation will reduce risk instead of creating guesswork.

Different files do not automatically make parallelism safe. Split work only when the lanes are behaviorally independent or joined by an agreed interface.

This skill is about staffing and ownership, not about replacing the spec, planning, issue, or review workflows themselves.

## Good candidates

- analysis -> implementation -> independent review
- documentation research -> design proposal -> implementation
- large refactors with clearly separated file ownership
- implementation plus separate regression checks or docs updates

## Avoid for

- one small fix
- overlapping write scopes
- unresolved product direction
- work that depends on continuous local reasoning across every step

## Standard roles

### Main agent

- owns the plan and routing
- decides whether delegation is justified
- assigns write ownership and review boundaries
- integrates results
- performs final verification

### Analysis

- locate causes
- list affected files
- identify risks
- gather evidence for the main agent

### Implementation

- change only approved files
- report exact edits
- report validation done

### Review / verification

- stay read-only and independent
- look for regressions
- identify missing tests
- challenge completion claims with evidence

### Writer / ops when relevant

- update docs, notes, playbooks, or run procedures

## Guardrails

1. Prefer the lightest execution mode that preserves quality: local first, then bounded delegation, then small team composition.
2. The main agent decides the plan first.
3. Do not let two sub-agents edit the same files.
4. Different files do not automatically make parallel work safe; shared behavior and dependency chains still matter.
5. Delegation does not widen authority or bypass protected paths.
6. The main agent integrates and validates.
7. Use sub-agents sparingly; speed matters only when coordination overhead stays low.

## Resources

- See `references/subagent-patterns.md` for recommended split patterns.
- Use `planning-workflow` to decide the task breakdown first and `review-workflow` to define what a review should actually check.

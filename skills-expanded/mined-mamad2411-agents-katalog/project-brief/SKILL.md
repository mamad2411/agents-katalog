---
name: project-brief
description: "Convert a technical spec into a PM/CTO-readable executive summary. Simplify technical details, focus on business value."
allowed-tools: Read, Grep, Glob, Write, Agent
---

# Project Brief

## Trigger

- Keywords: executive summary, project brief, PM summary, CTO summary, project-brief

## When NOT to Use

- First-principles briefing (use `/fp-brief`)
- Technical spec writing (use `/tech-spec`)
- Document review (use `/codex-review-doc`)

## Agent Dispatch

```
Agent({
  description: "Convert technical spec into PM/CTO executive summary",
  subagent_type: "brief-writer",
  prompt: `Convert the following tech spec into a PM/CTO-readable executive summary.
Follow the conversion rules and execution flow defined in this skill.`
})
```

### Input

```
$ARGUMENTS
```

## Conversion Rules

| Tech Spec Section | PM/CTO Summary Treatment |
|-------------------|--------------------------|
| Trust boundary diagram | Simplify to 3-layer arch |
| Code analysis | Remove |
| Reusable modules | Remove |
| System architecture | Keep (simplified) |
| Implementation roadmap | Keep |
| Key design decisions | Remove |
| Alternative comparison | Keep |
| Risks & mitigations | Keep |
| Timeline | Keep |
| Immediate actions | Simplify to decision points |

## Execution Flow

### Step 1: Read Technical Spec

- Read the specified tech spec file
- Identify the core value proposition

### Step 2: Extract Key Information

- Project overview: one sentence on what, why, and value
- Current state vs target comparison
- Solution evaluation (keep pros/cons comparison)
- Milestone timeline
- Risk summary
- Resource requirements

### Step 3: Simplify Technical Details

- Remove code snippets
- Remove internal module names
- Remove technical implementation details
- Keep business logic descriptions

### Step 4: Produce Executive Summary

## Output

```markdown
# [Project Name] Executive Summary

## Project Overview
> One sentence: what, why, and value

## Current State vs Target
| Dimension | Current | Target |
|-----------|---------|--------|

## Solution Evaluation
| Solution | Pros | Cons | Recommendation |
|----------|------|------|----------------|

## Architecture Overview
(Simplified system diagram, 3 layers max)

## Milestones
| Week | Deliverable | Dependencies |
|------|-------------|--------------|

## Risk Summary
| Risk | Impact Level | Mitigation |
|------|-------------|------------|

## Resource Requirements
- **Headcount**:
- **Timeline**:
- **External Dependencies**:

## Decision Points
> Items requiring PM/CTO decision
- [ ] Decision 1:
- [ ] Decision 2:
```

## Save

By default, save to the same directory as the original file with a `-brief` suffix.
Example: `docs/features/xxx/architecture.md` -> `docs/features/xxx/architecture-brief.md`

If `$ARGUMENTS` contains `--output <path>`, save to the specified location.

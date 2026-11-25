---
name: brief-starter
description: Use when starting a new product brief, project kickoff, or "start a brief for X". Auto-gathers relevant context from past projects before writing begins.
---

Auto-gather all relevant context before writing a product brief.

**Before starting:** Read `gotchas.md` and `runs.log` in this skill folder.

## Instructions

Given a project topic or problem statement:

1. Read `projects/INDEX.md` to find related projects by systems and domains.
2. Read truths.md, decisions.md, CONTEXT.md from the top 3-5 related projects.
3. Scan `reference-docs/` for relevant research or customer feedback.
4. If `data-science/` exists at the repo root (the DS add-on is enabled), check `data-science/INDEX.md` for relevant analyses. If not, skip this step.
5. Read `product/overview.md` for current product context.
6. Read `product/review-taste.md` for leadership review patterns.
7. Output a Brief Starter Kit:

```
## Brief Starter Kit: [Project Topic]

### Learnings from Related Projects
- [project]: [constraint, decision, or pattern]

### Customer/User Signal
- [source]: [relevant feedback]

### System Constraints
- [from truths.md]: [constraint]

### Data Insights
- [from DS analysis]: [finding]

### Leadership Review Patterns
- [from review-taste.md]: [what they'll push on]
```

8. Keep each section to 3-5 bullets max.
9. Ask: "Ready to start the brief, or want me to dig deeper on any of these?"

## Post-Run
Append to `runs.log`. If new failure patterns discovered, add to `gotchas.md`.

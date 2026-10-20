---
name: marketing-sync
description: >
  Synchronize product state with marketing strategy. Use after sprints 
  ship, when user feedback arrives, or when the marketing-context needs 
  updating. Also use when the user says "sync marketing", "update 
  positioning", "what should we communicate", "user feedback review",
  "marketing brief", or "prepare marketing for this sprint".
  This skill bridges the PM (technical) and marketing (market) directions.
---

# Marketing Sync

You bridge the gap between what's built and how it's communicated.
You keep marketing-context.md in sync with project-state.md and 
translate technical progress into marketing opportunities.

## Mode 1 — Post-sprint sync

After a sprint ships, update the marketing side:

1. Read `briefs/project-state.md` (what changed technically)
2. Read `briefs/marketing-context.md` (current positioning)
3. Read the sprint retrospective

For each user-facing change:
- Does it affect the landing page? (new feature, pricing change, 
  new capability)
- Does it affect the positioning? (new differentiator, new audience)
- Does it need a changelog? → invoke /changelog
- Does it need a social post? → write one in content/social/

Update `briefs/marketing-context.md` if positioning shifted.

## Mode 2 — User feedback processing

When user feedback arrives:

1. Read `briefs/user-feedback.md` (or the raw feedback source)
2. Classify each piece:
   - **Feature request** → does it align with positioning? Flag PM
   - **Bug report** → already in backlog? Note for communication
   - **Positive feedback** → capture for social proof / testimonials
   - **Churn signal** → flag PM as urgent, propose retention response
   - **Confusion** → documentation or UX issue, flag for next sprint

3. Update `briefs/user-feedback.md` with structured analysis
4. Write a summary for the PM in `briefs/feedback-summary.md`

## Mode 3 — Pre-sprint marketing input

Before a sprint starts, provide marketing perspective:

1. Read the backlog
2. Read recent user feedback
3. Read marketing-context.md

Propose to the PM:
- Which backlog items have the highest user demand
- Which items would improve positioning/differentiation
- Which items address churn risks
- What the marketing sprint should cover in parallel

Write recommendations in `briefs/marketing-directive.md`.

## Mode 4 — Marketing context generation

First time setup or major refresh:

1. Read CLAUDE.md (product vision and stack)
2. Read the landing page source (i18n files, content)
3. Read pricing if it exists
4. Read any existing user feedback

Generate `briefs/marketing-context.md`:

```markdown
# Marketing Context

## Product
[What it is, who it's for, what problem it solves]

## Positioning
[How we differentiate from alternatives]

## Audience segments
[Primary and secondary, their needs, their language]

## Tone of voice
[How we sound — examples of good and bad]

## Key messages
[3-5 core messages we repeat consistently]

## Competitive landscape
[Main alternatives, our advantages, their advantages]

## Metrics that matter
[What we track — signups, activation, retention, etc.]

## Current campaigns / initiatives
[What's active right now]
```

## Rules

- Always check what's actually built before marketing it
- User feedback is evidence, not noise — treat it seriously
- Positioning changes are strategic decisions — log them in decisions-log.md
- Never promise features in marketing that aren't shipped
- The PM has final say on technical priority, you have final say on messaging
---
name: prd-writing
description: "Write product requirement documents that engineers want to read and can actually build from. Covers structure, scope discipline, and the balance between clarity and over-specification. Use when writing PRDs, reviewing spec quality, or when engineering keeps asking clarifying questions."
---

# PRD Writing

Write PRDs that communicate intent, scope, and constraints without over-specifying implementation.

## How to use

- `/prd-writing` Apply PRD constraints to this conversation.
- `/prd-writing <feature>` Draft or review a PRD for the described feature.

## Constraints

### Problem First
- MUST start with the problem, never the solution
- Problem statement MUST be understandable by someone who just joined the team in under 60 seconds
- MUST include user evidence (data, quotes, support tickets) not just PM intuition
- NEVER jump to features without establishing why this matters

### Structure
- One-pager format for smaller features: problem, proposed solution, success metrics, scope boundaries, open questions
- Full PRD for larger initiatives: background, problem with evidence, goals, user stories, requirements, scope in/out, design considerations, rollout plan, risks
- Apply the "so what" test to every section: if removing it wouldn't confuse the engineer, cut it
- NEVER exceed 3 pages unless the initiative genuinely requires it. Length is not thoroughness.

### Scope Discipline
- MUST include an explicit "out of scope" section
- SHOULD answer "is this essential for v1?" for every requirement
- MUST flag scope creep when requirements expand beyond the original problem
- NEVER let scope grow without re-evaluating timeline and resources

### Success Metrics
- MUST define 1-3 concrete, measurable outcomes
- Each metric MUST specify: what you'll measure, how, target, and evaluation timeline
- "Improve user experience" is not a metric. "Reduce task completion time by 20%" is.
- NEVER ship without knowing how you'll measure whether it worked

### Engineering Empathy
- Define what, not how. NEVER prescribe implementation details.
- MUST respect the reader's time — engineers are busy
- SHOULD surface edge cases, failure states, and unusual inputs
- MUST keep the document updated as scope evolves. PRDs are living documents.

### Anti-Patterns
- The Novel: 15-page PRDs nobody reads past page 2
- Solution-first: jumping to features without the problem
- Implementation prescription: telling engineers which API to use
- The Static Artifact: writing once and never updating as scope changes
- Vague metrics that can't fail ("make it better")

---
name: brainstorm-to-issues
description: Interactive brainstorming session that refines an idea into a PRD and breaks it into GitHub issues labeled ai-ready. Use when user wants to brainstorm, has an idea to discuss, or says "brainstorm".
---

# Brainstorm to Issues

Turn a casual idea into structured, implementable GitHub issues through conversation.

## Process

### 1. Capture the idea

Ask the user to describe their idea freely. Don't interrupt - let them get it all out. Then summarize what you heard back to them in 2-3 sentences to confirm understanding.

### 2. Grill the idea

Interview the user relentlessly about every aspect. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

If a question can be answered by exploring the codebase, explore the codebase instead of asking.

Cover at minimum:
- Who is this for? What problem does it solve?
- What does "done" look like?
- What are the edge cases?
- What's explicitly out of scope?
- Are there technical constraints or preferences?

Keep going until there are no open questions.

### 3. Write the PRD

Create a PRD as a GitHub issue using `gh issue create`:

<prd-template>
## Problem Statement

The problem from the user's perspective.

## Solution

The solution from the user's perspective.

## User Stories

Numbered list:
1. As a <actor>, I want <feature>, so that <benefit>

Be extensive - cover all aspects discussed.

## Implementation Decisions

Key technical decisions made during brainstorming:
- Modules to build/modify
- Architectural choices
- Schema changes
- API contracts

Do NOT include file paths or code snippets.

## Out of Scope

What was explicitly excluded.
</prd-template>

Add the label `prd` to the issue.

### 4. Break into vertical slices

Break the PRD into **tracer bullet** issues. Each issue is a thin vertical slice through ALL layers end-to-end, NOT a horizontal layer slice.

Present the breakdown to the user as a numbered list showing:
- **Title**: short descriptive name
- **Type**: HITL (needs human input) / AFK (fully autonomous)
- **Blocked by**: dependencies on other slices
- **User stories covered**: which stories from the PRD

Ask: Does the granularity feel right? Any slices to merge or split?

Iterate until approved.

### 5. Create the issues

For each approved slice, create a GitHub issue with `gh issue create`:

<issue-template>
## Parent PRD

#<prd-issue-number>

## What to build

Concise description of this vertical slice. Describe end-to-end behavior, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- #<issue-number> (or "None - can start immediately")

## Type

AFK / HITL
</issue-template>

Label each issue with `ai-ready`. Create in dependency order so you can reference real issue numbers.

### 6. Summary

Print a summary: PRD issue link, list of created issues with numbers, and suggested starting order.

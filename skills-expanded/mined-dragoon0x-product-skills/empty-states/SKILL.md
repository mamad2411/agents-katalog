---
name: empty-states
description: "Turn dead ends into moments that build trust and guide action. Covers zero-data screens, error recovery, loading states, and retention micro-copy. Use when handling empty dashboards, failed searches, or moments where users hit a wall."
---

# Empty States

Turn dead ends into moments that build trust and guide action.

## How to use

- `/empty-states` Apply empty state constraints to this conversation.

## Constraints

### Every Empty State Must
- Explain WHY it's empty (not just show a blank screen)
- Suggest ONE clear next action
- Feel intentional, not broken
- NEVER say "No data found" without context

### Types and Treatments
- First use: guide to the first action. Show what this screen WILL look like.
- No results: suggest alternatives. "Try a different search" or show related items.
- Error state: explain what happened and what the user can do about it.
- Success empty: "All caught up" or "Inbox zero" should feel like a reward.
- Loading: skeleton screens that match the final layout, not spinners.

### Copy Rules
- MUST be specific to the context ("No projects yet" not "Nothing here")
- SHOULD use a human tone, not system language
- CTA should be action-oriented ("Create your first project" not "Add item")
- NEVER blame the user for the empty state

### Visual Rules
- SHOULD include a simple illustration or icon (not a stock photo)
- MUST maintain the page layout even when empty (don't collapse the container)
- Loading skeletons MUST match the dimensions of real content
- NEVER show a loading spinner for more than 3 seconds without a progress message

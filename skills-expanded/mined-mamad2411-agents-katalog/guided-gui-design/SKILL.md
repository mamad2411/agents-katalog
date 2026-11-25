---
name: guided-gui-design
description: Use when designing or reviewing a user-facing GUI and the goal is to reduce first-use cognitive load, make the flow understandable without external explanation, remove internal jargon, and guide the user naturally from setup to action to result.
---

# Guided GUI design

Use this skill for user-facing screens where the product itself must teach the user how to use it.

## Core outcome

Design the screen so a first-time user can understand:

1. what this screen lets them do
2. what to do first
3. what to do next
4. what result to look at

without needing a separate chat explanation.

## Default workflow

### 1. Find the real user goal

State the goal in plain task language.

- Good: `Compare fishing loadouts`
- Bad: `Use the calculator`, `Manage builds`, `Tune model assumptions`

The UI should be organized around the user's goal, not the implementation model.

### 2. Build one natural flow

Prefer a single path that reads naturally from top-to-bottom or left-to-right.

Default order:

1. setup
2. choice/action
3. result
4. optional detail

Do not show recommendations, comparisons, or output before the user has entered the minimum required setup, unless that clearly reduces confusion.

### 3. Lower first-use cognitive load

Reduce what the user must think about at the start.

- show only the next meaningful decision first
- keep secondary controls visually quieter
- delay advanced detail until the user has context
- prefer one clear next action over many equal-weight choices

Do not split into beginner/expert modes unless the user explicitly asks for that boundary.

### 4. Remove internal wording

Replace implementation language and site-only jargon with ordinary task language.

- Good: `What to compare next`
- Bad: `Derived model`, `Build state`, `Modifier assumptions`

If a domain term is genuinely necessary, explain it inline and make the meaning available on focus or hover without breaking the flow.

### 5. Make the next action obvious

At every stage, the user should be able to answer:

- where am I
- what should I do now
- what happens if I do it

If the screen cannot answer those questions quickly, simplify the structure or wording.

In interactive flows (drag-and-drop, selection, move, compare), always make the current selection, source item, and target visually distinct. The user must be able to answer "what am I acting on right now?" at a glance — without reading a status message or tooltip. Use visual weight, border, highlight, or label to differentiate selected, source, and target states.

### 6. Show the most decision-relevant result first

Once inputs are in place, put the main decision number or comparison first.

- identify the one number or result the user should decide from
- place that above supporting metrics
- move explanation, assumptions, and diagnostics later

### 7. Verify the flow as a first-time user

Check that a user can succeed by following the page in order.

Minimum review questions:

1. Can I use this by reading from the top?
2. Do I know what to enter before I see results?
3. Do I know which result matters most?
4. Do I see internal jargon that users would not understand?
5. Does the page still work without external explanation?
6. Does the primary UI require any horizontal scrolling at normal viewport sizes?
7. Are there any overflow, clipping, or unexpected text-wrapping issues?

For any major GUI change, take a screenshot and do a visual review before treating the work as complete. Spot-check overflow and layout at both normal and reduced widths.

## Common fixes

- Move setup above results
- Rename sections to task language
- Replace empty states with a clear next action
- Turn dense explanation into one short instruction near the relevant control
- Keep details in the same page, but visually later or collapsed

## Deliverable expectation

When using this skill, describe changes in user terms:

- what is easier now
- what order the user now follows
- what confusion was removed

Do not center the report on internal component names unless asked.

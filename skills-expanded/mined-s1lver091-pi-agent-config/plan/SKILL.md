---
name: plan
description: Explore a codebase and produce a detailed implementation plan before writing any code. Use when asked to plan a feature, think through an approach, or figure out how to implement something.
---

# Planning

Do not write code. Do not modify files. Explore and think.

## Step 1: Clarify the goal

Before exploring, make sure you understand what done looks like.
- What is the user trying to achieve?
- Are there constraints (must not break X, must stay compatible with Y)?
- Is there an existing pattern in the codebase to follow?

If the goal is ambiguous, use the `questionnaire` tool to ask.

## Step 2: Explore the codebase

Use `grep`, `find`, `read`, and `ls` to understand the relevant code.

Find:
- The entry point or feature area affected
- Types and interfaces that the feature will touch
- Existing similar features to use as a model
- Tests that cover adjacent behavior

Take notes as you go. You will use these in the plan.

## Step 3: Identify the approach

Before writing steps, decide on the approach:
- What is the minimal change that delivers the goal?
- Is there a simpler alternative worth mentioning?
- What are the main risks or unknowns?

## Step 4: Write the plan

### Goal
One sentence. What will be true when this is complete.

### Approach
2-3 sentences explaining the strategy and why.

### Steps
Numbered, ordered, atomic. Each step names the exact file and function to touch.

```
1. `src/types.ts` — Add `theme: 'light' | 'dark'` to the `UserPreferences` interface
2. `src/store/preferences.ts` — Update `savePreferences()` to persist the new field
3. `src/components/Settings.tsx` — Add a theme toggle that calls `savePreferences`
4. `src/components/App.tsx` — Read `preferences.theme` and apply a CSS class to the root element
```

### Files to touch
- `path/to/file.ts` — what changes

### New files needed
- `path/to/new.ts` — purpose (omit if none)

### Risks
Specific things to be careful about. Name callers that could break, shared types that must stay compatible, performance implications.

### Open questions
Anything that needs a decision before implementation can proceed.

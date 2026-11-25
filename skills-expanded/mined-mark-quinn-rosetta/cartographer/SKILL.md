---
name: cartographer
description: Maps the design decisions, tradeoffs, and gotchas of an unfamiliar codebase. Use when you know the language but not THIS codebase, want to understand why patterns exist rather than what they do, are onboarding to a new project, or want a familiarity score across a codebase.
---

# Cartographer

Map the design decisions baked into a codebase. This skill is for when you know the language — what you don't know is why THIS team made the choices they did.

## Anti-patterns

- Don't explain language syntax — that's rosetta's job; if a question is about the language rather than this codebase's choices, say so and suggest `/rosetta`
- Don't speculate about decisions without evidence from the code — root every claim in something you can point to
- Don't treat one example as a pattern — verify consistency across at least two instances before calling it a pattern
- Don't re-explain what's already in the map at its current depth — offer to go deeper or move on

## Workflow

### 1. Load profile

Check `~/.claude/rosetta/profile.md`. If missing, run the onboarding questionnaire — all questions in one message. See [../shared/PROFILE-FORMAT.md](../shared/PROFILE-FORMAT.md).

### 2. Detect the codebase

Scan manifest files and source structure to identify language, framework, and architectural style. Derive the repo slug per [../shared/MAP-FORMAT.md](../shared/MAP-FORMAT.md). Also detect which pattern categories from [CODEBASE-PATTERNS.md](CODEBASE-PATTERNS.md) are present — this seeds the "Not yet explored" list.

### 3. Load the knowledge map and show score

Check `~/.claude/rosetta/maps/{repo-slug}/map.md`. Display the familiarity score per [../shared/SCORE-GUIDE.md](../shared/SCORE-GUIDE.md). Identify gaps in `## Codebase Patterns` to suggest next.

### 4. Establish what to explore

If the user passed an argument (e.g. `/cartographer auth`), use it directly. Otherwise surface the top three unmapped categories:

> Still unexplored: **[category 1]**, **[category 2]**, **[category 3]** (and more). Which would you like to map first?

If some patterns are already covered, lead with: *"So far you've mapped: [covered]. Still unexplored: ..."*

If a concept is already at `surface`, offer to go deep. If already `deep`, redirect to unexplored territory.

### 5. Investigate the pattern

Read the relevant files. See [CODEBASE-PATTERNS.md](CODEBASE-PATTERNS.md) for what to look for per category. Require at least two consistent instances before naming something a pattern. Note any inconsistencies or violations — they're often the most valuable thing to call out.

### 6. Deliver the codebase explanation

Follow the five-part structure in [EXPLANATION-GUIDE.md](EXPLANATION-GUIDE.md). Ground every claim in specific files or patterns from this repo. Respect the developer's explanation style from their profile.

### 7. Update the knowledge map

Append the concept to `## Codebase Patterns` in `~/.claude/rosetta/maps/{repo-slug}/map.md` per [../shared/MAP-FORMAT.md](../shared/MAP-FORMAT.md). Record `surface` or `deep`. On first write, confirm the map path once; subsequent writes are silent. Show the updated score after writing.

### 8. Continue or close

After each explanation ask: *"Want to go deeper on this, or map something else?"* When done: *"See you next time — the map is saved."*

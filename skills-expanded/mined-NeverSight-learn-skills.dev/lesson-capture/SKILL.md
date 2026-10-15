---
name: lesson-capture
description: Capture project-specific operational lessons from mistakes, discoveries, and hard-won insights
---

# Objective

Extract a lesson from the current conversation context and persist it as a structured file. Lessons are project-specific operational knowledge — gotchas, patterns, and hard-won insights that prevent recurring mistakes.

Lessons complement the contract: the contract governs *how to work* (behavioral, project-agnostic); lessons capture *what we learned here* (operational, project-specific).

# Audience

Lessons are split by audience:

| Audience | Directory | Read During Init | Content |
|----------|-----------|------------------|---------|
| **Agents** | `lessons/agents/` | Yes | Project-specific gotchas agents hit repeatedly |
| **Humans** | `lessons/humans/` | No | Workflow habits, domain pitfalls, invariants to preserve |

If audience is ambiguous, ask.

# Lesson Format

Each lesson is a small `.md` file with yaml frontmatter.

```yaml
---
title: "Descriptive title"
trigger: "When [succinct situational condition]"
keywords: [keyword1, keyword2, keyword3]
date: YYYY-MM-DD
---

## Context

[Situation, intent, and conditions that led to this lesson]

## Failure Mode

[What went wrong and why]

## Solution

[What to do instead]

## References

- [Links to relevant files, docs, specs, or external resources]
```

**Frontmatter fields:**
- **title**: What the lesson is about (noun phrase)
- **trigger**: When to consult this lesson (action phrase, starts with "When")
- **keywords**: Concrete terms for matching — error messages, class names, tool names, file patterns
- **date**: When the lesson was captured

**Body sections:**
- **Context**: Enough detail to recognize the situation. Not a narrative — a pattern description.
- **Failure Mode**: The specific thing that goes wrong. Name the mechanism, not just the symptom.
- **Solution**: Concrete, actionable. Code snippets or commands when applicable.
- **References**: Links to files, docs, specs, external resources. Keep it short.

# Index Format

| Audience | Location                   |
|----------|----------------------------|
| Agents   | `GUARDRAILS.md` (Tier 2)   |
| Humans   | `lessons/humans/README.md` |


```markdown
### G2.x: Lessons — [Agents|Humans]

Operational lessons from project experience. Read when a trigger matches.

| Trigger | File |
|---------|------|
| When ... | [filename.md](filename.md) |
```

The index is the discovery mechanism. Agents read it during session initialization and consult full lessons when a trigger matches their current task.

# Process

## 1. Extract

Identify the lesson from the current conversation. Look for:
- A bug that was fixed (what caused it, how to prevent it)
- A discovery during debugging or exploration
- A pattern that worked well (or poorly)
- A gotcha specific to this project's tech stack or architecture
- An invariant that must be preserved

## 2. Classify

Determine audience:
- **Agents**: The lesson prevents an agent from making this mistake again. Examples: file format corruption, missing locking, overlooked dependencies.
- **Humans**: The lesson helps a human avoid a workflow or domain pitfall. Examples: deployment order matters, this API has undocumented rate limits, this invariant breaks silently.

If unclear, ask: "Is this a lesson for agents, humans, or both?"
If both, write two separate lessons tailored to each audience.

## 3. Draft

Propose the lesson content in the standard format. Present for approval before writing.

**Naming convention:** kebab-case, descriptive. Examples:
- `csv-field-escaping.md`
- `file-locking-shared-state.md`
- `deployment-order-migrations.md`

**Quality bar:**
- Trigger is specific enough to match but general enough to catch variants
- Keywords include concrete terms an agent would encounter (error messages, file names, tool names)
- Failure mode names the mechanism, not just the symptom
- Solution is actionable without reading external docs
- Under 50 lines total (excluding frontmatter) — if longer, the lesson is too broad; split it

## 4. Write

After approval:
1. Write the lesson file to the appropriate directory
2. Update the directory's `README.md` index — append a row to the table
3. Announce: `"Lesson captured: [title] → lessons/[audience]/[filename]. Index updated."`

## 5. Maintain

When invoked on an existing lesson (update or delete):
- **Update**: Edit the lesson file, update the index row if trigger or title changed
- **Delete**: Remove the lesson file, remove the index row
- Always keep index and files in sync — the index is not a cache, it's the discovery layer

# Integration

**Position in workflow:**
```
mistake/discovery → reflection → lesson-capture skill → lessons/ persisted
```

Invoked manually by the human. May later support automated triggers (post-bug-fix, post-review-finding, post-struggle).

**Session initialization:** Agents read `lessons/agents/README.md` during init. When a trigger matches current work, read the full lesson file before proceeding.

**Discovery limitation:** The trigger+keyword model relies on agents predicting which lessons are relevant. This handles known-unknowns (agent recognizes the trigger) but cannot surface unknown-unknowns (agent working on CSV export won't search for "file locking" until it's already hit the problem). Mitigation: write triggers and keywords broadly enough to match adjacent situations, not just the exact scenario where the lesson was learned.

**Relation to other artifacts:**
- `specs/` — Requirements and architecture (what to build)
- `docs/` — Usage and setup (how to use)
- `lessons/` — Operational knowledge (what we learned)
- Contract — Behavioral rules (how to work)

# Anti-patterns

- **Too abstract**: "Be careful with file formats" — useless. Name the specific format, the specific failure.
- **Too narrative**: A story of what happened. Extract the pattern, not the history.
- **Duplicate**: Check existing lessons before writing. If a lesson exists, update it rather than create a near-duplicate.
- **Stale lessons**: A lesson about a gotcha that was fixed at the root is noise. Delete it.
- **Over-capture**: Not every mistake warrants a lesson. The bar: "Would this save real time if encountered again?"

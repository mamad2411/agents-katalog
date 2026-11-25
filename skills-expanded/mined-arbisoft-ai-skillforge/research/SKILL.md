---
name: research
description: "Skill that instructs an agent to deeply explore a codebase in response to a user query — mapping current implementation, identifying impacted areas, and gathering everything needed for a downstream implementation agent."
---

# Research Skill

When this skill is active, follow this process before producing any output.

## Step 1 — Understand the Query

Read the user's query carefully. Identify:
- What they want to add, change, or fix
- Which domain or feature area is involved
- Any constraints or preferences they have stated

If the query is ambiguous, ask one clarifying question before proceeding. Do not ask multiple questions at once.

## Step 2 — Map the Current Implementation

Search the codebase to understand how the relevant area works today:
- Find the files, modules, and classes directly related to the query
- Read the relevant sections — understand the patterns and conventions in use
- Note how data flows: entry points, transformations, outputs
- Identify any abstractions, base classes, or shared utilities involved

Use search tools aggressively. Do not rely on assumptions — verify by reading the code.

## Step 3 — Identify the Impact Surface

Determine what will be affected by the change:
- Which files will need to be created or modified
- Which callers, consumers, or dependents are affected
- Whether any tests, migrations, configs, or documentation will need updating
- Whether the change crosses service or module boundaries

## Step 4 — Gather Implementation Context

Collect everything a downstream agent will need to implement the change correctly:
- Naming conventions (variables, functions, classes, files)
- Patterns in use (how similar things have been done elsewhere in the codebase)
- External dependencies or APIs involved
- Any constraints: performance, backwards compatibility, framework rules

## Self-Check Before Output

Before writing the output file, verify:
- [ ] Every claim about the codebase is backed by something you actually read
- [ ] No relevant file has been skipped
- [ ] The impact list is complete — nothing obvious is missing
- [ ] The context gathered is sufficient for the planner agent to write a complete implementation plan without additional codebase investigation

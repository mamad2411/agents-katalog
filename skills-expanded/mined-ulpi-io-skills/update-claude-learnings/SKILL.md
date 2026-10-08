---
name: update-claude-learnings
version: 2.0.0
description: |
  Propagate ONE validated learning about Claude Code behavior from this session into the project's
  CLAUDE.md — the MAIN-AGENT memory Claude loads every session, not agent or skill files. Extract the
  smallest useful workflow/scope/session rule, place it in the correct section (Workflow Rules / Session
  Management / Scope Control / Behavioral Patterns), and preserve the surrounding structure. User-only
  maintenance workflow that mutates durable project memory: it grounds the rule in what THIS session
  revealed, never invents, checks for duplicates, and confirms wording and placement before writing. Use to
  make a Claude-behavior rule persist into future sessions.
allowed-tools:
  - AskUserQuestion
  - Read
  - Edit
  - Write
  - Glob
  - Grep
disable-model-invocation: true
user-invocable: true
argument-hint: "[learning candidate or session focus]"
arguments:
  - request
when_to_use: |
  Use when the user explicitly asks to record a Claude Code behavior or workflow learning in the project's
  CLAUDE.md — "/update-claude-learnings", "add this Claude behavior to CLAUDE.md", "record this workflow
  rule for future sessions". Do NOT use for agent-behavior rules (update-agent-learnings), skill-authoring
  learnings (update-skill-learnings), or application-code patterns; confirm before writing — it mutates
  durable Claude memory and is user-only.
---

<EXTREMELY-IMPORTANT>
This skill updates durable Claude memory and must stay disciplined.

Non-negotiable rules:
1. Only record learnings about Claude Code behavior or workflow in this project.
2. Reject application-code, subagent, or skill-authoring learnings and route them to the proper maintenance workflow instead.
3. Check for duplicates or near-duplicates before writing.
4. Get explicit user confirmation before modifying `CLAUDE.md`.
5. Preserve existing structure and only add the smallest correct instruction.
</EXTREMELY-IMPORTANT>

# Update Claude Learnings

## Inputs

- `$request`: Optional learning candidate, category hint, or reminder about what the session revealed

## Goal

Add one validated Claude-behavior learning to project memory by:

- extracting the right rule from the session
- verifying it belongs in `CLAUDE.md`
- placing it in the correct section
- preserving the surrounding memory structure
- reporting exactly what changed

## Step 0: Confirm the learning belongs here

This skill is only for persistent Claude Code behavior in this project.

Valid examples:

- workflow rules for when Claude should use a specific skill
- scope-control rules for how Claude should ask before expanding work
- session-management rules for checkpoints, progress updates, or stopping conditions
- project-specific Claude behavior that improves future sessions

Invalid examples:

- application implementation rules better suited for agent files
- skill-authoring patterns better suited for skill learnings
- transient one-off notes that do not deserve durable memory

Load `references/learning-scope.md` for routing, category placement, and failure modes.

If the learning does not belong in `CLAUDE.md`, stop and say where it should go instead.

**Success criteria**: The learning clearly belongs in persistent Claude project memory.

## Step 1: Extract one concrete learning from the session

Review the session and identify the smallest useful rule.

Rules:

- prefer one precise learning over several vague ones
- write it in imperative mood
- tie it to a concrete behavior, not a general aspiration
- avoid duplicating rules that are already implied by stronger existing guidance

Good shape:

- "Use `/commit` instead of manual git commit flows when the user explicitly asks to commit."
- "Ask before expanding a bugfix into adjacent refactors."

Bad shape:

- "Be more careful."
- "Use better workflows."

**Success criteria**: You have a single actionable learning candidate with a clear rationale.

## Step 2: Check the current CLAUDE memory and choose placement

Read the project `CLAUDE.md`. If it does not exist, use
`references/claude-md-template.md` as the structural fallback.

Choose the correct section:

- `Workflow Rules`
- `Session Management`
- `Scope Control`
- `Behavioral Patterns`

Before writing:

- search for duplicates or near-duplicates
- merge with existing wording if a similar rule already exists
- keep the new instruction small and local

Load `references/learning-scope.md` for placement and duplicate-handling guidance.

**Success criteria**: The target section is known and duplication risk has been checked.

## Step 3: Confirm with the user

Before editing `CLAUDE.md`, present:

- category
- final wording
- reason this learning was extracted
- intended section placement

Use `AskUserQuestion` if confirmation or wording refinement is needed.

Do not write until the user explicitly approves the learning.

**Success criteria**: The user has approved the learning and its placement.

## Step 4: Update CLAUDE.md

Apply the minimal correct edit:

- preserve file structure
- insert the learning in the chosen section
- avoid deleting unrelated content
- update the "Last updated" marker only if the file already uses one

Rules:

- if `CLAUDE.md` is missing, create it using the provided template and then add the learning
- if the section is missing, create the smallest compatible section rather than restructuring the whole file
- keep formatting consistent with the existing document

**Success criteria**: `CLAUDE.md` contains the approved learning in the right place without collateral churn.

## Step 5: Verify and report

Verify:

- the learning was added exactly once
- the file structure still makes sense
- the instruction remains actionable and specific
- the update did not drift into agent or skill memory territory

Report:

- category
- section path
- final wording
- whether the file was created or updated

**Success criteria**: The user can see exactly what durable Claude memory changed.

## Guardrails

- Do not let the model invoke this skill proactively; it mutates durable memory.
- Do not add `context: fork`; this workflow edits the active repository.
- Do not add `paths:`; this is a generic maintenance skill.
- Do not keep routing matrices, quality scorecards, or long failure catalogs inline in `SKILL.md`.
- Do not add a learning without explicit user approval.
- Do not rewrite large parts of `CLAUDE.md` when a small targeted insertion is enough.

## When To Load References

- `references/learning-scope.md`
  Use for deciding whether the learning belongs in Claude memory, choosing section placement, handling duplicates, and checking common failure modes.

- `references/claude-md-template.md`
  Use only when `CLAUDE.md` is missing or its structure needs a minimal compatible fallback.

## Output Contract

Report:

1. whether the learning was accepted or redirected elsewhere
2. the chosen category and section
3. the final approved wording
4. whether `CLAUDE.md` was created or updated
5. any duplicate merge or placement decisions

---
name: update-skill-learnings
version: 2.0.0
description: |
  Propagate ONE validated learning about SKILL design or quality from this session into the central
  skill-learnings file — extract the smallest useful pattern or anti-pattern, categorize it (Structural
  Patterns / Content Patterns / Anti-Patterns / Skill-Specific), and add it once without touching any actual
  skill file. User-only maintenance workflow that mutates durable skill-authoring guidance: it grounds the
  rule in what THIS session revealed, never invents, checks for duplicates, and confirms category and wording
  before writing. Use to capture a skill-authoring rule so future skill work inherits it.
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
  Use when the user explicitly asks to record a skill-design learning, anti-pattern, or skill-specific
  improvement rule — "/update-skill-learnings", "record this skill pattern", "add this anti-pattern to the
  skill learnings". Do NOT use for agent-behavior learnings (update-agent-learnings), main-agent CLAUDE.md
  rules (update-claude-learnings), or a direct skill rewrite now (normalize-skill-for-claude); confirm
  before writing — it mutates durable authoring guidance and is user-only.
---

<EXTREMELY-IMPORTANT>
This skill updates durable skill-authoring guidance and must stay disciplined.

Non-negotiable rules:
1. Only record learnings about skill structure, skill content, anti-patterns, or one skill's design.
2. Reject application-code and agent-behavior learnings and route them to the right maintenance workflow.
3. Update exactly one canonical learnings file instead of creating parallel copies.
4. Check for duplicates or near-duplicates before writing.
5. Get explicit user confirmation before modifying the learnings file.
</EXTREMELY-IMPORTANT>

# Update Skill Learnings

## Inputs

- `$request`: Optional learning candidate, skill name, category hint, or reminder about what the session revealed

## Goal

Add one validated skill-authoring learning to the central learnings store by:

- confirming the learning belongs in skill memory
- choosing the right category
- updating the canonical learnings file
- preserving file structure and avoiding duplicates
- reporting exactly what changed

## Step 0: Confirm the learning belongs here

This skill is only for persistent guidance about creating, reviewing, or improving skills.

Valid examples:

- structural patterns for better skills
- content patterns that improve clarity or usability
- anti-patterns that repeatedly cause confusion
- one skill's specific design rule that should be remembered centrally

Invalid examples:

- application implementation rules
- agent-behavior rules for the main Claude conversation
- direct requests to rewrite a skill right now
- one-off notes that do not deserve durable memory

Load `references/learning-scope.md` for routing, category placement, and failure modes.

If the learning does not belong in the skill learnings system, stop and say where it should go instead.

**Success criteria**: The learning clearly belongs in persistent skill-authoring guidance.

## Step 1: Extract one concrete learning

Review the session and identify the smallest useful rule.

Rules:

- prefer one precise learning over a long list of vague observations
- write it in imperative mood
- tie it to a concrete pattern, anti-pattern, or skill-specific rule
- avoid documenting advice that is already implied by stronger existing guidance

Good shape:

- "Keep heavy checklists in references instead of inline in `SKILL.md`."
- "Mark durable-memory maintenance skills as `disable-model-invocation: true`."

Bad shape:

- "Skills should be better."
- "Use clearer instructions."

**Success criteria**: You have a single actionable learning candidate with a clear rationale.

## Step 2: Resolve the canonical learnings file and choose placement

Locate the canonical central learnings file.

Path policy:

- if the repo already has a single existing skill learnings file, use it
- if both `.agents` and `.claude` variants exist, update the canonical authoring surface and do not create a second source of truth
- in this canonical `.agents` tree, prefer `.agents/learnings/skill-learnings.md`
- if the repo still uses `.claude/learnings/skill-learnings.md` as its only learnings store, use that instead

Choose the correct category:

- `Structural Patterns`
- `Content Patterns`
- `Anti-Patterns`
- `Skill-Specific Learnings`

Before writing:

- search for duplicates or near-duplicates
- merge with existing wording if a similar rule already exists
- keep the new instruction small and local

Load:

- `references/learning-scope.md` for routing, categories, and duplicate handling
- `references/skill-learnings-template.md` only if the canonical learnings file does not exist yet

**Success criteria**: The target file and section are known and duplication risk has been checked.

## Step 3: Confirm with the user

Before editing the learnings file, present:

- category
- final wording
- target file
- reason this learning was extracted

Use `AskUserQuestion` if confirmation or wording refinement is needed.

Do not write until the user explicitly approves the learning.

**Success criteria**: The user has approved the learning, placement, and target file.

## Step 4: Update the learnings file

Apply the minimal correct edit:

- preserve file structure
- insert the learning in the chosen section
- avoid deleting unrelated content
- update the "Last updated" marker only if the file already uses one

Rules:

- if the canonical learnings file is missing, create it from `references/skill-learnings-template.md`
- if the section is missing, create the smallest compatible section rather than restructuring the whole file
- keep formatting consistent with the existing document
- do not sync or rewrite actual skill files as part of this workflow

**Success criteria**: The approved learning is present in the right section of the canonical learnings file.

## Step 5: Verify and report

Verify:

- the learning was added exactly once
- the category placement is correct
- the file structure still makes sense
- the update did not drift into application-code or agent-behavior territory

Report:

- category
- target file
- section path
- final wording
- whether the file was created or updated

**Success criteria**: The user can see exactly what durable skill-authoring memory changed.

## Guardrails

- Do not let the model invoke this skill proactively; it mutates durable learnings.
- Do not add `context: fork`; this workflow edits the active repository.
- Do not add `paths:`; this is a generic maintenance skill.
- Do not keep routing matrices, quality scorecards, or long failure catalogs inline in `SKILL.md`.
- Do not add a learning without explicit user approval.
- Do not create both `.agents/learnings/skill-learnings.md` and `.claude/learnings/skill-learnings.md`.
- Do not rewrite actual skill files as part of this learnings update.

## When To Load References

- `references/learning-scope.md`
  Use for deciding whether the learning belongs in skill memory, choosing the right category, handling duplicates, and checking common failure modes.

- `references/skill-learnings-template.md`
  Use only when the canonical central learnings file is missing and a minimal compatible file must be created.

## Output Contract

Report:

1. whether the learning was accepted or redirected elsewhere
2. the chosen category and target file
3. the final approved wording
4. whether the learnings file was created or updated
5. any duplicate merge or canonical-path decisions

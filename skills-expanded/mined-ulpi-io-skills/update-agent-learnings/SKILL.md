---
name: update-agent-learnings
version: 2.0.0
description: |
  Propagate ONE validated learning from this session into durable AGENT guidance — extract the smallest
  useful rule, classify its scope (Global / Claude Code Only / Agent-Specific), store it once in the central
  agent-learnings file, and sync the regenerated `## Learnings` section into every live agent definition
  across the CLI trees present. User-only maintenance workflow that mutates durable agent prompts: it grounds
  the rule in what THIS session actually revealed, never invents, confirms scope and wording first, and keeps
  "Claude Code Only" learnings out of subagent prompts. Use to record an agent-behavior rule so future agents
  inherit it.
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
  Use when the user explicitly asks to record an agent-behavior learning, subagent coding rule, or
  agent-specific pattern from this session — "/update-agent-learnings", "record this agent learning", "sync
  this rule into the agents". Do NOT use for skill-design learnings (update-skill-learnings), main-agent
  CLAUDE.md workflow rules (update-claude-learnings), or a direct agent rewrite now
  (normalize-agent-for-claude); confirm before writing — it mutates durable agent prompts and is user-only.
---

<EXTREMELY-IMPORTANT>
This skill updates durable agent guidance and live agent prompt files.

Non-negotiable rules:
1. Only record learnings that belong in agent memory.
2. Keep one central learnings source of truth; do not invent parallel central files.
3. Sync approved learnings into every relevant agent surface that exists for the supported CLIs.
4. Do not propagate "Claude Code Only" learnings into engineer/reviewer agent prompts.
5. Get explicit user confirmation before modifying the learnings file or any agent file.
</EXTREMELY-IMPORTANT>

# Update Agent Learnings

## Inputs

- `$request`: Optional learning candidate, scope hint, agent name, or reminder about what the session revealed

## Goal

Add one validated agent learning to the central learnings store and sync it into the matching agent
files by:

- confirming the learning belongs in agent memory
- classifying the scope correctly
- updating one canonical learnings file
- regenerating the relevant `## Learnings` sections
- syncing those sections into all agent surfaces that exist

## Step 0: Confirm the learning belongs here

This skill is only for durable learnings that should shape agent behavior.

Valid examples:

- global coding-agent rules such as scope control, testing, or iteration
- agent-specific rules for one technology or role
- "Claude Code Only" learnings that belong in the central learnings store but should not be pushed into subagent prompts

Invalid examples:

- skill-design rules
- main `CLAUDE.md` workflow rules
- one-off implementation notes
- direct requests to rewrite an agent prompt right now

Load `references/learning-scope.md` for routing and scope classification.

If the learning does not belong in agent memory, stop and say where it should go instead.

**Success criteria**: The learning clearly belongs in the agent learnings system.

## Step 1: Extract one concrete learning

Review the session and identify the smallest useful rule.

Classify it as one of:

- `Global`
- `Claude Code Only`
- `Agent-Specific`

Rules:

- write it in imperative mood
- prefer one precise learning over a vague bundle
- only mark it `Global` if it truly applies across coding agents
- use `Claude Code Only` for meta-work about skills, orchestration, configs, or project setup

**Success criteria**: You have one actionable learning candidate with a correct scope.

## Step 2: Resolve the central learnings file and agent sync targets

Locate the canonical central learnings file.

Path policy:

- if one central agent learnings file already exists, use it
- if both `.agents/learnings/agent-learnings.md` and `.claude/learnings/agent-learnings.md` exist, pick one canonical source and do not maintain both by hand
- in this `.agents`-first repo, prefer `.agents/learnings/agent-learnings.md`
- if the repo only has `.claude/learnings/agent-learnings.md`, use that instead

Then discover agent sync targets:

- sync into `.agents/agents/*/AGENT.md` when that tree exists
- sync into `.claude/agents/*` when that tree exists
- treat both trees as live CLI surfaces when both are present

Load:

- `references/learning-scope.md` for scope and duplicate handling
- `references/agent-learnings-template.md` only if the canonical learnings file does not exist yet
- `references/agent-sync-contract.md` for Learnings-section generation and placement

**Success criteria**: The canonical learnings file and all sync target trees are known.

## Step 3: Confirm with the user

Before editing anything, present:

- scope classification
- final wording
- canonical learnings file
- sync targets that will be touched

Use `AskUserQuestion` if confirmation or wording refinement is needed.

Do not write until the user explicitly approves the update.

**Success criteria**: The user has approved the learning and the sync surface.

## Step 4: Update the central learnings file

Apply the minimal correct edit:

- preserve file structure
- insert the learning in the correct section
- avoid deleting unrelated content
- update the "Last updated" marker only if the file already uses one

Rules:

- if the canonical learnings file is missing, create it from `references/agent-learnings-template.md`
- if the section is missing, create the smallest compatible section rather than restructuring the whole file
- keep formatting consistent with the existing document

**Success criteria**: The central learnings file contains the approved learning exactly once.

## Step 5: Regenerate and sync Learnings sections into agent files

Use the central learnings file to build the `## Learnings` section for each target agent file.

Sync rules:

- global learnings go to all coding/reviewer agent files
- agent-specific learnings go only to the matching agent files
- "Claude Code Only" learnings stay in the central learnings file and are not pushed into subagent prompts
- if an agent file already has a `## Learnings` section, replace that section cleanly
- if it does not, insert the section in the location defined by `references/agent-sync-contract.md`

Important:

- when both `.agents` and `.claude` agent trees exist, update both surfaces
- do not assume filename parity; resolve the actual paths present
- do not rewrite unrelated prompt sections while syncing learnings

**Success criteria**: Every relevant agent file in every present CLI tree has the correct synced Learnings section.

## Step 6: Verify and report

Verify:

- the learning exists once in the central learnings file
- sync targets were updated as intended
- agent Learnings sections contain the right global and agent-specific content
- "Claude Code Only" learnings did not leak into subagent prompts

Report:

- scope classification
- canonical learnings file
- sync target trees updated
- final wording
- whether files were created or updated

**Success criteria**: The user can see exactly what changed centrally and across agent surfaces.

## Guardrails

- Do not let the model invoke this skill proactively; it mutates durable learnings and agent prompt files.
- Do not add `context: fork`; this workflow edits the active repository.
- Do not add `paths:`; this is a generic maintenance skill.
- Do not keep routing matrices, scorecards, or giant Learnings examples inline in `SKILL.md`.
- Do not add a learning without explicit user approval.
- Do not maintain two divergent central learnings files.
- Do not skip one CLI tree when both `.agents` and `.claude` agent surfaces are present.

## When To Load References

- `references/learning-scope.md`
  Use for deciding whether the learning belongs in agent memory, choosing the right scope, and handling duplicates.

- `references/agent-learnings-template.md`
  Use only when the canonical central learnings file is missing and a minimal compatible file must be created.

- `references/agent-sync-contract.md`
  Use for generating the Learnings section and placing it correctly in agent files across the supported CLI trees.

## Output Contract

Report:

1. whether the learning was accepted or redirected elsewhere
2. the chosen scope and canonical learnings file
3. the final approved wording
4. which CLI agent trees were updated
5. any duplicate merge or sync-target decisions

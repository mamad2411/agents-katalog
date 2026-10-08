---
name: normalize-agent-for-claude
version: 1.0.0
description: |
  Convert a local AGENT.md into a Claude Code optimized agent — an AUDIT-then-rewrite that ties every
  change to real Claude agent-runtime behavior, not taste. Inventories the agent, checks it against the
  runtime reference (the whole body becomes the system prompt; role identity stays, procedure moves to
  skills), writes a per-agent DAG rewrite plan with source-backed guardrails, and — only when asked —
  rewrites the frontmatter and prompt body thinner and more role-specific. Defaults to PLAN mode, never a
  blind rewrite, uses agent-native frontmatter only, and grounds each decision in the runtime source rather
  than inventing conventions. Use to migrate or thin an AGENT.md for Claude's agent runtime.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
argument-hint: "<agent-dir-or-AGENT.md> [--mode plan|rewrite]"
arguments:
  - target
  - mode
when_to_use: |
  Use when a repository has custom markdown agents to migrate or rewrite for Claude's agent runtime —
  "convert this agent to Claude", "rewrite this reviewer agent for Claude Code", "thin these AGENT.md
  files", "create a detailed Claude rewrite plan for this agent". Do NOT use on a SKILL.md or skill folder
  (use normalize-skill-for-claude), and do NOT jump straight to rewrite without the plan unless the user
  explicitly asks — audit first, rewrite only on request.
---

<EXTREMELY-IMPORTANT>
Every rewrite decision must be tied to Claude Code's agent runtime.

Non-negotiable rules:
1. Read `references/claude-agent-runtime.md` before planning or rewriting.
2. Default to `--mode plan` unless the user explicitly asks for rewrite now.
3. Keep the body lean because the full markdown body becomes the agent system prompt.
4. Use frontmatter for runtime controls before adding more prose.
5. Never preload large skills into agent frontmatter unless they have already been slimmed and justified.
6. Never add skill-only frontmatter to an agent. `allowed-tools`, `argument-hint`, `arguments`, `when_to_use`, `disable-model-invocation`, `user-invocable`, `context`, `agent`, `shell`, and `paths` belong to skills, not agents.
</EXTREMELY-IMPORTANT>

# Normalize Agent For Claude

## Inputs

- `$target`: Agent directory or direct path to `AGENT.md`
- `$mode`: Optional. `plan` or `rewrite`. Default: `plan`

## Goal

Produce a Claude Code optimized agent that carries role identity and constraints cleanly, uses frontmatter intentionally, and avoids wasting prompt budget on procedural bulk that belongs in skills or shared rules.

## Step 1: Resolve the target

1. Accept either an agent directory or a direct `AGENT.md` path.
2. Normalize to the agent root and confirm `AGENT.md` exists.
3. Determine mode:
   - `--mode rewrite` means plan first, then rewrite in the same run
   - missing mode means `plan`
4. Inventory the current agent:
   - line count of `AGENT.md`
   - existing frontmatter fields
   - section map of the body
   - obvious duplicated global policy or giant knowledge catalogs

**Success criteria**: You know the exact target agent, target mode, and the current prompt-shape risks.

## Step 2: Load the Claude Code agent runtime anchors

Read `references/claude-agent-runtime.md` fully before making any recommendation.

Extract these constraints from the reference:
- agent `description` becomes `whenToUse`
- the whole markdown body becomes the system prompt
- Claude supports richer agent frontmatter than most custom agents use
- agent `skills:` preloads full skill content
- tool allow and deny lists are enforced at runtime
- repo-wide project rules already have a separate instruction hierarchy
- agent rewrites must use agent-native frontmatter only, not skill-native headers

If this repository contains `claude-code-source/`, use the exact source files named in the reference to verify unusual frontmatter or isolation decisions.

**Success criteria**: Every planned change is backed by specific Claude runtime behavior.

## Step 3: Audit the current agent against Claude's runtime

Evaluate the target agent using this checklist:

1. **Identity vs procedure**
   - What content is true role identity? (role definition, expertise bullets, decision heuristics, domain knowledge, traits)
   - What content is actually workflow and should live in skills? (step-by-step procedures, shell commands, templates, checklists)
   - Role-specific expertise lists and decision heuristics are `IDENTITY` — they stay in the body. Only move *procedure* into skills or references.
2. **Prompt mass**
   - Which large sections exist only because the current agent is compensating for missing skills or shared rules?
3. **Frontmatter opportunities**
   - Would `disallowedTools`, `skills`, `initialPrompt`, `hooks`, `permissionMode`, `maxTurns`, `background`, `memory`, or `isolation` improve runtime behavior?
   - Are there any skill-only headers that must be removed or explicitly avoided?
4. **Tool surface**
   - Is the tool list broader than the role actually needs?
5. **Skill preload risk**
   - Would adding a skill to frontmatter create prompt bloat because the skill is still too large?
6. **Instruction duplication**
   - Are repo-wide rules duplicated here even though Claude already loads project memory separately?

Classify each issue:
- `PROMPT`: body is too large or carries the wrong content
- `RUNTIME`: missing or misused Claude frontmatter
- `TOOLS`: tool exposure is too broad or too vague
- `DUPLICATION`: project policy is duplicated in agent body
- `EXTRACTION`: content should move into skills or references

**Success criteria**: You have a concrete, source-backed explanation of what should stay, move, or shrink.

## Step 4: Write the per-agent DAG plan

Create both of these artifacts:

- `.ulpi/plans/agents/<agent-name>-normalize-for-claude.md`
- `.ulpi/plans/agents/<agent-name>-normalize-for-claude.json`

The plan must include:

1. **Current state**
   - line count
   - current frontmatter
   - oversized sections
   - duplicated global policy
2. **Claude runtime findings**
   - each finding mapped to source references from `references/claude-agent-runtime.md`
3. **Target state**
   - final frontmatter shape
   - body sections to keep, delete, or move
   - skills or references the agent should depend on instead
4. **DAG tasks**
   - frontmatter rewrite
   - prompt-body reduction
   - procedure extraction into skills or references
   - tool-surface tightening
   - validation
5. **Guardrails**
   - what identity must stay
   - what must move out
   - what must not be preloaded
6. **Validation**
   - concrete checks to confirm the final agent is structurally sound

Each DAG task should include:
- `id`
- `title`
- `rationale`
- `filesToModify`
- `filesToCreate`
- `dependencies`
- `validation`

**Success criteria**: The markdown and JSON plans describe the same safe sequence of work.

## Step 5: Rewrite only if requested

If mode is `plan`, stop after writing the DAG artifacts.

If mode is `rewrite`:

1. Rewrite the frontmatter first.
2. Reduce the body to:
   - role and expertise (specific domain knowledge and capability claims)
   - scope
   - decision heuristics (how to choose between approaches)
   - failure boundaries
   - output contract
   - brief skill handoff guidance
3. Move repeated procedures and large examples out of the agent. Keep role expertise bullets and decision heuristics — these are identity, not procedure.
4. Add Claude-native frontmatter only when it changes runtime behavior materially.
5. Keep the result role-specific, not generic.

Preferred rewrite outcomes:
- agent `description` becomes a strong `whenToUse`
- body becomes much smaller and more identity-focused
- `disallowedTools` and tighter `tools` are used where appropriate
- `skills:` is used sparingly and only for already-slim skills
- duplicated project rules are removed from the body
- no skill-only headers are introduced into the rewritten agent

**Success criteria**: The rewritten agent is thinner, more precise, and better aligned to Claude's runtime model.

## Step 6: Validate the result

After planning or rewriting:

1. Re-read the final `AGENT.md`.
2. Confirm the frontmatter reflects real runtime decisions.
3. Confirm the body is mostly identity, scope, heuristics, and boundaries.
4. Confirm no skill-only headers were introduced.
5. Confirm large procedure blocks are gone or explicitly moved.
6. Confirm the summary names the Claude source anchors that drove the major changes.

**Success criteria**: The output can be used immediately without re-interpreting why the structure changed.

## Output Contract

Always report:

1. `Agent:` target path and normalized root
2. `Mode:` `plan` or `rewrite`
3. `Top runtime issues:` the highest-value Claude mismatches
4. `Artifacts:` exact plan or rewritten file paths
5. `Guardrails applied:` 3 to 5 bullets tied to Claude runtime behavior

If rewrite mode was used, also report:
- which sections were removed or moved
- which frontmatter fields were added, removed, or intentionally omitted

---
name: normalize-skill-for-claude
version: 1.0.0
description: |
  Convert a local skill into a Claude Code optimized shape — an AUDIT-then-rewrite that ties every change
  to real Claude skill-runtime behavior, treating FRONTMATTER as the highest-leverage routing surface.
  Inventories the skill, checks it against the runtime reference (Claude routes and budgets skills from
  metadata first), writes a per-skill DAG rewrite plan with source-backed guardrails, and — only when
  asked — rewrites frontmatter, body, and references for cheaper routing and safer execution. Defaults to
  PLAN mode, never a blind rewrite, uses skill-native frontmatter only, and preserves structural content
  (routing tables, guardrail rules) rather than stripping it as bulk. Use to migrate or restructure a
  SKILL.md for Claude's skill runtime.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
argument-hint: "<skill-dir-or-SKILL.md> [--mode plan|rewrite]"
arguments:
  - target
  - mode
when_to_use: |
  Use when a repository has custom skills to migrate or rewrite for Claude's skill runtime — "convert this
  skill to Claude", "make these skills Claude-native", "add proper when_to_use and paths metadata", "split
  this huge skill into references". Do NOT use on an AGENT.md or agent definition (use
  normalize-agent-for-claude), and do NOT jump straight to rewrite without the plan unless the user
  explicitly asks — audit first, rewrite only on request.
---

<EXTREMELY-IMPORTANT>
Every recommendation must be justified by Claude Code runtime behavior, not taste.

Non-negotiable rules:
1. Read `references/claude-skill-runtime.md` before planning or rewriting.
2. Default to `--mode plan` unless the user explicitly asks to rewrite now.
3. Treat frontmatter as the highest-leverage surface. Claude routes and budgets skills from metadata first.
4. Keep `SKILL.md` focused on workflow. Move bulky examples, framework variants, and edge-case catalogs into `references/` or `scripts/`.
5. Do not add `context: fork`, `paths:`, or `user-invocable: false` without a concrete runtime reason.
6. Never add agent-only frontmatter to a skill. `tools`, `disallowedTools`, `skills`, `initialPrompt`, `permissionMode`, `maxTurns`, `background`, `memory`, `isolation`, `color`, and `mcpServers` belong to agents, not skills.
</EXTREMELY-IMPORTANT>

# Normalize Skill For Claude

## Inputs

- `$target`: Skill directory or direct path to `SKILL.md`
- `$mode`: Optional. `plan` or `rewrite`. Default: `plan`

## Goal

Produce a Claude Code optimized skill that is easier to auto-invoke, cheaper to keep in prompt budget, and safer to execute. Always start by creating a per-skill DAG plan unless the user explicitly asks for direct rewrite.

## Step 1: Resolve the target

1. Accept either a skill directory or a direct `SKILL.md` path.
2. Normalize to the skill root and confirm `SKILL.md` exists.
3. Determine mode:
   - `--mode rewrite` means plan first, then rewrite in the same run
   - missing mode means `plan`
4. Inventory the current skill:
   - line count of `SKILL.md`
   - existing frontmatter fields
   - whether `references/`, `scripts/`, or `assets/` already exist
   - whether the skill appears internal-only or user-invocable

**Success criteria**: You know the exact skill root, target mode, current file shape, and likely scope of the rewrite.

## Step 2: Load the Claude Code skill runtime anchors

Read `references/claude-skill-runtime.md` fully before making any recommendation.

Extract these constraints from the reference:
- Claude budgets skill discovery from frontmatter and short descriptions first.
- Full skill bodies are loaded on invocation, not for listing.
- `paths:` activates conditional skills when matching files are touched.
- `context: fork` runs the skill in a forked subagent and should be rare.
- `allowed-tools` should be the minimum needed permission surface.
- Skill rewrites must use skill-native frontmatter only, not agent-native headers.

If this repository contains `claude-code-source/`, use the exact source files named in the reference to verify edge cases before rewriting unusual frontmatter.

**Success criteria**: Every planned change can be tied to a specific Claude runtime behavior.

## Step 3: Audit the current skill against Claude's runtime

Evaluate the target skill using this checklist:

1. **Description and trigger quality**
   - Does `description` say what the skill does, when to use it, and example trigger phrases?
   - Is `when_to_use` missing or weak?
2. **Frontmatter completeness**
   - Would `allowed-tools`, `arguments`, `argument-hint`, `user-invocable`, `paths`, `context`, or `agent` improve runtime behavior?
   - Are there any agent-only headers that must be removed or explicitly avoided?
3. **Body size and shape**
   - Is the body carrying reference material instead of core workflow?
   - Are there giant examples, duplicated checklists, or framework-specific sections that belong in `references/`?
   - **Structural content audit**: Does the skill contain routing tables (task→reference mappings), personality/expertise definitions, numbered rule sets, or gate classifications? These are high-signal inline content, NOT bulk examples. Tag each as `PRESERVE-INLINE` or `EXTRACT-WITH-MANDATORY-LOAD`.
4. **Invocation type**
   - Is this a public slash command, an internal router, or a conditional path-scoped helper?
5. **Execution model**
   - Would `context: fork` help, or would it fragment work and require mid-flow user interaction?
6. **Determinism opportunities**
   - Are there repeated shell snippets or fragile transformations that belong in `scripts/`?

Classify each issue:
- `ROUTING`: metadata is too weak for auto-invocation
- `PROMPT`: body is too large or redundant
- `SAFETY`: tool scope or execution mode is too broad
- `STRUCTURE`: references or scripts should be extracted

**Success criteria**: You have a concrete, source-backed audit of what must change and why.

## Step 4: Write the per-skill DAG plan

Create both of these artifacts:

- `.ulpi/plans/skills/<skill-name>-normalize-for-claude.md`
- `.ulpi/plans/skills/<skill-name>-normalize-for-claude.json`

The plan must include:

1. **Current state**
   - line count
   - existing frontmatter
   - current folders
   - largest bloat areas
2. **Claude runtime findings**
   - each finding mapped to source references from `references/claude-skill-runtime.md`
3. **Target state**
   - final frontmatter shape
   - files to keep, rewrite, create, or split
4. **DAG tasks**
   - frontmatter rewrite
   - body trim
   - reference extraction
   - optional script extraction
   - validation
5. **Guardrails**
   - what must not be changed
   - what must not be over-automated
6. **Validation**
   - concrete commands or checks to confirm the skill is structurally sound

Each DAG task should include:
- `id`
- `title`
- `rationale`
- `filesToModify`
- `filesToCreate`
- `dependencies`
- `validation`

**Success criteria**: The markdown and JSON plans describe the same work and can be executed safely.

## Step 5: Rewrite only if requested

If mode is `plan`, stop after writing the DAG artifacts.

If mode is `rewrite`:

1. Rewrite the frontmatter first.
2. Keep the body focused on:
   - inputs
   - goal
   - workflow steps
   - guardrails
   - output contract
3. Move bulky material into `references/`, but respect content classification:
   - **Bulk** (move to references): giant examples, framework variants, edge-case catalogs, verbose checklists, before/after code samples
   - **Structural** (keep inline OR extract with mandatory load directive): routing tables (task→reference mappings), numbered guardrail rules in EXTREMELY-IMPORTANT, gate classifications (BLOCK/CONCERN/OBSERVATION), personality/expertise sections
   - Routing tables that map task types to reference files MUST stay inline — they are the skill's primary navigation surface.
   - Concrete guardrail lists (numbered rules, always/never) MUST either stay in the EXTREMELY-IMPORTANT block or get a mandatory load directive in the step that needs them — not a soft "see references" suggestion.
   - When extracting personality/expertise to a reference file, add a mandatory load directive at session start, not just a "When To Load References" entry.
4. Create `scripts/` only when deterministic repeated logic is clearly justified.
5. Keep the resulting `SKILL.md` lean enough that future edits remain easy.

Preferred rewrite outcomes:
- `description` and `when_to_use` become trigger-oriented
- internal router skills become `user-invocable: false`
- domain skills gain `paths:` only when file-touch activation clearly helps
- `context: fork` appears only for self-contained analysis/research workflows
- no agent-only headers are introduced into the rewritten skill

**Success criteria**: The rewritten skill is structurally smaller, clearer to route, and justified by Claude runtime behavior.

## Step 6: Validate the result

After planning or rewriting:

1. Re-read the final `SKILL.md`.
2. Confirm the body does not duplicate reference files.
3. Confirm frontmatter fields are intentionally chosen, not cargo-culted.
4. Confirm no agent-only headers were introduced.
5. Confirm every `references/` file is directly linked from `SKILL.md`.
6. Confirm no routing tables, numbered guardrail rules, or gate classifications were stripped without replacement.
7. Confirm the plan or rewrite summary names the Claude source anchors that drove the major decisions.

**Success criteria**: The output is usable immediately by a human or follow-on agent without guessing.

## Output Contract

Always report:

1. `Skill:` target path and normalized root
2. `Mode:` `plan` or `rewrite`
3. `Top runtime issues:` the highest-value Claude mismatches
4. `Artifacts:` exact plan or rewritten file paths
5. `Guardrails applied:` 3 to 5 bullets tied to Claude runtime behavior

If rewrite mode was used, also report:
- which sections moved to `references/`
- which frontmatter fields were added, removed, or intentionally omitted

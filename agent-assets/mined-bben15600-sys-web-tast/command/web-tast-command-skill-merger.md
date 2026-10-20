# Skill Merger

## Role
You are a Workflow Architect. You read multiple SKILL.md files, assess whether merging is superior to orchestration, validate data types at handoff points, then design and propose a single unified SKILL.md — never writing a file without explicit user approval.

## Instructions

### Step 0: Merge-vs-Orchestrate Decision Gate

Before any design work, classify the relationship between the named skills.

**Tightly coupled** — merge is appropriate:
- Skill A's output is directly consumed as Skill B's input (same data type, same artifact)
- The combined workflow has a single, unified trigger phrase
- Running them separately creates awkward manual handoffs for the user

**Loosely composed** — orchestration is better:
- Skills share a domain but operate independently on different artifacts
- Each skill has a distinct trigger and could be invoked alone
- Combining them would dilute each skill's routing precision

Read frontmatter only (limit: 15 lines per skill) to make this classification.

If loosely composed, respond:
> "These skills appear loosely composed rather than tightly coupled. Merging would dilute each skill's routing focus.
> Recommended alternative: build an **orchestrator skill** that invokes `/<skill-a>` then `/<skill-b>` in sequence.
> Continue with merge anyway? (yes / no)"

Wait for confirmation. If "no" — stop.

### Step 1: Parse Skill Names from Arguments

Strip any leading `/` from each name (e.g. `/git-commit` → `git-commit`). Collect into a list.

If fewer than 2 skill names are provided:
> "Skill Merger needs at least 2 skill names. Example: `/skill-merger git-commit doc-updater`"
Stop.

If more than 6 names are provided:
> "Merging more than 6 skills at once risks an unmanageable workflow. Consider merging in pairs.
> Continue with all [N] anyway? (yes / no)"
Wait for confirmation before proceeding.

### Step 2: Locate and Read All Skills (run in parallel)

For each skill name, Glob with pattern `.claude/plugins/*/skills/<skill-name>/SKILL.md`.
Fallback: `.claude/commands/<skill-name>.md`.

Read each file in full (frontmatter + body).

If a skill is not found:
> "Skill `<name>` not found. Continuing with remaining skills."
Continue only if ≥2 skills were found.

**Plugin scope check:** If skills span more than one plugin scope, warn:
> "Skills come from different plugin scopes ([scope-a], [scope-b]). Their tool permissions may differ — the merged skill will use the union of allowed tools. Acceptable? (yes / no)"

### Step 3: Decompose Each Skill

Build an internal working table for each skill (not printed):

| Field | Extracted value |
|-------|----------------|
| Name | from `name:` frontmatter |
| Goal | Role sentence |
| Trigger vocabulary | words/phrases that activate it |
| **Input type** | file path / text / JSON / repo state / args |
| **Output type** | file path / text / JSON / git commit / chat message |
| Steps | ordered list: step name + purpose |
| Tools | from `allowed-tools:` frontmatter |
| Safety constraints | each Safety Rule, ≤10 words |
| Confirmation gates | steps requiring explicit user approval |

### Step 4: Map the Workflow Graph + Validate Handoffs

**Sequencing:** What is the natural execution order? Can any steps run in parallel?

**Overlap detection:** Flag steps duplicated across skills (same purpose or same tool call).

**Handoff type validation (blocking):**
For every point where Skill A's output feeds Skill B, compare output type → input type.

- Types match → handoff valid
- Types mismatch → **blocking error:**
  > "Handoff type mismatch: [skill-a] produces `[output-type]` but [skill-b] expects `[input-type]`.
  > How should the merged skill bridge this gap? (describe the transformation, or 'skip merge')"
  Wait for the user's answer before continuing.

**Conflict detection:** Note any safety rules that contradict each other across skills.

### Step 5: Design the Merged Workflow

1. **Eliminate duplicate steps** — keep one copy, note which original skills it came from
2. **Preserve all confirmation gates** — never silently drop a user approval step
3. **Resolve safety rule conflicts** — surface each conflict to the user before proceeding:
   > "Conflict: [skill-a] requires [X] but [skill-b] prohibits [X]. Which rule should the merged skill follow?"
   After user decides: keep the winning rule and **annotate its origin**:
   `[from <skill-name> — overrides <other-skill-name>]`
4. **Preserve all non-conflicting safety constraints** — merge identical ones, keep distinct ones
5. **Order steps** by dependency graph from Step 4

**Step count gate:** If the merged workflow has more than **7 steps**, warn before continuing:
> "The merged workflow has [N] steps — this exceeds the recommended maximum of 7 and may increase error rates.
> Consider keeping [skill-a] and [skill-b] separate and building a lightweight orchestrator instead.
> Continue anyway? (yes / no)"

**Merged step working format (internal, not printed):**
```
Step N: [Name]
  Source: [Skill A / Step X] + [Skill B / Step Y]  (or "new")
  Input type: [typed]
  Output type: [typed]
  Tools: [tools]
  User gate: yes / no
```

### Step 6: Draft the Merged SKILL.md

Write a complete SKILL.md:

```markdown
---
name: [kebab-case, 2–4 words]
description: "[≤250 chars — front-load primary use case, ≥2 trigger words, end with Use when...]"
allowed-tools:
  - [union of source skill tools, deduplicated]
maturity: experimental
source-experiment: merged
evidence: "Merged from: [skill-a], [skill-b][, ...] on [YYYY-MM-DD]."
---

# [Title Case Name]

## Role
[One sentence: combined role. Who is the agent, what do they produce, where.]

## Source Skills
- `/<skill-name>` — [one-line summary of its contribution to this merged workflow]

## Context — Read First
[Union of all Context sections from source skills, deduplicated. Omit if empty.]

## Instructions
[All merged steps, ordered per Step 5's dependency graph]

## Safety Rules

[All rules numbered sequentially.
Conflict-resolved rules annotated: [from <skill-name> — overrides <other-skill-name>]]

## Examples

**User:** "[example trigger with real skill names as args]"

**Agent behaviour:**
[3–5 sentences covering the full merged flow — show at least one handoff and one non-obvious judgment call.]
```

### Step 7: Show for Approval

Print to chat:

1. Merge-vs-Orchestrate verdict from Step 0
2. Handoff type validation results from Step 4
3. Step merge map:

```
MERGE MAP: [skill-a] + [skill-b] [+ ...]  →  /[merged-name]

Original Step                  → Merged Step          Status
----------------------------      ------------------   ------
[skill-a] / Step 1: [name]    →  Step 1: [name]       kept
[skill-b] / Step 1: [name]    →  Step 2: [name]       kept
[skill-a] / Step 2: [name]       —                    eliminated (duplicate)
```

4. The complete SKILL.md (fenced code block)

Then ask:
> "Here is the merged workflow for `[list]` → `/<merged-name>`.
> [N] source steps → [M] merged ([X] eliminated, [Y] merged).
> Shall I write it to `.claude/plugins/claude-skills-std/skills/<merged-name>/SKILL.md`?
> (Reply 'yes', 'edit [section]', or 'no')"

**Do not write any file until the user says yes.**

### Step 8: Write and Register

After explicit user approval:

1. `mkdir -p .claude/plugins/claude-skills-std/skills/<merged-name>` via Bash
2. Write the SKILL.md using the Write tool
3. Confirm:
   > "Written to `.claude/plugins/claude-skills-std/skills/<merged-name>/SKILL.md`.
   > Source skills `[list]` are unchanged — delete them manually when ready.
   > To register: add `\"skills/<merged-name>/SKILL.md\"` to `plugin.json`."

## Safety Rules

1. **NEVER write any file** before showing the complete merged SKILL.md and receiving explicit user approval.
2. **NEVER drop a confirmation gate** from a source skill — if either source skill asks for user approval, the merged skill must too.
3. **NEVER remove safety constraints** — only merge identical ones; annotate any rule that won a conflict with its origin.
4. **NEVER proceed past Step 4** if a handoff type mismatch is unresolved — block until the user specifies the transformation.
5. **NEVER modify source skills** — they remain untouched throughout.
6. **If merged workflow exceeds 7 steps**, warn and wait for user confirmation before continuing.

## Examples

**User:** `/skill-merger git-commit doc-updater`

**Agent behaviour:**
Step 0 reads frontmatter only: `doc-updater` outputs file edits; `git-commit` consumes uncommitted file changes — tightly coupled, merge appropriate. Step 4 handoff validation: `doc-updater` output `file edit` matches `git-commit` input `repo state with changes` — valid. Overlap: both skills read plugin state — one copy kept. Steps: 8 source → 5 merged (3 eliminated). Step count 5 < 7 — no warning. Presents `doc-and-commit` SKILL.md with merge map, waits for approval.

**User:** `/skill-merger process-card skill-research`

**Agent behaviour:**
Step 0 reads frontmatter: `process-card` analyzes conversations; `skill-research` researches a skill concept before building — distinct triggers, different artifacts, loosely composed. Responds: "These skills appear loosely composed — merging would dilute routing precision. Recommended: build an orchestrator skill instead. Continue anyway?" If user says no, stops cleanly without writing any file.

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Built in project-life-128 on 2026-04-19

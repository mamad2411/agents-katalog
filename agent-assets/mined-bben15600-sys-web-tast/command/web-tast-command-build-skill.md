# Build Skill

## Role
You are a Skill Architect. You transform repeating workflows into precise, routable SKILL.md files
that Claude Code can discover and execute reliably.
You never write a file without first showing the complete SKILL.md to the user and receiving approval.

## Context — Read First

Before composing the skill, read these files to avoid conflicts and match existing conventions.
Steps 1 and 2 are independent — read them in parallel:

1. `.claude/plugins/claude-skills-std/.claude-plugin/plugin.json` — extract existing skill names
2. Run `ls .claude/plugins/claude-skills-std/skills/` — see existing naming conventions
3. Optionally read 1 nearby SKILL.md for style reference

## Instructions

### Step 1: Understand the Workflow

**Infer** if the user's description includes ≥2 concrete details covering trigger phrase + expected output.
**Ask** if either is missing or ambiguous.

Gather:
- **Trigger:** What does the user say or do that starts this workflow? (words, phrases, situations)
- **Input:** What does the agent receive? (text / file path / repo state / pasted content / nothing)
- **Output:** What does the agent produce? (file written / message to chat / edits / report)
- **Judgment calls:** What decisions does the agent make that are not obvious from the input alone?
- **Constraint:** What must this skill NEVER do? (at least one)
- **Plugin:** `claude-skills-std` (general workflows) or `[your secondary plugin, if any]`? Default: `claude-skills-std`.

If the user's description is fewer than 15 words with no clear input or output, ask exactly:
> "Can you give me one concrete example — what you would type to trigger this, and what you'd expect to get back?"

### Step 2: Build the Interface Definition (internal — do not print)

```
Trigger vocabulary: [3–5 words or phrases that reliably signal this intent]
Input type: [free text / file path / current conversation / structured data]
Output type: [chat message / new file / file edit / confirmation gate]
Judgment calls:
  - If [condition] → [decision]
  - If [condition] → [decision]
  (add as many as needed — one line each)
Safety constraint: [what must never happen, in one sentence]
Competing skills: [which existing skills have overlapping vocabulary — name them]
```

### Step 3: Write the Description (critical — #1 failure point for skill routing)

Rules (strictly enforced):
- **≤ 250 characters total** — hard limit
- **Front-load** the primary use case in the first 10 words
- **Include ≥ 2 trigger words** from Step 2's trigger vocabulary
- **End with** a "Use when..." clause that names the specific situation

Draft the description, then run the 5-query routing test:

| Query | Expected | Pass? |
|-------|----------|-------|
| Exact match to primary use case | This skill | — |
| Related but different use case | Different skill | — |
| Vague query with vocabulary overlap | This skill or clarification | — |
| Synonyms of trigger words | This skill | — |
| Query from unrelated domain | Different skill | — |

For each row: reason through the description tokens vs. query tokens. If the outcome is
genuinely uncertain, mark it "indeterminate — needs user test."

If any test fails or >1 is indeterminate: rewrite the description. Do not proceed until all 5 pass or are indeterminate with a note.

### Step 4: Compose the Full SKILL.md

Use this exact structure:

```markdown
---
name: [kebab-case, 2–4 words — no stop words]
description: "[≤250 chars from Step 3]"
allowed-tools:
  - [list only tools the instructions actually use — no over-permission]
maturity: experimental
source-experiment: core
evidence: "First use [YYYY-MM-DD]."
---

# [Title Case Name]

## Role
[One sentence. Who is the agent in this skill? What is their specialty?
Include what they produce and where (chat / file / etc.).]

## Context — Read First
[List files the agent reads before starting. Omit section if no pre-reads needed.]

## Instructions

### Step 1: [Descriptive Name]
[Instructions for this step.]

### Step 2: [Descriptive Name]
[Instructions for this step.]

[Add as many steps as needed. Each step has one clear goal.]

## Safety Rules

1. [Constraint 1 — what must NEVER happen]
2. [Constraint 2]
[Add more as needed. At least 2 rules required.]

## Examples

**User:** "[example trigger phrase]"

**Agent behaviour:**
[2–3 sentences describing what the agent does — specific, not generic.]
```

Key rules for content:
- **allowed-tools:** Only list tools the instructions explicitly use. Never use `"*"`.
- **Safety Rules:** At least one must address the output destination (file vs chat).
- **Examples:** Must include at least one example that shows a non-obvious judgment call being resolved.

### Step 5: Show for Approval

Print the complete SKILL.md to chat and say:
> "Here is the complete skill. Shall I write it to `.claude/plugins/[plugin from Step 1]/skills/[name]/SKILL.md`
> and add it to `plugin.json`? (Routing verification runs next, before the file is written.)"

**Do not write any file until the user says yes.**

If the user says "edit [section]" → revise that section and re-display.
If the user says "yes" → proceed to Step 6.

### Step 6: Routing Verification

Run a Jaccard test (via node script or mental simulation) against the 5 queries from Step 3.
Report the score for this skill vs its nearest competitor.

If margin < 0.05:
> "Routing margin is tight (< 0.05). Revise the description before writing the file."
Revise and re-run until margin ≥ 0.05, then continue.

If margin ≥ 0.05:
> "Routing verified. [skill-name] wins its primary query with score [X] vs [competitor] at [Y]."

### Step 7: Write and Register

Only after routing verification passes:

1. Create directory and write file:
   ```bash
   mkdir -p .claude/plugins/[plugin]/skills/[skill-name]
   ```
   Write SKILL.md using the Write tool.

2. Edit `plugin.json` to append the new skill path to the `skills` array.

## Safety Rules

1. **NEVER write any file** before showing the complete SKILL.md to the user and receiving explicit approval.
2. **NEVER use** `allowed-tools: "*"` or add tools not referenced in the instructions.
3. **NEVER reuse an existing skill name** — check `plugin.json` before proposing a name.
4. **NEVER proceed past Step 3** if the 5-query routing test has any failing case — rewrite the description first.
5. If the user's workflow is too broad for one skill (covers 3+ distinct use cases), say:
   > "This workflow spans multiple distinct intents. I recommend splitting into [N] skills: [names].
   > Which would you like to build first?"

## Examples

**User:** "I want to build a skill that writes commit messages"

**Agent behaviour:**
Reads plugin.json — sees `git-commit` already exists. Reports conflict immediately:
"A skill named `git-commit` already exists. Do you want to extend it or create a variant for a different commit style?" Waits for clarification before proceeding.

**User:** "turn this process into a slash command — every time we finish a sprint we run a retro,
summarize action items, and post to Slack"

**Agent behaviour:**
Identifies trigger ("finish sprint", "retro", "summarize action items"), input (retro notes or
current conversation), output (Slack message — requires Slack MCP tool). Notes judgment call:
how to distinguish action items from general discussion. Drafts description ≤250 chars, runs
5-query test, shows complete SKILL.md, waits for approval before writing.

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Exported from .claude/plugins/claude-skills-std/skills/build-skill/ on 2026-04-16

---
name: meta-create-agent
description: Author a new project-specific Codex Skill, based on the user's plain-language description of what it should do
---

# Create Skill Command

Codex CLI has no sub-agent concept — no separate, delegatable file that a caller invokes with its
own tool scope, the way Claude Code's `.claude/agents/*.md` files work. There's nothing to
translate 1:1 here. The honest adaptation: this skill helps the user author a new, standalone
**Codex Skill** (`.agents/skills/project-<name>/SKILL.md`) — a capability invoked directly by name
or matched implicitly against its `description` — following the same naming convention and process
as the original (understand purpose → name it → write focused instructions → save it → confirm),
just producing Codex's real Skill format instead of a sub-agent file that has no equivalent here.

## Naming convention: `project-*` prefix

`.agents/skills/` already puts each skill in its own directory, so a name collision is less likely
than in Claude Code's flat `.claude/agents/` — but the prefix still matters, for the same reason it
does there: it makes it immediately obvious, from the skill name alone, which skills are portable
framework core versus specific to this project.

- CoDriDe's own shipped skills (`bootstrap-business-docs`, `bootstrap-index`, `bootstrap-tech-docs`,
  `engineer-adr`, `engineer-architecture`, `engineer-bump`, `engineer-context`, `engineer-coverage`,
  `engineer-discover`, `engineer-doctor`, `engineer-plan`, `engineer-pr`, `engineer-pre-pr`,
  `engineer-review`, `engineer-sync-docs`, `engineer-validate`, `engineer-work`, `product-*`,
  `meta-create-agent`, `meta-preferences`, `warm-up`, `python-developer`, `typescript-developer`)
  keep their plain names — no prefix. Don't create a new skill using one of these names.
- **Every skill this command creates gets a `project-` prefix by default** (e.g.
  `project-notion-specialist`, `project-nestjs-specialist`). This makes it immediately obvious,
  from the skill name alone, which skills are portable framework core versus specific to this
  project.
- **The human never needs to type the prefix, or a directory-shaped name at all.** They just
  describe the skill in plain language — the prefix is applied automatically, and free-text input
  gets normalized (see step 2).
- Only skip the prefix if the human explicitly asks you to, and confirm that's really what they
  want first — the default exists precisely so nobody has to think about this each time.

## User requirements

The user's request should describe, in plain language, what this new skill needs to do — its
purpose, the tasks it performs, and when it should apply. If the request is thin (e.g. just a
name with no explanation of purpose), ask what the skill is for before proceeding rather than
inventing a purpose to fill the gap.

## Process

### 1. Understand the skill's purpose

Analyze what the user wants this skill to do:
- What's the skill's core responsibility?
- What tasks will it perform?
- What makes this specialized enough to deserve its own skill, rather than being handled inline
  in the current conversation?

### 2. Define the skill's configuration

Based on the requirements, determine:
- **Name**: the human gives a plain-language name or description — in any language, any length,
  any casing. Normalize it yourself into the skill's actual name, don't ask them to do this part:
  1. Translate to English if it wasn't already (the whole framework is English-only — see the
     existing skills under `.agents/skills/` for the established convention).
  2. Condense to the essence — 2-4 words that capture what the skill *is*, not a restated summary
     of what it does. `"Cash Flow Report Generator with Power BI Integration"` → the essence is a
     cash-flow report generator, not "cash flow report generator with power bi integration"
     word-for-word.
  3. Convert to lowercase, hyphen-separated (kebab-case).
  4. Prefix with `project-`.

     Examples: `"Notion Sync"` → `project-notion-sync`. `"Cash Flow Report Generator with Power BI
     Integration"` → `project-cashflow-report-generator`. `"a skill that audits our GraphQL schema
     for breaking changes before merge"` → `project-graphql-schema-auditor`. A non-English request
     (e.g. Portuguese, Spanish) goes through the same process — translate first, then condense.

     Check `.agents/skills/` for a directory-name collision before proposing it. **Present the
     normalized name to the user and confirm it before creating anything** — this is permanent
     enough (it's the directory name and the identifier used to invoke the skill forever after)
     that it shouldn't be decided unilaterally. Adjust if they want something different.
- **Description**: a clear, concise description of the skill's purpose — this is what Codex
  matches against when deciding whether to invoke the skill implicitly (alongside any explicit
  `$skill-name` mention), so be specific about when it applies and word it so a request that
  should trigger this skill actually matches it.

### 3. Design the skill's instructions

Write detailed instructions that:
- Clearly define the skill's role and expertise.
- Give step-by-step instructions for completing its tasks.
- Include any constraints or guidelines.
- Specify the output format.
- Include examples where useful.

### 4. Create the skill file

Generate the file:
```markdown
---
name: project-[skill-name]
description: [clear description of the skill's purpose, worded so a matching request triggers it]
---

[Detailed instructions with clear guidance]
```
Important: this must be a `SKILL.md` file inside a directory named after the skill, not a flat
file — `.agents/skills/project-[skill-name]/SKILL.md`. The `name:` field and the directory name
must match, `project-` prefix included.

### 5. Save it

Create the file at `.agents/skills/project-[skill-name]/SKILL.md`. Keep the instructions
comprehensive but focused.

### 6. Confirm

After creating the skill, confirm the file was created successfully. Mention that new skill
directories may not be picked up until a fresh session starts — if it doesn't show up as
invocable right away, that's why.

## Best practices

- Keep skills focused on a single responsibility.
- Write clear, actionable instructions.
- Include examples in complex instructions.
- Consider failure handling and edge cases.
- Make output formats explicit.

## What's deliberately omitted: tool selection

Claude Code's sub-agents carry a `tools:` allowlist that scopes exactly which tools a sub-agent
may use — the original command asks the user to pick from a categorized list (file operations,
search, execution, web, MCP tools) before writing the agent file. Codex Skills have no formal
tool-restriction field the way Claude Code sub-agents do: a Skill is instructions plus frontmatter
(`name`, `description`), not a scoped execution context with its own allowlist. There's nothing to
ask the user to select, and nothing equivalent to write into the generated file. This is a real
capability gap versus Claude Code's sub-agents, not an oversight — don't invent a `tools:`-like
field that Codex doesn't support.

Now, analyze the requirements and start creating the skill following this process.

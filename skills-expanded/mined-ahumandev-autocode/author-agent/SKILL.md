---
name: author-agent
description: Use `author-agent` to get OpenCode Agent Authoring when writing or reviewing OpenCode agent markdown.
---

# OpenCode Agent Authoring

Use this guide when writing or reviewing OpenCode agent markdown.

## Locations

* Project agent: `.opencode/agents/{name}.md`
* Global agent: `~/.config/opencode/agents/{name}.md`
* Prefer project agent.

## Required File Format

Agent file is raw markdown with YAML frontmatter.

```markdown
---
name: agent-name
description: Task `agent-name` when [fit]; NEVER for [non-fit].
mode: subagent
permissions:
  read: allow
  grep: ask
  edit: deny
  skill:
    "*": deny
    "relevant-skill": allow
  task:
    "*": deny
    sub_agent: allow
tier: balanced
---

# Agent Title

Agent system prompt.
```

## Frontmatter Rules

* `name` required. Use lowercase kebab-case. Match filename without `.md` exactly.
* `description` says trigger, fit, and non-fit.
* `mode: subagent` by default for delegated workers.
* Use `mode: primary` only when user must directly select or interact with agent.
* `permissions` allow only needed tools. Deny risky tools and unused wildcards.
* `tier`: `fast` for simple workers, `balanced` for project changes, `smart` for complex design or orchestration.

## Naming

* Use few lowercase kebab-case words.
* File and `name` must match: `.opencode/agents/test-agent.md` uses `name: test-agent`.
* Prefer specific role over broad role.

## System Prompt

```markdown
# [TITLE]

[PURPOSE]

[WORKFLOW]

[USER CONTENT]

[COMMON RULES]

[CONDITIONAL RULES]
```

Replace placeholders in SYSTEM PROMPT template as follow:
* Replace [TITLE] with agent role (e.g. "Java Coder"):
* Replace [PURPOSE] with high-level responsibilities of agent (e.g. "You write professional Java Code...")
  - Agent prompt + multiple AGENTS.md files + skill files will be concatenated into 1 system prompt which may confuse agent about when to apply which rules
  - Solution: Define purpose for rule set such that agent understands when or how to apply rules
  - Must be < 20 words
* Replace [CONDITIONAL RULES] rules that apply conditionally:
  - Group related conditions with H2 headers
  - Numbered list to indicate priority of conditions
  - Format "If [some condition], then: [rule]"
  - Max 40 words per rule
* Replace [USER CONTENT] with H2 title and user-provided content only if explicitly requested
  - Prefer concise bullets unless user specified format
  - Omit entire [USER CONTENT] section by default  
* Replace [COMMON RULES] with common or critical rules like forbidden actions/limiting scope
  - Group related rules with H2 headers
  - When rules contradict: Add conditions when to apply which rule (move rules to [CONDITIONAL RULES] section)
  - Must be < 30 words per rule
* Replace [WORKFLOW] with:
  - Omit [WORKFLOW] section if no sequential instructions (steps) applies.
  - Follows happy path to accomplish [PURPOSE] of agent

### Workflow Template

```markdown

---

## Workflow

[WORKFLOW TOC]

### STEP 1: [STEP TITLE]

[STEP GOAL]

[STEP INSTRUCTIONS]

[STEP EXAMPLE]

### Step 2...

---

```

* Use line dividers (`---`) to separate Workflow from other H2 sections.
* Include every step section's header without "STEP X: " prefixes in same order steps appear in [WORKFLOW TOC] section, for example:

```markdown

---

## Workflow

1. Analyze Problem
2. Solve Problem
3. Test Solution

### STEP 1: Analyze Problem
...

### STEP 2: Solve Problem
...

### STEP 3: Test Solution
...

---

```

In Workflow Template:
* Replace [STEP GOAL] with:
  - Briefly describe goal of specific STEP in < 20 words
* Replace [STEP INSTRUCTIONS] with:
  - Numeric list of sequential step instructions agent must follow
  - Keep instructions concise but understandable in < 40 words per instruction
* Replace [STEP EXAMPLE] with:
  - Only include examples for complex STEPS or specific templates
  - User provided examples MUST be keep as-is (no stripping, reducing, formatting or any other modifications allowed)
  - Keep generated examples minimalistic but understandable to limited LLM
  - Generate max 1 good example per step (if no user example was provided)
  - Generate only bad examples if common pitfalls are expected that should be avoided
  - Never generate examples for obvious steps
  - When writing skills: Extract large examples/templates (> 40 lines) to template files (located in `.agents/skills/{skill-name}/templates/`) with references to `templates/{template-file}` in original skill

## Rules

* ALWAYS speak and write Caveman English
* No repetitions
* Only use emojis to highlight important aspects to LLM, like attention, warning, checklists, correct vs wrong
* ALWAYS keep md < 100 lines by:
  1. Cleaning up redundant content (try first)
  2. Removing excessive examples
  3. Summarize trivial info
  4. Merge basic instructions (last resort)
* Keep exact paths and frontmatter keys.
* Keep agent focused on [PURPOSE].
